"""
Reusable UI components for the Streamlit app.
"""
import streamlit as st
import requests
from typing import Dict, List, Any
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from ui.models import PersonaMode
from config.config import Config

class UIComponents:
    """Reusable UI components."""
    
    @staticmethod
    def render_header():
        """Render the main header."""
        st.markdown("""
        <div class="main-header">
            <h1>🎓 LaYumba Functional C# Code Expert</h1>
            <p>AI-powered analysis of functional programming patterns in C#</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_persona_selector() -> PersonaMode:
        """Render simple persona selection with radio buttons."""
        st.markdown("### 🎭 Choose Your AI Expert")
        
        # Initialize session state for persona if not exists
        if "selected_persona" not in st.session_state:
            st.session_state.selected_persona = PersonaMode.DOMAIN_EXPERT
        
        # Simple radio button selection
        persona_options = {
            PersonaMode.DOMAIN_EXPERT: "🧠 Functional Programming Domain Expert",
            PersonaMode.SOFTWARE_ARCHITECT: "🏗️ Software Architect"
        }
        
        selected = st.radio(
            "Select Persona",
            options=list(persona_options.keys()),
            format_func=lambda x: persona_options[x],
            index=0 if st.session_state.selected_persona == PersonaMode.DOMAIN_EXPERT else 1,
            key="persona_selector"
        )
        
        # Update session state
        st.session_state.selected_persona = selected
        
        # Show description for selected persona
        if selected == PersonaMode.DOMAIN_EXPERT:
            st.info("🎯 **Focus:** Option, Either, Validation, Monads, Function Composition\n\n"
                   "Explains FP concepts, patterns, and best practices with educational examples")
        else:
            st.info("🎯 **Focus:** Dependencies, Patterns, Modularity, Code Quality\n\n"
                   "Analyzes code structure, design patterns, and architectural decisions")
        
        return selected
    
    @staticmethod
    def render_example_queries(api_url: str, selected_persona: PersonaMode):
        """Render example queries section with simple styling."""
        st.markdown("### 💡 Example Queries")
        
        try:
            response = requests.get(f"{api_url}/examples/", timeout=5)
            if response.status_code == 200:
                examples = response.json()
                
                persona_key = selected_persona.value
                if persona_key in examples:
                    for i, example in enumerate(examples[persona_key]):
                        if st.button(f"📝 {example}", key=f"example_{i}"):
                            st.session_state.user_question = example
                            st.session_state.auto_submit = True  # Flag to auto-submit
                            st.rerun()
            else:
                st.warning("Could not load example queries from API")
                
        except requests.RequestException:
            # Fallback static examples
            if selected_persona == PersonaMode.DOMAIN_EXPERT:
                examples = [
                    "Explain how the Option type prevents null reference exceptions",
                    "Show me examples of function composition in the codebase",
                    "What are the benefits of using Either for error handling?",
                    "How does the Validation type work for data validation?"
                ]
            else:
                examples = [
                    "Analyze the dependency structure of the LaYumba.Functional library",
                    "What design patterns are used in the codebase?",
                    "Review the modular architecture of the functional library",
                    "Explain the separation of concerns in the code organization"
                ]
            
            for i, example in enumerate(examples):
                if st.button(f"📝 {example}", key=f"static_example_{i}"):
                    st.session_state.user_question = example
                    st.session_state.auto_submit = True  # Flag to auto-submit
                    st.rerun()
    
    @staticmethod
    def render_health_status(api_url: str = None):
        """Render API health status using Config if no URL provided."""
        if api_url is None:
            api_url = Config.get_api_url()
            
        try:
            response = requests.get(f"{api_url}/health/", timeout=Config.API_TIMEOUT)
            if response.status_code == 200:
                status = response.json()
                if status.get("ready"):
                    st.markdown('<div class="health-status health-ready">✅ API Ready</div>', 
                              unsafe_allow_html=True)
                else:
                    st.markdown('<div class="health-status health-error">❌ API Not Ready</div>', 
                              unsafe_allow_html=True)
            else:
                st.markdown('<div class="health-status health-error">❌ API Error</div>', 
                          unsafe_allow_html=True)
        except requests.RequestException:
            st.markdown('<div class="health-status health-error">❌ API Unavailable</div>', 
                      unsafe_allow_html=True)
    
    @staticmethod
    def render_response(response_data: Dict[str, Any], debug_mode: bool = False):
        """Render the chatbot response."""
        if "answer" in response_data:
            st.markdown("### 🤖 Response")
            st.markdown(response_data["answer"])
            
            # Sources
            if "sources" in response_data and response_data["sources"]:
                st.markdown("### 📚 Sources")
                for i, source in enumerate(response_data["sources"], 1):
                    st.markdown(f"""
                    <div class="source-citation">
                        <strong>Source {i}:</strong> {source}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Debug information
            if debug_mode:
                st.markdown("### 🔍 Debug Information")
                st.markdown(f"""
                <div class="debug-info">
                    <strong>Persona:</strong> {response_data.get('persona', 'Unknown')}<br>
                    <strong>Query Time:</strong> {response_data.get('query_time', 'Unknown')}s<br>
                    <strong>Sources Found:</strong> {len(response_data.get('sources', []))}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Invalid response format")