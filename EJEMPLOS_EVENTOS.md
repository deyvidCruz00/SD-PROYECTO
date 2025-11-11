# Ejemplos de Eventos Kafka

## 1. Evento: Usuario Registrado

### Topic: `users` y `emails`

```json
{
  "event_type": "user_registered",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "juanartista",
  "email": "juan@example.com",
  "full_name": "Juan Pérez García",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Consumo en Email Service:**
- Renderiza plantilla `welcome`
- Envía email de bienvenida a `juan@example.com`
- Registra en `email_logs` con `event_type: "user_registered"`

---

## 2. Evento: Solicitud de Membresía Enviada

### Topic: `notifications` y `emails`

```json
{
  "event_type": "join_request_sent",
  "request_id": "660e8400-e29b-41d4-a716-446655440001",
  "project_creator_id": "550e8400-e29b-41d4-a716-446655440002",
  "project_creator_email": "creador@example.com",
  "project_creator_name": "María Directora",
  "applicant_id": "550e8400-e29b-41d4-a716-446655440000",
  "applicant_username": "juanartista",
  "applicant_email": "juan@example.com",
  "project_id": "770e8400-e29b-41d4-a716-446655440003",
  "project_title": "Documental Ecológico",
  "timestamp": "2024-01-15T11:45:00Z"
}
```

**Consumo en Notifications Service:**
```
Crear notificación:
- user_id: 550e8400-e29b-41d4-a716-446655440002 (creador)
- type: "join_request"
- title: "Nueva Solicitud de Membresía"
- message: "juanartista ha solicitado unirse a 'Documental Ecológico'"
- related_project_id: 770e8400-e29b-41d4-a716-446655440003
- related_user_id: 550e8400-e29b-41d4-a716-446655440000
```

**Consumo en Email Service:**
- Renderiza plantilla `project_invitation`
- Envía email a `creador@example.com`
- Subject: "Nuevo artista quiere unirse a tu proyecto"

---

## 3. Evento: Solicitud de Membresía Aprobada

### Topic: `notifications` y `emails`

```json
{
  "event_type": "join_request_approved",
  "request_id": "660e8400-e29b-41d4-a716-446655440001",
  "approved_by": "550e8400-e29b-41d4-a716-446655440002",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_email": "juan@example.com",
  "user_name": "Juan Pérez García",
  "project_id": "770e8400-e29b-41d4-a716-446655440003",
  "project_title": "Documental Ecológico",
  "timestamp": "2024-01-15T14:20:00Z"
}
```

**Consumo en Notifications Service:**
```
Crear notificación:
- user_id: 550e8400-e29b-41d4-a716-446655440000 (usuario que solicito)
- type: "join_request_approved"
- title: "¡Aceptado al Proyecto!"
- message: "María Directora te ha aceptado en 'Documental Ecológico'"
- related_project_id: 770e8400-e29b-41d4-a716-446655440003
```

**Consumo en Email Service:**
- Renderiza plantilla `request_approved`
- Envía email a `juan@example.com`
- Notifica que fue aceptado

---

## 4. Evento: Tarea Asignada

### Topic: `notifications` y `emails`

```json
{
  "event_type": "task_assigned",
  "task_id": "880e8400-e29b-41d4-a716-446655440004",
  "project_id": "770e8400-e29b-41d4-a716-446655440003",
  "project_title": "Documental Ecológico",
  "assigned_to_id": "550e8400-e29b-41d4-a716-446655440000",
  "assigned_to_email": "juan@example.com",
  "assigned_to_name": "Juan Pérez García",
  "assigned_by_id": "550e8400-e29b-41d4-a716-446655440002",
  "assigned_by_name": "María Directora",
  "task_title": "Edición de Intro",
  "task_description": "Editar intro del documental con música de fondo",
  "priority": "high",
  "due_date": "2024-01-22T17:00:00Z",
  "timestamp": "2024-01-15T15:00:00Z"
}
```

**Consumo en Notifications Service:**
```
Crear notificación:
- user_id: 550e8400-e29b-41d4-a716-446655440000
- type: "task_assigned"
- title: "Nueva Tarea Asignada: Edición de Intro"
- message: "María Directora te ha asignado una tarea en 'Documental Ecológico'"
- related_project_id: 770e8400-e29b-41d4-a716-446655440003
- related_task_id: 880e8400-e29b-41d4-a716-446655440004
```

**Consumo en Email Service:**
- Renderiza plantilla `task_assigned`
- Envía email con detalles de la tarea

---

## 5. Evento: Proyecto Creado

### Topic: `projects`

```json
{
  "event_type": "project_created",
  "project_id": "770e8400-e29b-41d4-a716-446655440003",
  "creator_id": "550e8400-e29b-41d4-a716-446655440002",
  "creator_name": "María Directora",
  "title": "Documental Ecológico",
  "description": "Documental sobre biodiversidad en la selva amazónica",
  "category": "Documentary",
  "required_skills": [
    {
      "skill": "video_editing",
      "level": "advanced"
    },
    {
      "skill": "color_grading",
      "level": "intermediate"
    }
  ],
  "status": "open",
  "timestamp": "2024-01-15T09:00:00Z"
}
```

**Consumo:**
- Indexar proyecto en búsqueda
- Notificar a usuarios interesados en las skills requeridas

---

## 6. Evento: Estado de Tarea Actualizado

### Topic: `notifications`

```json
{
  "event_type": "task_status_updated",
  "task_id": "880e8400-e29b-41d4-a716-446655440004",
  "project_id": "770e8400-e29b-41d4-a716-446655440003",
  "project_title": "Documental Ecológico",
  "task_title": "Edición de Intro",
  "old_status": "in_progress",
  "new_status": "review",
  "updated_by_id": "550e8400-e29b-41d4-a716-446655440000",
  "updated_by_name": "Juan Pérez García",
  "timestamp": "2024-01-16T16:30:00Z"
}
```

**Consumo en Notifications Service:**
```
Crear notificación para creador del proyecto:
- user_id: 550e8400-e29b-41d4-a716-446655440002
- type: "task_status_changed"
- title: "Tarea en Revisión"
- message: "Juan Pérez García ha marcado 'Edición de Intro' para revisión"
- related_task_id: 880e8400-e29b-41d4-a716-446655440004
```

---

## 7. Evento: Colaborador Removido

### Topic: `notifications` y `emails`

```json
{
  "event_type": "member_removed",
  "project_id": "770e8400-e29b-41d4-a716-446655440003",
  "project_title": "Documental Ecológico",
  "removed_user_id": "550e8400-e29b-41d4-a716-446655440000",
  "removed_user_email": "juan@example.com",
  "removed_user_name": "Juan Pérez García",
  "removed_by_id": "550e8400-e29b-41d4-a716-446655440002",
  "removed_by_name": "María Directora",
  "reason": "Project requirements changed",
  "timestamp": "2024-01-17T10:15:00Z"
}
```

**Consumo:**
- Notificación al usuario removido
- Email informando la remoción

---

## Estructura General de Eventos

Todo evento debe contener:
```json
{
  "event_type": "string",        // Tipo único del evento
  "timestamp": "ISO8601",        // Cuando ocurrió
  "correlation_id": "string",    // (opcional) para trazar flujos
  "source": "backend",           // De donde viene
  "version": "1.0"               // Versión del evento
}
```

## Testing con Kafka Console

### Enviar evento manual a Kafka:

```bash
# Desde la máquina host
docker exec -it kafka kafka-console-producer \
  --broker-list kafka:9092 \
  --topic notifications

# Luego pega el JSON del evento
```

### Consumir eventos:

```bash
# Ver eventos en tiempo real
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic notifications \
  --from-beginning

# Ver solo últimos eventos
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic notifications
```
