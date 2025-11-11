const { Kafka } = require('kafkajs');
const config = require('../config');
const emailService = require('./emailService');

class KafkaService {
  constructor() {
    this.kafka = new Kafka({
      clientId: config.SERVICE_NAME,
      brokers: [config.KAFKA.BROKER]
    });
    
    this.consumer = null;
    this.producer = null;
  }

  async initialize() {
    try {
      // Verificar si Kafka está configurado
      if (!config.KAFKA.BROKER || config.KAFKA.BROKER === '') {
        console.log('⚠️  Kafka no configurado, saltando inicialización');
        return;
      }

      console.log('🔄 Intentando conectar a Kafka...');
      
      this.producer = this.kafka.producer();
      this.consumer = this.kafka.consumer({ groupId: config.KAFKA.GROUP_ID });
      
      // Timeout para conexión de Kafka más largo y con manejo de error
      const connectPromise = (async () => {
        await this.producer.connect();
        await this.consumer.connect();
      })();

      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('Timeout conectando a Kafka')), 15000);
      });

      await Promise.race([connectPromise, timeoutPromise]);
      
      console.log('✅ Kafka conectado exitosamente');
      
      // Suscribirse al topic de emails
      await this.consumer.subscribe({ topic: config.KAFKA.EMAIL_TOPIC });
      
      // Procesar mensajes
      await this.consumer.run({
        eachMessage: async ({ topic, partition, message }) => {
          try {
            const emailData = JSON.parse(message.value.toString());
            console.log(`📨 Mensaje recibido de Kafka:`, emailData);
            
            // Procesar el email
            await emailService.sendEmail(emailData);
          } catch (error) {
            console.error('❌ Error procesando mensaje de Kafka:', error);
          }
        }
      });
      
      console.log('🎧 Consumidor de Kafka iniciado');
      
    } catch (error) {
      console.error('❌ Error conectando a Kafka:', error.message);
      console.log('⚠️  Continuando sin Kafka...');
      // No lanzar error, permitir que el servicio continúe sin Kafka
      
      // Limpiar referencias en caso de error parcial
      if (this.producer) {
        try { await this.producer.disconnect(); } catch (e) { /* ignore */ }
        this.producer = null;
      }
      if (this.consumer) {
        try { await this.consumer.disconnect(); } catch (e) { /* ignore */ }
        this.consumer = null;
      }
    }
  }

  async publishEmail(emailData) {
    try {
      if (!this.producer) {
        throw new Error('Producer no inicializado');
      }

      await this.producer.send({
        topic: config.KAFKA.EMAIL_TOPIC,
        messages: [{
          key: emailData.to_email,
          value: JSON.stringify({
            ...emailData,
            timestamp: new Date().toISOString()
          })
        }]
      });

      console.log('📤 Mensaje enviado a Kafka');
    } catch (error) {
      console.error('❌ Error enviando mensaje a Kafka:', error);
      throw error;
    }
  }

  async disconnect() {
    try {
      if (this.producer) await this.producer.disconnect();
      if (this.consumer) await this.consumer.disconnect();
      console.log('🔌 Kafka desconectado');
    } catch (error) {
      console.error('❌ Error desconectando Kafka:', error);
    }
  }
}

module.exports = new KafkaService();