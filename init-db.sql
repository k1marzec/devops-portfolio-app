-- Initialize the database with some sample data
-- This file will be executed when PostgreSQL container starts for the first time

-- Ensure the database exists (this is usually handled by POSTGRES_DB env var)
-- CREATE DATABASE IF NOT EXISTS todoapp;

-- Create tables will be handled by Flask-Migrate
-- But we can add some initial configuration or data here if needed

-- Example: Create an extension if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- You can add initial data here after the application creates tables
-- INSERT INTO task (title, description, completed, created_at, updated_at) 
-- VALUES 
--   ('Welcome to DevOps Todo App!', 'This is your first sample task. You can edit or delete it.', false, NOW(), NOW()),
--   ('Set up CI/CD Pipeline', 'Configure GitHub Actions for automated testing and deployment.', false, NOW(), NOW()),
--   ('Configure Monitoring', 'Set up application monitoring and logging.', false, NOW(), NOW());

-- Create a simple function for cleanup (example of advanced SQL)
CREATE OR REPLACE FUNCTION cleanup_old_completed_tasks()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM task 
    WHERE completed = true 
    AND updated_at < NOW() - INTERVAL '30 days';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;