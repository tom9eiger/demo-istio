#!/bin/bash
echo '#### Label Kafka Namespace for Istio Injection ####'
kubectl label namespace kafka istio-injection=enabled

echo '#### Create VirtualService and DestinationRule ####'
kubectl apply -f istio/kafka-virtualservice.yaml
kubectl apply -f istio/kafka-destinationrule.yaml

echo '#### Create Gateway and External VirtualService ####'
kubectl apply -f istio/kafka-gateway.yaml
kubectl apply -f istio/kafka-external-virtualservice.yaml

echo '#### Implement JWT Authentication ####'
kubectl apply -f istio/kafka-jwt-authentication.yaml

echo '#### Implement Authorization Policy ####'
kubectl apply -f istio/kafka-consumer-authorization.yaml

echo '#### Restrict Access to Producer and Use JWT ####'
kubectl apply -f istio/kafka-authorization.yaml

echo '### Enable Mutual TLS ###'
kubectl apply -f istio/peer-authentication.yaml


