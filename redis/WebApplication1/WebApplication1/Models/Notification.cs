namespace WebApplication1.Models
{
    public class Notification
    {
        public string Id { get; set; } = default!;
        public int UserId { get; set; }
        public string Title { get; set; } = default!;
        public string Message { get; set; } = default!;
        public int Priority { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
