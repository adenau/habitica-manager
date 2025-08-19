"""
Habitica API service for interacting with the Habitica REST API.
"""

import os
import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class HabiticaAPIError(Exception):
    """Custom exception for Habitica API errors"""
    pass

class HabiticaService:
    """Service class for interacting with Habitica API"""
    
    def __init__(self):
        self.api_url = os.getenv('HABITICA_API_URL', 'https://habitica.com/api/v3')
        self.user_id = os.getenv('HABITICA_USER_ID')
        self.api_token = os.getenv('HABITICA_API_TOKEN')
        
        # Validate credentials
        self._validate_credentials()
    
    def _validate_credentials(self):
        """Validate that API credentials are properly configured"""
        print(f"\n🔍 Validating Habitica API Credentials:")
        print(f"   User ID: {'✅ Set' if self.user_id else '❌ Missing'}")
        print(f"   API Token: {'✅ Set' if self.api_token else '❌ Missing'}")
        
        if not self.user_id or self.user_id == 'your-user-id':
            raise ValueError("HABITICA_USER_ID is not configured. Please set your Habitica User ID in the .env file.")
        
        if not self.api_token or self.api_token == 'your-api-token':
            raise ValueError("HABITICA_API_TOKEN is not configured. Please set your Habitica API Token in the .env file.")
        
        # Basic format validation
        if len(self.user_id) != 36 or self.user_id.count('-') != 4:
            print(f"⚠️  Warning: User ID format looks unusual. Expected UUID format (36 chars with 4 dashes)")
            print(f"   Current User ID: {self.user_id}")
        
        if len(self.api_token) != 36 or self.api_token.count('-') != 4:
            print(f"⚠️  Warning: API Token format looks unusual. Expected UUID format (36 chars with 4 dashes)")
            print(f"   Current API Token: {self.api_token[:8]}...{self.api_token[-4:]}")
        
        print(f"✅ Habitica API credentials validated successfully")
        logger.info("Habitica API credentials validated successfully")
    
    def get_credentials_info(self) -> Dict[str, str]:
        """Get information about configured credentials (for debugging)"""
        return {
            'api_url': self.api_url,
            'user_id_configured': bool(self.user_id and self.user_id != 'your-user-id'),
            'api_token_configured': bool(self.api_token and self.api_token != 'your-api-token'),
            'user_id_preview': f"{self.user_id[:8]}..." if self.user_id else None
        }
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Habitica API requests"""
        # The x-client header should contain the developer's User ID and app name
        # Format: {developer-user-id}-{app-name}
        x_client_value = f"{self.user_id}-HabiticaManager" if self.user_id else "unknown-HabiticaManager"
        
        headers = {
            'x-api-user': self.user_id or '',
            'x-api-key': self.api_token or '',
            'x-client': x_client_value,
            'Content-Type': 'application/json'
        }
        
        # Debug header info (without exposing full credentials)
        print(f"\n🔑 API Headers Debug:")
        print(f"   x-api-user: {self.user_id[:8]}...{self.user_id[-4:] if self.user_id else 'None'}")
        print(f"   x-api-key: {self.api_token[:8]}...{self.api_token[-4:] if self.api_token else 'None'}")
        print(f"   x-client: {x_client_value}")
        print(f"   Content-Type: {headers['Content-Type']}")
        
        return headers
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict:
        """Make a request to the Habitica API"""
        try:
            url = f"{self.api_url}/{endpoint}"
            headers = self._get_headers()
            
            # Log request details
            print(f"\n🔄 Making Habitica API Request:")
            print(f"   URL: {url}")
            print(f"   Headers: {headers}")
            print(f"   Method: {method}")
            if data:
                print(f"   Data: {data}")
            
            logger.info(f"Making {method} request to: {url}")
            
            # Make the appropriate request
            if method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:  # Default to GET
                response = requests.get(url, headers=headers, timeout=10)
            
            # Log response details
            print(f"\n📥 Habitica API Response:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Headers: {dict(response.headers)}")
            
            try:
                response_json = response.json()
                print(f"   Response Body: {response_json}")
            except Exception as json_error:
                print(f"   Response Text: {response.text}")
                print(f"   JSON Parse Error: {json_error}")
            
            # Check for specific error codes
            if response.status_code == 401:
                print(f"❌ Authentication Error: Invalid credentials")
                raise HabiticaAPIError("Invalid Habitica API credentials. Please check your User ID and API Token.")
            
            if response.status_code == 400:
                print(f"❌ Bad Request Error")
                raise HabiticaAPIError(f"Bad request to Habitica API: {response.text}")
            
            if response.status_code == 404:
                print(f"❌ Not Found Error")
                raise HabiticaAPIError(f"Habitica API endpoint not found: {endpoint}")
            
            if response.status_code == 429:
                print(f"❌ Rate Limit Error")
                raise HabiticaAPIError("Rate limit exceeded. Please wait before making more requests.")
            
            if response.status_code >= 500:
                print(f"❌ Server Error")
                raise HabiticaAPIError(f"Habitica server error: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            if not data.get('success', False):
                print(f"❌ API Error: {data.get('message', 'Unknown error')}")
                raise HabiticaAPIError(f"API returned error: {data.get('message', 'Unknown error')}")
            
            print(f"✅ Request successful, returning data")
            return data.get('data', {})
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {e}")
            logger.error(f"Error making request to Habitica API: {e}")
            if "401" in str(e):
                raise HabiticaAPIError("Invalid Habitica API credentials. Please check your User ID and API Token.")
            raise HabiticaAPIError(f"Failed to connect to Habitica API: {e}")
    
    def test_connection(self) -> Dict:
        """Test the connection to Habitica API with minimal data request"""
        print(f"\n🧪 Testing Habitica API Connection...")
        try:
            # Make a simple request to test authentication
            result = self._make_request('user')
            print(f"✅ Connection test successful!")
            return {
                'success': True,
                'message': 'Connection successful',
                'user_data': result
            }
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return {
                'success': False,
                'message': str(e),
                'user_data': None
            }
    
    def get_tasks(self) -> Dict[str, List]:
        """Get all tasks (todos, habits, dailies) from Habitica"""
        raw_tasks = self._make_request('tasks/user')
        
        print(f"\n📊 Task Processing Debug:")
        print(f"   Total tasks received: {len(raw_tasks)}")
        
        # The API returns a flat list, so we need to separate by type
        todos = [task for task in raw_tasks if task.get('type') == 'todo']
        habits = [task for task in raw_tasks if task.get('type') == 'habit']
        dailies = [task for task in raw_tasks if task.get('type') == 'daily']
        
        print(f"   Todos: {len(todos)}")
        print(f"   Habits: {len(habits)}")
        print(f"   Dailies: {len(dailies)}")
        
        # Show a sample of each type for debugging
        if todos:
            print(f"   Sample Todo: {todos[0].get('text', 'No text')}")
        if habits:
            print(f"   Sample Habit: {habits[0].get('text', 'No text')}")
        if dailies:
            print(f"   Sample Daily: {dailies[0].get('text', 'No text')}")
        
        return {
            'todos': todos,
            'habits': habits,
            'dailys': dailies  # Note: Habitica API uses 'dailys' not 'dailies'
        }
    
    def get_todos(self) -> List[Dict]:
        """Get todo tasks from Habitica"""
        tasks = self.get_tasks()
        return tasks.get('todos', [])
    
    def get_habits(self) -> List[Dict]:
        """Get habits from Habitica"""
        tasks = self.get_tasks()
        return tasks.get('habits', [])
    
    def get_dailies(self) -> List[Dict]:
        """Get daily tasks from Habitica"""
        tasks = self.get_tasks()
        return tasks.get('dailys', [])
    
    def clone_todo(self, todo_id: str) -> Dict:
        """Clone a todo task by creating a copy with the same properties"""
        try:
            logger.info(f"Cloning todo with ID: {todo_id}")
            
            # First, get the original todo details
            original_todo = self._make_request(f'tasks/{todo_id}')
            logger.info(f"Retrieved original todo: {original_todo.get('text', 'Unknown')}")
            
            # Prepare the new todo data
            new_todo_data = {
                'text': original_todo['text'],
                'type': 'todo',
                'notes': original_todo.get('notes', ''),
                'priority': original_todo.get('priority', 1),
                'date': original_todo.get('date'),
                'reminders': original_todo.get('reminders', []),
                'tags': original_todo.get('tags', [])
            }
            
            # Clone checklist if it exists
            if original_todo.get('checklist'):
                new_todo_data['checklist'] = [
                    {
                        'text': item['text'],
                        'completed': False  # Start with uncompleted checklist items
                    }
                    for item in original_todo['checklist']
                ]
            
            logger.info(f"Creating new todo with data: {new_todo_data}")
            
            # Create the new todo
            result = self._make_request('tasks/user', method='POST', data=new_todo_data)
            
            logger.info(f"Successfully cloned todo. New ID: {result.get('id', 'Unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Error cloning todo {todo_id}: {e}")
            raise HabiticaAPIError(f"Failed to clone todo: {str(e)}")
    
    def get_user_stats(self) -> Dict:
        """Get user stats from Habitica (optional feature)"""
        return self._make_request('user')
