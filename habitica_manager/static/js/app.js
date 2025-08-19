// Habitica Manager - Main JavaScript File
// This file currently does simple DOM manipulation and API testing

document.addEventListener('DOMContentLoaded', function() {
    console.log('Habitica Manager JavaScript loaded successfully!');
    
    // Initialize navigation
    initializeNavigation();
    
    // Get DOM elements
    const testConnectionBtn = document.getElementById('testConnectionBtn');
    const loadDataBtn = document.getElementById('loadDataBtn');
    const apiBtn = document.getElementById('apiBtn');
    const output = document.getElementById('output');
    const tasksSection = document.getElementById('tasksSection');
    const habitsSection = document.getElementById('habitsSection');
    const dailiesSection = document.getElementById('dailiesSection');
    
    // Test Habitica connection button handler
    if (testConnectionBtn) {
        testConnectionBtn.addEventListener('click', async function() {
            console.log('Test Habitica connection button clicked!');
            await testHabiticaConnection();
        });
    }
    
    // Load Habitica data button handler
    if (loadDataBtn) {
        loadDataBtn.addEventListener('click', async function() {
            console.log('Load Habitica data button clicked!');
            await loadHabiticaData();
        });
    }
    
    // API test button handler
    if (apiBtn) {
        apiBtn.addEventListener('click', async function() {
            console.log('API test button clicked!');
            
            try {
                // Show loading state
                output.classList.add('active');
                output.innerHTML = '<p>Testing API connection...</p>';
                
                // Make API call to our Flask backend
                const response = await fetch('/api');
                const data = await response.json();
                
                // Display API response
                output.innerHTML = `
                    <p><strong>API Test Successful!</strong></p>
                    <p>Status: ${data.status}</p>
                    <p>Message: ${data.message}</p>
                    <p>Version: ${data.version}</p>
                `;
                
            } catch (error) {
                console.error('API test failed:', error);
                output.innerHTML = `
                    <p><strong>API Test Failed!</strong></p>
                    <p>Error: ${error.message}</p>
                `;
            }
            
            // Remove active class after 5 seconds
            setTimeout(() => {
                output.classList.remove('active');
            }, 5000);
        });
    }

    // Initialize navigation functionality
    function initializeNavigation() {
        const navToggle = document.getElementById('navToggle');
        const navMobileMenu = document.getElementById('navMobileMenu');
        
        // Set active link based on current page
        setActiveNavLink();
        
        if (navToggle && navMobileMenu) {
            navToggle.addEventListener('click', function() {
                navToggle.classList.toggle('active');
                navMobileMenu.classList.toggle('active');
            });
            
            // Close mobile menu when clicking on a link
            const mobileLinks = document.querySelectorAll('.nav-mobile-link');
            mobileLinks.forEach(link => {
                link.addEventListener('click', function() {
                    navToggle.classList.remove('active');
                    navMobileMenu.classList.remove('active');
                });
            });
            
            // Close mobile menu when clicking outside
            document.addEventListener('click', function(event) {
                const isClickInsideNav = navToggle.contains(event.target) || navMobileMenu.contains(event.target);
                if (!isClickInsideNav) {
                    navToggle.classList.remove('active');
                    navMobileMenu.classList.remove('active');
                }
            });
        }
    }
    
    // Set active navigation link
    function setActiveNavLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link, .nav-mobile-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === currentPath || (currentPath === '/' && link.textContent.trim() === 'Home')) {
                link.classList.add('active');
            }
        });
    }
    
    // Test Habitica API connection
    async function testHabiticaConnection() {
        try {
            // Show loading state
            output.classList.add('active');
            output.innerHTML = '<div class="loading-spinner"></div> Testing Habitica API connection...';
            
            // Test API connection
            const response = await fetch('/api/test-connection');
            const data = await response.json();
            
            if (data.status === 'success') {
                output.innerHTML = `
                    <p><strong>✅ Habitica Connection Successful!</strong></p>
                    <p>Username: ${data.user_info?.username || 'Unknown'}</p>
                    <p>Level: ${data.user_info?.level || 0}</p>
                    <p>You can now load your Habitica data!</p>
                `;
            } else {
                output.innerHTML = `
                    <p><strong>❌ Habitica Connection Failed!</strong></p>
                    <p>${data.message}</p>
                    <p>Please check your API credentials in the .env file.</p>
                `;
            }
            
        } catch (error) {
            console.error('Failed to test Habitica connection:', error);
            output.innerHTML = `
                <p><strong>❌ Connection Test Failed!</strong></p>
                <p>Error: ${error.message}</p>
                <p>Please check your API credentials and try again.</p>
            `;
        }
        
        // Remove active class after 5 seconds
        setTimeout(() => {
            output.classList.remove('active');
        }, 5000);
    }
    
    // Load all Habitica data
    async function loadHabiticaData() {
        try {
            // Show loading state
            output.classList.add('active');
            output.innerHTML = '<div class="loading-spinner"></div> Loading Habitica data...';
            
            // Load all data in parallel
            const [todosResponse, habitsResponse, dailiesResponse] = await Promise.all([
                fetch('/api/todos'),
                fetch('/api/habits'),
                fetch('/api/dailies')
            ]);
            
            const todosData = await todosResponse.json();
            const habitsData = await habitsResponse.json();
            const dailiesData = await dailiesResponse.json();
            
            // Display the data
            displayTodos(todosData.data || []);
            displayHabits(habitsData.data || []);
            displayDailies(dailiesData.data || []);
            
            // Show success message
            output.innerHTML = `
                <p><strong>Habitica Data Loaded Successfully!</strong></p>
                <p>Todos: ${todosData.data?.length || 0}</p>
                <p>Habits: ${habitsData.data?.length || 0}</p>
                <p>Dailies: ${dailiesData.data?.length || 0}</p>
            `;
            
            // Show sections
            tasksSection.style.display = 'block';
            habitsSection.style.display = 'block';
            dailiesSection.style.display = 'block';
            
        } catch (error) {
            console.error('Failed to load Habitica data:', error);
            output.innerHTML = `
                <p><strong>Failed to Load Habitica Data!</strong></p>
                <p>Error: ${error.message}</p>
            `;
        }
        
        // Remove active class after 3 seconds
        setTimeout(() => {
            output.classList.remove('active');
        }, 3000);
    }

    // Refresh only todos (used after cloning)
    async function refreshTodos() {
        try {
            console.log('Refreshing todos...');
            
            // Load just the todos
            const todosResponse = await fetch('/api/todos');
            const todosData = await todosResponse.json();
            
            // Update the todos display
            displayTodos(todosData.data || []);
            
            console.log(`Todos refreshed: ${todosData.data?.length || 0} todos loaded`);
            
        } catch (error) {
            console.error('Failed to refresh todos:', error);
            utils.showNotification('Failed to refresh todos', 'error');
        }
    }
    
    // Display todos
    function displayTodos(todos) {
        const todosList = document.getElementById('todosList');
        
        if (!todos || todos.length === 0) {
            todosList.innerHTML = '<div class="empty-state"><p>No todo tasks found</p></div>';
            return;
        }
        
        todosList.innerHTML = todos.map(todo => {
            // Build checklist HTML if it exists
            let checklistHtml = '';
            if (todo.checklist && todo.checklist.length > 0) {
                checklistHtml = `
                    <div class="checklist">
                        <h4>Subtasks:</h4>
                        <ul class="checklist-items">
                            ${todo.checklist.map(item => `
                                <li class="checklist-item ${item.completed ? 'completed' : ''}">
                                    <span class="checklist-checkbox">${item.completed ? '✅' : '☐'}</span>
                                    <span class="checklist-text">${escapeHtml(item.text)}</span>
                                </li>
                            `).join('')}
                        </ul>
                        <div class="checklist-progress">
                            ${todo.checklist.filter(item => item.completed).length} of ${todo.checklist.length} completed
                        </div>
                    </div>
                `;
            }
            
            return `
                <div class="task-item ${todo.completed ? 'completed' : ''}">
                    <div class="task-header">
                        <p class="task-text">${escapeHtml(todo.text)}</p>
                        <div class="task-actions">
                            <span class="task-badge badge-todo">Todo</span>
                            ${todo.completed ? '<span class="task-badge badge-completed">Completed</span>' : ''}
                            <button class="clone-btn" onclick="cloneTodo('${todo.id}', this)" title="Clone this todo">
                                Clone
                            </button>
                        </div>
                    </div>
                    <div class="task-meta">
                        ${todo.priority ? `<span>Priority: <div class="priority-indicator priority-${getPriorityLevel(todo.priority)}"></div></span>` : ''}
                        ${todo.date ? `<span>📅 ${formatDate(todo.date)}</span>` : ''}
                        ${todo.notes ? `<span>📝 Has notes</span>` : ''}
                        ${todo.checklist && todo.checklist.length > 0 ? `<span>📋 ${todo.checklist.length} subtasks</span>` : ''}
                    </div>
                    ${checklistHtml}
                </div>
            `;
        }).join('');
    }
    
    // Display habits
    function displayHabits(habits) {
        const habitsList = document.getElementById('habitsList');
        
        if (!habits || habits.length === 0) {
            habitsList.innerHTML = '<div class="empty-state"><p>No habits found</p></div>';
            return;
        }
        
        habitsList.innerHTML = habits.map(habit => `
            <div class="task-item">
                <div class="task-header">
                    <p class="task-text">${escapeHtml(habit.text)}</p>
                    <span class="task-badge badge-habit">Habit</span>
                </div>
                <div class="habit-counters">
                    ${habit.up ? `<span class="counter positive">↑ ${habit.counterUp || 0}</span>` : ''}
                    ${habit.down ? `<span class="counter negative">↓ ${habit.counterDown || 0}</span>` : ''}
                </div>
            </div>
        `).join('');
    }
    
    // Display dailies
    function displayDailies(dailies) {
        const dailiesList = document.getElementById('dailiesList');
        
        if (!dailies || dailies.length === 0) {
            dailiesList.innerHTML = '<div class="empty-state"><p>No daily tasks found</p></div>';
            return;
        }
        
        dailiesList.innerHTML = dailies.map(daily => `
            <div class="task-item ${daily.completed ? 'completed' : ''}">
                <div class="task-header">
                    <p class="task-text">${escapeHtml(daily.text)}</p>
                    <div>
                        <span class="task-badge badge-daily">Daily</span>
                        ${daily.completed ? '<span class="task-badge badge-completed">Completed</span>' : ''}
                    </div>
                </div>
                <div class="task-meta">
                    ${daily.streak ? `<span>🔥 Streak: ${daily.streak}</span>` : ''}
                </div>
            </div>
        `).join('');
    }

    // Clone todo function
    async function cloneTodo(todoId, buttonElement) {
        let button = buttonElement;
        let originalText = '';
        
        try {
            console.log('Cloning todo with ID:', todoId);
            
            // If no button element passed, try to find it from event
            if (!button && window.event && window.event.target) {
                button = window.event.target;
            }
            
            // Show loading feedback if button is available
            if (button) {
                originalText = button.textContent;
                button.textContent = 'Cloning...';
                button.disabled = true;
            }
            
            // Make API call to clone the todo
            const response = await fetch('/api/clone_todo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ todo_id: todoId })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                console.log('Todo cloned successfully:', result);
                utils.showNotification('Todo cloned successfully!', 'success');
                
                // Reload just the todos to show the new cloned item immediately
                await refreshTodos();
            } else {
                console.error('Failed to clone todo:', result);
                utils.showNotification(`Failed to clone todo: ${result.error || 'Unknown error'}`, 'error');
            }
            
        } catch (error) {
            console.error('Error cloning todo:', error);
            utils.showNotification(`Error cloning todo: ${error.message}`, 'error');
        } finally {
            // Restore button state if button is available
            if (button && originalText) {
                button.textContent = originalText;
                button.disabled = false;
            }
        }
    }

    // Make cloneTodo available globally
    window.cloneTodo = cloneTodo;

