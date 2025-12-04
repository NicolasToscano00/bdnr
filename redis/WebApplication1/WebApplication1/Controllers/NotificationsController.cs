using Microsoft.AspNetCore.Mvc;
using WebApplication1.Models;
using WebApplication1.Services;

namespace WebApplication1.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class NotificationsController : ControllerBase
    {
        private readonly INotificationService _service;

        public NotificationsController(INotificationService service)
        {
            _service = service;
        }

        [HttpPost]
        public async Task<IActionResult> Create(CreateNotificationRequest request)
        {
            return Ok(await _service.CreateNotificationAsync(request));
        }

        [HttpGet("{userId:int}")]
        public async Task<IActionResult> GetValid(int userId)
        {
            return Ok(await _service.GetValidNotificationsAsync(userId));
        }

        [HttpGet("stream/{userId:int}")]
        public async Task<IActionResult> GetStream(int userId)
        {
            return Ok(await _service.GetNotificationStreamAsync(userId));
        }

        [HttpDelete("flush")]
        public async Task<IActionResult> Flush()
        {
            await _service.FlushAllAsync();
            return Ok(new { message = "Redis limpiado" });
        }
    }
}
