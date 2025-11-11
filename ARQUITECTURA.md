## Arquitectura y Flujos de Datos

### Flujo 1: Nuevo Usuario Se Registra

```
1. Usuario llena formulario de registro
   └─> POST /auth/register (Backend)
       ├─> Crear usuario en MySQL
       ├─> Publicar evento: "user_registered" a Kafka (topic: emails)
       └─> Retornar JWT

2. Email Service consume evento
   └─> Procesa mensaje de Kafka
       ├─> Busca plantilla "welcome"
       ├─> Renderiza con datos del usuario
       └─> Envía email de bienvenida
           └─> Registra en email_logs

3. Backend retorna response al cliente
   └─> Cliente guarda JWT en localStorage
```

### Flujo 2: Usuario Solicita Membresía a Proyecto

```
1. Artista clica en "Solicitar Membresía"
   └─> POST /projects/{id}/join-request (Backend)
       ├─> Verificar skills del usuario
       ├─> Crear join_request en MySQL
       ├─> Publicar evento: "join_request_sent" (topic: notifications + emails)
       └─> Retornar 201 Created

2. Notifications Service consume evento
   └─> Procesa mensaje de Kafka
       ├─> Crear notificación para creador del proyecto
       ├─> Guardar en memory/BD
       └─> Notificar si hay WebSocket conectado

3. Email Service consume evento
   └─> Procesa mensaje de Kafka
       ├─> Obtener email del creador del proyecto
       ├─> Renderizar plantilla "project_invitation"
       └─> Enviar email notificando de la solicitud

4. Creador recibe notificación
   └─> Ve en UI y puede aceptar/rechazar
       ├─> POST /projects/{id}/join-request/{requestId}/approve
       ├─> Actualizar join_request status
       ├─> Agregar usuario a project_members
       ├─> Publicar evento: "join_request_approved"
       └─> Notificar al usuario solicitante
```

### Flujo 3: Tarea Asignada a Usuario

```
1. Creador del proyecto asigna tarea
   └─> PUT /projects/{id}/tasks/{taskId}
       ├─> Actualizar assigned_to
       ├─> Publicar evento: "task_assigned" (topic: notifications + emails)
       └─> Retornar 200 OK

2. Notifications Service consume evento
   └─> Crear notificación para usuario asignado
       └─> is_read = false

3. Email Service consume evento
   └─> Enviar email al usuario
       └─> Template: "task_assigned"

4. Usuario ve notificación
   └─> GET /api/v1/notifications?user_id=xxx
       └─> Retorna lista de notificaciones no leídas
```

## Patrones de Implementación

### Pattern: Event Sourcing
Todos los cambios importantes se registran como eventos en Kafka, permitiendo:
- Auditoria completa
- Integración débil entre servicios
- Posibilidad de replaying eventos

### Pattern: SAGA (Transacciones Distribuidas)
Para operaciones que afectan múltiples servicios:
```
Request → Backend → Publica Evento 1 → Servicio A (confirma/rechaza)
                  → Publica Evento 2 → Servicio B (confirma/rechaza)
```

### Pattern: Circuit Breaker
Importante implementar en Backend para comunicación con microservicios:
```python
# Ejemplo en Backend (Java)
@CircuitBreaker(delay = 2000, timeout = 1000)
public void sendNotification(NotificationEvent event) {
    // Llamar a notifications-service
}
```

## Escalabilidad

### Horizontal Scaling
- Kafka permite múltiples consumidores del mismo topic
- Cada instancia de servicio se registra en un grupo de consumidores
- Las particiones se distribuyen automáticamente

### Vertical Scaling
- Aumentar réplicas en Docker Compose
- Usar load balancer (ya incluido HAProxy)

## Limitaciones Actuales y Mejoras Futuras

### Limitaciones
1. ✗ Persistencia real en microservicios (usando memoria)
2. ✗ No hay retries con backoff exponencial
3. ✗ WebSocket no implementado para notificaciones en tiempo real
4. ✗ No hay rate limiting

### Mejoras Futuras
1. Implementar persistencia en PostgreSQL
2. Agregar autenticación entre servicios
3. Implementar WebSocket para push notifications
4. Agregar circuit breakers
5. Implementar distributed tracing (Jaeger)
6. Agregar métricas (Prometheus + Grafana)
7. Rate limiting y throttling
8. Message queue persistence en Kafka
