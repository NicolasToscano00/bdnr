using StackExchange.Redis;

namespace WebApplication1.Redis
{
    public class RedisConnectionFactory
    {
        private static readonly Lazy<ConnectionMultiplexer> LazyConnection =
        new(() => ConnectionMultiplexer.Connect("localhost:6379"));

        public static ConnectionMultiplexer Connection => LazyConnection.Value;
    }
}
