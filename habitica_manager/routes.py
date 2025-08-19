from flask import Blueprint, jsonify, request, render_template
import logging
from .habitica_service import HabiticaService, HabiticaAPIError

# Get logger for this module
logger = logging.getLogger(__name__)

# Create blueprint
main_bp = Blueprint('main', __name__)

# Initialize Habitica service
habitica_service = HabiticaService()

@main_bp.route('/', methods=['GET'])
def home():
    """Serve the main HTML page"""
    return render_template('index.html')

@main_bp.route('/api', methods=['GET'])
def api_info():
    """API information endpoint"""
    try:
        creds_info = habitica_service.get_credentials_info()
        return jsonify({
            'status': 'success',
            'message': 'Habitica Manager API is running',
            'version': '1.0.0',
            'habitica_connection': creds_info
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'API configuration error: {str(e)}',
            'version': '1.0.0'
        }), 500

@main_bp.route('/api/test-connection', methods=['GET'])
def test_habitica_connection():
    """Test connection to Habitica API"""
    try:
        # Use the new test connection method
        result = habitica_service.test_connection()
        
        if result['success']:
            user_data = result['user_data']
            return jsonify({
                'status': 'success',
                'message': 'Successfully connected to Habitica API',
                'user_info': {
                    'username': user_data.get('auth', {}).get('local', {}).get('username', 'Unknown'),
                    'level': user_data.get('stats', {}).get('lvl', 0),
                    'class': user_data.get('stats', {}).get('class', 'Unknown'),
                    'experience': user_data.get('stats', {}).get('exp', 0)
                }
            })
        else:
            return jsonify({
                'status': 'error',
                'message': result['message']
            }), 500
            
    except Exception as e:
        logger.error(f"Unexpected error testing connection: {e}")
        return jsonify({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }), 500

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for load balancers"""
    return jsonify({
        'status': 'healthy',
        'timestamp': request.headers.get('Date')
    })

@main_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks from Habitica"""
    try:
        tasks = habitica_service.get_tasks()
        return jsonify({
            'status': 'success',
            'data': tasks,
            'message': 'Tasks retrieved successfully'
        })
    except HabiticaAPIError as e:
        logger.error(f"Error getting tasks: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/habits', methods=['GET'])
def get_habits():
    """Get habits from Habitica"""
    try:
        habits = habitica_service.get_habits()
        return jsonify({
            'status': 'success',
            'data': habits,
            'message': 'Habits retrieved successfully'
        })
    except HabiticaAPIError as e:
        logger.error(f"Error getting habits: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/dailies', methods=['GET'])
def get_dailies():
    """Get daily tasks from Habitica"""
    try:
        dailies = habitica_service.get_dailies()
        return jsonify({
            'status': 'success',
            'data': dailies,
            'message': 'Dailies retrieved successfully'
        })
    except HabiticaAPIError as e:
        logger.error(f"Error getting dailies: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/todos', methods=['GET'])
def get_todos():
    """Get todo tasks from Habitica"""
    try:
        todos = habitica_service.get_todos()
        return jsonify({
            'status': 'success',
            'data': todos,
            'message': 'Todos retrieved successfully'
        })
    except HabiticaAPIError as e:
        logger.error(f"Error getting todos: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/clone_todo', methods=['POST'])
def clone_todo():
    """Clone a todo task"""
    try:
        # Get the todo ID from request
        data = request.get_json()
        if not data or 'todo_id' not in data:
            return jsonify({
                'status': 'error',
                'error': 'Missing todo_id in request body'
            }), 400
        
        todo_id = data['todo_id']
        logger.info(f"Cloning todo with ID: {todo_id}")
        
        # Clone the todo using the habitica service
        result = habitica_service.clone_todo(todo_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Todo cloned successfully',
            'cloned_todo': result
        })
        
    except HabiticaAPIError as e:
        logger.error(f"Habitica API error cloning todo: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error cloning todo: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@main_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500
