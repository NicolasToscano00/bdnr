FROM node:18-alpine

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Instalar dependencias
# RUN npm ci --only=production
RUN npm install --omit=dev

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 5014

# Comando para iniciar
CMD ["node", "server.js"]

