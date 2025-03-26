"""
Frontend application entry point.
"""
import streamlit as st
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the main Streamlit app
from ui.streamlit_app import main

if __name__ == "__main__":
    main()