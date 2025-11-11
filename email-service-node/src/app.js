const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const config = require('./config');
const emailRoutes = require('./routes/emails');
const kafkaService = require('./services/kafkaService');

const app = express();

// Middlewares de seguridad
app.use(helmet());
app.use(cors());

// Middleware para parsing JSON
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Middleware de logging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Rutas principales
app.get('/', (req, res) => {
  res.json({
    service: config.SERVICE_NAME,
    version: '1.0.0',
    status: 'running',
    timestamp: new Date().toISOString(),
    endpoints: [
      'GET / - Service info',
      'GET /api/v1/emails/health - Health check',
      'POST /api/v1/emails/send - Send email',
      'GET /api/v1/emails/logs - Get email logs',
      'GET /api/v1/emails/stats - Get statistics'
    ]
  });
});

// API Routes
app.use('/api/v1/emails', emailRoutes);

// Middleware de manejo de errores
app.use((err, req, res, next) => {
  console.error('Error no manejado:', err);
  res.status(500).json({
    error: 'Error interno del servidor',
    message: config.NODE_ENV === 'development' ? err.message : 'Ha ocurrido un error'
  });
});

// Manejo de rutas no encontradas
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Ruta no encontrada',
    path: req.originalUrl
  });
});

// Función para inicializar servicios
async function initializeServices() {
  try {
    console.log('🚀 Iniciando servicios...');
    
    // Inicializar Kafka solo si está configurado
    if (config.KAFKA.BROKER && config.KAFKA.BROKER !== '') {
      await kafkaService.initialize();
    } else {
      console.log('⚠️  Kafka no configurado, funcionando sin integración');
    }
    
    console.log('✅ Servicios inicializados');
  } catch (error) {
    console.error('❌ Error inicializando servicios:', error);
    // No terminar el proceso, continuar sin Kafka
  }
}

// Manejo de cierre graceful
process.on('SIGTERM', async () => {
  console.log('🔄 Recibido SIGTERM, cerrando servidor...');
  await kafkaService.disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('🔄 Recibido SIGINT, cerrando servidor...');
  await kafkaService.disconnect();
  process.exit(0);
});

// Iniciar servidor
const PORT = config.PORT;
app.listen(PORT, async () => {
  console.log(`🚀 ${config.SERVICE_NAME} ejecutándose en puerto ${PORT}`);
  console.log(`📧 SMTP configurado: ${config.SMTP.HOST}:${config.SMTP.PORT}`);
  console.log(`🌍 Ambiente: ${config.NODE_ENV}`);
  
  // Inicializar servicios después de que el servidor esté funcionando
  await initializeServices();
});

module.exports = app;