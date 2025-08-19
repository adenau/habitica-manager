# Habitica Manager

A Flask-based web application for managing your Habitica tasks, habits, and dailies with an intuitive interface.

![Habitica Manager](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2.0-red.svg)

## Features

- 🔐 **Secure API Integration** - Connect to your Habitica account with API credentials
- 📝 **Todo Management** - View and clone your todo tasks with subtask support
- 🔄 **Habits Tracking** - Monitor your habits and streaks
- 📅 **Daily Tasks** - Keep track of your daily routines
- 📱 **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Real-time Updates** - Instant refresh after task operations
- 🎨 **Modern UI** - Clean, intuitive interface with visual feedback

## Screenshots

- **Desktop Layout**: Three-column responsive grid showing todos, habits, and dailies side by side
- **Task Cloning**: One-click cloning of todos with all subtasks and properties
- **Visual Notifications**: Success/error feedback for all operations

## Installation

### Prerequisites

- Python 3.12 or higher
- Habitica account with API credentials

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/habitica-manager.git
   cd habitica-manager
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   HABITICA_USER_ID=your-user-id-here
   HABITICA_API_TOKEN=your-api-token-here
   HABITICA_API_URL=https://habitica.com/api/v3
   ```

   Get your credentials from: https://habitica.com/user/settings/api

5. **Run the application**
   
   **Development:**
   ```bash
   start_dev.bat  # Windows
   # or
   python run.py  # Cross-platform
   ```
   
   **Production:**
   ```bash
   start_prod.bat  # Windows
   # or
   gunicorn -c gunicorn.conf.py run:app
   ```

6. **Open your browser**
   Navigate to http://localhost:5000

## Usage

1. **Test Connection** - Verify your Habitica API credentials
2. **Load Data** - Fetch your current tasks, habits, and dailies
3. **Clone Todos** - Create copies of existing todos with all properties preserved
4. **Monitor Progress** - View subtasks, streaks, and completion status

## API Endpoints

- `GET /api` - API information and status
- `GET /api/test-connection` - Test Habitica connection
- `GET /api/todos` - Get all todo tasks
- `GET /api/habits` - Get all habits
- `GET /api/dailies` - Get all daily tasks
- `POST /api/clone_todo` - Clone a todo task

## Project Structure

```
habitica-manager/
├── habitica_manager/          # Main application package
│   ├── __init__.py           # Package initialization
│   ├── app.py                # Flask application factory
│   ├── routes.py             # API routes and endpoints
│   ├── habitica_service.py   # Habitica API integration
│   ├── static/               # Static assets
│   │   ├── css/style.css     # Application styles
│   │   └── js/app.js         # Frontend JavaScript
│   └── templates/            # HTML templates
│       └── index.html        # Main interface
├── .env                      # Environment configuration
├── requirements.txt          # Python dependencies
├── gunicorn.conf.py         # Production server config
├── run.py                   # Development server entry point
├── start_dev.bat            # Windows development script
└── start_prod.bat           # Windows production script
```

## Technologies Used

- **Backend**: Flask 3.0.0, Gunicorn 21.2.0
- **Frontend**: Vanilla JavaScript, CSS Grid, Responsive Design
- **API**: Habitica REST API v3
- **Environment**: python-dotenv, requests
- **CORS**: flask-cors for cross-origin support

## Development

### Running Tests
```bash
# Add test commands when tests are implemented
python -m pytest
```

### Code Style
The project follows Python PEP 8 style guidelines.

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

- ⚠️ Never commit your `.env` file with real API credentials
- 🔒 API credentials are validated on startup
- 🛡️ All API requests include proper authentication headers

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Habitica](https://habitica.com) for providing the excellent API
- Flask community for the robust web framework
- Contributors and users of this project

## Support

If you encounter any issues:

1. Check that your API credentials are correct
2. Ensure you have an active internet connection
3. Verify that Habitica's API is accessible
4. Check the console logs for detailed error messages

For bugs and feature requests, please open an issue on GitHub.

---

**Habitica Manager** - Making task management easier, one habit at a time! 🚀
