#!/bin/bash

# Script para crear topics en Kafka
# Ejecutar después de que Kafka haya iniciado

echo "📋 Creando topics en Kafka..."

# Esperar a que Kafka esté listo
sleep 10

# Crear topics
docker exec -it kafka kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic notifications \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

docker exec -it kafka kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic emails \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

docker exec -it kafka kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic users \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

docker exec -it kafka kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic projects \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

docker exec -it kafka kafka-topics --create \
  --bootstrap-server kafka:9092 \
  --topic tasks \
  --partitions 3 \
  --replication-factor 1 \
  --if-not-exists

echo "✅ Topics creados exitosamente"

# Listar topics
echo ""
echo "📚 Topics existentes:"
docker exec kafka kafka-topics --list --bootstrap-server kafka:9092
