using WebApplication1.Models;

namespace WebApplication1.Services
{
    public interface INotificationService
    {
        Task<Notification> CreateNotificationAsync(CreateNotificationRequest request);
        Task<IEnumerable<Notification>> GetValidNotificationsAsync(int userId);
        Task<IEnumerable<object>> GetNotificationStreamAsync(int userId);
        Task FlushAllAsync();
    }
}
