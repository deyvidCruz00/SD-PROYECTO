# Email Service - Node.js

Microservicio de email desarrollado con Node.js, Express y Nodemailer.

## 🚀 Características

- **Framework**: Express.js para APIs REST
- **Email**: Nodemailer para envío de emails SMTP
- **Validación**: Joi para validación de datos
- **Mensajería**: Integración con Apache Kafka
- **Contenización**: Docker y Docker Compose
- **Seguridad**: Helmet y CORS
- **Logs**: Logging estructurado

## 📋 Prerrequisitos

- Node.js 18+
- Docker y Docker Compose
- Cuenta de Gmail con App Password configurada

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` con:

```env
PORT=8003
SERVICE_NAME=email-service-node

# SMTP Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=tu-email@gmail.com
SMTP_PASS=tu-app-password
SMTP_FROM_EMAIL=tu-email@gmail.com
SMTP_FROM_NAME=Tu App

# Kafka Configuration (opcional)
KAFKA_BROKER=kafka:9092
KAFKA_EMAIL_TOPIC=emails
KAFKA_GROUP_ID=email-service-group

# Environment
NODE_ENV=production
LOG_LEVEL=info
```

### Configurar Gmail App Password

1. Ir a Google Account Settings
2. Security > 2-Step Verification
3. App passwords > Generate app password
4. Usar la contraseña generada en `SMTP_PASS`

## 🐳 Ejecución con Docker

```bash
# Desde el directorio raíz del proyecto
docker-compose up -d email-service
```

## 💻 Ejecución Local

```bash
# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev

# Ejecutar en producción
npm start
```

## 📡 API Endpoints

### Health Check
```http
GET /api/v1/emails/health
```

### Enviar Email
```http
POST /api/v1/emails/send
Content-Type: application/json

{
    "to_email": "destinatario@example.com",
    "to_name": "Nombre Destinatario",
    "subject": "Asunto del email",
    "body": "Contenido del email",
    "template_data": {
        "variable": "valor"
    },
    "event_type": "welcome"
}
```

### Ver Logs de Emails
```http
GET /api/v1/emails/logs?limit=50
```

### Estadísticas
```http
GET /api/v1/emails/stats
```

## 🧪 Testing con Postman

Importar la colección `Email_Service_Collection.json` en Postman y configurar:

- Variable `base_url`: `http://localhost:8003`

## 📊 Monitoreo

El servicio incluye:
- Health checks automáticos
- Logging estructurado
- Métricas de emails enviados/fallidos
- Manejo de errores robusto

## 🔧 Desarrollo

```bash
# Instalar dependencias de desarrollo
npm install

# Ejecutar en modo desarrollo con auto-reload
npm run dev

# Ejecutar tests
npm test

# Análisis de código
npm run lint
```

## 📁 Estructura del Proyecto

```
email-service-node/
├── src/
│   ├── app.js              # Aplicación principal
│   ├── config/
│   │   └── index.js        # Configuración
│   ├── routes/
│   │   └── emails.js       # Rutas de API
│   └── services/
│       ├── emailService.js # Lógica de email
│       └── kafkaService.js # Integración Kafka
├── logs/                   # Logs del servicio
├── Dockerfile             # Configuración Docker
├── package.json           # Dependencias
└── README.md              # Este archivo
```

## 🚨 Seguridad

- ⚠️ **NUNCA** subir archivos `.env` a Git
- 🔐 Usar App Passwords de Gmail, no contraseñas normales
- 🛡️ El servicio funciona con usuario no-root en Docker
- 📝 Logs no incluyen información sensible

## 🐛 Troubleshooting

### Error de módulo no encontrado
```bash
# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

### Error de conexión SMTP
- Verificar credenciales de Gmail
- Confirmar que 2FA esté habilitado
- Usar App Password, no contraseña normal

### Error de Kafka (opcional)
- El servicio funciona sin Kafka
- Verificar que Kafka esté ejecutándose
- Revisar configuración de red en Docker

## 📚 Dependencias Principales

- **express**: Framework web
- **nodemailer**: Cliente SMTP
- **joi**: Validación de datos  
- **kafkajs**: Cliente Apache Kafka
- **helmet**: Seguridad HTTP
- **cors**: Control de CORS
- **dotenv**: Gestión de variables de entorno