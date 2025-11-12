# Proyecto Microservicios# Proyecto de Microservicios - Colabora App



Sistema de microservicios para gestión de proyectos colaborativos.Sistema de gestión de proyectos colaborativos entre artistas, con microservicios para notificaciones y emails.

## Servicios

## Servicios Docker

### Backend Principal (Spring Boot)

- `zookeeper`: Coordinación para Kafka- **Puerto**: 8001

- `kafka`: Message broker- **Funcionalidad**:

- `redis`: Cache y sesiones  - Autenticación JWT

- `mysql`: Base de datos principal  - Gestión de usuarios (Admin, Artistas)

- `email-service`: Servicio de emails (Node.js)  - CRUD de proyectos

- `notifications-service`: Servicio de notificaciones (Python)  - Gestión de tareas (tipo Jira)

- `api-gateway`: Proxy reverso (HAProxy)  - Gestión de solicitudes de membresía

  - Publicación de eventos a Kafka

## Configuración

### Notifications Service (FastAPI)

Cada microservicio requiere variables de entorno específicas. Ver archivos `.env.example` en cada directorio de servicio.- **Puerto**: 8002

- **Funcionalidad**:

### Email Service  - Almacenamiento de notificaciones

```env  - Lectura/no lectura de notificaciones

SMTP_USER=your-email@gmail.com  - Consumo de eventos de Kafka

SMTP_PASS=your-app-password  - WebSocket para notificaciones en tiempo real (opcional)

```

### Email Service (FastAPI)

## Monitoreo- **Puerto**: 8003

- **Funcionalidad**:

- **Health Checks**: Cada servicio expone `/health`  - Envío de emails

- **HAProxy Stats**: `http://localhost:8080/stats`  - Plantillas de email

- **Logs**: `docker-compose logs <service>`  - Consumo de eventos de Kafka
  - Registro de logs de envíos

## Características de la Aplicación

### Gestión de Usuarios
- Registro de artistas (nombre, alias, teléfono, correo)
- Autenticación con JWT
- Dos tipos de usuarios: Admin y Artista
- Perfiles públicos de artistas

### Gestión de Skills
- Agregar skills al perfil
- Niveles de skill (beginner, intermediate, advanced, expert)
- Descripción de experiencia

### Gestión de Proyectos
- Crear proyectos con skills requeridos
- Filtrar proyectos por skills/categorías
- Dashboard de proyectos abiertos
- Editar proyecto (solo creador)
- Seguimiento de progreso

### Gestión de Tareas
- Crear tareas en proyectos
- Asignar tareas a miembros
- Estados de tarea (todo, in_progress, review, done)
- Editar tareas (solo creador del proyecto)

### Gestión de Membresía
- Solicitar membresía a proyectos
- Aceptar/rechazar solicitudes
- Notificaciones de nuevas solicitudes
- Eliminar colaboradores (solo creador)

## Instalación y Configuración

### Requisitos
- Docker y Docker Compose
- Java 17+ (si ejecutas backend localmente)
- Python 3.11+ (si ejecutas servicios FastAPI localmente)

### Inicio Rápido

```bash
# Clonar el repositorio
git clone <repository>
cd proyecto-microservicios

# Iniciar todos los servicios con Docker Compose
docker-compose up -d

# Verificar que los servicios están corriendo
docker-compose ps
```

### Configuración de Servicios FastAPI Localmente

#### Notificaciones Service

```bash
cd notifications-service

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Ejecutar
python -m uvicorn app.main:app --reload --port 8002
```

#### Email Service

```bash
cd email-service

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env
# Configurar credenciales SMTP en .env

# Ejecutar
python -m uvicorn app.main:app --reload --port 8003
```

## Endpoints API

### Notificaciones Service

```
GET    /api/v1/notifications?user_id=xxx&skip=0&limit=10  - Obtener notificaciones
GET    /api/v1/notifications/unread/count?user_id=xxx     - Contar no leídas
POST   /api/v1/notifications                               - Crear notificación
PUT    /api/v1/notifications/{id}/read                     - Marcar como leída
PUT    /api/v1/notifications/user/{user_id}/read-all       - Marcar todas como leídas
DELETE /api/v1/notifications/{id}                          - Eliminar notificación
GET    /api/v1/notifications/health                        - Health check
```

### Email Service

```
POST   /api/v1/emails/send                        - Enviar email
GET    /api/v1/emails/logs?skip=0&limit=10       - Obtener logs
GET    /api/v1/emails/logs/{email_id}            - Obtener log específico
GET    /api/v1/emails/stats                      - Estadísticas
GET    /api/v1/emails/health                     - Health check
```

## Eventos Kafka

### Topics

- **notifications**: Eventos para el servicio de notificaciones
- **emails**: Eventos para el servicio de email

### Ejemplos de Eventos

#### Evento de Invitación a Proyecto

```json
{
  "event_type": "project_invitation",
  "user_id": "user-123",
  "notification_type": "project_invitation",
  "title": "Invitación a Proyecto",
  "message": "Has sido invitado al proyecto X",
  "timestamp": "2024-01-10T10:30:00Z",
  "related_project_id": "project-456"
}
```

#### Evento de Registro de Usuario

```json
{
  "event_type": "user_registered",
  "to_email": "artist@example.com",
  "to_name": "Juan Artist",
  "subject": "¡Bienvenido a Colabora!",
  "template_name": "welcome",
  "template_data": {
    "user_name": "Juan"
  },
  "timestamp": "2024-01-10T10:30:00Z",
  "related_user_id": "user-123"
}
```

## Base de Datos

Se utilizan las siguientes tablas:
- `users` - Usuarios del sistema
- `skills` - Catálogo de habilidades
- `user_skills` - Habilidades por usuario
- `projects` - Proyectos
- `project_required_skills` - Habilidades requeridas por proyecto
- `project_members` - Miembros de proyectos
- `project_join_requests` - Solicitudes para unirse
- `tasks` - Tareas de proyectos
- `notifications` - Notificaciones
- `email_logs` - Registro de emails

## Seguridad

- Autenticación JWT en el backend
- Validación de permisos en operaciones
- CORS configurado en todos los servicios
- Validación de entrada con Pydantic

## Monitoreo

### Health Checks
- `GET /health` - Verificación de estado en cada servicio
- Logs centralizados en `docker-compose` con `docker-compose logs`

### HAProxy Stats
- `GET http://localhost:8080/stats` - Dashboard de HAProxy

## Desarrollo

### Agregar Nueva Notificación

1. En el backend, publicar evento en Kafka:
```python
kafka_producer.send("notifications", {
    "event_type": "nuevo_evento",
    "user_id": "user-123",
    "notification_type": "tipo_notif",
    "title": "Título",
    "message": "Mensaje",
    "timestamp": datetime.utcnow()
})
```

2. El microservicio de notificaciones consume y almacena

### Agregar Nuevo Template de Email

1. Agregar plantilla en `email_service/app/services/email_service.py`
2. Usar al publicar evento en Kafka
3. El servicio renderiza con Jinja2

## Despliegue

### Con Docker Compose
```bash
docker-compose up -d
```

