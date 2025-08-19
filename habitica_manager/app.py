from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_environment():
    """Validate required environment variables"""
    required_vars = {
        'HABITICA_USER_ID': 'Habitica User ID is required. Get it from https://habitica.com/user/settings/api',
        'HABITICA_API_TOKEN': 'Habitica API Token is required. Get it from https://habitica.com/user/settings/api'
    }
    
    missing_vars = []
    invalid_vars = []
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value:
            missing_vars.append(f"  - {var}: {description}")
        elif value in ['your-user-id', 'your-api-token']:
            invalid_vars.append(f"  - {var}: Please set your actual {var.replace('_', ' ').lower()}")
    
    if missing_vars or invalid_vars:
        error_msg = "\n❌ Configuration Error: Habitica API credentials are not properly configured.\n"
        
        if missing_vars:
            error_msg += "\nMissing variables:\n" + "\n".join(missing_vars)
        
        if invalid_vars:
            error_msg += "\nInvalid variables (still using default values):\n" + "\n".join(invalid_vars)
        
        error_msg += "\n\nTo fix this:"
        error_msg += "\n1. Go to https://habitica.com/user/settings/api"
        error_msg += "\n2. Copy your User ID and API Token"
        error_msg += "\n3. Update the .env file with your actual credentials"
        error_msg += "\n4. Restart the application\n"
        
        print(error_msg, file=sys.stderr)
        sys.exit(1)

def create_app(config_name=None):
    """Application factory pattern"""
    # Validate environment before creating app
    validate_environment()
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Enable CORS
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Register blueprints
    from habitica_manager.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

# For gunicorn
app = create_app()
