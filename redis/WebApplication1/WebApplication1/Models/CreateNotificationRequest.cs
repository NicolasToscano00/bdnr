namespace WebApplication1.Models
{
    public class CreateNotificationRequest
    {
        public int UserId { get; set; }
        public string Title { get; set; } = default!;
        public string Message { get; set; } = default!;
        public int Priority { get; set; } = 2;
        public int TtlSeconds { get; set; } = 3600;
    }
}
