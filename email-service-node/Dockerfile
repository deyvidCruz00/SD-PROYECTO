# Usar Node.js LTS Alpine para imagen más pequeña
FROM node:18-alpine

# Instalar dependencias del sistema necesarias
RUN apk add --no-cache wget curl

# Crear directorio de trabajo
WORKDIR /app

# Copiar todo el proyecto primero (evita que COPY . . sobrescriba node_modules creados más tarde)
COPY package*.json ./
COPY . .

# Instalar dependencias en la imagen (hacerlo después de copiar evita problemas de sobre-escritura
# cuando el contexto local tiene directorios vacíos). Ejecutamos como root en build y luego
# ajustamos permisos para el usuario no-root.
RUN npm ci --only=production

# Crear usuario no-root para seguridad
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 && \
    chown -R nodejs:nodejs /app

USER nodejs

EXPOSE 8003

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8003/api/v1/emails/health || exit 1

CMD ["npm", "start"]
