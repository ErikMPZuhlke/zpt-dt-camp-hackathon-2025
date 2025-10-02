# 🚀 GPU Acceleration Setup Guide

## 🎯 Overview

The RAG Chatbot system supports **NVIDIA GPU acceleration** for both **Ollama LLM inference** and **HuggingFace embedding generation**. This can dramatically improve performance from 70+ seconds to 10-15 seconds per query.

## ✅ Current GPU Configuration Status

The system is **already configured** for GPU acceleration with:
- **Ollama**: GPU-accelerated LLM inference with 24-hour model keep-alive
- **Backend**: GPU-accelerated embedding generation using CUDA
- **Performance Optimization**: Model persistence to eliminate cold starts

## 🏃‍♂️ Quick GPU Verification

### 1. Check GPU Availability
```bash
# Verify GPU is detected
nvidia-smi

# Test GPU in Docker (if NVIDIA runtime is installed)
docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu20.04 nvidia-smi
```

### 2. Verify Container GPU Access
```bash
# Check if containers have GPU access
docker-compose up -d
docker exec rag_backend python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

### 3. Performance Testing
```bash
# Test API response time with GPU
curl -w "\nTime: %{time_total}s\n" -X GET "http://localhost:8000/query/?user_question=What%20is%20the%20Option%20type&persona=domain_expert"
```

## ⚙️ GPU Setup by Platform

### 🐧 **Linux with NVIDIA GPU** (Recommended)

#### Prerequisites
- NVIDIA GPU with CUDA Compute Capability 6.0+
- NVIDIA drivers 470.57.02+
- Docker 19.03+

#### Setup NVIDIA Container Runtime
```bash
# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
          sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
          sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker daemon
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify installation
docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu20.04 nvidia-smi
```

### 🪟 **Windows with WSL2** (Current Working Setup)

#### Prerequisites
- Windows 11 or Windows 10 version 21H2+
- WSL2 enabled
- NVIDIA GPU drivers 470.76+ installed on Windows
- Docker Desktop with WSL2 backend

#### Verification Steps
```powershell
# Check GPU in WSL2
wsl -d Ubuntu -- nvidia-smi

# Verify Docker GPU access
docker run --rm --gpus all nvidia/cuda:12.0-base-ubuntu20.04 nvidia-smi
```

### 🍎 **macOS** (Limited Support)

**⚠️ Limitation**: Docker Desktop on macOS doesn't support GPU acceleration.

**Alternative Approach**:
1. Run Ollama natively on macOS for Metal GPU acceleration
2. Keep backend and frontend in Docker containers
3. Update `OLLAMA_URL` to point to host machine

```bash
# Install Ollama natively on macOS
brew install ollama

# Start Ollama service
ollama serve

# Pull the model
ollama pull llama3.2:3b

# Update docker-compose.yml to remove ollama service
# Update backend OLLAMA_URL to http://host.docker.internal:11434
```

## 🔧 GPU Configuration Details

### Current docker-compose.yml Configuration
```yaml
services:
  ollama:
    image: ollama/ollama:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    environment:
      - OLLAMA_KEEP_ALIVE=24h  # Keep model in GPU memory
    
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - TORCH_CUDA_ARCH_LIST=6.0;6.1;7.0;7.5;8.0;8.6;9.0
```

### Performance Optimizations Implemented

#### 1. Model Keep-Alive (Eliminates Cold Starts)
- **Setting**: `OLLAMA_KEEP_ALIVE=24h`
- **Benefit**: Model stays loaded in GPU memory
- **Impact**: First request: ~50s, subsequent: ~10-15s

#### 2. CUDA Compatibility
- **Architecture Support**: CUDA 6.0 through 9.0
- **Memory Management**: Automatic GPU memory allocation
- **Fallback**: CPU execution if GPU unavailable

#### 3. Embedding Acceleration
- **Library**: Sentence Transformers with CUDA support
- **Models**: `all-MiniLM-L6-v2` optimized for GPU
- **Caching**: Embedding results cached to avoid recomputation

## 📊 Performance Benchmarks

### Response Time Comparison

| Configuration | First Request | Subsequent Requests | Model Loading |
|---------------|---------------|---------------------|---------------|
| **CPU Only** | 180+ seconds | 60-90 seconds | Every request |
| **GPU + Keep-Alive** | 50-60 seconds | 10-15 seconds | Once per day |
| **Optimal** | 10-15 seconds | 10-15 seconds | Pre-warmed |

### GPU Memory Usage
- **Ollama (llama3.2:3b)**: ~2GB VRAM
- **Backend Embeddings**: ~500MB VRAM  
- **Total Requirements**: ~3GB VRAM minimum
- **Tested Hardware**: NVIDIA RTX 2000 Ada Generation (8GB VRAM)

## 🚨 Troubleshooting

### Common Issues

#### 1. "No CUDA GPUs Available"
```bash
# Check NVIDIA runtime
docker info | grep nvidia

# Reinstall NVIDIA container toolkit if missing
sudo apt-get install nvidia-container-toolkit
sudo systemctl restart docker
```

#### 2. "Driver Version Too Old"
```bash
# Check driver version
nvidia-smi

# Update NVIDIA drivers (Ubuntu/Debian)
sudo ubuntu-drivers autoinstall
sudo reboot
```

#### 3. "Out of Memory" Errors
```bash
# Check GPU memory usage
nvidia-smi

# Restart containers to free GPU memory
docker-compose down
docker-compose up -d
```

#### 4. Slow Performance Despite GPU
```bash
# Check if model is staying loaded
docker-compose logs ollama | grep "llama runner"

# Verify OLLAMA_KEEP_ALIVE setting
docker exec rag_ollama env | grep KEEP_ALIVE
```

### Debug Commands
```bash
# Check container GPU access
docker exec rag_backend python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
docker exec rag_ollama ollama list

# Monitor GPU usage during requests
watch nvidia-smi

# Check container resource usage
docker stats
```

## 🎯 Expected Performance

### With GPU Acceleration ✅
- **Setup Time**: ~2-3 minutes (includes model download)
- **First Query**: 50-60 seconds (model loading to GPU)
- **Subsequent Queries**: 10-15 seconds
- **Model Persistence**: 24 hours in GPU memory

### Without GPU Acceleration ⚠️
- **Setup Time**: ~1-2 minutes
- **Every Query**: 60-180+ seconds
- **Model Loading**: Every request or after timeout

## 🔗 Related Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture with GPU integration details
- **[DEBUG_GUIDE.md](DEBUG_GUIDE.md)** - Debugging GPU-accelerated containers
- **[README.md](../README.md)** - Quick start guide with GPU verification steps
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