using System.Text.Json;
using StackExchange.Redis;
using WebApplication1.Models;

namespace WebApplication1.Services
{
    public class NotificationService : INotificationService
    {
        private readonly IDatabase _db;
        public NotificationService(IConnectionMultiplexer redis)
        {
            _db = redis.GetDatabase();
        }

        private string NotificationKey(string id) => $"notification:{id}";
        private string PriorityKey(int userId) => $"notifications:priority:{userId}";
        private string StreamKey(int userId) => $"notifications:stream:{userId}";
        public async Task<Notification> CreateNotificationAsync(CreateNotificationRequest request)
        {
            var id = Guid.NewGuid().ToString();
            var timestamp = DateTime.UtcNow;

            var notification = new Notification
            {
                Id = id,
                UserId = request.UserId,
                Title = request.Title,
                Message = request.Message,
                Priority = request.Priority,
                Timestamp = timestamp
            };

            var data = JsonSerializer.Serialize(notification);

            // 1. Guardar con TTL
            await _db.StringSetAsync(
                NotificationKey(id),
                data,
                expiry: TimeSpan.FromSeconds(request.TtlSeconds)
            );

            // 2. Agregar a Sorted Set por prioridad
            await _db.SortedSetAddAsync(
                PriorityKey(request.UserId),
                id,
                request.Priority
            );

            // 3. Agregar a Stream (historial temporal)
            var streamData = new NameValueEntry[]
            {
            new("id", notification.Id),
            new("userId", notification.UserId.ToString()),
            new("title", notification.Title),
            new("message", notification.Message),
            new("priority", notification.Priority.ToString()),
            new("timestamp", notification.Timestamp.ToString("o"))
            };

            await _db.StreamAddAsync(StreamKey(request.UserId), streamData);

            return notification;
        }

        public async Task FlushAllAsync()
        {
            var endpoints = _db.Multiplexer.GetEndPoints();
            var server = _db.Multiplexer.GetServer(endpoints.First());
            await server.FlushDatabaseAsync();
        }

        public async Task<IEnumerable<object>> GetNotificationStreamAsync(int userId)
        {
            var entries = await _db.StreamRangeAsync(StreamKey(userId), "-", "+");

            return entries.Select(e => new
            {
                StreamId = e.Id.ToString(),
                Values = e.Values.ToDictionary(x => x.Name.ToString(), x => x.Value.ToString())
            });
        }

        public async Task<IEnumerable<Notification>> GetValidNotificationsAsync(int userId)
        {
            var results = new List<Notification>();

            // Obtener todos los IDs del Sorted Set
            var ids = await _db.SortedSetRangeByRankAsync(PriorityKey(userId));

            foreach (var redisId in ids)
            {
                string key = NotificationKey(redisId!);

                var raw = await _db.StringGetAsync(key);

                if (raw.HasValue)
                {
                    var notif = JsonSerializer.Deserialize<Notification>(raw!);
                    if (notif != null)
                        results.Add(notif);
                }
            }

            return results;
        }
    }
}
