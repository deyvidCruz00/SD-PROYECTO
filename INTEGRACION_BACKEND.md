# Guía de Integración: Cómo el Backend Publica Eventos

## Archivo: KafkaProducerConfig.java

```java
package com.colabora.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.DefaultKafkaProducerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.core.ProducerFactory;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.kafka.support.serializer.JsonSerializer;
import org.springframework.beans.factory.annotation.Value;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaProducerConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Bean
    public ProducerFactory<String, Object> producerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        configProps.put(ProducerConfig.ACKS_CONFIG, "all");
        configProps.put(ProducerConfig.RETRIES_CONFIG, 3);
        return new DefaultKafkaProducerFactory<>(configProps);
    }

    @Bean
    public KafkaTemplate<String, Object> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}
```

## Archivo: EventPublisher.java

```java
package com.colabora.kafka;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class EventPublisher {

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    public void publishUserRegisteredEvent(UserRegisteredEvent event) {
        log.info("Publicando evento: user_registered");
        kafkaTemplate.send("users", "user_registered", event);
        kafkaTemplate.send("emails", "user_registered", event);
    }

    public void publishJoinRequestSentEvent(JoinRequestSentEvent event) {
        log.info("Publicando evento: join_request_sent");
        kafkaTemplate.send("notifications", "join_request_sent", event);
        kafkaTemplate.send("emails", "join_request_sent", event);
    }

    public void publishJoinRequestApprovedEvent(JoinRequestApprovedEvent event) {
        log.info("Publicando evento: join_request_approved");
        kafkaTemplate.send("notifications", "join_request_approved", event);
        kafkaTemplate.send("emails", "join_request_approved", event);
    }

    public void publishTaskAssignedEvent(TaskAssignedEvent event) {
        log.info("Publicando evento: task_assigned");
        kafkaTemplate.send("notifications", "task_assigned", event);
        kafkaTemplate.send("emails", "task_assigned", event);
    }

    public void publishProjectCreatedEvent(ProjectCreatedEvent event) {
        log.info("Publicando evento: project_created");
        kafkaTemplate.send("projects", "project_created", event);
    }
}
```

## Archivo: UserController.java

```java
@RestController
@RequestMapping("/api/auth")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private EventPublisher eventPublisher;

    @PostMapping("/register")
    public ResponseEntity<UserDTO> register(@RequestBody RegisterRequest request) {
        // 1. Crear usuario
        User user = userService.createUser(request);

        // 2. Publicar evento
        eventPublisher.publishUserRegisteredEvent(new UserRegisteredEvent(
            user.getId(),
            user.getUsername(),
            user.getEmail(),
            user.getFullName()
        ));

        // 3. Retornar response
        return ResponseEntity.status(201).body(new UserDTO(user));
    }
}
```

## Archivo: ProjectController.java

```java
@RestController
@RequestMapping("/api/projects")
public class ProjectController {

    @Autowired
    private ProjectService projectService;

    @Autowired
    private EventPublisher eventPublisher;

    @PostMapping("/{projectId}/join-request")
    public ResponseEntity<?> sendJoinRequest(
            @PathVariable String projectId,
            @RequestBody JoinRequestDTO request,
            @AuthenticationPrincipal User currentUser) {

        // 1. Validar solicitud
        projectService.validateJoinRequest(projectId, currentUser.getId());

        // 2. Crear solicitud
        JoinRequest joinRequest = projectService.createJoinRequest(projectId, currentUser.getId(), request);

        // 3. Obtener proyecto y creador
        Project project = projectService.getProject(projectId);
        User projectCreator = userService.getUser(project.getCreatorId());

        // 4. Publicar evento
        eventPublisher.publishJoinRequestSentEvent(new JoinRequestSentEvent(
            joinRequest.getId(),
            projectCreator.getId(),
            projectCreator.getEmail(),
            projectCreator.getFullName(),
            currentUser.getId(),
            currentUser.getUsername(),
            project.getId(),
            project.getTitle()
        ));

        // 5. Retornar response
        return ResponseEntity.status(201).body(new JoinRequestDTO(joinRequest));
    }

    @PostMapping("/{projectId}/join-request/{requestId}/approve")
    public ResponseEntity<?> approveJoinRequest(
            @PathVariable String projectId,
            @PathVariable String requestId,
            @AuthenticationPrincipal User currentUser) {

        // 1. Validar que sea el creador
        projectService.validateProjectCreator(projectId, currentUser.getId());

        // 2. Obtener solicitud
        JoinRequest joinRequest = projectService.getJoinRequest(requestId);

        // 3. Aprobar solicitud
        projectService.approveJoinRequest(requestId);
        projectService.addProjectMember(projectId, joinRequest.getUserId());

        // 4. Obtener usuario que solicito
        User requestingUser = userService.getUser(joinRequest.getUserId());

        // 5. Publicar evento
        eventPublisher.publishJoinRequestApprovedEvent(new JoinRequestApprovedEvent(
            joinRequest.getId(),
            requestingUser.getId(),
            requestingUser.getEmail(),
            projectId,
            projectService.getProject(projectId).getTitle()
        ));

        return ResponseEntity.ok().build();
    }
}
```

## Modelos de Eventos

```java
// UserRegisteredEvent.java
@Data
@AllArgsConstructor
public class UserRegisteredEvent {
    private String userId;
    private String username;
    private String email;
    private String fullName;
    private LocalDateTime timestamp = LocalDateTime.now();
}

// JoinRequestSentEvent.java
@Data
@AllArgsConstructor
public class JoinRequestSentEvent {
    private String requestId;
    private String projectCreatorId;
    private String projectCreatorEmail;
    private String projectCreatorName;
    private String applicantId;
    private String applicantUsername;
    private String projectId;
    private String projectTitle;
    private LocalDateTime timestamp = LocalDateTime.now();
}

// TaskAssignedEvent.java
@Data
@AllArgsConstructor
public class TaskAssignedEvent {
    private String taskId;
    private String userId;
    private String userEmail;
    private String projectId;
    private String projectTitle;
    private String taskTitle;
    private String taskDescription;
    private LocalDateTime timestamp = LocalDateTime.now();
}
```

## Configuración application.yml

```yaml
spring:
  kafka:
    bootstrap-servers: kafka:9092
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all
      retries: 3
      
logging:
  level:
    org.springframework.kafka: INFO
    com.colabora.kafka: DEBUG
```

## Resumen de Flujo

1. **Usuario registra** → Backend crea usuario → Publica `user_registered`
   - ✉️ Email Service: Envía email de bienvenida
   - 🔔 Notifications Service: (opcional) crear notificación de bienvenida

2. **Usuario solicita membresía** → Backend crea join_request → Publica `join_request_sent`
   - 🔔 Notifications Service: Notifica al creador del proyecto
   - ✉️ Email Service: Envía email al creador del proyecto

3. **Creador aprueba solicitud** → Backend agrega usuario → Publica `join_request_approved`
   - 🔔 Notifications Service: Notifica al usuario que fue aceptado
   - ✉️ Email Service: Envía email de confirmación

4. **Tarea asignada** → Backend asigna tarea → Publica `task_assigned`
   - 🔔 Notifications Service: Notifica al usuario
   - ✉️ Email Service: Envía email de tarea asignada
