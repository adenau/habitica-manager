from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import sys
import logging
from dotenv import load_dotenv
from .database import init_database, test_connection

# Load environment variables
load_dotenv()

def configure_logging(app):
    """Configure logging for the application"""
    # Set logging level based on environment
    log_level = logging.INFO
    if app.config.get('ENV') == 'development' or app.config.get('DEBUG'):
        log_level = logging.DEBUG
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set levels for specific loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)  # Reduce Flask request logs
    logging.getLogger('requests').setLevel(logging.WARNING)  # Reduce requests library logs
    
    # Get logger for this module
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully")
    return logger

def validate_environment():
    """Validate required environment variables"""
    logger = logging.getLogger(__name__)
    
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
        error_msg = "Configuration Error: Habitica API credentials are not properly configured."
        
        if missing_vars:
            error_msg += "\nMissing variables:\n" + "\n".join(missing_vars)
        
        if invalid_vars:
            error_msg += "\nInvalid variables (still using default values):\n" + "\n".join(invalid_vars)
        
        error_msg += "\n\nTo fix this:"
        error_msg += "\n1. Go to https://habitica.com/user/settings/api"
        error_msg += "\n2. Copy your User ID and API Token"
        error_msg += "\n3. Update the .env file with your actual credentials"
        error_msg += "\n4. Restart the application"
        
        logger.critical(error_msg)
        sys.exit(1)

def create_app(config_name=None):
    """Application factory pattern"""
    # Validate environment before creating app
    validate_environment()
    
    # Initialize database
    logger = logging.getLogger(__name__)
    try:
        init_database()
        db_info = test_connection()
        if db_info['success']:
            logger.info(f"Database ready at {db_info['db_path']} with {db_info['table_count']} tables")
        else:
            logger.error(f"Database test failed: {db_info['error']}")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Configure logging
    logger = configure_logging(app)
    
    # Enable CORS
    CORS(app)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info("Flask application initialized")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    # Register blueprints
    from habitica_manager.routes import main_bp
    app.register_blueprint(main_bp)
    logger.info("Blueprints registered successfully")
    
    return app

# For gunicorn
app = create_app()
