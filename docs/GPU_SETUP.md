# GPU Setup for Ollama

## Overview
The Docker Compose configuration has been updated to support GPU acceleration for the Ollama service, which can significantly improve LLM inference performance.

## Prerequisites

### For Linux Systems with NVIDIA GPUs

1. **Install NVIDIA Container Toolkit**:
   ```bash
   # Add the package repositories
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
         && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
         && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
               sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
               sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

   # Install the package
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit

   # Configure Docker to use the NVIDIA runtime
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```

2. **Verify GPU Access**:
   ```bash
   # Test GPU access in Docker
   docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi
   ```

### For macOS Systems
⚠️ **Note**: Docker Desktop on macOS does not support GPU acceleration. For optimal performance on Mac, run Ollama as a standalone application outside of Docker containers.

### For Windows Systems with WSL2
1. Install WSL2 with GPU support
2. Follow the Linux setup steps within WSL2
3. Ensure Docker Desktop is configured to use WSL2 backend

## Configuration Changes Made

### docker-compose.yml
Added GPU resource allocation to the Ollama service:
```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

### docker-compose.debug.yml
Added the same GPU configuration to ensure debug mode also has GPU support.

## Running with GPU Support

### Production Mode
```bash
docker-compose up -d
```

### Debug Mode
```bash
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up -d
```

## Fallback to CPU-Only Mode

If you don't have a compatible GPU or the NVIDIA Container Toolkit installed, you can run in CPU-only mode by:

1. **Temporarily disable GPU**: Comment out or remove the `deploy` section from the Ollama service in both compose files
2. **Alternative**: Create a separate `docker-compose.cpu.yml` override file without GPU configuration

## Verification

Once the containers are running, you can verify GPU usage:

1. **Check if Ollama is using GPU**:
   ```bash
   docker exec -it rag_ollama nvidia-smi
   ```

2. **Monitor GPU usage while running models**:
   ```bash
   watch -n 1 'docker exec -it rag_ollama nvidia-smi'
   ```

## Performance Benefits

With GPU acceleration, you can expect:
- Significantly faster model inference (2-10x speedup depending on model size and GPU)
- Better performance with larger models (7B, 13B, 70B parameter models)
- Reduced latency for chat responses
- Ability to run multiple models simultaneously

## Troubleshooting

### Common Issues:

1. **"could not select device driver" error**: 
   - Ensure NVIDIA Container Toolkit is properly installed
   - Restart Docker daemon after installation

2. **GPU not detected**:
   - Verify NVIDIA drivers are installed: `nvidia-smi`
   - Check Docker GPU support: `docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu20.04 nvidia-smi`

3. **Performance not improved**:
   - Verify the model is actually loaded on GPU (check `nvidia-smi` output)
   - Some smaller models (1B-3B parameters) may not benefit significantly from GPU acceleration