# Digital Complaint Management System 🚀

> A **production‑grade**, full‑stack complaint management platform built with Flask, featuring role‑based access, RESTful APIs, analytics dashboards, and polished UI/UX.

---

## 🌟 Features

- **Secure Authentication** – Session‑based login with Bcrypt password hashing.
- **Complaint Submission** – Title, description, category, priority, file upload (≤ 16 MB).
- **Tracking System** – Unique tracking IDs (`CMP-XXXXXXXX`).
- **User Dashboard** – View own complaints, status history.
- **Admin Dashboard** – Manage all complaints, filter/search, update status, activity logs.
- **Analytics** – Plotly.js visualizations (status distribution, priority breakdown, monthly trends).
- **REST API** – `/api/complaints`, `/api/complaints/<id>`, `/health`, `/api/docs`.
- **System Health** – `/health` endpoint returns JSON status and DB health.
- **API Documentation** – Self‑hosted Swagger‑style page at `/api/docs`.
- **Dark/Light Theme** – Toggle with persistent `localStorage`.
- **Custom Error Pages** – Branded 404 & 500 pages.
- **CSV Export** – Admin can download all complaints.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.12, Flask, Flask‑Login, Flask‑Bcrypt |
| **Database** | SQLite via Flask‑SQLAlchemy |
| **Frontend** | HTML5, CSS3, JavaScript (Jinja2), Plotly.js |
| **Environment** | python‑dotenv (`.env`), `requirements.txt` |
| **Testing / Linting** | pytest, flake8 |

---

## 🏗 Architecture Overview

- `config.py` – Central configuration (environment variables, DB URI, upload folder, secret key).
- `models.py` – SQLAlchemy models: `User`, `Category`, `Complaint`, `ActivityLog`.
- `routes.py` – Blueprint `main_bp` containing auth, user, admin, API, health, docs routes.
- `app.py` – Application factory (`create_app`) registers extensions, blueprints, and error handlers.
- `templates/` – Jinja2 hierarchy:
  - `auth/` – login & register pages.
  - `admin/` – admin dashboard, analytics.
  - `user/` – user dashboard, complaint form.
  - `errors/` – custom 404/500.
  - `base.html` – global layout, navbar (includes links to API docs & health).
- `static/` – CSS, JS, uploads.
- `seed_data.py` – Script to populate demo data.

---

