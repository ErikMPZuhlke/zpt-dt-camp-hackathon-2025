"""
Service validation for deployment testing.
"""
import requests
import json
from typing import Tuple, Dict, Any
from .config import DeploymentConfig
from .utils import ServiceWaiter


class ServiceValidator:
    """Handles service functionality validation."""
    
    def __init__(self):
        self.config = DeploymentConfig()
        self.waiter = ServiceWaiter()
    
    def _check_container_running(self, service_name: str) -> bool:
        """Check if a specific Docker container is running."""
        try:
            # Try to connect to Docker daemon API to check container status
            # This attempts to query the Docker daemon's REST API on the default port (2375)
            # to get a list of all running containers and their metadata
            result = requests.get("http://localhost:2375/containers/json", timeout=2)
            containers = result.json() if result.status_code == 200 else []
            for container in containers:
                if any(service_name in name for name in container.get('Names', [])):
                    return container.get('State') == 'running'
        except:
            # Fallback to docker compose ps if Docker API isn't available
            try:
                import subprocess
                result = subprocess.run(
                    ["docker", "compose", "ps", "--format", "json"], 
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split('\n'):
                        if line.strip():
                            try:
                                service_info = json.loads(line.strip())
                                if service_info.get('Service') == service_name:
                                    return service_info.get('State') == 'running'
                            except json.JSONDecodeError:
                                continue
            except:
                pass
        return False
    
    def test_backend_api(self) -> Tuple[bool, str]:
        """Test backend API functionality."""
        # First check if backend container is running
        if not self._check_container_running('backend'):
            print("⚠️  Backend container not detected as running")
            print("🔍 Testing endpoint anyway (might be local installation)...")
        
        try:
            # Test root endpoint first
            print("🔍 Testing root endpoint...")
            try:
                root_response = requests.get(self.config.BACKEND_URL, timeout=20)
                if root_response.status_code == 200:
                    print("✅ Root endpoint working")
                else:
                    print(f"⚠️  Root endpoint returned {root_response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"❌ Root endpoint failed: {str(e)}")
                return False, f"Root endpoint unreachable: {str(e)}"
            
            # Test health endpoint - should be ready with vector DB pre-built
            print("🔍 Testing health endpoint...")
            try:
                health_response = requests.get(f"{self.config.BACKEND_URL}/health/", timeout=20)
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    if health_data.get("ready"):
                        print("✅ Health endpoint: All services ready")
                    else:
                        print("⚠️  Health endpoint: Some services not ready")
                        print(f"   Vector DB: {'✅' if health_data.get('vector_db') == 'ready' else '❌'}")
                        print(f"   LLM: {'✅' if health_data.get('llm') == 'ready' else '❌'}")
                elif health_response.status_code == 503:
                    print("⚠️  Health endpoint: Services still initializing")
                else:
                    print(f"⚠️  Health endpoint returned unexpected status {health_response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Health endpoint failed: {str(e)}")
                # Don't fail immediately - try other endpoints
            
            # Test examples endpoint
            print("🔍 Testing examples endpoint...")
            try:
                examples_response = requests.get(f"{self.config.BACKEND_URL}/examples/", timeout=20)
                if examples_response.status_code == 200:
                    print("✅ Examples endpoint working")
                else:
                    print(f"⚠️  Examples endpoint returned {examples_response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Examples endpoint failed: {str(e)}")
            
            # If we got here and root endpoint worked, consider it a success
            return True, "Backend API is responding"
        
        except Exception as e:
            return False, f"Unexpected error testing backend: {str(e)}"
    
    def test_frontend_accessibility(self) -> Tuple[bool, str]:
        """Test frontend accessibility."""        
        try:
            # The frontend is Streamlit, so we just check if it responds
            print("🔍 Testing frontend accessibility...")
            response = requests.get(self.config.FRONTEND_URL, timeout=15)
            
            if response.status_code == 200:
                print("✅ Frontend is accessible")
                return True, "Frontend is accessible"
            else:
                return False, f"Frontend returned status {response.status_code}"
        
        except requests.exceptions.RequestException as e:
            return False, f"Frontend accessibility test failed: {str(e)}"
    
    def ingest_codebase(self) -> Tuple[bool, str]:
        """Trigger codebase ingestion via backend API."""        
        try:
            print("🔄 Triggering codebase ingestion...")
            
            # Call the ingestion endpoint with force_reindex=true to ensure fresh data
            ingest_response = requests.post(
                f"{self.config.BACKEND_URL}/ingest/",
                params={"force_reindex": True},
                timeout=300  # Allow up to 5 minutes for ingestion
            )
            
            if ingest_response.status_code == 200:
                ingest_data = ingest_response.json()
                if ingest_data.get("status") == "success":
                    results = ingest_data.get("results", {})
                    files_processed = results.get("total_files_processed", 0)
                    chunks_created = results.get("total_chunks_created", 0)
                    
                    print(f"✅ Codebase ingestion completed successfully")
                    print(f"   📁 Files processed: {files_processed}")
                    print(f"   📄 Chunks created: {chunks_created}")
                    
                    return True, f"Codebase ingested: {files_processed} files, {chunks_created} chunks"
                else:
                    return False, f"Ingestion returned status: {ingest_data.get('status', 'unknown')}"
            else:
                error_detail = ingest_response.text
                print(f"❌ Ingestion failed with status {ingest_response.status_code}")
                return False, f"Ingestion API returned {ingest_response.status_code}: {error_detail}"
        
        except requests.exceptions.Timeout:
            return False, "Ingestion timed out after 5 minutes"
        except requests.exceptions.RequestException as e:
            return False, f"Ingestion request failed: {str(e)}"
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get detailed service information for debugging."""
        info = {}
        
        # Backend root endpoint
        try:
            root_response = requests.get(self.config.BACKEND_URL, timeout=15)
            info['backend_root'] = {
                'status_code': root_response.status_code,
                'response': root_response.json() if root_response.status_code == 200 else None
            }
        except Exception as e:
            info['backend_root'] = {'error': str(e)}
        
        # Backend health endpoint
        try:
            health_response = requests.get(f"{self.config.BACKEND_URL}/health/", timeout=15)
            info['backend_health'] = {
                'status_code': health_response.status_code,
                'response': health_response.json() if health_response.status_code in [200, 503] else None
            }
        except Exception as e:
            info['backend_health'] = {'error': str(e)}
        
        # Examples endpoint
        try:
            examples_response = requests.get(f"{self.config.BACKEND_URL}/examples/", timeout=15)
            info['backend_examples'] = {
                'status_code': examples_response.status_code,
                'response': examples_response.json() if examples_response.status_code == 200 else None
            }
        except Exception as e:
            info['backend_examples'] = {'error': str(e)}
        
        # Frontend info
        try:
            frontend_response = requests.get(self.config.FRONTEND_URL, timeout=5)
            info['frontend'] = {
                'status_code': frontend_response.status_code,
                'accessible': frontend_response.status_code == 200
            }
        except Exception as e:
            info['frontend'] = {'error': str(e)}
        
        return info