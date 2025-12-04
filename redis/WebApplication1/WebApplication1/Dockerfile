FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copiar csproj y restaurar dependencias
COPY WebApplication1.csproj ./
RUN dotnet restore

# Copiar el resto del código
COPY . .

# Build
RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

# Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=publish /app/publish .

# Exponer puerto
EXPOSE 5014

# Variables de entorno
ENV ASPNETCORE_URLS=http://+:5014
ENV ASPNETCORE_ENVIRONMENT=Development

ENTRYPOINT ["dotnet", "WebApplication1.dll"]

