# ⚡ QUICKSTART

## 🚀 Levantar Todo

```bash
docker-compose up
```

Abre: **http://localhost:8080**

---

## 🎯 Servicios que se Levantan

✅ **Redis** → Puerto 6379  
✅ **Backend Node.js** → Puerto 5014  
✅ **Backend .NET** → Puerto 5015  
✅ **Frontend** → Puerto 8080  

---

## 🔄 Cambiar de Backend

Por defecto usa **Node.js (5014)**

Para usar **.NET (5015)**:

1. Edita `demo-frontend/app.js` línea 3:
```javascript
const API_URL = "http://localhost:5015/Notifications";
```

2. Recarga: **Cmd + Shift + R**

---

## 🛑 Detener

```bash
docker-compose down
```

---

## 📊 Comparación Rápida

| Feature | Node.js | .NET |
|---------|---------|------|
| Puerto | 5014 | 5015 |
| Velocidad | ⚡⚡⚡ | ⚡⚡ |
| Tamaño | 5 MB | 14 MB |
| Arquitectura | Simple | Enterprise |

**Ambos funcionan igual a nivel de Redis.**

---

## 💡 Tips

- Ver logs: `docker-compose logs -f`
- Solo Node.js: `docker-compose logs -f backend-node`
- Solo .NET: `docker-compose logs -f backend-dotnet`

---

**¡Ambos backends corriendo al mismo tiempo!** 🎉