// Utility functions
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
    
    function getPriorityLevel(priority) {
        if (priority >= 2) return 'high';
        if (priority >= 1.5) return 'medium';
        return 'low';
    }
});

// Simple utility functions (currently unused but ready for expansion)
const utils = {
    // Format date for display
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    // Simple debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Show notification with visual feedback
    showNotification: function(message, type = 'info') {
        console.log(`[${type.toUpperCase()}] ${message}`);
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        // Create message element safely
        const messageSpan = document.createElement('span');
        messageSpan.className = 'notification-message';
        messageSpan.textContent = message; // This safely escapes HTML
        
        const closeButton = document.createElement('button');
        closeButton.className = 'notification-close';
        closeButton.textContent = '×';
        closeButton.onclick = () => notification.remove();
        
        notification.appendChild(messageSpan);
        notification.appendChild(closeButton);
        
        // Add to page
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.add('notification-show');
        }, 10);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.remove('notification-show');
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 5000);
    }
};

// Example of a simple class (ready for future habitica data models)
class HabiticaItem {
    constructor(id, text, type) {
        this.id = id;
        this.text = text;
        this.type = type;
        this.completed = false;
        this.createdAt = new Date();
    }
    
    toggle() {
        this.completed = !this.completed;
        console.log(`${this.text} marked as ${this.completed ? 'completed' : 'incomplete'}`);
    }
    
    getInfo() {
        return {
            id: this.id,
            text: this.text,
            type: this.type,
            completed: this.completed,
            createdAt: this.createdAt
        };
    }
}

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { utils, HabiticaItem };
}
