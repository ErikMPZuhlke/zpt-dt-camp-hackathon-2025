# 🐛 VS Code Remote Debugging Guide

## 🎯 Overview

This guide shows how to set up real-time debugging for both frontend and backend services using Visual Studio Code while they run in Docker containers. This enables you to set breakpoints, inspect variables, and step through code running inside Docker containers as if it were running locally.

## 🛠️ Prerequisites

### Required VS Code Extensions
1. **Python Debugger (Pylance)** - `ms-python.debugpy`
2. **Docker** - `ms-azuretools.vscode-docker`
3. **Python** - `ms-python.python`

### System Requirements
- VS Code 1.80+
- Docker Desktop running
- Python 3.10+ (for local development)

## 🚀 Quick Start Debugging

### 1. Start Debug Services
```bash
# Option 1: Use VS Code Command Palette
# Ctrl+Shift+P → "Tasks: Run Task" → "Start Debug Stack"

# Option 2: Use terminal
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up -d --build
```

### 2. Attach Debugger
```bash
# Option 1: Use VS Code Debug Panel (Ctrl+Shift+D)
# Select "Debug Full Stack" and press F5

# Option 2: Individual services
# Select "Debug Backend (Docker)" or "Debug Frontend (Docker)"
```

### 3. Set Breakpoints
- Open any Python file in `backend/` or `frontend/`
- Click in the gutter to set breakpoints (red dots)
- The debugger will pause execution when breakpoints are hit

## 🔧 Debug Configuration Details

### Debug Ports
- **Backend Debug Port**: `5678` (mapped to host)
- **Frontend Debug Port**: `5679` (mapped to host)
- **Backend Application**: `8000`
- **Frontend Application**: `8501`

### Debug Commands
The debug containers run with `debugpy` waiting for client attachment:

```bash
# Backend debug command
python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Frontend debug command  
python -m debugpy --listen 0.0.0.0:5679 --wait-for-client -m streamlit run ui/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

## 📁 File Structure for Debugging

### VS Code Configuration Files
```
.vscode/
├── launch.json          # Debug configurations
└── tasks.json           # Build and deploy tasks
```

### Docker Debug Files
```
docker-compose.debug.yml    # Debug service overrides
backend/Dockerfile.debug    # Backend with debugpy
frontend/Dockerfile.debug   # Frontend with debugpy
```

## 🎛️ Available Debug Configurations

### 1. Debug Backend (Docker)
- **Purpose**: Debug FastAPI backend service
- **Port**: 5678
- **Debugs**: API routes, RAG engine, data processing
- **Pre-task**: Starts backend + ollama services

### 2. Debug Frontend (Docker)
- **Purpose**: Debug Streamlit frontend service  
- **Port**: 5679
- **Debugs**: UI components, user interactions
- **Pre-task**: Starts frontend + backend + ollama services

### 3. Debug Full Stack
- **Purpose**: Debug both services simultaneously
- **Features**: Compound configuration, coordinated startup/shutdown
- **Use Case**: End-to-end debugging across services

## � GPU Debugging Support

### GPU-Accelerated Debug Containers
The debug configuration supports **NVIDIA GPU acceleration** for both services:

```yaml
# docker-compose.debug.yml includes GPU support
services:
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
  
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

### GPU Debug Verification
```bash
# Check GPU access in debug containers
docker exec rag_backend python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Monitor GPU usage during debugging
nvidia-smi --loop=2

# Debug GPU memory usage
docker exec rag_backend python -c "import torch; print(f'GPU memory: {torch.cuda.memory_summary()}')"
```

### Performance Debugging Tips
1. **Model Loading**: First debug session may take 50+ seconds while model loads to GPU
2. **Subsequent Sessions**: Should respond in 10-15 seconds once model is warm
3. **Memory Issues**: Use `nvidia-smi` to monitor VRAM usage during debugging
4. **Performance Comparison**: Set breakpoints to measure GPU vs CPU execution times

## �🔄 Development Workflow

### Making Changes During Debug Sessions

#### Backend Changes
1. Modify files in `backend/` directory
2. Code changes are reflected due to volume mounts
3. Uvicorn auto-reloads on file changes
4. Debugger remains attached through reloads

#### Frontend Changes
1. Modify files in `frontend/` directory
2. Streamlit auto-reloads on file changes
3. Browser refresh may be needed for UI updates
4. Debugger maintains connection

### Hot Reload Features
- **Backend**: Uvicorn `--reload` flag enables automatic restart
- **Frontend**: Streamlit file watcher for auto-refresh
- **Volume Mounts**: Local code changes immediately available in containers
- **Persistent Debugging**: Debugger reconnects after service restarts

## 🐛 Debugging Strategies

### Setting Effective Breakpoints

