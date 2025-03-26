"""
Docker operations for deployment validation.
"""
import json
from typing import Tuple, Dict, Any, List
from .config import DeploymentConfig
from .utils import CommandRunner, ServiceWaiter


class DockerManager:
    """Handles Docker operations."""
    
    def __init__(self, verbose: bool = False):
        self.config = DeploymentConfig()
        self.runner = CommandRunner()
        self.waiter = ServiceWaiter()
        self.verbose = verbose
        # Ensure we run Docker commands from project root
        import os
        os.chdir(self.config.PROJECT_ROOT)
    
    def cleanup_previous_deployment(self) -> Tuple[bool, str]:
        """Clean up any previous deployment."""        
        try:
            # First check if Docker daemon is running
            result = self.runner.run("docker ps", check=False, capture_output=True)
            if result.returncode != 0:
                return False, f"Docker daemon not available: {result.stderr.decode().strip()}"
            
            # Stop and remove containers using standard compose file
            print("🧹 Stopping containers...")
            self.runner.run("docker compose -f docker-compose.yml down --remove-orphans", check=False)
            
            # Remove dangling images
            print("🧹 Removing dangling images...")
            self.runner.run("docker image prune -f", check=False)
            
            print("✅ Cleanup completed")
            return True, "Previous deployment cleaned up"
        
        except Exception as e:
            return False, f"Cleanup failed: {str(e)}"
    
    def build_containers(self) -> Tuple[bool, str]:
        """Build Docker containers."""        
        try:
            print("🔨 Building containers (this may take a few minutes)...")
            
            if self.verbose:
                print("📺 Live build output:")
                print("-" * 50)
                # Use streaming output for build command
                success, output = self.runner.run_with_streaming_output("docker compose -f docker-compose.yml build")
                print("-" * 50)
            else:
                print("⏳ Building containers... (use --verbose to see detailed output)")
                # Run silently and just show progress
                success, output = self.runner.run_with_quiet_output("docker compose -f docker-compose.yml build")
            
            if success:
                print("✅ All containers built successfully")
                return True, "Docker containers built successfully"
            else:
                print("❌ Container build failed")
                if not self.verbose:
                    print("💡 Run with --verbose to see detailed build output")
                return False, "Build output indicates failure"
        
        except Exception as e:
            return False, f"Container build failed: {str(e)}"
    
    def start_services(self) -> Tuple[bool, str]:
        """Start Docker services."""        
        try:
            print("🚀 Starting all services...")
            
            if self.verbose:
                print("📺 Live startup output:")
                print("-" * 50)
                # Use streaming output for service startup
                success, output = self.runner.run_with_streaming_output("docker compose -f docker-compose.yml up -d --build")
                print("-" * 50)
            else:
                print("⏳ Starting services... (use --verbose to see detailed output)")
                # Run silently
                success, output = self.runner.run_with_quiet_output("docker compose -f docker-compose.yml up -d --build")
            
            if not success:
                if not self.verbose:
                    print("💡 Run with --verbose to see detailed startup output")
                return False, "Failed to start services"
            
            # Check if all services are running
            result = self.runner.run("docker compose -f docker-compose.yml ps --format json")
            
            # Parse multiple JSON objects (one per line)
            services = []
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            services.append(json.loads(line.strip()))
                        except json.JSONDecodeError as e:
                            print(f"⚠️ Warning: Failed to parse service line: {line[:100]}...")
                            continue
            
            if not services:
                return False, "No services found running"
            
            running_services = [s for s in services if s.get('State') == 'running']
            print(f"✅ Started {len(running_services)}/{len(services)} services")
            
            for service in services:
                status = "✅" if service.get('State') == 'running' else "❌"
                print(f"   {status} {service.get('Service', 'Unknown')}: {service.get('State', 'Unknown')}")
            
            if len(running_services) >= len(services) - 1:  # Allow one service to potentially be starting
                return True, "Docker services started"
            else:
                return False, f"Only {len(running_services)}/{len(services)} services are running"
        
        except Exception as e:
            return False, f"Failed to start services: {str(e)}"
    
    def wait_for_services(self) -> Tuple[bool, str]:
        """Wait for services to be ready."""        
        # First check if containers are actually running
        print("🔍 Checking container status...")
        container_status = self.get_container_status()
        if container_status:
            running_containers = [c for c in container_status if c.get('State') == 'running']
            print(f"📦 Found {len(running_containers)}/{len(container_status)} containers running")
            for container in container_status:
                status_icon = "✅" if container.get('State') == 'running' else "❌"
                service_name = container.get('Service', 'Unknown')
                state = container.get('State', 'Unknown')
                print(f"   {status_icon} {service_name}: {state}")
            
            if len(running_containers) == 0:
                return False, "No Docker containers are running"
        else:
            print("⚠️  Could not check container status (Docker may not be available)")
        
        # Check if Ollama container is running first
        ollama_container_running = False
        if container_status:
            for container in container_status:
                if container.get('Service') == 'ollama' and container.get('State') == 'running':
                    ollama_container_running = True
                    break
        
        if not ollama_container_running:
            print("❌ Ollama container is not running")
            return False, "Ollama container is not running - Docker deployment required"
        
        # Check Ollama service endpoint
        ollama_ready = self.waiter.wait_for_url(self.config.OLLAMA_URL, "Ollama", 60)
        if not ollama_ready:
            print("❌ Ollama container running but service not responding")
            return False, "Ollama service not responding despite container running"
        
        # Check if Backend container is running first
        backend_container_running = False
        if container_status:
            for container in container_status:
                if container.get('Service') == 'backend' and container.get('State') == 'running':
                    backend_container_running = True
                    break
        
        if not backend_container_running:
            print("❌ Backend container is not running")
            return False, "Backend container is not running - Docker deployment required"
        
        # Check Backend API with extended timeout and fallback verification
        backend_ready = self.waiter.wait_for_url(self.config.BACKEND_URL, "Backend API", 90)
        
        if not backend_ready:
            # Backend waiter failed, but let's verify manually with a more forgiving check
            print("🔍 Performing manual backend verification...")
            try:
                import requests
                response = requests.get(self.config.BACKEND_URL, timeout=20)
                if response.status_code == 200:
                    print("✅ Backend API is actually responding (waiter timeout was too strict)")
                    backend_ready = True
                else:
                    print(f"❌ Backend responded with status {response.status_code}")
            except Exception as e:
                print(f"❌ Backend verification failed: {str(e)}")
        
        if backend_ready:
            return True, "All critical services are ready"
        else:
            return False, "Backend API failed to become ready"
    
    def get_container_status(self) -> List[Dict[str, Any]]:
        """Get detailed container status for debugging."""
        try:
            result = self.runner.run("docker compose -f docker-compose.yml ps --format json")
            if not result.stdout.strip():
                return []
            
            # Parse multiple JSON objects (one per line)
            services = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        services.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
            return services
        except Exception as e:
            print(f"⚠️  Could not get container status: {str(e)}")
            return []
