from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import uuid
import json
import csv
from io import StringIO
from flask import Response
from sqlalchemy import func
from models import db, bcrypt, User, Complaint, Category, ActivityLog

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Redirect authenticated users to their respective dashboards
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        else:
            return redirect(url_for('main.user_dashboard'))
            
    tracking_id = request.args.get('tracking_id')
    tracked_complaint = None
    if tracking_id:
        tracked_complaint = Complaint.query.filter_by(tracking_id=tracking_id).first()
        if not tracked_complaint:
            flash('No complaint found with that Tracking ID.', 'danger')
            
    return render_template('index.html', tracked_complaint=tracked_complaint)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords must match.', 'danger')
            return redirect(url_for('main.register'))
            
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Email already registered.', 'danger')
            return redirect(url_for('main.register'))
            
        username_exists = User.query.filter_by(username=username).first()
        if username_exists:
            flash('Username is already taken.', 'danger')
            return redirect(url_for('main.register'))
        
        # Hash password and create user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # By default, make first user an admin, others users (simple logic for now)
        role = 'admin' if User.query.count() == 0 else 'user'
        
        new_user = User(username=username, email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get('remember'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    if current_user.role != 'user':
        return redirect(url_for('main.index'))
        
    categories = Category.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category')
        priority = request.form.get('priority', 'Low')
        
        # Ensure category exists, else create a default or handle
        if not category_id and categories:
            category_id = categories[0].id
            
        attachment_filename = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                # Generate unique filename
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                attachment_filename = unique_filename
                
        # Generate tracking ID
        tracking_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
        
        new_complaint = Complaint(
            title=title,
            description=description,
            tracking_id=tracking_id,
            priority=priority,
            attachment=attachment_filename,
            user_id=current_user.id,
            category_id=category_id if category_id else None
        )
        db.session.add(new_complaint)
        db.session.commit()
        
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('main.user_dashboard'))
        
    user_complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    
    return render_template('user_dashboard.html', complaints=user_complaints, categories=categories)

@main_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('main.index'))
        
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'All')
    search_query = request.args.get('search', '')
    
    query = Complaint.query
    if status_filter != 'All':
        query = query.filter_by(status=status_filter)
    if search_query:
        query = query.filter(
            db.or_(
                Complaint.tracking_id.ilike(f"%{search_query}%"),
                Complaint.title.ilike(f"%{search_query}%")
            )
        )
        
    complaints = query.order_by(Complaint.created_at.desc()).paginate(page=page, per_page=10)
    
    # Recent Activity Log
    recent_logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(5).all()
    
    # Analytics Data for Plotly
    # 1. Status Distribution
    status_counts = db.session.query(Complaint.status, func.count(Complaint.id)).group_by(Complaint.status).all()
    status_labels = [s[0] for s in status_counts]
    status_values = [s[1] for s in status_counts]
    
    # 2. Priority Distribution
    priority_counts = db.session.query(Complaint.priority, func.count(Complaint.id)).group_by(Complaint.priority).all()
    priority_labels = [p[0] for p in priority_counts]
    priority_values = [p[1] for p in priority_counts]
    
    analytics_data = {
        'status': {'labels': status_labels, 'values': status_values},
        'priority': {'labels': priority_labels, 'values': priority_values}
    }
    
    return render_template('admin_dashboard.html', 
                           complaints=complaints, 
                           status_filter=status_filter,
                           search_query=search_query,
                           recent_logs=recent_logs,
                           analytics_data=json.dumps(analytics_data))

@main_bp.route('/export_csv')
@login_required
def export_csv():
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
        
    status_filter = request.args.get('status', 'All')
    search_query = request.args.get('search', '')
    
    query = Complaint.query
    if status_filter != 'All':
        query = query.filter_by(status=status_filter)
    if search_query:
        query = query.filter(
            db.or_(
                Complaint.tracking_id.ilike(f"%{search_query}%"),
                Complaint.title.ilike(f"%{search_query}%")
            )
        )
        
    complaints = query.order_by(Complaint.created_at.desc()).all()
    
    def generate():
        data = StringIO()
        writer = csv.writer(data)
        writer.writerow(['Tracking ID', 'Title', 'User', 'Category', 'Priority', 'Status', 'Date Submitted'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)
        
        for c in complaints:
            cat_name = c.category.name if c.category else 'N/A'
            writer.writerow([c.tracking_id, c.title, c.author.username, cat_name, c.priority, c.status, c.created_at.strftime('%Y-%m-%d')])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
            
    response = Response(generate(), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="complaints_report.csv")
    return response

@main_bp.route('/update_complaint/<int:complaint_id>', methods=['POST'])
@login_required
def update_complaint(complaint_id):
    if current_user.role != 'admin':
        return redirect(url_for('main.index'))
        
    complaint = Complaint.query.get_or_404(complaint_id)
    new_status = request.form.get('status')
    
    if new_status and new_status in ['Pending', 'In Progress', 'Resolved', 'Rejected']:
        complaint.status = new_status
        # Log the activity
        log = ActivityLog(action=f"Updated status to {new_status}", complaint_id=complaint.id, admin_id=current_user.id)
        db.session.add(log)
        db.session.commit()
        flash(f'Complaint {complaint.tracking_id} updated to {new_status}', 'success')
        
    return redirect(url_for('main.admin_dashboard'))
