podman build -t nutrirack:latest .
podman tag nutrirack:latest localhost:5000/nutritrack:latest
podman push --tls-verify=false localhost:5000/nutritrack:latest