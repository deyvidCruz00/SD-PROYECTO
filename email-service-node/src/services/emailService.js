const nodemailer = require('nodemailer');
const { v4: uuidv4 } = require('uuid');
const config = require('../config');

class EmailService {
  constructor() {
    this.transporter = null;
    this.emailLogs = []; // En producción, esto debería ser una base de datos
    this.stats = {
      total_sent: 0,
      total_failed: 0,
      total_pending: 0
    };
    this.initializeTransporter();
  }

  async initializeTransporter() {
    try {
      this.transporter = nodemailer.createTransport({
        host: config.SMTP.HOST,
        port: config.SMTP.PORT,
        secure: config.SMTP.SECURE,
        auth: {
          user: config.SMTP.USER,
          pass: config.SMTP.PASS
        }
      });

      // Verificar la conexión
      await this.transporter.verify();
      console.log('✅ Transporter SMTP configurado correctamente');
    } catch (error) {
      console.error('❌ Error configurando transporter SMTP:', error.message);
    }
  }

  async sendEmail({ to_email, to_name, subject, body, template_data, event_type, related_user_id, related_project_id }) {
    const emailId = uuidv4();
    const timestamp = new Date();

    try {
      // Procesar template si hay datos
      let processedBody = body;
      if (template_data && typeof template_data === 'object') {
        processedBody = this.processTemplate(body, template_data);
      }

      // Configurar el email
      const mailOptions = {
        from: `"${config.SMTP.FROM_NAME}" <${config.SMTP.FROM_EMAIL}>`,
        to: to_name ? `"${to_name}" <${to_email}>` : to_email,
        subject: subject,
        html: this.formatEmailBody(processedBody),
        text: processedBody
      };

      console.log(`📧 Enviando email a ${to_email}...`);
      
      // Enviar el email
      const info = await this.transporter.sendMail(mailOptions);
      
      // Registro del email enviado
      const emailLog = {
        id: emailId,
        to_email,
        to_name,
        subject,
        status: 'sent',
        created_at: timestamp,
        sent_at: new Date(),
        message_id: info.messageId,
        event_type,
        related_user_id,
        related_project_id,
        error_message: null
      };

      this.emailLogs.unshift(emailLog);
      this.stats.total_sent++;
      
      console.log(`✅ Email enviado exitosamente: ${emailId}`);
      console.log(`📨 Message ID: ${info.messageId}`);
      
      return emailLog;

    } catch (error) {
      console.error(`❌ Error enviando email: ${error.message}`);
      
      // Registro del email fallido
      const emailLog = {
        id: emailId,
        to_email,
        to_name,
        subject,
        status: 'failed',
        created_at: timestamp,
        sent_at: null,
        message_id: null,
        event_type,
        related_user_id,
        related_project_id,
        error_message: error.message
      };

      this.emailLogs.unshift(emailLog);
      this.stats.total_failed++;
      
      throw error;
    }
  }

  processTemplate(template, data) {
    let processed = template;
    for (const [key, value] of Object.entries(data)) {
      const regex = new RegExp(`{{${key}}}`, 'g');
      processed = processed.replace(regex, value);
    }
    return processed;
  }

  formatEmailBody(body) {
    // Convertir saltos de línea a HTML
    return body.replace(/\n/g, '<br>');
  }

  getEmailLogs(limit = 50) {
    return this.emailLogs.slice(0, limit);
  }

  getStats() {
    return this.stats;
  }

  getHealth() {
    return {
      status: 'healthy',
      service: config.SERVICE_NAME,
      smtp_configured: !!this.transporter,
      timestamp: new Date().toISOString()
    };
  }
}

module.exports = new EmailService();