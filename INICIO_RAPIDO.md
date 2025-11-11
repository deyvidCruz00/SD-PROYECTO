# 🚀 GUÍA DE INICIO RÁPIDO

## Requisitos Previos

✅ Verificar que tienes instalado:
- Docker Desktop (o Docker + Docker Compose)
- Git
- cURL (para testing)

## 1️⃣ INICIO EN 5 MINUTOS

### Opción A: Con Docker Compose (RECOMENDADO)

```bash
# 1. Clonar o descargar el proyecto
cd proyecto-microservicios

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Esperar a que todo inicie (15-30 segundos)
# 4. Verificar que todo está corriendo
docker-compose ps

# 5. Ver logs
docker-compose logs -f
```

✅ ¡Listo! Los servicios están corriendo.

### URLs de Acceso
- 📧 Notificaciones: http://localhost:8002
- ✉️ Email: http://localhost:8003
- 🌐 API Gateway: http://localhost:8080
- 📊 HAProxy Stats: http://localhost:8080/stats
- 🐘 MySQL: localhost:3306
- 🍃 Kafka: localhost:9092

---

## 2️⃣ PROBAR LOS SERVICIOS

### Test 1: Verificar que los servicios están vivos

```bash
# Notificaciones
curl http://localhost:8002/health

# Email
curl http://localhost:8003/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "service": "notifications-service"
}
```

### Test 2: Crear una notificación

```bash
curl -X POST http://localhost:8002/api/v1/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user",
    "type": "welcome",
    "title": "¡Bienvenido!",
    "message": "Bienvenido a Colabora"
  }'
```

### Test 3: Listar notificaciones

```bash
curl "http://localhost:8002/api/v1/notifications?user_id=test-user"
```

### Test 4: Enviar email

```bash
curl -X POST http://localhost:8003/api/v1/emails/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "test@example.com",
    "to_name": "Test User",
    "subject": "Test Email",
    "body": "<h1>Hola</h1><p>Este es un test</p>"
  }'
```

### Test 5: Ver estadísticas de email

```bash
curl http://localhost:8003/api/v1/emails/stats
```

---

## 3️⃣ USAR LA DOCUMENTACIÓN INTERACTIVA

Los servicios FastAPI tienen Swagger automático:

- 📚 **Notificaciones Swagger**: http://localhost:8002/docs
- 📚 **Email Swagger**: http://localhost:8003/docs

Aquí puedes:
- Ver todos los endpoints
- Probar directamente desde el navegador
- Ver ejemplos de request/response

---

## 4️⃣ TRABAJAR CON KAFKA

### Ver logs de Kafka

```bash
docker-compose logs -f kafka
```

### Crear topics manualmente

```bash
docker exec -it kafka kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic test-topic \
  --partitions 1 \
  --replication-factor 1 \
  --if-not-exists
```

### Enviar evento de prueba

```bash
docker exec -it kafka kafka-console-producer \
  --broker-list kafka:9092 \
  --topic notifications
```

Luego pega esto y presiona Enter:
```json
{
  "event_type": "test",
  "user_id": "test-user",
  "notification_type": "test",
  "title": "Test",
  "message": "This is a test",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

Presiona Ctrl+C para salir.

### Ver eventos en tiempo real

```bash
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic notifications \
  --from-beginning
```

---

## 5️⃣ VER LOGS

### Logs en tiempo real de todos los servicios
```bash
docker-compose logs -f
```

### Logs de un servicio específico
```bash
docker-compose logs -f notifications-service
docker-compose logs -f email-service
docker-compose logs -f mysql
docker-compose logs -f kafka
```

### Últimas 100 líneas
```bash
docker-compose logs --tail=100
```

---

## 6️⃣ USAR LA BASE DE DATOS MYSQL

### Acceder a MySQL

```bash
docker-compose exec mysql mysql -u user -p proyectos_db
# Contraseña: password

# Listar tablas
SHOW TABLES;

# Ver estructura de tabla
DESCRIBE notifications;

# Ejemplo query
SELECT * FROM notifications;
```

### Salir de MySQL
```bash
EXIT;
```

---

## 7️⃣ PARAR LOS SERVICIOS

### Detener (sin perder datos)
```bash
docker-compose down
```

### Detener y eliminar volúmenes (reinicio limpio)
```bash
docker-compose down -v
```

### Detener un servicio específico
```bash
docker-compose stop notifications-service
docker-compose stop email-service
```

### Reiniciar un servicio
```bash
docker-compose restart notifications-service
```

---

## 8️⃣ TROUBLESHOOTING

### Puerto ya está en uso

```bash
# Encontrar qué está usando el puerto (ej: 8002)
lsof -i :8002
# o en Windows
netstat -ano | findstr :8002

