#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import os
from app import create_app, db

# Create Flask application
app = create_app(os.environ.get('FLASK_ENV', 'production'))

# Initialize database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()