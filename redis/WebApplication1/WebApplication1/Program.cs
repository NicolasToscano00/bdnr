using Microsoft.AspNetCore.Builder;
using StackExchange.Redis;
using WebApplication1.Redis;
using WebApplication1.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();
builder.Services.AddSingleton<IConnectionMultiplexer>(RedisConnectionFactory.Connection);
builder.Services.AddScoped<INotificationService, NotificationService>();
builder.Services.AddControllers();

// Configurar CORS para el frontend
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseStaticFiles();

app.UseRouting();

// Habilitar CORS
app.UseCors("AllowFrontend");

app.UseAuthorization();

app.MapRazorPages();
app.MapControllers();

app.Run();
