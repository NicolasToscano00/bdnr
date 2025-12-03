using StackExchange.Redis;

namespace WebApplication1.Redis
{
    public class RedisConnectionFactory
    {
        private static readonly Lazy<ConnectionMultiplexer> LazyConnection =
        new(() => 
        {
            var redisHost = Environment.GetEnvironmentVariable("REDIS_HOST") ?? "localhost";
            var redisPort = Environment.GetEnvironmentVariable("REDIS_PORT") ?? "6379";
            var connectionString = $"{redisHost}:{redisPort}";
            return ConnectionMultiplexer.Connect(connectionString);
        });

        public static ConnectionMultiplexer Connection => LazyConnection.Value;
    }
}
