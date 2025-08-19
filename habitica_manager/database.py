import sqlite3
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def get_db_path():
    """Get the path to the SQLite database file"""
    # Get the project root directory (parent of habitica_manager)
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    
    # Ensure data directory exists
    data_dir.mkdir(exist_ok=True)
    
    return data_dir / "hbm.db"

def init_database():
    """Initialize the SQLite database with required tables"""
    db_path = get_db_path()
    
    # Check if database already exists
    if db_path.exists():
        logger.info(f"Database already exists at {db_path}")
        return
    
    logger.info(f"Creating new database at {db_path}")
    
    try:
        # Create database and tables
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Create tables for storing Habitica data locally
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                type TEXT NOT NULL,
                notes TEXT,
                priority REAL,
                value REAL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                completed BOOLEAN DEFAULT FALSE,
                streak INTEGER DEFAULT 0,
                data TEXT  -- JSON data for additional fields
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                notes TEXT,
                priority REAL,
                value REAL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                up BOOLEAN DEFAULT TRUE,
                down BOOLEAN DEFAULT TRUE,
                counter_up INTEGER DEFAULT 0,
                counter_down INTEGER DEFAULT 0,
                data TEXT  -- JSON data for additional fields
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dailies (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                notes TEXT,
                priority REAL,
                value REAL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                completed BOOLEAN DEFAULT FALSE,
                streak INTEGER DEFAULT 0,
                data TEXT  -- JSON data for additional fields
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                notes TEXT,
                priority REAL,
                value REAL,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                completed BOOLEAN DEFAULT FALSE,
                due_date TIMESTAMP,
                checklist TEXT,  -- JSON data for checklist items
                data TEXT  -- JSON data for additional fields
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sync_type TEXT NOT NULL,
                sync_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL,
                message TEXT,
                record_count INTEGER
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_todos_due_date ON todos(due_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sync_log_time ON sync_log(sync_time)')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully with all tables")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def get_connection():
    """Get a database connection"""
    db_path = get_db_path()
    return sqlite3.connect(str(db_path))

def test_connection():
    """Test database connection and return basic info"""
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get table count
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        conn.close()
        
        return {
            'success': True,
            'db_path': str(db_path),
            'table_count': len(tables),
            'tables': [table[0] for table in tables]
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return {
            'success': False,
            'error': str(e)
        }