# Matar el proceso
kill <PID>  # En Windows: taskkill /PID <PID> /F
```

### Servicio no inicia

```bash
# Ver logs del servicio
docker-compose logs notifications-service

# Logs de todo
docker-compose logs

# Verificar que estén corriendo
docker-compose ps

# Reiniciar Docker
docker-compose down
docker-compose up -d
```

### Base de datos corrupta

```bash
# Eliminar volumen y recrear
docker-compose down -v
docker-compose up -d
```

### Kafka no conecta

```bash
# Verificar que Zookeeper está running
docker-compose logs zookeeper

# Verificar que Kafka está running  
docker-compose logs kafka

# Verificar conectividad
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
```

---

## 9️⃣ DESARROLLO LOCAL (Sin Docker)

### Notificaciones Service

```bash
cd notifications-service

# Crear venv
python -m venv venv

# Activar
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear .env
cp .env.example .env

# Editar .env con valores locales:
# KAFKA_BROKER=localhost:9092

# Ejecutar
python -m uvicorn app.main:app --reload --port 8002
```

### Email Service

```bash
cd email-service

# Mismo proceso que arriba, pero:
python -m uvicorn app.main:app --reload --port 8003
```

---

## 🔟 DOCUMENTACIÓN ADICIONAL

Después de revisar esta guía, consulta:

1. **README.md** - Documentación general completa
2. **ARQUITECTURA.md** - Diseño del sistema y flujos de datos
3. **ESTRUCTURA_PROYECTO.md** - Estructura de directorios
4. **INTEGRACION_BACKEND.md** - Cómo integrar con Spring Boot
5. **EJEMPLOS_EVENTOS.md** - Ejemplos de eventos Kafka
6. **TESTING.md** - Pruebas detalladas

---

## ✨ Checklist de Validación

- [ ] Docker Compose inició sin errores
- [ ] `docker-compose ps` muestra todos los servicios corriendo
- [ ] GET http://localhost:8002/health retorna 200
- [ ] GET http://localhost:8003/health retorna 200
- [ ] POST notificación funciona
- [ ] GET notificaciones funciona
- [ ] POST email funciona
- [ ] HAProxy stats en http://localhost:8080/stats
- [ ] Swagger en http://localhost:8002/docs
- [ ] Swagger en http://localhost:8003/docs

---

## 🎯 Próximos Pasos

### 1. Implementar Backend Spring Boot
- Ver INTEGRACION_BACKEND.md
- Crear project con Spring Boot
- Implementar Controllers, Services, Models
- Integrar Kafka Producer

### 2. Agregar Persistencia Real
- Actualmente los servicios usan memoria
- Necesita cambiar a usar Base de Datos real
- Usar SQLAlchemy en FastAPI

### 3. Implementar Frontend
- React, Vue o Angular
- Consumir APIs del Backend
- Integración con notificaciones (opcional: WebSocket)

### 4. Despliegue en Producción
- Configurar variables de entorno
- Setup de HTTPS
- Configurar dominios
- Monitoreo y alertas

---

## 📞 Comandos Útiles Rápidos

```bash
# Ver todo corriendo
docker-compose ps

# Logs en tiempo real
docker-compose logs -f

# Ejecutar comando en contenedor
docker-compose exec [servicio] [comando]

# Entrar a bash
docker-compose exec notifications-service bash

# Copiar archivo del contenedor
docker-compose cp notifications-service:/app/file.txt .

# Variables de entorno en servicio
docker-compose exec email-service env

# Reiniciar todo
docker-compose restart

# Parar todo
docker-compose stop

# Eliminar todo
docker-compose down

# Eliminar todo + volúmenes
docker-compose down -v

# Actualizar imágenes
docker-compose pull

# Construir imágenes
docker-compose build

# Ver tamaño de volúmenes
docker volume ls
docker volume inspect [nombre]
```

---

## 🎓 Ejemplo Completo: Flujo de Registro de Usuario

1. **Usuario registra** en la UI
2. **Backend recibe** POST /auth/register
3. **Backend crea** usuario en MySQL
4. **Backend publica** evento `user_registered` en Kafka topic `emails`
5. **Email Service** consume evento
6. **Email Service** renderiza plantilla `welcome.html`
7. **Email Service** envía email a usuario
8. **Email Service** registra en `email_logs`
9. **Usuario recibe** email de bienvenida

¡Así de simple! El sistema es asíncrono y desacoplado. 🎉

---

## 💪 ¡Estás Listo!

Ahora tienes:
- ✅ 2 microservicios FastAPI completamente funcionales
- ✅ Kafka para event streaming
- ✅ MySQL para persistencia
- ✅ Redis para caché
- ✅ HAProxy como API Gateway
- ✅ Docker Compose para orquestación

¡Comienza a desarrollar tu aplicación! 🚀
