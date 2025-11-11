# Testing de Microservicios

## Pruebas Manuales con cURL

### Notificaciones Service

#### 1. Health Check
```bash
curl -X GET http://localhost:8002/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "notifications-service"
}
```

#### 2. Crear Notificación
```bash
curl -X POST http://localhost:8002/api/v1/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "type": "project_invitation",
    "title": "Invitación a Proyecto",
    "message": "Has sido invitado al proyecto X",
    "related_project_id": "project-456"
  }'
```

**Respuesta esperada:**
```json
{
  "id": "notification-789",
  "user_id": "user-123",
  "type": "project_invitation",
  "title": "Invitación a Proyecto",
  "message": "Has sido invitado al proyecto X",
  "is_read": false,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00",
  "related_project_id": "project-456",
  "related_user_id": null,
  "related_task_id": null
}
```

#### 3. Obtener Notificaciones
```bash
curl -X GET "http://localhost:8002/api/v1/notifications?user_id=user-123&skip=0&limit=10"
```

#### 4. Marcar como Leída
```bash
curl -X PUT http://localhost:8002/api/v1/notifications/notification-789/read
```

#### 5. Contar No Leídas
```bash
curl -X GET "http://localhost:8002/api/v1/notifications/unread/count?user_id=user-123"
```

**Respuesta:**
```json
{
  "user_id": "user-123",
  "unread_count": 5
}
```

---

### Email Service

#### 1. Health Check
```bash
curl -X GET http://localhost:8003/health
```

#### 2. Enviar Email
```bash
curl -X POST http://localhost:8003/api/v1/emails/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "usuario@example.com",
    "to_name": "Juan Pérez",
    "subject": "Bienvenido a Colabora",
    "body": "<html><body>¡Hola Juan!</body></html>",
    "event_type": "welcome"
  }'
```

#### 3. Enviar Email con Plantilla
```bash
curl -X POST http://localhost:8003/api/v1/emails/send \
  -H "Content-Type: application/json" \
  -d '{
    "to_email": "usuario@example.com",
    "to_name": "Juan Pérez",
    "subject": "Invitación a Proyecto",
    "template_name": "project_invitation",
    "template_data": {
      "user_name": "Juan",
      "inviter_name": "María",
      "project_name": "Documental",
      "required_skills": "Video Editing, Color Grading"
    },
    "event_type": "project_invitation"
  }'
```

#### 4. Ver Logs
```bash
curl -X GET "http://localhost:8003/api/v1/emails/logs?skip=0&limit=10"
```

#### 5. Estadísticas
```bash
curl -X GET http://localhost:8003/api/v1/emails/stats
```

**Respuesta:**
```json
{
  "total_sent": 42,
  "total_failed": 2,
  "total_pending": 1
}
```

---

## Pruebas con Docker Compose

### Ver logs de un servicio
```bash
docker-compose logs notifications-service
docker-compose logs email-service
docker-compose logs -f notifications-service  # Seguimiento en tiempo real
```

### Ver logs de todos los servicios
```bash
docker-compose logs -f
```

### Ejecutar comando en contenedor
```bash
docker-compose exec notifications-service bash
docker-compose exec email-service bash
```

### Verificar estado de servicios
```bash
docker-compose ps
```

---

## Testing con Kafka

### Enviar evento de prueba

```bash
# 1. Acceder al contenedor de Kafka
docker exec -it kafka bash

# 2. Usar kafka-console-producer para enviar evento
kafka-console-producer --broker-list localhost:9092 --topic notifications

# 3. Pegar el siguiente JSON y presionar Enter:
{
  "event_type": "test_notification",
  "user_id": "test-user-123",
  "notification_type": "test",
  "title": "Test Notification",
  "message": "This is a test message",
  "timestamp": "2024-01-15T10:30:00Z"
}

# Presionar Ctrl+C para salir
```

### Consumir eventos

```bash
# Ver eventos en tiempo real
docker exec kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic notifications \
  --from-beginning

# Listar todos los topics
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

---

## Test Suite Automático (Python)

### Crear archivo `test_services.py`

```python
import requests
import json
from datetime import datetime

BASE_NOTIFICATIONS = "http://localhost:8002"
BASE_EMAIL = "http://localhost:8003"

def test_notifications_health():
    """Test health check"""
    response = requests.get(f"{BASE_NOTIFICATIONS}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Notifications health check passed")

def test_email_health():
    """Test health check"""
    response = requests.get(f"{BASE_EMAIL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Email health check passed")

def test_create_notification():
    """Test creating a notification"""
    payload = {
        "user_id": "test-user-123",
        "type": "test",
        "title": "Test Notification",
        "message": "This is a test message"
    }
    response = requests.post(
        f"{BASE_NOTIFICATIONS}/api/v1/notifications",
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test-user-123"
    print(f"✅ Created notification: {data['id']}")
    return data["id"]

def test_get_notifications():
    """Test getting notifications"""
    response = requests.get(
        f"{BASE_NOTIFICATIONS}/api/v1/notifications?user_id=test-user-123&skip=0&limit=10"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(f"✅ Retrieved {len(data)} notifications")

def test_mark_as_read(notification_id):
    """Test marking notification as read"""
    response = requests.put(
        f"{BASE_NOTIFICATIONS}/api/v1/notifications/{notification_id}/read"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_read"] == True
    print(f"✅ Marked notification as read")

def test_send_email():
    """Test sending email"""
    payload = {
        "to_email": "test@example.com",
        "to_name": "Test User",
        "subject": "Test Email",
        "body": "<html><body>This is a test email</body></html>"
    }
    response = requests.post(
        f"{BASE_EMAIL}/api/v1/emails/send",
        json=payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["to_email"] == "test@example.com"
    assert data["status"] == "sent"
    print(f"✅ Sent email: {data['id']}")

def test_email_stats():
    """Test email stats"""
    response = requests.get(f"{BASE_EMAIL}/api/v1/emails/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_sent" in data
    assert "total_failed" in data
    print(f"✅ Email stats: {data}")

if __name__ == "__main__":
    try:
        print("🧪 Running tests...\n")
        
        # Notifications tests
        print("📧 Testing Notifications Service...")
        test_notifications_health()
        notif_id = test_create_notification()
        test_get_notifications()
        test_mark_as_read(notif_id)
        
        # Email tests
        print("\n📧 Testing Email Service...")
        test_email_health()
        test_send_email()
        test_email_stats()
        
        print("\n✅ All tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
```

### Ejecutar tests

```bash
pip install requests
python test_services.py
```

---

## Checklist de Validación

- [ ] MySQL está corriendo
- [ ] Kafka está corriendo
- [ ] Redis está corriendo
- [ ] Notifications Service health check: ✅
- [ ] Email Service health check: ✅
- [ ] Crear notificación: ✅
- [ ] Listar notificaciones: ✅
- [ ] Marcar como leída: ✅
- [ ] Contar no leídas: ✅
- [ ] Enviar email: ✅
- [ ] Ver stats de email: ✅
- [ ] Eventos de Kafka se procesan: ✅

---

## Troubleshooting

### El servicio no responde
```bash
# Verificar logs
docker-compose logs notifications-service

# Verificar puerto
netstat -tulpn | grep 8002

# Reiniciar servicio
docker-compose restart notifications-service
```

### Kafka no conecta
```bash
# Verificar que Zookeeper está corriendo
docker-compose logs zookeeper

# Verificar conectividad a Kafka
docker exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
```

### Base de datos no inicia
```bash
# Ver logs de MySQL
docker-compose logs mysql

# Eliminar volúmenes y recrear
docker-compose down -v
docker-compose up -d
```
