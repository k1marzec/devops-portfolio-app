#!/usr/bin/env python3
"""
Manual test runner - runs tests without pytest command
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Task

def test_basic_functionality():
    """Basic test of app functionality."""
    print("🧪 Testing basic app functionality...")
    
    # Create test app
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Test 1: Create task
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        print("✅ Task creation - PASSED")
        
        # Test 2: Query task
        found_task = Task.query.filter_by(title='Test Task').first()
        assert found_task is not None
        assert found_task.title == 'Test Task'
        print("✅ Task query - PASSED")
        
        # Test 3: Test routes with test client
        with app.test_client() as client:
            # Test index page
            response = client.get('/')
            assert response.status_code == 200
            print("✅ Index route - PASSED")
            
            # Test API endpoint
            response = client.get('/api/tasks')
            assert response.status_code == 200
            print("✅ API route - PASSED")
            
            # Test health check
            response = client.get('/health')
            assert response.status_code == 200
            print("✅ Health check - PASSED")
    
    print("\n🎉 All basic tests PASSED!")
    return True

if __name__ == '__main__':
    try:
        test_basic_functionality()
        print("✅ Manual tests completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)