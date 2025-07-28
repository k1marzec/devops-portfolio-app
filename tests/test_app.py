import pytest
import json
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import create_app, db
from app.models import Task

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    app.config.from_object(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class TestRoutes:
    """Test application routes."""
    
    def test_index_empty(self, client):
        """Test index page with no tasks."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'No tasks yet' in response.data
        assert b'Add Your First Task' in response.data
    
    def test_add_task_get(self, client):
        """Test GET request to add task page."""
        response = client.get('/add')
        assert response.status_code == 200
        assert b'Add New Task' in response.data
        assert b'Task Title' in response.data
    
    def test_add_task_post_valid(self, client):
        """Test POST request to add task with valid data."""
        response = client.post('/add', data={
            'title': 'Test Task',
            'description': 'Test Description'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Task added successfully!' in response.data
        assert b'Test Task' in response.data
    
    def test_add_task_post_missing_title(self, client):
        """Test POST request to add task without title."""
        response = client.post('/add', data={
            'description': 'Test Description'
        })
        
        assert response.status_code == 200
        assert b'Title is required!' in response.data
    
    def test_complete_task(self, client, app):
        """Test completing a task."""
        with app.app_context():
            # Create a task
            task = Task(title='Test Task', description='Test Description')
            db.session.add(task)
            db.session.commit()
            task_id = task.id
        
        # Complete the task
        response = client.post(f'/complete/{task_id}', 
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['completed'] is True
    
    def test_delete_task(self, client, app):
        """Test deleting a task."""
        with app.app_context():
            # Create a task
            task = Task(title='Test Task', description='Test Description')
            db.session.add(task)
            db.session.commit()
            task_id = task.id
        
        # Delete the task
        response = client.post(f'/delete/{task_id}', 
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_api_tasks_empty(self, client):
        """Test API endpoint with no tasks."""
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_api_tasks_with_data(self, client, app):
        """Test API endpoint with tasks."""
        with app.app_context():
            # Create tasks
            task1 = Task(title='Task 1', description='Description 1')
            task2 = Task(title='Task 2', description='Description 2', completed=True)
            db.session.add_all([task1, task2])
            db.session.commit()
        
        response = client.get('/api/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data) == 2
        assert data[0]['title'] == 'Task 2'  # Most recent first
        assert data[0]['completed'] is True
        assert data[1]['title'] == 'Task 1'
        assert data[1]['completed'] is False
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'message' in data

class TestModels:
    """Test database models."""
    
    def test_task_creation(self, app):
        """Test creating a task."""
        with app.app_context():
            task = Task(title='Test Task', description='Test Description')
            db.session.add(task)
            db.session.commit()
            
            assert task.id is not None
            assert task.title == 'Test Task'
            assert task.description == 'Test Description'
            assert task.completed is False
            assert task.created_at is not None
            assert task.updated_at is not None
    
    def test_task_repr(self, app):
        """Test task string representation."""
        with app.app_context():
            task = Task(title='Test Task')
            assert repr(task) == '<Task Test Task>'
    
    def test_task_to_dict(self, app):
        """Test task serialization to dictionary."""
        with app.app_context():
            task = Task(title='Test Task', description='Test Description')
            db.session.add(task)
            db.session.commit()
            
            task_dict = task.to_dict()
            assert task_dict['title'] == 'Test Task'
            assert task_dict['description'] == 'Test Description'
            assert task_dict['completed'] is False
            assert 'id' in task_dict
            assert 'created_at' in task_dict
            assert 'updated_at' in task_dict

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_task_workflow(self, client):
        """Test complete workflow: add task -> complete -> verify."""
        # Add task
        response = client.post('/add', data={
            'title': 'Integration Test Task',
            'description': 'Test complete workflow'
        }, follow_redirects=True)
        assert response.status_code == 200
        
        # Get task from API
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert len(tasks) == 1
        task_id = tasks[0]['id']
        
        # Complete task
        response = client.post(f'/complete/{task_id}', 
                             content_type='application/json')
        assert response.status_code == 200
        
        # Verify completion
        response = client.get('/api/tasks')
        tasks = json.loads(response.data)
        assert tasks[0]['completed'] is True
    
    def test_task_statistics(self, client, app):
        """Test task statistics calculation."""
        with app.app_context():
            # Create mixed tasks
            tasks = [
                Task(title='Task 1', completed=False),
                Task(title='Task 2', completed=True),
                Task(title='Task 3', completed=True),
                Task(title='Task 4', completed=False),
            ]
            db.session.add_all(tasks)
            db.session.commit()
        
        # Check index page shows correct stats
        response = client.get('/')
        assert response.status_code == 200
        
        # Check if tasks are displayed
        assert b'Task 1' in response.data or b'Task 2' in response.data or b'Task 3' in response.data
        
        # Check statistics section exists
        response_text = response.data.decode()
        assert 'Pending Tasks' in response_text
        assert 'Completed Tasks' in response_text
        assert 'Total Tasks' in response_text