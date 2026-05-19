# Digital Complaint Management System 🚀

A complete, full-stack web application designed for organizations, colleges, and municipalities to digitally manage complaints submitted by users. Built with modern web development practices, this platform ensures transparency, tracking, and efficient resolution of issues.

## 🌟 Features

### For Users
- **Secure Authentication**: Session-based login with hashed passwords.
- **Complaint Submission**: Log complaints with a title, description, category, priority, and file attachments (images, PDFs).
- **Complaint Tracking**: Instantly check the status of any complaint using a unique Tracking ID (e.g. `CMP-A1B2C3D4`).
- **Dashboard History**: View past complaints and real-time status updates directly from your dashboard.

### For Administrators
- **Interactive Analytics**: Monitor resolution rates and complaint distributions via built-in Plotly.js charts.
- **Complaint Management**: Filter complaints by status (Pending, In Progress, Resolved) and update statuses inline.
- **Activity Logging**: Track which admin updated what complaint for better accountability.
- **CSV Export**: Generate and download comprehensive CSV reports of filtered complaints.

### UI / UX
- **Responsive Design**: Mobile-friendly layout ensuring a great experience on any device.
- **Dark/Light Mode**: User preference toggle seamlessly switching between light and dark themes.
- **Professional Dashboard**: Clean typography (Inter font), modern cards, and interactive hover states.

## 🛠 Tech Stack
- **Frontend**: HTML5, CSS3 (Custom Variables), JavaScript
- **Backend Framework**: Python (Flask)
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Authentication**: Flask-Login, Flask-Bcrypt
- **Analytics**: Plotly.js

## ⚙️ Installation & Setup

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd DigitalComplaintSystem
   ```

2. **Create a virtual environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database with Dummy Data**:
   The provided seed script creates an admin account, user accounts, categories, and dummy complaints to help you test the system immediately.
   ```bash
   python seed_data.py
   ```
   *Note: Admin login is `admin@example.com` / `admin123`. User login is `user1@example.com` / `user123`.*

5. **Run the Server**:
   ```bash
   python app.py
   ```
   Navigate to `http://127.0.0.1:5000` in your web browser.

## 📸 Screenshots & Demo
*(Insert your high-quality screenshots and GIF demonstrations here. Consider showing the Dark Mode toggle, the Analytics dashboard, and the complaint submission process.)*

> **[Demo Video Link]**: If you have recorded a video walkthrough for your presentation, link it here.

## 🚀 Future Enhancements
- [ ] **Email Notifications**: Send an email when a complaint status changes.
- [ ] **AI Categorization**: Automatically categorize complaints based on their text descriptions.
- [ ] **REST API Integration**: Build a standalone API for mobile app consumption.
- [ ] **Real-time Notifications**: Implement WebSockets for instant status updates.
- [ ] **Docker Support**: Containerize the application for scalable deployments.
- [ ] **PostgreSQL Migration**: Upgrade from SQLite for heavy production workloads.

---
**Developed for Final Year Engineering / Portfolio Presentation**