#### Backend Debugging Points
```python
# API routes (backend/api/routes.py)
@app.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    breakpoint()  # Debug incoming requests
    
# RAG processing (backend/chat/rag_engine.py)
def generate_response(self, query: str, persona: str):
    breakpoint()  # Debug response generation
    
# Database operations (backend/ingestion/database.py)
def search_similar_documents(self, query: str, k: int = 5):
    breakpoint()  # Debug vector search
```

#### Frontend Debugging Points
```python
# User interactions (frontend/ui/streamlit_app.py)
if st.button("Send"):
    breakpoint()  # Debug user input processing
    
# API calls (frontend/ui/components.py)
def send_chat_request(query: str, persona: str):
    breakpoint()  # Debug API communication
```

### Variable Inspection
- **Local Variables**: Automatically shown in Variables panel
- **Call Stack**: Navigate through function calls
- **Watch Expressions**: Monitor specific variables/expressions
- **Debug Console**: Execute Python commands in debug context

### Step-by-Step Debugging
- **F10**: Step Over (next line in current function)
- **F11**: Step Into (enter function calls)
- **Shift+F11**: Step Out (exit current function)
- **F5**: Continue (run until next breakpoint)

## 🔍 Troubleshooting Debug Issues

### Common Problems

#### Debugger Won't Attach
```bash
# Check if debug ports are open
netstat -tulpn | grep 5678
netstat -tulpn | grep 5679

# Verify containers are running with debug ports
docker-compose -f docker-compose.yml -f docker-compose.debug.yml ps

# Check container logs
docker-compose -f docker-compose.yml -f docker-compose.debug.yml logs backend
docker-compose -f docker-compose.yml -f docker-compose.debug.yml logs frontend
```

#### Service Won't Start in Debug Mode
```bash
# Check for port conflicts
docker ps | grep 5678
docker ps | grep 5679

# Clean up previous debug sessions
docker-compose -f docker-compose.yml -f docker-compose.debug.yml down
docker system prune -f

# Rebuild debug images
docker-compose -f docker-compose.yml -f docker-compose.debug.yml build --no-cache
```

#### Breakpoints Not Triggering
1. **Verify Path Mappings**: Check `launch.json` localRoot/remoteRoot paths
2. **Check File Sync**: Ensure volume mounts are working
3. **Restart Debug Session**: Detach and reattach debugger
4. **Clear Python Cache**: Remove `__pycache__` directories

### Debug Logs
```bash
# View debug-specific logs
docker-compose -f docker-compose.yml -f docker-compose.debug.yml logs -f

# Check individual service debug output
docker-compose -f docker-compose.yml -f docker-compose.debug.yml logs backend | grep debugpy
docker-compose -f docker-compose.yml -f docker-compose.debug.yml logs frontend | grep debugpy
```

## ⚡ Performance Optimization

### Debug vs Production
- **Debug Mode**: Slower startup, debug symbols, verbose logging
- **Production Mode**: Optimized builds, minimal logging, fast startup
- **Switching**: Use different docker-compose files

### Resource Usage
```yaml
# Debug containers use more resources
services:
  backend:
    mem_limit: 2g
    mem_reservation: 1g
    cpus: 1.0
```

### Build Optimization
```bash
# Use cached debug images
docker-compose -f docker-compose.debug.yml up -d

# Force rebuild when needed
docker-compose -f docker-compose.debug.yml up -d --build

# Clean build (slower but ensures fresh state)
docker-compose -f docker-compose.debug.yml build --no-cache
```

## 🎯 Advanced Debug Techniques

### Multi-Service Debugging
1. Start debug stack
2. Attach to backend service first
3. Set breakpoints in API routes
4. Open second VS Code window for frontend
5. Attach to frontend service
6. Debug user interactions that trigger backend calls

### Cross-Service Request Tracing
```python
# Add correlation IDs for tracing requests across services
import uuid

# In frontend
request_id = str(uuid.uuid4())
headers = {"X-Request-ID": request_id}

# In backend
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    # Set breakpoint here to trace requests
    response = await call_next(request)
    return response
```

### Database Debugging
```python
# Debug vector database operations
from backend.ingestion.database import VectorDatabase

# In debug console
db = VectorDatabase()
results = db.search_similar_documents("Option type", k=3)
# Inspect results in Variables panel
```

## 📚 Additional Resources

### Documentation Links
- [VS Code Python Debugging](https://code.visualstudio.com/docs/python/debugging)
- [Docker Development Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Debugging](https://fastapi.tiangolo.com/tutorial/debugging/)
- [Streamlit Development](https://docs.streamlit.io/library/advanced-features/app-testing)

### Useful Commands
```bash
# Quick debug restart
docker-compose -f docker-compose.debug.yml restart backend frontend

# View all debug containers
docker ps --filter "label=com.docker.compose.project=rag_chatbot_project"

# Check debug port availability
ss -tlnp | grep 567[89]

# Monitor container resource usage
docker stats rag_backend rag_frontend
```

---

**🎉 Happy Debugging!** With this setup, you have full debugging capabilities for both services while they run in production-like Docker environments.