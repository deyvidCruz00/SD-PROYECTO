require('dotenv').config();

const config = {
  // Server Configuration
  PORT: process.env.PORT || 8003,
  SERVICE_NAME: process.env.SERVICE_NAME || 'email-service-node',
  
  // SMTP Configuration
  SMTP: {
    HOST: process.env.SMTP_HOST || 'smtp.gmail.com',
    PORT: parseInt(process.env.SMTP_PORT) || 587,
    SECURE: process.env.SMTP_SECURE === 'true',
    USER: process.env.SMTP_USER || '',
    PASS: process.env.SMTP_PASS || '',
    FROM_EMAIL: process.env.SMTP_FROM_EMAIL || process.env.SMTP_USER,
    FROM_NAME: process.env.SMTP_FROM_NAME || 'Colabora App'
  },
  
  // Kafka Configuration
  KAFKA: {
    BROKER: process.env.KAFKA_BROKER || 'localhost:9092',
    EMAIL_TOPIC: process.env.KAFKA_EMAIL_TOPIC || 'emails',
    GROUP_ID: process.env.KAFKA_GROUP_ID || 'email-service-group'
  },
  
  // Environment
  NODE_ENV: process.env.NODE_ENV || 'development',
  LOG_LEVEL: process.env.LOG_LEVEL || 'info'
};

module.exports = config;