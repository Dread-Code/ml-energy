# 🚀 CUDA & cuDNN Installation Guide for TensorFlow (Linux)

This document outlines the complete process to set up CUDA and cuDNN on your Linux system so that TensorFlow can detect and use the GPU properly.

---

## 1. Identify Required Versions for TensorFlow

1. Open a Python interpreter and run:

   ```python
   import tensorflow as tf
   build_info = tf.sysconfig.get_build_info()
   print("Required CUDA:", build_info["cuda_version"])
   print("Required cuDNN:", build_info["cudnn_version"])
   ```

2. Note the output values:

   - `Required CUDA`: e.g., `12.5.1`
   - `Required cuDNN`: e.g., `9`

---

## 2. Install the NVIDIA Driver

 Make sure your system has an NVIDIA driver compatible with the required CUDA version:

```bash
sudo apt update
sudo apt install nvidia-driver-570
```

Reboot your system and verify:

```bash
nvidia-smi
```

You should see your GPU and the driver version listed.

---

## 3. Install the CUDA Toolkit

1. Download and install the appropriate CUDA version (e.g., 12.5):

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"
sudo apt update
sudo apt install cuda-12-5 -y
```

2. Add CUDA to your environment in `~/.bashrc`:

```bash
echo 'export PATH=/usr/local/cuda-12.5/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.5/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

3. Verify the installation:

```bash
nvcc --version  # Should display: release 12.5.1
```

---

## 4. Install cuDNN

1. Download the cuDNN 9 `.deb` files (runtime + dev) from NVIDIA.
2. Install them:

```bash
sudo dpkg -i libcudnn9_*_amd64.deb
sudo dpkg -i libcudnn9-dev_*_amd64.deb
```

3. Reload the shared library cache:

```bash
sudo ldconfig
```

4. Confirm cuDNN is registered:

```bash
ldconfig -p | grep cudnn
```

You should see entries like `/usr/local/cuda-12.5/lib64/libcudnn.so.9`.

---

## 5. Validate GPU Detection in Python

Run:

```bash
python3 - <<EOF
import tensorflow as tf
print("Built with CUDA:", tf.test.is_built_with_cuda())
print("GPUs:", tf.config.list_physical_devices("GPU"))
EOF
```

Expected output:
- `Built with CUDA:` should be `True`
- `GPUs:` should list your device, e.g. `[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]`

---

## 6. Troubleshooting Tips

- **Command not found**: Ensure `cuda-12-5` is installed and `PATH` is correctly set.
- **cuDNN conflicts**: Make sure only the required cuDNN version is loaded via `/etc/ld.so.conf.d/`.
- **GPU not detected**: Check if the NVIDIA driver is loaded (`lsmod | grep nvidia`) and that `nouveau` is disabled.

---

# 🐳 Docker Configuration for NVIDIA GPU Runtime

## 1. Verify NVIDIA Driver on the Host

```bash
nvidia-smi
```

If not found:

```bash
sudo apt update
sudo apt install -y nvidia-driver-525
sudo reboot
```

---

## 2. Install the NVIDIA Container Toolkit

```bash
sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /usr/share/keyrings
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | \
  sudo tee /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg > /dev/null

# Replace with your distro
distribution=$(. /etc/os-release && echo $ID$VERSION_ID)

curl -s -L https://nvidia.github.io/libnvidia-container/config/${distribution}/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
```

---

## 3. Configure Docker Daemon

Create or edit `/etc/docker/daemon.json`:

```json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

Check:

```bash
docker info | grep -i nvidia
```

---

## 4. Test Docker with GPU

```bash
docker run --rm --gpus all nvidia/cuda:12.5.1-base-ubuntu22.04 nvidia-smi
```

For TensorFlow:

```bash
docker run --rm --gpus all -it tensorflow/tensorflow:latest-gpu-jupyter bash
```

Inside container:

```bash
python3 - <<EOF
import tensorflow as tf
print("GPUs detected:", tf.config.list_physical_devices("GPU"))
EOF
```

---

## 5. JupyterHub DockerSpawner with GPU Support

Add in `jupyterhub_config.py`:

```python
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner

c.DockerSpawner.extra_container_spec = {
  "runtime": "nvidia",
  "device_requests": [
    {
      "Driver": "nvidia",
      "Count": -1,
      "Capabilities": [["gpu"]],
    }
  ]
}

c.DockerSpawner.image = "tensorflow/tensorflow:latest-gpu-jupyter"
```

---

## 6. Docker Compose Snippet Example

```yaml
version: "3.8"

services:
  notebook:
    image: tensorflow-notebook
    build:
      context: .
      dockerfile: Dockerfile.notebook
    runtime: nvidia
    gpus: all
    environment:
      NVIDIA_VISIBLE_DEVICES: all
    networks:
      - jupyterhub-network

  hub:
    build:
      context: .
      dockerfile: Dockerfile.jupyterhub
      args:
        JUPYTERHUB_VERSION: latest
    restart: always
    image: jupyterhub
    container_name: jupyterhub
    runtime: nvidia
    environment:
      JUPYTERHUB_ADMIN: jupyteradmin
      DOCKER_NETWORK_NAME: jupyterhub-network
      DOCKER_NOTEBOOK_IMAGE: tensorflow-notebook
      DOCKER_NOTEBOOK_DIR: /home/jovyan/work
      GITHUB_CLIENT_ID: ${GITHUB_CLIENT_ID}
      GITHUB_CLIENT_SECRET: ${GITHUB_CLIENT_SECRET}
      OAUTH_CALLBACK_URL: ${OAUTH_CALLBACK_URL}
    ports:
      - "8000:8000"
    volumes:
      - "./jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py:ro"
      - "/var/run/docker.sock:/var/run/docker.sock:rw"
      - "jupyterhub-data:/data"
      - "/etc/passwd:/etc/passwd:ro"
      - "/etc/shadow:/etc/shadow:ro"
      - "/etc/group:/etc/group:ro"
    networks:
      - jupyterhub-network

volumes:
  jupyterhub-data:

networks:
  jupyterhub-network:
    name: jupyterhub-network
```

You now have a fully working GPU-enabled TensorFlow + Docker + JupyterHub setup. ✅