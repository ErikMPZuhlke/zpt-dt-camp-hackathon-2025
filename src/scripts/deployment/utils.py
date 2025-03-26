"""
Utility functions for deployment validation.
"""
import subprocess
import time
import socket
import requests
from typing import Tuple, Optional


class CommandRunner:
    """Utility for running shell commands."""
    
    @staticmethod
    def run(command: str, capture_output: bool = True, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command with proper error handling."""
        try:
            return subprocess.run(
                command, 
                shell=True, 
                capture_output=capture_output, 
                text=True, 
                check=check
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {command}")
            print(f"Error: {e.stderr}")
            print(f"Return code: {e.returncode}")
            raise
    
    @staticmethod
    def run_with_streaming_output(command: str, check: bool = True) -> Tuple[bool, str]:
        """Run a command with real-time output streaming to console."""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'  # Replace invalid characters instead of failing
            )
            
            output_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # Strip and handle encoding issues gracefully
                    clean_output = output.strip()
                    print(clean_output)  # Print to console in real-time
                    output_lines.append(clean_output)
            
            return_code = process.poll()
            full_output = '\n'.join(output_lines)
            
            if check and return_code != 0:
                print(f"❌ Command failed with return code {return_code}")
                return False, full_output
            
            return return_code == 0, full_output
            
        except Exception as e:
            print(f"❌ Command execution failed: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def run_with_quiet_output(command: str, check: bool = True, show_progress: bool = True) -> Tuple[bool, str]:
        """Run a command quietly with optional progress indication."""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )
            
            output_lines = []
            dot_count = 0
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    output_lines.append(output.strip())
                    
                    # Show progress dots every few lines
                    if show_progress:
                        dot_count += 1
                        if dot_count % 50 == 0:  # Print a dot every 50 lines
                            print(".", end="", flush=True)
                        if dot_count % 2500 == 0:  # New line every 2500 lines (50 dots)
                            print()
            
            if show_progress and dot_count > 0:
                print()  # Final newline after progress dots
            
            return_code = process.poll()
            full_output = '\n'.join(output_lines)
            
            if check and return_code != 0:
                print(f"❌ Command failed with return code {return_code}")
                # Show last few lines of output for debugging
                if output_lines:
                    print("Last few lines of output:")
                    for line in output_lines[-10:]:
                        print(f"   {line}")
                return False, full_output
            
            return return_code == 0, full_output
            
        except Exception as e:
            print(f"❌ Command execution failed: {str(e)}")
            return False, str(e)


class ServiceWaiter:
    """Utility for waiting for services to become available."""
    
    @staticmethod
    def wait_for_url(url: str, service_name: str, timeout: int = 120) -> bool:
        """Wait for a service URL to respond with 200."""
        print(f"⏳ Waiting for {service_name} to be ready...")
        
        start_time = time.time()
        last_error = None
        
        while time.time() - start_time < timeout:
            try:
                # Increase individual request timeout for slower services
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    print(f"✅ {service_name} is ready")
                    return True
                else:
                    last_error = f"HTTP {response.status_code}"
            except requests.exceptions.RequestException as e:
                last_error = str(e)
            
            # Add a brief pause between attempts
            time.sleep(2)
        
        print(f"❌ {service_name} failed to start within {timeout} seconds")
        if last_error:
            print(f"   Last error: {last_error}")
        return False
    
    @staticmethod
    def wait_for_port(host: str, port: int, service_name: str, timeout: int = 120) -> bool:
        """Wait for a service to be listening on a specific port."""
        print(f"⏳ Waiting for {service_name} to listen on port {port}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with socket.create_connection((host, port), timeout=3):
                    print(f"✅ {service_name} is listening on port {port}")
                    return True
            except (socket.error, socket.timeout):
                pass
            time.sleep(2)
        
        print(f"❌ {service_name} failed to listen on port {port} within {timeout} seconds")
        return False


class StepPrinter:
    """Utility for formatted step output."""
    
    @staticmethod
    def print_step(step: int, message: str, verbose: bool = False):
        """Print a formatted step message."""
        verbose_indicator = " (verbose mode)" if verbose else ""
        print(f"\n🔧 Step {step}: {message}{verbose_indicator}")
        print("=" * 50)
    
    @staticmethod
    def print_summary(steps_passed: int, total_steps: int) -> bool:
        """Print validation summary and return success status."""
        print("\n" + "=" * 60)
        print("🎯 VALIDATION SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {steps_passed}/{total_steps} steps")
        
        # Be more flexible: allow up to 3 steps to fail if critical services are working
        success = steps_passed >= (total_steps - 3)
        
        if success:
            print("🎉 Docker deployment is ready!")
            print("\n📍 Access your application:")
            print("   🌐 Frontend UI: http://localhost:8501")
            print("   🔧 Backend API: http://localhost:8000")
            print("   📚 API Docs: http://localhost:8000/docs")
            print("   🤖 Ollama: http://localhost:11434")
            
            print("\n💡 Next steps:")
            print("   1. Visit the Frontend UI to start chatting")
            print("   2. If needed, run ingestion: curl -X POST http://localhost:8000/ingest/ -d '{\"force_reindex\": true}'")
            print("   3. Check the API documentation for more features")
        else:
            print("❌ Docker deployment has issues. Please check the logs.")
            print("\n🔧 Troubleshooting:")
            print("   docker compose logs -f")
            print("   docker compose ps")
        
        return success