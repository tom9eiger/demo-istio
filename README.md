# Istio-Kafka Authentication and Authorization Setup

This repository contains the necessary configurations and deployment files to set up a Kafka consumer application with Istio, including JWT authentication and authorization policies.

## Prerequisites

- Kubernetes cluster (Minikube, kind, or managed Kubernetes service)
- kubectl configured to interact with your cluster
- Istio CLI (`istioctl`) installed
- Calico for network policies
- Docker installed for building images

## Step-by-Step Instructions

### 1. Install Istio

1. Download Istio:
    ```sh
    curl -L https://istio.io/downloadIstio | sh -
    cd istio-1.14.1
    export PATH=$PWD/bin:$PATH
    ```

2. Install Istio Base:
    ```sh
    istioctl install --set profile=demo -y
    ```

3. Enable Ingress and Egress Gateways:
    ```sh
    kubectl apply -f samples/addons
    ```

### 2. Install Calico

1. Install Calico for Network Policies:
    ```sh
    kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
    ```

### 3. Deploy Kafka Components

1. Create Kafka Namespace:
    ```sh
    kubectl create namespace kafka
    ```

2. Deploy Zookeeper:
    ```sh
    kubectl apply -f deployments/zookeeper-deployment.yaml
    ```

3. Deploy Kafka:
    ```sh
    kubectl apply -f deployments/kafka-deployment.yaml
    ```

4. Create Kafka Service:
    ```sh
    kubectl apply -f deployments/kafka-service.yaml
    ```

### 4. Deploy Kafka Consumer

1. Deploy Kafka Consumer:
    ```sh
    kubectl apply -f deployments/kafka-consumer-deployment.yaml
    ```

### 5. Deploy JWT Issuer

1. Build and Push Docker Image:
    ```sh
    docker build -t jwt-issuer:latest ./jwt-issuer
    docker tag jwt-issuer:latest <your-dockerhub-username>/jwt-issuer:latest
    docker push <your-dockerhub-username>/jwt-issuer:latest
    ```

2. Deploy JWT Issuer:
    ```sh
    kubectl apply -f deployments/jwt-issuer-deployment.yaml
    kubectl apply -f deployments/jwt-issuer-service.yaml
    ```

### 6. Configure Istio for Kafka

1. Label Kafka Namespace for Istio Injection:
    ```sh
    kubectl label namespace kafka istio-injection=enabled
    ```

2. Create VirtualService and DestinationRule:
    ```sh
    kubectl apply -f istio/kafka-virtualservice.yaml
    kubectl apply -f istio/kafka-destinationrule.yaml
    ```

3. Create Gateway and External VirtualService:
    ```sh
    kubectl apply -f istio/kafka-gateway.yaml
    kubectl apply -f istio/kafka-external-virtualservice.yaml
    ```

### 7. Implement JWT Authentication

1. Create JWT Authentication Policy:
    ```sh
    kubectl apply -f istio/kafka-jwt-authentication.yaml
    ```

### 8. Implement Authorization Policy

1. Create Authorization Policy:
    ```sh
    kubectl apply -f istio/kafka-consumer-authorization.yaml
    ```

### 9. Restrict Access to Producer and Use JWT

1. Create AuthorizationPolicy to restrict access to the Kafka broker:
    ```sh
    kubectl apply -f istio/kafka-authorization.yaml
    ```

### 10. Enable Mutual TLS

1. Create PeerAuthentication Policy:
    ```sh
    kubectl apply -f istio/peer-authentication.yaml
    ```

### 11. Observability with Istio

1. Deploy Prometheus, Grafana, and Jaeger:
    ```sh
    kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/addons/prometheus.yaml
    kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/addons/grafana.yaml
    kubectl apply -f https://raw.githubusercontent.com/istio/istio/master/samples/addons/jaeger.yaml
    ```

2. Access Grafana Dashboard:
    ```sh
    istioctl dashboard grafana
    ```

3. Access Jaeger Tracing:
    ```sh
    istioctl dashboard jaeger
    ```

### 12. Configure External Kafka Producer

1. Build and Run Kafka Producer Docker Image:

    ```sh
    docker build -t kafka-producer:latest ./kafka-producer
    docker run --rm -it kafka-producer:latest
    ```

## Verifying the Setup

### Test JWT Authentication

1. Ensure you have a valid JWT token from the specified issuer.
2. Make a request to the Kafka consumer service with the JWT token in the Authorization header:
    ```sh
    curl --header "Authorization: Bearer <your-jwt-token>" http://<kafka-consumer-service-url>
    ```

### Test Authorization

1. Ensure that only requests matching the authorization policy (e.g., GET requests to `/`) are allowed:
    ```sh
    curl --header "Authorization: Bearer <your-jwt-token>" http://<kafka-consumer-service-url>
    ```

### Verify External Producer

1. Check the logs of the Kafka consumer in Kubernetes to ensure it received messages from the external producer:
    ```sh
    kubectl logs <kafka-consumer-pod-name> -n kafka
    ```

## Files

- **deployments/kafka-consumer-deployment.yaml**: Deployment configuration for Kafka consumer.
- **deployments/kafka-service.yaml**: Service configuration for Kafka.
- **deployments/zookeeper-deployment.yaml**: Deployment configuration for Zookeeper.
- **deployments/kafka-deployment.yaml**: Deployment configuration for Kafka.
- **deployments/jwt-issuer-deployment.yaml**: Deployment configuration for JWT issuer.
- **deployments/jwt-issuer-service.yaml**: Service configuration for JWT issuer.
- **istio/kafka-jwt-authentication.yaml**: JWT authentication policy.
- **istio/kafka-consumer-authorization.yaml**: Authorization policy for Kafka consumer.
- **istio/kafka-virtualservice.yaml**: VirtualService for Kafka.
- **istio/kafka-destinationrule.yaml**: DestinationRule for Kafka.
- **istio/kafka-gateway.yaml**: Gateway configuration for external access.
- **istio/kafka-external-virtualservice.yaml**: VirtualService for external access.
- **istio/kafka-authorization.yaml**: AuthorizationPolicy for restricting access.
- **istio/peer-authentication.yaml**: PeerAuthentication policy to enable mutual TLS.
- **jwt-issuer/Dockerfile**: Dockerfile for JWT issuer.
- **jwt-issuer/package.json**: Package.json for JWT issuer.
- **jwt-issuer/server.js**: Server script for JWT issuer.
- **jwt-issuer/jwks.json**: JWKS file for JWT issuer.
- **kafka-producer/Dockerfile**: Dockerfile for Kafka producer.
- **kafka-producer/kafka_producer.py**: Kafka producer script to run in the Docker container.