## 📡 API Endpoints & Security

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/complaints` | Paginated list, filter by status/priority/search | **Admin only** (session) |
| GET | `/api/complaints/<id>` | Detailed view of a single complaint | Owner or **Admin** |
| GET | `/health` | Health check – service & DB status | Public |
| GET | `/api/docs` | Interactive API documentation | Public |

All API responses are JSON. Session‑based authentication via Flask‑Login protects sensitive routes. Passwords are never stored in plain text.

---

## 🔐 Security Measures

- **Password hashing** with Bcrypt.
- **SQL injection protection** via ORM queries.
- **File upload validation** (`secure_filename`, UUID prefix, 16 MB limit).
- **Role‑based access control** enforced in route decorators.
- **CSRF protection** can be added via Flask‑WTF (future enhancement).

---

## 📂 Project Structure

```
DigitalComplaintSystem/
├─ app.py                 # Application factory
├─ config.py              # Environment config
├─ models.py              # DB models
├─ routes.py              # Blueprint with all routes
├─ seed_data.py           # Database seeding script
├─ requirements.txt       # Python dependencies
├─ .env.example           # Sample env file
├─ templates/
│   ├─ base.html
│   ├─ index.html
│   ├─ auth/   (login, register)
│   ├─ user/   (dashboard, complaint form)
│   ├─ admin/  (admin dashboard, analytics)
│   └─ errors/ (404.html, 500.html)
├─ static/
│   ├─ css/style.css
│   ├─ uploads/   # user uploaded files
│   └─ js/ …
└─ README.md              # This file
```

---

## 📸 Screenshots / Demo

*Add screenshots of the homepage, user dashboard, admin analytics, and API docs here.*

---

## 🚀 Future Enhancements

- **JWT token‑based API authentication** for stateless clients.
- **Database indexing** on `tracking_id`, `status` for faster queries.
- **Dockerization** – `Dockerfile` + `docker‑compose.yml` for container deployment.
- **Rate limiting** on API endpoints (Flask‑Limiting).
- **API versioning** (`/api/v1/`).
- **CI/CD pipeline** with GitHub Actions (tests, lint, deployment). 

---

## 📄 ATS‑Optimized Resume Bullet Points

- Built a full‑stack **Digital Complaint Management System** using Flask with role‑based authentication and modular MVC architecture.
- Designed and exposed RESTful APIs with pagination, filtering, and secure session‑based access (Flask‑Login).
- Developed interactive admin analytics dashboards using Plotly for real‑time status, priority distribution, and trend visualization.
- Secured the backend with Bcrypt password hashing, validated file uploads, and ORM‑based queries to prevent SQL injection.
- Created a responsive UI with dark/light mode support, reusable template hierarchy, and dynamic dashboards for improved UX.
- Added system health monitoring endpoint, self‑hosted API documentation, and custom 404/500 error pages for production readiness.

---

## 🎤 Interview Q&A (Ready Answers)

**Q:** *Can you explain your project architecture?*  
**A:** It follows a modular MVC pattern on Flask. `config.py` holds environment settings, `models.py` defines SQLAlchemy entities, `routes.py` contains Blueprints for auth, user, admin, and API logic, while `templates/` provides a hierarchical Jinja2 UI. Flask‑Login manages session authentication and role‑based access.

**Q:** *How did you implement role‑based access control?*  
**A:** The first registered user is assigned the `admin` role; all others receive `user`. Each protected route checks `current_user.role` and either renders the appropriate view or redirects/returns a 403.

**Q:** *Describe your REST API design.*  
**A:** Endpoints `/api/complaints` (paginated list) and `/api/complaints/<id>` (detail) return JSON. Admin‑only endpoints require an authenticated session and admin role. Query parameters enable filtering by status, priority, and search terms.

**Q:** *What error‑handling strategy did you adopt?*  
**A:** Custom 404 and 500 error handlers render branded HTML pages that respect the global dark/light theme, improving user experience and masking stack traces.

**Q:** *Which security measures are in place?*  
**A:** Bcrypt for password hashing, server‑side input validation, secure file uploads with `secure_filename` and UUID prefixes, ORM queries preventing SQL injection, and role‑based route protection via Flask‑Login.

**Q:** *Why did you choose Plotly for analytics?*  
**A:** Plotly provides interactive, client‑side charts with minimal setup, allowing admins to explore complaint trends dynamically without heavy front‑end frameworks.

---

## 📢 3‑5 Minute Demo Speech

"I developed a **Digital Complaint Management System** using Flask to showcase a production‑ready full‑stack solution. Users can register, log in, and submit complaints with attachments, receiving a unique tracking ID to monitor progress. The admin panel offers a comprehensive dashboard with Plotly visualizations—showing status distribution, priority breakdown, and monthly trends—and the ability to filter, update, and export complaints. All data is stored in SQLite via SQLAlchemy, secured with Bcrypt‑hashed passwords and session‑based authentication.

The system also exposes RESTful APIs for external integration, complete with pagination and filtering, plus a `/health` endpoint for monitoring. A self‑hosted API docs page provides interactive reference. The UI is responsive, featuring a dark/light theme toggle and custom error pages for a polished user experience.

Overall, this project demonstrates solid backend architecture, secure authentication, data analytics, and a clean frontend—all packaged in a GitHub‑ready repository suitable for portfolio presentations and technical interviews."

---

*Feel free to clone the repo, run `seed_data.py` for demo data, and start the app with `python app.py`. Enjoy exploring!*
