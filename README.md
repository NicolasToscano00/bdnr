# 🚀 Sistema de Notificaciones - Tipo Duolingo

Sistema de notificaciones temporal con Redis, inspirado en Duolingo.

---

## ⚡ Inicio Rápido

```bash
docker-compose up
```

Abre: **http://localhost:8080**

**¡Levanta ambos backends al mismo tiempo!**

---

## 🎯 Arquitectura

Docker Compose levanta 4 servicios:

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **Redis** | 6379 | Base de datos |
| **Backend Node.js** | 5014 | API Express.js |
| **Backend .NET** | 5015 | API ASP.NET Core |
| **Frontend** | 8080 | Nginx con UI |

---

## 🔄 Cambiar de Backend

El frontend se conecta por defecto al **backend Node.js** (puerto 5014).

### Para usar Backend .NET:

Edita `demo-frontend/app.js` línea 3:

```javascript
// Node.js (por defecto)
const API_URL = "http://localhost:5014/Notifications";

// .NET
const API_URL = "http://localhost:5015/Notifications";
```

Luego recarga el navegador: **Cmd + Shift + R**

---

## 📊 Comparación de Backends

| Característica | Node.js (5014) | .NET (5015) |
|----------------|----------------|-------------|
| **Lenguaje** | JavaScript | C# |
| **Framework** | Express | ASP.NET Core |
| **Tamaño** | ~5 MB | ~14 MB |
| **Arquitectura** | 1 archivo | Capas (MVC) |
| **Compilación** | No | Sí |
| **Tiempo inicio** | < 1s | ~5s |
| **Endpoints** | ✅ Idénticos | ✅ Idénticos |
| **Redis Model** | ✅ Idéntico | ✅ Idéntico |

**Ambos son funcionalmente equivalentes.**

---

## 🐳 Comandos Docker

### Iniciar todo (ambos backends)
```bash
docker-compose up
```

### Iniciar en background
```bash
docker-compose up -d
```

### Ver logs
```bash
# Todos
docker-compose logs -f

# Solo Node.js
docker-compose logs -f backend-node

# Solo .NET
docker-compose logs -f backend-dotnet
```

### Detener todo
```bash
docker-compose down
```

### Reconstruir
```bash
docker-compose up --build
```

---

## 📡 Endpoints API

Ambos backends tienen los mismos endpoints:

```bash
# Con Node.js (puerto 5014)
POST   http://localhost:5014/Notifications
GET    http://localhost:5014/Notifications/:userId
GET    http://localhost:5014/Notifications/stream/:userId
DELETE http://localhost:5014/Notifications/flush

# Con .NET (puerto 5015)
POST   http://localhost:5015/Notifications
GET    http://localhost:5015/Notifications/:userId
GET    http://localhost:5015/Notifications/stream/:userId
DELETE http://localhost:5015/Notifications/flush
```

---

## 🗄️ Modelado de Redis

Ambos backends usan **exactamente** las mismas estructuras:

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
│   ├── server.js              (205 líneas)
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

### 2. Usar Backend Node.js (por defecto)
- Frontend: http://localhost:8080
- Ya está configurado ✅

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

## 🎯 ¿Cuál Backend Usar?

### Node.js (puerto 5014)
**Usa si:**
- ✅ Prefieres código simple y directo
- ✅ Quieres desarrollo rápido
- ✅ No necesitas tipado fuerte

### .NET (puerto 5015)
**Usa si:**
- ✅ Trabajas en equipos grandes
- ✅ Prefieres arquitectura estructurada
- ✅ Quieres mejor tooling e IntelliSense

**Ambos tienen el mismo comportamiento en Redis.**

---

## 🧪 Probar Ambos

Puedes tener el frontend abierto y cambiar entre backends editando la URL en `app.js`:

```javascript
// Probar Node.js
const API_URL = "http://localhost:5014/Notifications";

// Probar .NET
const API_URL = "http://localhost:5015/Notifications";
```

Cada vez que cambies, recarga: `Cmd + Shift + R`

---

## 🛑 Detener

```bash
# Detener todo
docker-compose down

# Detener y eliminar volúmenes (limpia Redis)
docker-compose down -v
```

---

## 🔍 Verificar que Ambos Funcionen

```bash
# Node.js
curl http://localhost:5014/

# .NET
curl http://localhost:5015/

# Ambos deberían responder con información del servicio
```

---

**Dos backends, un frontend, infinitas posibilidades.** 🚀

Elige el que prefieras cambiando una línea en `app.js`.
