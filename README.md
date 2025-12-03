# Sistema de Notificaciones 

Sistema de notificaciones temporal con Redis
---

## Inicio Rápido

```bash
docker-compose up
```

Abre: **http://localhost:8080**



## 📡 Endpoints API


```bash
POST   http://localhost:5014/Notifications
GET    http://localhost:5014/Notifications/:userId
GET    http://localhost:5014/Notifications/stream/:userId
DELETE http://localhost:5014/Notifications/flush

```

---

## 🗄️ Modelado de Redis


### 1. Strings con TTL

```
Key: notification:{id}
Value: JSON de la notificación
TTL: Configurable (ej: 120 segundos)
```

### 2. Sorted Sets (Índice por Prioridad)

```
Key: notifications:priority:{userId}
Members: IDs ordenados por score
Score: Prioridad (1=alta, 3=baja)
```

### 3. Streams (Historial)

```
Key: notifications:stream:{userId}
Entries: Log inmutable cronológico
```

---

## 🔗 URLs

- **Frontend**: http://localhost:8080
- **Backend Node.js**: http://localhost:5014
- **Backend .NET**: http://localhost:5015
- **Redis**: localhost:6379

---

## 📁 Estructura del Proyecto

```
bdnr/
├── docker-compose.yml          # Levanta todo
├── README.md
│
├── backend-node/               # Backend Node.js
│   ├── server.js              
│   ├── package.json
│   └── Dockerfile
│
├── redis/WebApplication1/      # Backend .NET
│   └── WebApplication1/
│       ├── Controllers/
│       ├── Services/
│       ├── Models/
│       ├── Redis/
│       ├── Program.cs
│       └── Dockerfile
│
└── demo-frontend/              # Frontend
    ├── index.html
    ├── styles.css
    └── app.js                  # Cambiar API_URL aquí
```

---

## 💡 Ejemplo de Uso

### 1. Levantar todo

```bash
docker-compose up -d
```

### 2. Usar Backend Node.js 

- Frontend: http://localhost:8080
- Ya está configurado 

### 3. Cambiar a Backend .NET

```javascript
// demo-frontend/app.js línea 3
const API_URL = "http://localhost:5015/Notifications";
```

### 4. Recargar navegador

```
Cmd + Shift + R  (Mac)
Ctrl + Shift + R (Windows/Linux)
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



