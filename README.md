# 🚀 RAG Chatbot Project: AI-Powered Functional Programming Assistant

## 🎯 Project Overview

**An AI-powered chatbot that analyzes the LaYumba Functional C# codebase to teach functional programming concepts through intelligent code analysis and interactive learning.**

This project provides a complete Docker-based foundation using Retrieval-Augmented Generation (RAG) to create an intelligent code analysis assistant. The system transforms complex functional programming concepts into accessible, interactive learning experiences using the renowned [LaYumba Functional Programming in C#](https://github.com/la-yumba/functional-csharp-code) repository as its knowledge base.

### 🎯 Purpose & Mission

Transform how developers learn functional programming by providing:
- **AI-Guided Learning**: Intelligent explanations of complex FP concepts with practical examples
- **Interactive Code Analysis**: Deep dive into real-world functional programming implementations
- **Dual Perspectives**: Domain expert explanations and software architect insights
- **Hands-On Exploration**: Learn by questioning and exploring actual production-quality code

---

## 🚀 Quick Start (One Command Setup)

**Get started in under 3 minutes:**

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.8+ (for setup validation and dependency auto-installation)
- **Optional**: NVIDIA GPU with 3GB+ VRAM for 10x performance boost
  - **With GPU**: 10-15 second responses
  - **CPU Only**: 60+ second responses
  - **Auto-detection**: System automatically uses GPU if available

### Automated Deployment
```bash
# Clone the repository
git clone https://github.com/ErikMPZuhlke/zpt-dt-camp-hackathon-2025.git
cd zpt-dt-camp-hackathon-2025

# Run the comprehensive setup validation with dependency auto-installation
python src/scripts/setup_environment.py --verbose
```

**This single command will:**
- ✅ Validate system requirements (Docker, Python, Docker Compose)
- ✅ **Auto-install Python dependencies** (docker, GitPython, psutil, pyyaml, etc.)
- ✅ Build **GPU-accelerated** Docker containers with optimized dependencies
- ✅ Start all services with **NVIDIA GPU support** (Ollama, Backend, Frontend)
- ✅ Download and configure local LLM (llama3.2:3b) with **24-hour keep-alive**
- ✅ Process LaYumba codebase into searchable knowledge base (**478 chunks**)
- ✅ Validate complete system functionality with **10-step health checks**
- ✅ Provide access URLs and **performance metrics**

### Alternative Quick Start
```bash
# Start all services manually
docker-compose up -d --build

# Or use VS Code tasks (Ctrl+Shift+P)
# "Tasks: Run Task" → "Start Debug Stack"
```

---

## 🎯 Core Features

### 🧠 AI Personas
1. **Domain Expert Mode**: Deep explanations of functional programming concepts
   - Option types, Either monads, Validation patterns
   - Function composition and higher-order functions
   - Immutable data structures and their benefits
   - Practical examples with executable code

2. **Software Architect Mode**: System-level analysis and design insights
   - Code structure and architectural patterns
   - Dependency relationships and design decisions
   - Testing strategies and code organization
   - Performance considerations and trade-offs

### 🏗️ System Architecture
- **🐳 Optimized Docker**: Multi-stage builds with efficient layer caching
- **🚀 GPU Acceleration**: NVIDIA GPU support for 10x faster inference (10-15s vs 60+ seconds)
- **🤖 Local LLM**: Ollama integration with 24-hour model keep-alive
- **📊 Vector Database**: ChromaDB for efficient semantic code search
- **⚡ FastAPI Backend**: High-performance API with GPU-accelerated embeddings
- **🎨 Streamlit Frontend**: Interactive web interface with debug mode toggle
- **🔧 Development Tools**: VS Code debugging, hot reload, comprehensive validation

---

## 🌐 Access Points

Once setup is complete, access the system through:

- **🎨 Frontend Interface**: http://localhost:8501 (Main user interface)
- **⚙️ Backend API**: http://localhost:8000 (REST API endpoints)  
- **📖 API Documentation**: http://localhost:8000/docs (Interactive API docs)
- **🤖 LLM Service**: http://localhost:11434 (Ollama local inference)

### Quick Validation
```bash
# Verify all services are running
curl http://localhost:8000/health/        # Backend status
curl http://localhost:8501/_stcore/health # Frontend status
curl http://localhost:11434/api/tags      # LLM availability
```

---

## 📚 About the LaYumba Functional Codebase

The project analyzes the **LaYumba Functional Programming in C#** repository, which demonstrates:

### 🧩 Key Concepts Covered
- **Option<T>**: Elegant null safety without exceptions
- **Either<L,R>**: Composable error handling patterns  
- **Validation<T>**: Error accumulation for complex validation
- **Functional Composition**: Chaining operations with Map, Bind, Apply
- **Immutable Structures**: Thread-safe, predictable data management
- **Higher-Order Functions**: Functions as first-class citizens

### 🏛️ Architectural Patterns
- **Railway Oriented Programming**: Error handling without exceptions
- **Domain-Driven Design**: Clean separation of business logic
- **Functional Core, Imperative Shell**: Side effects at boundaries
- **Monadic Patterns**: Composable operations with context preservation

---

## 📊 System Validation

### Health Check Results
The setup script performs comprehensive validation:

**✅ 10-Step Validation Process:**
1. **System requirements** (Python, Docker, Docker Compose)
2. **Install Python dependencies** (automatic pip installation)
3. **Directory structure** verification  
4. **Previous deployment cleanup**
5. **GPU-accelerated container builds**
6. **Service startup** with GPU coordination
7. **Wait for services** readiness
8. **Backend API functionality** testing
9. **Frontend accessibility** verification
10. **Codebase ingestion** (222 files → 478 chunks)

### Performance Metrics
- **Frontend Build**: ~29 seconds (minimal dependencies)
- **Backend Build**: ~6 minutes (cached AI/ML dependencies with GPU support)
- **Service Ready**: <2 minutes for complete stack
- **GPU Model Loading**: ~50-60 seconds (first request only)
- **Query Response Time**: **10-15 seconds** (with GPU acceleration vs 60+ seconds CPU)
- **Success Rate**: 10/10 steps typically pass on supported hardware

---

## 🎯 Example Interactions

### Domain Expert Queries
```
"Explain how the Option type prevents null reference exceptions"
"Show me examples of function composition in the codebase"  
"What are the benefits of using Either for error handling?"
"How does the Validation type accumulate multiple errors?"
```

### Software Architect Queries
```
"Analyze the dependency structure of the LaYumba.Functional library"
"What design patterns are used in the codebase?"
"How is separation of concerns achieved in this functional design?"
"Identify the core abstractions and their relationships"
```

---

## 🛠️ Development Environment

### VS Code Integration
Full debugging support with remote container debugging:

```bash
# Start debug environment
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up -d --build
```

**Debug Features:**
- **Remote Debugging**: Attach VS Code to running containers
- **Hot Reload**: Live code changes without container restart
- **Breakpoint Support**: Full debugging capabilities
- **Debug Ports**: Backend (5678), Frontend (5679)

### Development Workflow
1. **Code Changes**: Edit files in `src/backend/` or `src/frontend/`
2. **Auto-Reload**: Changes sync to containers automatically
3. **Debug Integration**: VS Code debugger maintains connection
4. **Live Testing**: Test immediately at http://localhost:8501

---

## 📁 Project Structure

```
zpt-dt-camp-hackathon-2025/
├── 📄 README.md                    # Project overview and setup (this file)
├── 🐳 docker-compose.yml           # Production container orchestration with GPU
├── 🐳 docker-compose.debug.yml     # Development/debug configuration
├── 📁 src/                         # Application source code
│   ├── 📁 backend/                 # FastAPI microservice with GPU support
│   │   ├── 📁 api/                 # REST API layer
│   │   ├── 📁 chat/                # RAG engine and AI personas
│   │   ├── 📁 core/                # Configuration and models
│   │   └── 📁 ingestion/           # Code processing and vector DB
│   ├── 📁 frontend/                # Streamlit microservice
│   │   └── 📁 ui/                  # Web interface with debug mode
│   └── 📁 scripts/                 # Deployment and validation
│       ├── setup_environment.py    # 10-step validation with dependency install
│       └── 📁 validation_states/   # State pattern validation framework
├── 📁 data/                        # Persistent data storage
│   ├── 📁 vector_db/               # ChromaDB vector database
│   └── 📁 codebase/                # LaYumba functional C# source (222 files)
└── 📁 docs/                        # Documentation
    ├── ARCHITECTURE.md              # Technical architecture and patterns
    ├── HACKATHON_GUIDE.md           # Development and challenge guide
    ├── DEBUG_GUIDE.md               # Advanced debugging techniques
    └── GPU_SETUP.md                 # GPU acceleration setup guide
```

---

## 🚨 Troubleshooting

### Common Issues & Quick Fixes

**Environment Setup**
```bash
# Complete environment validation with dependency auto-install
python src/scripts/setup_environment.py --verbose

# Manual Docker restart with GPU support
docker-compose down && docker-compose up -d --build
```

**Service Issues**
```bash
# Check service status
docker-compose ps

# View service logs  
docker-compose logs backend
docker-compose logs frontend
docker-compose logs ollama
```

**Port Conflicts**
- Default ports: Frontend (8501), Backend (8000), Ollama (11434)
- Modify `docker-compose.yml` if ports are in use

**Performance Issues**
- Allow 2GB+ RAM for Ollama model (3GB+ VRAM for GPU acceleration)
- Frontend build: ~29 seconds, Backend build: ~6 minutes
- Use `--verbose` flag to monitor build progress
- **GPU Setup**: See [docs/GPU_SETUP.md](docs/GPU_SETUP.md) for NVIDIA GPU configuration
- **Slow Responses**: First request takes 50-60s (model loading), subsequent: 10-15s

---

## 📚 Documentation

### Complete Documentation Set
This project maintains clear separation of documentation concerns:

- **[README.md](README.md)** - Project overview, setup, and essential information (this file)
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Technical architecture, design patterns, and technology stack
- **[docs/HACKATHON_GUIDE.md](docs/HACKATHON_GUIDE.md)** - Development workflow, challenges, and time-optimized strategies  
- **[docs/DEBUG_GUIDE.md](docs/DEBUG_GUIDE.md)** - Advanced VS Code debugging and troubleshooting

### Key Areas Covered
- **Setup & Deployment**: One-command setup with comprehensive validation
- **Architecture**: Modern microservices with design pattern implementation
- **Development**: Hot reload debugging and live testing workflows
- **Challenges**: Time-boxed hackathon strategies and enhancement ideas
- **Troubleshooting**: Common issues, solutions, and performance optimization

---

## 🎓 Learning Outcomes

By using this system, developers will:
- **Master Functional Programming**: Deep understanding through interactive exploration
- **Understand Design Patterns**: See real-world implementations of functional patterns
- **Build AI-Powered Tools**: Experience creating intelligent code analysis systems
- **Practice Modern Architecture**: Work with microservices, containers, and vector databases
- **Experience RAG Applications**: Build knowledge retrieval systems with practical applications

---

## 🤝 Contributing

We welcome contributions that enhance the learning experience:

- **Feature Enhancements**: New AI personas, improved analysis capabilities
- **UI/UX Improvements**: Better visualization of functional concepts
- **Documentation**: Clearer explanations and examples
- **Bug Fixes**: Platform compatibility and performance improvements

### Development Setup
1. Fork the repository
2. Run `python scripts/setup_environment.py --verbose`
3. Make changes with hot reload enabled
4. Test with VS Code debugging
5. Submit pull request with clear description

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Content
This project incorporates educational materials from the [LaYumba Functional Programming in C#](https://github.com/la-yumba/functional-csharp-code) repository, which is also MIT licensed. See [NOTICE](NOTICE) file for complete attribution details.

Both licenses are compatible and allow free use, modification, and distribution for educational and commercial purposes.

---

## 🚀 Getting Started

Ready to explore functional programming through AI-guided learning?

1. **Clone**: `git clone https://github.com/ErikMPZuhlke/zpt-dt-camp-hackathon-2025.git`
2. **Setup**: `python src/scripts/setup_environment.py --verbose`
3. **Access**: http://localhost:8501
4. **Learn**: Start with "Explain the Option type" in Domain Expert mode (10-15s response)
5. **Explore**: Try architectural analysis in Software Architect mode
6. **Debug**: Toggle Debug Mode to see performance metrics

**For detailed technical information**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)  
**For development workflow**: See [docs/HACKATHON_GUIDE.md](docs/HACKATHON_GUIDE.md)  
**For debugging setup**: See [docs/DEBUG_GUIDE.md](docs/DEBUG_GUIDE.md)

**Happy learning! 🚀**