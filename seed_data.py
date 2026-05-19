from app import create_app
from models import db, User, Category, Complaint, ActivityLog, bcrypt
import uuid
import random
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    with app.app_context():
        # Clear existing data (optional, careful in production!)
        db.drop_all()
        db.create_all()
        
        print("Creating categories...")
        categories = ['Hardware Issue', 'Software Issue', 'Network & Internet', 'HR & Payroll', 'Facilities']
        category_objs = []
        for cat_name in categories:
            cat = Category(name=cat_name)
            db.session.add(cat)
            category_objs.append(cat)
        db.session.commit()
        
        print("Creating users...")
        # Create Admin
        admin_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', email='admin@example.com', password_hash=admin_pw, role='admin')
        db.session.add(admin)
        
        # Create Users
        users = []
        for i in range(1, 6):
            pw = bcrypt.generate_password_hash('user123').decode('utf-8')
            user = User(username=f'user{i}', email=f'user{i}@example.com', password_hash=pw, role='user')
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        
        print("Creating complaints...")
        statuses = ['Pending', 'In Progress', 'Resolved', 'Rejected']
        priorities = ['Low', 'Medium', 'High']
        
        for i in range(20):
            user = random.choice(users)
            category = random.choice(category_objs)
            status = random.choice(statuses)
            priority = random.choice(priorities)
            
            # Random date within last 30 days
            random_days = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=random_days)
            
            tracking_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
            
            complaint = Complaint(
                title=f'Sample Complaint {i+1}',
                description=f'This is a detailed description for sample complaint {i+1}. The user has reported an issue regarding {category.name}.',
                status=status,
                priority=priority,
                tracking_id=tracking_id,
                user_id=user.id,
                category_id=category.id,
                created_at=created_at
            )
            db.session.add(complaint)
            
        db.session.commit()
        print("Database seeded successfully with dummy data!")

if __name__ == '__main__':
    seed_database()
