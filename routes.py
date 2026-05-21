from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
import uuid
import json
import csv
from datetime import datetime
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
        
    return render_template('auth/register.html')

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
            
    return render_template('auth/login.html')

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
    
    return render_template('user/user_dashboard.html', complaints=user_complaints, categories=categories)

@main_bp.route('/admin_dashboard')
def admin_dashboard():
    # Ensure an admin user exists; create default if none
    admin_user = User.query.filter_by(role='admin').first()
    if not admin_user:
        admin_user = User(username='admin', email='admin@example.com', password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'), role='admin')
        db.session.add(admin_user)
        db.session.commit()

    # Auto-login admin for demo if not authenticated
    if not current_user.is_authenticated:
        login_user(admin_user)
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
    
    return render_template('admin/admin_dashboard.html', 
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


# ─── Health Check ──────────────────────────────────────────────────────────────

@main_bp.route('/health')
def health_check():
    """System health status endpoint. Returns JSON with DB connectivity and uptime info."""
    try:
        # Quick DB probe
        user_count = User.query.count()
        complaint_count = Complaint.query.count()
        db_status = 'ok'
    except Exception as e:
        db_status = f'error: {str(e)}'
        user_count = None
        complaint_count = None

    return jsonify({
        'status': 'healthy' if db_status == 'ok' else 'degraded',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': '1.0.0',
        'database': {
            'status': db_status,
            'users': user_count,
            'complaints': complaint_count
        },
        'service': 'Digital Complaint Management System'
    }), 200 if db_status == 'ok' else 503


# ─── REST API Endpoints ────────────────────────────────────────────────────────

@main_bp.route('/api/complaints')
@login_required
def api_complaints():
    """GET /api/complaints — Returns a paginated JSON list of complaints (admin only)."""
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden. Admin access required.'}), 403

    page      = request.args.get('page', 1, type=int)
    per_page  = request.args.get('per_page', 10, type=int)
    status    = request.args.get('status')
    priority  = request.args.get('priority')
    search    = request.args.get('search', '')

    query = Complaint.query
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if search:
        query = query.filter(
            db.or_(
                Complaint.tracking_id.ilike(f'%{search}%'),
                Complaint.title.ilike(f'%{search}%')
            )
        )

    paginated = query.order_by(Complaint.created_at.desc()).paginate(page=page, per_page=per_page)

    data = []
    for c in paginated.items:
        data.append({
            'id': c.id,
            'tracking_id': c.tracking_id,
            'title': c.title,
            'description': c.description,
            'status': c.status,
            'priority': c.priority,
            'category': c.category.name if c.category else None,
            'submitted_by': c.author.username,
            'created_at': c.created_at.isoformat(),
            'updated_at': c.updated_at.isoformat() if c.updated_at else None,
            'attachment': c.attachment
        })

    return jsonify({
        'complaints': data,
        'pagination': {
            'page': paginated.page,
            'per_page': paginated.per_page,
            'total': paginated.total,
            'pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    }), 200


@main_bp.route('/api/complaints/<int:complaint_id>')
@login_required
def api_complaint_detail(complaint_id):
    """GET /api/complaints/<id> — Returns a single complaint's full detail."""
    complaint = Complaint.query.get_or_404(complaint_id)

    # Users can only view their own; admins can view all
    if current_user.role != 'admin' and complaint.user_id != current_user.id:
        return jsonify({'error': 'Forbidden.'}), 403

    return jsonify({
        'id': complaint.id,
        'tracking_id': complaint.tracking_id,
        'title': complaint.title,
        'description': complaint.description,
        'status': complaint.status,
        'priority': complaint.priority,
        'category': complaint.category.name if complaint.category else None,
        'submitted_by': complaint.author.username,
        'created_at': complaint.created_at.isoformat(),
        'updated_at': complaint.updated_at.isoformat() if complaint.updated_at else None,
        'attachment': complaint.attachment
    }), 200


# ─── API Documentation Page ────────────────────────────────────────────────────

@main_bp.route('/api/docs')
def api_docs():
    """Lightweight, self-hosted API documentation page."""
    return render_template('api_docs.html')
