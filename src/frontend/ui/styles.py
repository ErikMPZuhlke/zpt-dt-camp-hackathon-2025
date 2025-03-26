"""
UI styling and CSS components.
"""

MAIN_CSS = """
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.health-status {
    padding: 0.5rem;
    border-radius: 5px;
    margin: 0.5rem 0;
    font-weight: bold;
}

.health-ready {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.health-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.source-citation {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 0.5rem;
    margin: 0.2rem 0;
    font-size: 0.8em;
    color: #6c757d;
}

.debug-info {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 0.5rem;
    margin: 0.5rem 0;
    font-size: 0.8em;
}
</style>
"""

def get_main_css():
    """Get the main CSS styling."""
    return MAIN_CSS