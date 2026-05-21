# Digital Complaint Management System

A Flask-based web application used to manage and track complaints digitally with secure authentication, admin analytics, REST APIs, and complaint status management.

---

# Features

- User Registration & Login
- Admin Dashboard
- Complaint Submission
- Complaint Tracking
- Complaint Status Updates
- REST API Integration
- CSV Export
- Activity Logs
- Health Monitoring Endpoint
- Role-Based Authentication
- Responsive User Interface

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Flask | Web Framework |
| SQLite | Database |
| SQLAlchemy | ORM |
| HTML/CSS/Bootstrap | Frontend |
| JavaScript | UI Functionality |
| Git & GitHub | Version Control |

---

# Project Architecture

```text
Client Browser
      ↓
Flask Application
      ↓
Routes / Controllers
      ↓
SQLite Database
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/karthik2276/DigitalComplaintSystem.git
cd DigitalComplaintSystem
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
python app.py
```

Application runs on:

```text
http://127.0.0.1:5000
```

---

# API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home Page |
| `/login` | GET/POST | User Login |
| `/register` | GET/POST | User Registration |
| `/health` | GET | Health Check |
| `/api/complaints` | GET | Complaint API |
| `/admin_dashboard` | GET | Admin Dashboard |

---

# Screenshots

## Home Page

(Add Sc<img width="1920" height="1080" alt="home" src="https://github.com/user-attachments/assets/8f840a24-d044-4478-9e4a-bb46e7b2e06b" />
reenshot Here)

## User Dashboard

(Add S<img width="1920" height="1080" alt="user_dashboard" src="https://github.com/user-attachments/assets/60f5ea47-6e2b-465f-b811-3f40faa91f5e" />
creenshot Here)

## Admin Dashboard

(Add S<img width="1920" height="1080" alt="admin_dashboard" src="https://github.com/user-attachments/assets/fe8e1cc2-75ba-473b-9637-eb2afa11102e" />
creenshot Here)

---

# Future Enhancements

- Docker Deployment
- CI/CD Integration
- Email Notifications
- Cloud Hosting
- Mobile App Integration
- AI-Based Complaint Categorization

---

# Author

**Karthikeyan S**

GitHub:
https://github.com/karthik2276

---

# License

This project is created for academic and learning purposes.
