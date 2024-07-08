#!/bin/bash
echo '#### Deploy Kafka Components ####'
kubectl apply -f deployments/kafka-namespace.yaml
kubectl apply -f deployments/zookeeper-deployment.yaml
kubectl apply -f deployments/kafka-deployment.yaml
kubectl apply -f deployments/kafka-service.yaml

echo '#### Deploy Kafka Consumer ####'
kubectl apply -f deployments/kafka-consumer-deployment.yaml

echo '#### Deploy Deploy JWT Issuer ####'
kubectl apply -f deployments/jwt-issuer-deployment.yaml
kubectl apply -f deployments/jwt-issuer-service.yaml