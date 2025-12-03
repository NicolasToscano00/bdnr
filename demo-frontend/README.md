# 📱 Frontend - Sistema de Notificaciones

## Características

### 🎨 Diseño
- Inspirado en Duolingo (colores vibrantes, UI moderna)
- Responsive (funciona en desktop, tablet, móvil)
- Animaciones suaves y transiciones
- Feedback visual con toasts

### ⚡ Funcionalidad
- **Auto-refresh**: Actualización cada 3 segundos
- **Presets rápidos**: Ejemplos pre-cargados para demo
- **Filtro por usuario**: Ver notificaciones específicas
- **Estadísticas en vivo**: Métricas en tiempo real
- **Historial**: Stream de Redis visible

### 📊 Estructura

```
demo-frontend/
├── index.html   ← Estructura HTML
├── styles.css   ← Estilos CSS (Duolingo-style)
└── app.js       ← Lógica JavaScript
```

## Cómo Usar

### Opción 1: Abrir directamente
```bash
open index.html
```

### Opción 2: Con el script automático
```bash
cd ..
./iniciar-demo.sh
```

### Opción 3: Con servidor HTTP (opcional)
```bash
python3 -m http.server 8000
# Abre: http://localhost:8000
```

## Configuración

El frontend se conecta al API en:
```javascript
const API_URL = 'http://localhost:5014/Notifications';
```

Si cambias el puerto del backend, edita esta línea en `app.js`.

## Presets Incluidos

### 🔥 Racha de Aprendizaje
- Prioridad: Alta (1)
- TTL: 120 segundos
- Ejemplo: "¡Mantén tu racha!"

### 🏆 Logro Desbloqueado
- Prioridad: Media (2)
- TTL: 180 segundos
- Ejemplo: "¡Nuevo logro desbloqueado!"

### ⏰ Recordatorio
- Prioridad: Media (2)
- TTL: 90 segundos
- Ejemplo: "Hora de practicar"

### 📚 Lección Pendiente
- Prioridad: Baja (3)
- TTL: 300 segundos
- Ejemplo: "Lección pendiente"

### ⚡ Desafío Diario
- Prioridad: Alta (1)
- TTL: 86400 segundos (24 horas)
- Ejemplo: "Desafío del día"

## API Endpoints Utilizados

```javascript
// Crear notificación
POST /Notifications
{
  "userId": 1,
  "title": "Título",
  "message": "Mensaje",
  "priority": 1,
  "ttlSeconds": 60
}

// Obtener notificaciones activas
GET /Notifications/{userId}

// Obtener historial (Stream)
GET /Notifications/stream/{userId}

// Limpiar Redis
DELETE /Notifications/flush
```

## Colores de Prioridad

- 🔴 **Alta (1)**: Borde rojo (#FF4B4B)
- 🟡 **Media (2)**: Borde amarillo (#FFC800)
- 🟢 **Baja (3)**: Borde verde (#58CC02)

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

Usa Fetch API y JavaScript ES6+.

## Personalización

### Cambiar intervalo de auto-refresh

En `app.js` línea ~39:
```javascript
setInterval(() => {
    loadNotifications();
}, 3000); // Cambiar a 5000 para 5 segundos
```

### Agregar nuevos presets

En `app.js` en el objeto `PRESETS`:
```javascript
const PRESETS = {
    nuevo_tipo: {
        type: 'nuevo',
        title: 'Título',
        message: 'Mensaje',
        priority: 2,
        ttl: 120
    }
};
```

Luego agregar al HTML en el select.

### Cambiar colores

En `styles.css` variables CSS:
```css
:root {
    --primary-color: #58CC02;  /* Verde Duolingo */
    --danger-color: #FF4B4B;
    --warning-color: #FFC800;
}
```

## Troubleshooting

### Las notificaciones no cargan

1. Verifica que el backend esté corriendo
2. Abre la consola (F12) para ver errores
3. Verifica CORS en el backend
4. Verifica la URL del API en `app.js`

### Auto-refresh no funciona

1. Verifica errores en la consola
2. El interval se configura en el `DOMContentLoaded`
3. Si hay errores de red, el auto-refresh continúa

### Estilos no se aplican

1. Verifica que `styles.css` esté en el mismo directorio
2. Limpia caché del navegador (Ctrl+Shift+R)

## Demo Tips

- Usa el selector de tipo para cambiar rápidamente entre presets
- Los botones de "Ejemplos Rápidos" cargan presets al instante
- Mantén el panel de notificaciones visible para ver actualizaciones
- Usa TTL cortos (10-30s) para demos rápidas
- Abre en pantalla completa para mejor impacto visual

## Futuras Mejoras

- [ ] Notificaciones en tiempo real con WebSockets
- [ ] Sonido al recibir notificación
- [ ] Animaciones más elaboradas
- [ ] Modo oscuro
- [ ] Filtros avanzados (por tipo, fecha)
- [ ] Exportar historial a CSV
- [ ] Gráficos de estadísticas

