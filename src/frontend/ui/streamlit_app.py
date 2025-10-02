"""
Main Streamlit application.
"""
import streamlit as st
import requests
import json
import os
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ui.styles import get_main_css
from ui.components import UIComponents
from ui.models import PersonaMode
from config.config import Config

# Page configuration
st.set_page_config(
    page_title="🎓 LaYumba Functional C# Expert",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS
st.markdown(get_main_css(), unsafe_allow_html=True)

@st.cache_data(ttl=30)  # Cache for 30 seconds
def get_health_status():
    """Cached health check to avoid API calls on every rerun."""
    try:
        response = requests.get(f"{Config.get_api_url()}/health/", timeout=10)  # Shorter timeout for health
        return response.status_code == 200 and response.json().get("ready", False)
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def main():
    """Main application function."""
    
    # API configuration - Use Config class for Docker DNS resolution
    API_URL = Config.get_api_url()
    
    # Render header
    UIComponents.render_header()
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Cached health status to avoid API calls on every rerun
        is_healthy = get_health_status()
        if is_healthy:
            st.markdown('<div class="health-status health-ready">✅ API Ready</div>', 
                      unsafe_allow_html=True)
        else:
            st.markdown('<div class="health-status health-error">❌ API Unavailable</div>', 
                      unsafe_allow_html=True)
        
        # Debug mode
        debug_mode = st.checkbox("🔍 Debug Mode", help="Show additional query information")
        
        st.markdown("---")
        st.markdown("### 📖 About")
        st.markdown("""
        This AI expert analyzes the LaYumba Functional Programming in C# codebase 
        to help you understand functional programming concepts and architectural patterns.
        
        **Features:**
        - 🧠 Domain Expert: Explains FP concepts
        - 🏗️ Architect: Analyzes code structure  
        - 📚 Context-aware responses
        - 🔍 Source citations
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Persona selection
        selected_persona = UIComponents.render_persona_selector()
        
        # Example queries
        UIComponents.render_example_queries(API_URL, selected_persona)
    
    with col2:
        # Query input
        st.markdown("### 💬 Ask Your Question")
        
        # Initialize session state
        if "user_question" not in st.session_state:
            st.session_state.user_question = ""
        if "last_response" not in st.session_state:
            st.session_state.last_response = None
        if "last_submitted_question" not in st.session_state:
            st.session_state.last_submitted_question = ""
        
        # Update session state if text area changed
        user_question = st.text_area(
            "Enter your question about the functional programming codebase:",
            value=st.session_state.user_question,
            height=100,
            key="question_input"
        )
        
        # Sync text area changes back to session state
        if user_question != st.session_state.user_question:
            st.session_state.user_question = user_question
        
        # Check for auto-submit flag from example queries
        auto_submit = st.session_state.get("auto_submit", False)
        if auto_submit:
            st.session_state.auto_submit = False  # Reset flag
            
        # Submit button or auto-submit
        if st.button("🚀 Ask Expert", type="primary") or auto_submit:
            if user_question.strip():
                # Store the question that was submitted
                st.session_state.last_submitted_question = user_question
                
                with st.spinner("🤔 Thinking..."):
                    try:
                        import time
                        start_time = time.time()
                        if debug_mode:
                            st.write(f"⏱️ Starting API request at {time.strftime('%H:%M:%S')}")
                        
                        # Make API request
                        response = requests.get(
                            f"{API_URL}/query/",
                            params={
                                "user_question": user_question,
                                "persona": selected_persona.value
                            },
                            timeout=120  # Use the longer timeout from Config
                        )
                        
                        request_time = time.time() - start_time
                        if debug_mode:
                            st.write(f"⏱️ API request completed in {request_time:.2f}s")
                        
                        if response.status_code == 200:
                            parse_start = time.time()
                            response_data = response.json()
                            parse_time = time.time() - parse_start
                            if debug_mode:
                                st.write(f"⏱️ JSON parsing took {parse_time:.3f}s")
                            
                            # Store response in session state
                            st.session_state.last_response = response_data
                            total_time = time.time() - start_time
                            if debug_mode:
                                st.success(f"✅ Response received! Total time: {total_time:.2f}s")
                            else:
                                st.success("✅ Response received!")
                        else:
                            st.error(f"API Error: {response.status_code}")
                            st.session_state.last_response = None
                            if debug_mode:
                                try:
                                    st.json(response.json())
                                except:
                                    st.text(response.text)
                                
                    except requests.RequestException as e:
                        st.error(f"Connection Error: {str(e)}")
                        st.session_state.last_response = None
                        st.markdown(f"""
                        **Troubleshooting:**
                        1. Make sure the API server is running
                        2. Check that the API is accessible at {API_URL}
                        3. Verify your network connection and container communication
                        """)
            else:
                st.warning("Please enter a question")
        
        # Display last response if available (survives widget interactions)
        if st.session_state.last_response:
            st.markdown("---")
            st.markdown("### 🤖 Last Response")
            if st.session_state.last_submitted_question:
                st.markdown(f"**Question:** {st.session_state.last_submitted_question}")
            UIComponents.render_response(st.session_state.last_response, debug_mode)
            
            # Clear response button
            if st.button("🗑️ Clear Response"):
                st.session_state.last_response = None
                st.session_state.last_submitted_question = ""
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8em;">
        🚀 Powered by LaYumba Functional C#, LangChain, ChromaDB, and Ollama
    </div>
    """, unsafe_allow_html=True)

# Call main() directly so it runs when the module is loaded by Streamlit
main()