#!/bin/bash

# Script para iniciar la aplicación en desarrollo

set -e

echo "🚀 Iniciando proyecto de microservicios..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Iniciar servicios con Docker Compose
echo "📦 Iniciando servicios con Docker Compose..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 15

# Verificar salud de servicios
echo "🏥 Verificando salud de servicios..."

services=("notifications-service" "email-service")
for service in "${services[@]}"; do
    echo -n "Verificando $service..."
    if curl -s http://localhost:$(docker-compose port $service 8002 | cut -d: -f2)/health > /dev/null 2>&1 || \
       curl -s http://localhost:$(docker-compose port $service 8003 | cut -d: -f2)/health > /dev/null 2>&1; then
        echo " ✅"
    else
        echo " ⏳ (aún iniciando)"
    fi
done

echo ""
echo "✅ Servicios iniciados exitosamente!"
echo ""
echo "📋 URLs de servicios:"
echo "  - Backend:           http://localhost:8001"
echo "  - Notifications:     http://localhost:8002"
echo "  - Email:             http://localhost:8003"
echo "  - API Gateway:       http://localhost:8080"
echo "  - MySQL:             localhost:3306"
echo "  - Kafka:             localhost:9092"
echo "  - Redis:             localhost:6379"
echo ""
echo "📊 Dashboards:"
echo "  - HAProxy Stats:     http://localhost:8080/stats"
echo "  - Swagger Notif:     http://localhost:8002/docs"
echo "  - Swagger Email:     http://localhost:8003/docs"
echo ""
echo "Usa 'docker-compose logs -f' para ver logs en tiempo real"
echo "Usa 'docker-compose down' para detener los servicios"
