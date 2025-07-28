from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from app import db
from app.models import Task

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    current_app.logger.info(f'Retrieved {len(tasks)} tasks from database')
    return render_template('index.html', tasks=tasks)

@bp.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if not title:
            flash('Title is required!', 'error')
            return render_template('add_task.html')
        
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        
        current_app.logger.info(f'New task created: {task.title}')
        flash('Task added successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('add_task.html')

@bp.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    
    current_app.logger.info(f'Task {task.title} marked as {"completed" if task.completed else "incomplete"}')
    
    if request.is_json:
        return jsonify({'success': True, 'completed': task.completed})
    
    flash(f'Task {"completed" if task.completed else "marked as incomplete"}!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    
    current_app.logger.info(f'Task deleted: {title}')
    
    if request.is_json:
        return jsonify({'success': True})
    
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/api/tasks')
def api_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Todo App is running'})