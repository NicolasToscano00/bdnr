const API_URL = "http://localhost:5014/Notifications";

const PRESETS = {
  streak: {
    type: "streak",
    title: "🔥 ¡Mantén tu racha!",
    message: "Has completado 7 días seguidos. ¡No pierdas tu progreso!",
    priority: 1,
    ttl: 120,
  },
  achievement: {
    type: "achievement",
    title: "🏆 ¡Nuevo logro desbloqueado!",
    message: "Has completado la unidad de Español Básico. ¡Felicitaciones!",
    priority: 2,
    ttl: 180,
  },
  reminder: {
    type: "reminder",
    title: "⏰ Hora de practicar",
    message: "Tu lección diaria te está esperando. ¡Dedica 5 minutos ahora!",
    priority: 2,
    ttl: 90,
  },
  lesson: {
    type: "lesson",
    title: "📚 Lección pendiente",
    message:
      "Te quedan 3 lecciones para completar el nivel. ¡Continúa aprendiendo!",
    priority: 3,
    ttl: 300,
  },
  challenge: {
    type: "challenge",
    title: "⚡ Desafío del día",
    message: "Completa 10 ejercicios hoy y gana 50 XP extra",
    priority: 1,
    ttl: 86400,
  },
};

document.addEventListener("DOMContentLoaded", () => {
  loadNotifications();
  updateFormByType(); 

  // // Auto-refresh cada 3 segundos
  // setInterval(() => {
  //   loadNotifications();
  // }, 3000);
});

async function createNotification(event) {
  event.preventDefault();

  const userId = parseInt(document.getElementById("userId").value);
  const title = document.getElementById("title").value;
  const message = document.getElementById("message").value;
  const priority = parseInt(document.getElementById("priority").value);
  const ttlSeconds = parseInt(document.getElementById("ttl").value);

  const request = {
    userId,
    title,
    message,
    priority,
    ttlSeconds,
  };

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    showToast("✅ Notificación enviada exitosamente", "success");
    loadNotifications();

    // Limpiar formulario opcionalmente
    // document.getElementById('notificationForm').reset();
  } catch (error) {
    console.error("Error:", error);
    showToast("❌ Error al enviar notificación: " + error.message, "error");
  }
}

async function loadNotifications() {
  const userId = parseInt(document.getElementById("viewUserId").value);

  try {
    const response = await fetch(`${API_URL}/${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const notifications = await response.json();
    displayNotifications(notifications);

    const streamResponse = await fetch(`${API_URL}/stream/${userId}`);
    if (streamResponse.ok) {
      const stream = await streamResponse.json();
      displayStream(stream);
    }

    updateStats(notifications, await getStreamData(userId));
  } catch (error) {
    console.error("Error:", error);
    const list = document.getElementById("notificationsList");
    list.innerHTML = `
            <div class="empty-state">
                <p style="color: var(--danger-color);">⚠️ Error al cargar notificaciones</p>
                <p style="font-size: 14px;">Verifica que el servidor esté corriendo en ${API_URL}</p>
            </div>
        `;
  }
}

function displayNotifications(notifications) {
  const list = document.getElementById("notificationsList");

  if (!notifications || notifications.length === 0) {
    list.innerHTML = `
            <div class="empty-state">
                <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
                    <circle cx="40" cy="40" r="35" stroke="#E5E5E5" stroke-width="2"/>
                    <path d="M40 25V45M40 55V55.5" stroke="#E5E5E5" stroke-width="4" stroke-linecap="round"/>
                </svg>
                <p>No hay notificaciones activas</p>
            </div>
        `;
    return;
  }

  list.innerHTML = notifications
    .map((n) => {
      const priorityText = ["Alta", "Media", "Baja"][n.priority - 1] || "Media";
      const priorityEmoji = ["🔴", "🟡", "🟢"][n.priority - 1] || "🟡";
      const timestamp = new Date(n.timestamp).toLocaleString("es-ES", {
        day: "2-digit",
        month: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      });

      return `
            <div class="notification-card priority-${n.priority}">
                <div class="notification-header">
                    <div class="notification-title">${n.title}</div>
                    <div class="notification-priority priority-${n.priority}">
                        ${priorityEmoji} ${priorityText}
                    </div>
                </div>
                <div class="notification-message">${n.message}</div>
                <div class="notification-meta">
                    <span>ID: ${n.id.substring(0, 8)}...</span>
                    <span>📅 ${timestamp}</span>
                </div>
            </div>
        `;
    })
    .join("");
}

function displayStream(stream) {
  const list = document.getElementById("streamList");

  if (!stream || stream.length === 0) {
    list.innerHTML =
      '<div style="text-align: center; color: var(--text-secondary); padding: 20px;">Sin historial</div>';
    return;
  }

  list.innerHTML = stream
    .slice(-10)
    .reverse()
    .map((entry) => {
      const values = entry.values || entry.Values;
      return `
            <div class="stream-item">
                <div><strong>${values.title}</strong></div>
                <div style="font-size: 12px; color: var(--text-secondary);">${
                  values.message
                }</div>
                <div class="stream-id">Stream ID: ${
                  entry.streamId || entry.StreamId
                }</div>
            </div>
        `;
    })
    .join("");
}

async function getStreamData(userId) {
  try {
    const response = await fetch(`${API_URL}/stream/${userId}`);
    if (response.ok) {
      return await response.json();
    }
  } catch (error) {
    console.error("Error loading stream:", error);
  }
  return [];
}

function updateStats(notifications, stream) {
  document.getElementById("totalNotifications").textContent =
    notifications.length;

  const highPriority = notifications.filter((n) => n.priority === 1).length;
  document.getElementById("highPriority").textContent = highPriority;

  document.getElementById("streamCount").textContent = stream.length;
}

async function flushRedis() {
  if (
    !confirm(
      "⚠️ ¿Estás seguro de que deseas eliminar todas las notificaciones de Redis?"
    )
  ) {
    return;
  }

  try {
    const response = await fetch(`${API_URL}/flush`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    showToast("🗑️ Redis limpiado correctamente", "success");
    loadNotifications();
  } catch (error) {
    console.error("Error:", error);
    showToast("❌ Error al limpiar Redis", "error");
  }
}

function loadPreset(type) {
  const preset = PRESETS[type];
  if (!preset) return;

  document.getElementById("title").value = preset.title;
  document.getElementById("message").value = preset.message;
  document.getElementById("priority").value = preset.priority;
  document.getElementById("ttl").value = preset.ttl;

  showToast(`✨ Preset "${preset.title}" cargado`, "success");
}

function updateFormByType() {
  const type = document.getElementById("notificationType").value;
  const preset = PRESETS[type];

  if (preset) {
    document.getElementById("title").value = preset.title;
    document.getElementById("message").value = preset.message;
    document.getElementById("priority").value = preset.priority;
    document.getElementById("ttl").value = preset.ttl;
  }
}

function showToast(message, type = "success") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "toastSlide 0.3s ease reverse";
    setTimeout(() => {
      container.removeChild(toast);
    }, 300);
  }, 3000);
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleString("es-ES");
}
