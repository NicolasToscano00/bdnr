const express = require("express");
const cors = require("cors");
const redis = require("redis");

const app = express();
const PORT = 5014;

// Middleware
app.use(cors());
app.use(express.json());

// Conectar a Redis
const redisClient = redis.createClient({
  socket: {
    host: process.env.REDIS_HOST || "localhost",
    port: process.env.REDIS_PORT || 6379,
  },
});

redisClient.on("error", (err) => console.error("Redis Error:", err));
redisClient.on("connect", () => console.log("✅ Conectado a Redis"));

// Inicializar conexión
(async () => {
  await redisClient.connect();
})();

// ============================================
// HELPERS
// ============================================

const notificationKey = (id) => `notification:${id}`;
const priorityKey = (userId) => `notifications:priority:${userId}`;
const streamKey = (userId) => `notifications:stream:${userId}`;

// ============================================
// ENDPOINTS
// ============================================

// 📨 Crear Notificación
app.post("/Notifications", async (req, res) => {
  try {
    const {
      userId,
      title,
      message,
      priority = 2,
      ttlSeconds = 3600,
    } = req.body;

    // Validación básica
    if (!userId || !title || !message) {
      return res.status(400).json({
        error: "userId, title y message son requeridos",
      });
    }

    // Generar ID único
    const id = generateId();
    const timestamp = new Date().toISOString();

    const notification = {
      id,
      userId,
      title,
      message,
      priority,
      timestamp,
    };

    // 1. Guardar notificación con TTL
    await redisClient.setEx(
      notificationKey(id),
      ttlSeconds,
      JSON.stringify(notification)
    );

    // 2. Agregar al Sorted Set por prioridad
    await redisClient.zAdd(priorityKey(userId), {
      score: priority,
      value: id,
    });

    // 3. Agregar al Stream (historial)
    await redisClient.xAdd(streamKey(userId), "*", {
      id: notification.id,
      userId: notification.userId.toString(),
      title: notification.title,
      message: notification.message,
      priority: notification.priority.toString(),
      timestamp: notification.timestamp,
    });

    res.json(notification);
    console.log(`✅ Notificación creada: ${id} para usuario ${userId}`);
  } catch (error) {
    console.error("Error creando notificación:", error);
    res.status(500).json({ error: error.message });
  }
});

// 📬 Obtener notificaciones activas de un usuario
app.get("/Notifications/:userId", async (req, res) => {
  try {
    const userId = parseInt(req.params.userId);
    const notifications = [];

    // Obtener todos los IDs del Sorted Set (ordenados por prioridad)
    const ids = await redisClient.zRange(priorityKey(userId), 0, -1);

    // Obtener cada notificación
    for (const id of ids) {
      const data = await redisClient.get(notificationKey(id));

      if (data) {
        notifications.push(JSON.parse(data));
      } else {
        // Si la notificación expiró, limpiar del Sorted Set
        await redisClient.zRem(priorityKey(userId), id);
      }
    }

    res.json(notifications);
    console.log(
      `📬 ${notifications.length} notificaciones para usuario ${userId}`
    );
  } catch (error) {
    console.error("Error obteniendo notificaciones:", error);
    res.status(500).json({ error: error.message });
  }
});

// 📜 Obtener historial (Stream) de un usuario
app.get("/Notifications/stream/:userId", async (req, res) => {
  try {
    const userId = parseInt(req.params.userId);

    // Obtener todas las entradas del Stream
    const entries = await redisClient.xRange(streamKey(userId), "-", "+");

    const stream = entries.map((entry) => ({
      streamId: entry.id,
      values: entry.message,
    }));

    res.json(stream);
    console.log(
      `📜 ${stream.length} entradas en stream para usuario ${userId}`
    );
  } catch (error) {
    console.error("Error obteniendo stream:", error);
    res.status(500).json({ error: error.message });
  }
});

// 🗑️ Limpiar toda la base de datos
app.delete("/Notifications/flush", async (req, res) => {
  try {
    await redisClient.flushDb();
    res.json({ message: "Redis limpiado" });
    console.log("🗑️ Base de datos limpiada");
  } catch (error) {
    console.error("Error limpiando Redis:", error);
    res.status(500).json({ error: error.message });
  }
});

// ============================================
// UTILIDADES
// ============================================

function generateId() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

// ============================================
// HEALTH CHECK & START
// ============================================

app.get("/", (req, res) => {
  res.json({
    service: "Notifications API",
    version: "1.0.0",
    status: "running",
    endpoints: {
      "POST /Notifications": "Crear notificación",
      "GET /Notifications/:userId": "Obtener notificaciones activas",
      "GET /Notifications/stream/:userId": "Obtener historial",
      "DELETE /Notifications/flush": "Limpiar Redis",
    },
  });
});

app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════╗
║   🚀 Servidor de Notificaciones           ║
║                                            ║
║   Puerto: ${PORT}                           ║
║   API: http://localhost:${PORT}/Notifications ║
║                                            ║
║   Endpoints:                               ║
║   • POST   /Notifications                  ║
║   • GET    /Notifications/:userId          ║
║   • GET    /Notifications/stream/:userId   ║
║   • DELETE /Notifications/flush            ║
╚════════════════════════════════════════════╝
    `);
});

// Manejo de cierre limpio
process.on("SIGINT", async () => {
  console.log("\n👋 Cerrando servidor...");
  await redisClient.quit();
  process.exit(0);
});
