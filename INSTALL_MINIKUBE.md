### Prerequisites

- Install a hypervisor (e.g., VirtualBox, Docker).
- Install kubectl.
- Install Helm.

### Step 1: Install and Start Minikube

1. **Install Minikube**:

    ```sh
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube
    ```

2. **Start Minikube with Calico CNI**:

    ```sh
    minikube start --cni=calico --memory=4096 --cpus=2
    ```

3. **Verify Calico Installation**:

    ```sh
    kubectl get pods -n kube-system | grep calico
    ```

### Step 2: Install MetalLB

1. **Create the MetalLB Namespace**:

    ```sh
    kubectl create namespace metallb-system
    ```

2. **Apply the MetalLB Manifest**:

    ```sh
    kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.7/manifests/metallb.yaml
    ```

3. **Configure MetalLB**:

    Determine a range of IP addresses in your local network to use for MetalLB. This range should not overlap with your DHCP pool.

    Create a ConfigMap for MetalLB with the chosen IP range:

    ```sh
    kubectl apply -f - <<EOF
    apiVersion: v1
    kind: ConfigMap
    metadata:
      namespace: metallb-system
      name: config
    data:
      config: |
        address-pools:
        - name: default
          protocol: layer2
          addresses:
          - 192.168.49.240-192.168.49.250
    EOF
    ```

    Adjust the IP range (`192.168.49.240-192.168.49.250`) to fit your local network configuration.


### Step 4: Install Argo CD

1. **Create the Argo CD Namespace**:

    ```sh
    kubectl create namespace argocd
    ```

2. **Install Argo CD**:

    Apply the Argo CD manifests:

    ```sh
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    ```

3. **Verify the Argo CD Pods**:

    ```sh
    kubectl get pods -n argocd
    ```

4. **Expose Argo CD Server with MetalLB**:

    ```sh
    kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
    ```

5. **Get the External IP for Argo CD Server**:

    ```sh
    kubectl get svc -n argocd
    ```

6. **Access Argo CD**:

    - **Get the Initial Admin Password**:

        ```sh
        kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode ; echo
        ```

    - **Login to Argo CD**:

        Open `http://<EXTERNAL_IP_ARGOCD_SERVER>` in your browser.
        - **Username:** `admin`
        - **Password:** (password retrieved in the previous step)

    - **Change the Default Password**:

        After logging in, it's recommended to change the default password.
        - Go to `Settings` -> `Account` -> `admin`.
        - Change the password.

### Step 5: Verify All Services

Ensure that all services (Prometheus, Alertmanager, Grafana, and Argo CD) are running and accessible:

- **Argo CD:** `http://<EXTERNAL_IP_ARGOCD_SERVER>`
