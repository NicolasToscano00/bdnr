# 🚀 Sistema de Notificaciones - Tipo Duolingo

Sistema de notificaciones temporal con Redis, inspirado en Duolingo.

---

## ⚡ Inicio Rápido

### Opción 1: Docker 🐳

```bash
docker-compose up
```

Abre: **http://localhost:8080**

### Opción 2: Manual

**Terminal 1 - Redis:**

```bash
redis-server --daemonize yes
```

**Terminal 2 - Backend:**

```bash
cd backend-node
npm install
npm start
```

**Terminal 3 - Frontend:**

```bash
open demo-frontend/index.html
```

---

## 📦 Stack

- **Backend**: Node.js + Express
- **Base de Datos**: Redis 7.x
- **Frontend**: HTML + CSS + JavaScript

---

## 🎯 Endpoints API

```bash
POST   /Notifications              # Crear notificación
GET    /Notifications/:userId      # Obtener activas
GET    /Notifications/stream/:userId  # Historial
DELETE /Notifications/flush        # Limpiar Redis
```

---

## 📊 Estructuras Redis

1. **Strings con TTL** - Notificaciones con expiración automática
2. **Sorted Sets** - Ordenamiento por prioridad
3. **Streams** - Historial completo

---

## 🐳 Docker

```bash
# Iniciar
docker-compose up

# Detener
docker-compose down

# Ver logs
docker-compose logs -f
```

---

## 🛑 Detener

**Docker:**

```bash
docker-compose down
```

**Manual:**

- Backend: `Ctrl + C`
- Redis: `redis-cli shutdown`

---

## 🔗 URLs

- **Frontend**: http://localhost:8080 (Docker) o archivo local
- **API**: http://localhost:5014
- **Swagger**: http://localhost:5014/swagger

---

## 📁 Estructura

```
backend-node/
├── server.js           # Backend completo con lógica
├── package.json
└── Dockerfile

demo-frontend/
├── index.html          # Interfaz
├── styles.css          # Estilos
└── app.js              # Lógica frontend
```

---

**Simple y funcional.** 🚀
