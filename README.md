# 🗂️ Taskora

A full-featured **Task Management Web Application** built with **Flask**, **MySQL**, and **JWT Authentication**, featuring RESTful APIs, user authentication, and a clean front-end interface.  
This project demonstrates strong backend design, secure API development, frontend integration, and comprehensive testing coverage.

---

## 🚀 Features

### 🔐 Authentication
- User registration and login with secure password hashing.
- JWT-based authentication (Access + Refresh tokens).
- Auto token refresh and logout token blacklisting.

### ✅ Task Management
- Add, view, update, and delete personal tasks.
- Mark tasks as done or pending.
- Fully authenticated API endpoints.
- Paginated and structured API responses.

### 🧠 Technical Highlights
- Modular Flask project structure (Blueprints, Models, Routes, Services).
- Full **Test Suite** using `pytest` and `pytest-cov`.
- Custom **error handling** and structured JSON responses.
- Integrated **frontend JavaScript** for real-time API interactions.
- Configurable environments (Development, Testing, Production).

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend Framework | Flask |
| Database | MySQL |
| ORM | SQLAlchemy |
| Authentication | Flask-JWT-Extended |
| Testing | pytest, pytest-cov |
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Deployment | Azure (WSGI-based) |

---

## 📁 Project Structure

```
Task-Manager/
    ├── README.md
    ├── Procfile
    ├── .gitignore
    ├── requirements.txt
    ├── run.py
    ├── app/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── extensions.py
    │   ├── models.py
    │   ├── utils.py
    │   ├── auth/
    │   │   ├── __init__.py
    │   │   ├── api_routes.py
    │   │   ├── routes.py
    │   │   └── templates/
    │   │       ├── login.html
    │   │       └── register.html
    │   ├── dashboard/
    │   │   ├── __init__.py
    │   │   ├── api_routes.py
    │   │   ├── routes.py
    │   │   └── templates/
    │   │       └── tasks.html
    │   ├── home/
    │   │   ├── __init__.py
    │   │   ├── routes.py
    │   │   └── templates/
    │   │       └── home.html
    │   ├── static/
    │   │   ├── css/
    │   │   │   └── style.css
    │   │   └── js/
    │   │       ├── base.js
    │   │       ├── login.js
    │   │       ├── register.js
    │   │       └── tasks.js
    │   └── templates/
    │       ├── 404.html
    │       ├── 500.html
    │       └── base.html
    └── tests/
        ├── conftest.py
        ├── test_apis/
        │   ├── test_login_apis.py
        │   ├── test_logout_apis.py
        │   ├── test_refresh_apis.py
        │   ├── test_register_apis.py
        │   └── test_tasks_apis.py
        ├── test_models/
        │   ├── test_blacklistedtoken_model.py
        │   ├── test_task_model.py
        │   └── test_user_model.py
        └── test_routes/
            ├── test_home.py
            ├── test_login.py
            ├── test_register.py
            └── test_tasks.py
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Bharat-Panchal-3578/flask-To-Do-App.git
cd flask-To-Do-App
```

### 2. Create Virtual Environment
```bash
python -m venv env
env\Scripts\activate # (On linux/Mac) source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
- Create a MySQL database (e.g. `task_manager_db`)
- Update credentials in your environment variables or config file.

### 5. Apply Migrations
```bash
flask db upgrade
```

### 6. Run the Application
```bash
python run.py   
```
> App will run at: [https://flask-to-do-app-aufe.onrender.com/](https://flask-to-do-app-aufe.onrender.com/)
*(The demo may not function fully due to an expired database connection.)*

---

## 🧪 Running Tests

Run the entire test suite:
```bash
python -m pytest
```

Run with coverage report:
```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

## 🧰 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|-----------|--------------|----------------|
| `POST` | `/api/register` | Register a new user | ❌ |
| `POST` | `/api/login` | Login user & get tokens | ❌ |
| `POST` | `/api/refresh` | Refresh access token | ✅ (Refresh token) |
| `POST` | `/api/logout` | Blacklist refresh token | ✅ |
| `GET` | `/dashboard/api/tasks` | Fetch all tasks | ✅ |
| `POST` | `/dashboard/api/tasks` | Create a task | ✅ |
| `PUT` | `/dashboard/api/tasks/<id>` | Update a task | ✅ |
| `DELETE` | `/dashboard/api/tasks/<id>` | Delete a task | ✅ |

---

## 🧭 Frontend Overview

- **`base.js`** — Manages logout and token refresh globally.
- **`login.js`** — Handles user login and token storage.
- **`tasks.js`** — Handles all task CRUD operations via authenticated API calls.
- **`HTML Templates`** — Extend from `base.html` with modular structure for `home`, `auth`, and `dashboard`.

---

## 🧱 Testing Highlights

- 100% coverage for core models and routes.
- Mocked database setup via `pytest` fixtures.
- Includes model, route, and API endpoint tests.
- Separate test configuration using `TestingConfig`.

---

## 🧩 Future Enhancements

- Add visual analytics (graphs/charts) to show task completion trends over time.
- Implement dark mode for UI customization.
- Add a complete user dashboard for editing and viewing profile.
- Email verification & password reset flow.

---

## 📦 Deployment

Deployment-ready for platforms like:
- **Azure**
- **Render**
- **Railway**
- **Heroku (via Gunicorn)**
- or any **WSGI-compatible host**

Ensure to:
1. Set environment variable `FLASK_CONFIG=app.config.ProductionConfig`
2. Update your MySQL connection URI.
3. Add `.env` for secret keys and credentials.

---

## 👨‍💻 Author

**Bharat Panchal**  
Python Web Developer Learner  
[GitHub Profile](https://github.com/Bharat-Panchal15) · [LinkedIn](www.linkedin.com/in/bharat-panchal-585b35309)  

---

## 🪪 License

This project is licensed under the **MIT License** — feel free to use and modify it for learning or production.
