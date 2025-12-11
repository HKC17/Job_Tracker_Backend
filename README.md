# Job Application Tracker - Backend API

A comprehensive REST API for tracking job applications with analytics, machine learning capabilities, and automated insights. Built with Django, MongoDB, and designed for scalability.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-4.2.7-green)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-brightgreen)
![DRF](https://img.shields.io/badge/DRF-3.14.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Data Seeding](#-data-seeding)
- [Export Features](#-export-features)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Features

### ✅ Core Features

- **User Authentication** - JWT-based authentication with refresh tokens
- **Job Application Tracking** - Complete CRUD operations for job applications
- **Company Management** - Track and manage company information
- **Timeline Tracking** - Record interview stages, phone screens, and events
- **File Uploads** - Upload resumes, offer letters, and attachments
- **Status Management** - Track application status with automatic timeline updates
- **Search & Filters** - Powerful search with multiple filter options

### 📊 Analytics & Insights

- **Dashboard Statistics** - Success rate, response rate, applications over time
- **Skills Demand Analysis** - Identify most requested skills
- **Success Rate Trends** - Track success rate over time
- **Salary Insights** - Average, min, max salary analysis
- **Response Time Analysis** - Company response time metrics
- **Company Statistics** - Applications per company, industry breakdown

### 📥 Export Features

- **CSV Export** - Applications, companies, and analytics data
- **PDF Reports** - Professional PDF reports with statistics
- **Filtered Exports** - Export specific data based on filters

### 🔧 Developer Features

- **Interactive API Documentation** - Swagger UI and ReDoc
- **OpenAPI Schema** - Complete API specification
- **Comprehensive Testing** - Test scripts for all endpoints
- **Data Seeding** - Generate sample data for testing
- **RESTful Design** - Clean, intuitive API endpoints

---

## 🛠️ Tech Stack

### Backend Framework

- **Django 4.2.7** - Web framework
- **Django REST Framework 3.14** - REST API toolkit
- **drf-spectacular** - OpenAPI schema generation

### Databases

- **MongoDB 6.0+** - Document database for applications and companies
- **SQLite** - Relational database for user authentication

### Authentication

- **djangorestframework-simplejwt** - JWT authentication
- **JWT tokens** - Access & refresh token mechanism

### Additional Libraries

- **PyMongo 4.6.1** - MongoDB driver
- **ReportLab** - PDF generation
- **Pillow** - Image processing
- **django-cors-headers** - CORS support
- **django-filter** - Advanced filtering

---

## 🏗️ Architecture

### Hybrid Database Architecture

```
┌─────────────────────────────────────────┐
│         Django (Users App)              │
│  - Authentication & Authorization       │
│  - User Profile Management              │
│  - Django ORM + SQLite                  │
│  - Admin Panel                          │
└─────────────────┬───────────────────────┘
                  │
                  │ JWT Authentication
                  │
┌─────────────────▼───────────────────────┐
│   MongoDB (Applications & Companies)    │
│  - Job Applications (Flexible Schema)   │
│  - Company Information                  │
│  - PyMongo (Direct MongoDB Access)      │
│  - Aggregation Pipelines               │
└─────────────────────────────────────────┘
```

### Why Hybrid?

- **SQLite** handles user authentication perfectly (Django's strength)
- **MongoDB** provides flexibility for application data (document-based, ML-ready)
- **Best of both worlds** - Security + Flexibility

### Key Design Patterns

- **Service Layer** - Business logic separated from views
- **Denormalization** - Company data embedded for performance
- **Document-Oriented** - Nested structures (company, job, timeline)
- **Polyglot Persistence** - Right database for the right job

---

## 📦 Prerequisites

- **Python 3.12+**
- **MongoDB 6.0+**
- **pip** (Python package manager)
- **Virtual environment** (recommended)

### Install MongoDB

**Windows:**

```bash
# Download from: https://www.mongodb.com/try/download/community
# Or use Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**macOS:**

```bash
brew tap mongodb/brew
brew install mongodb-community@6.0
brew services start mongodb-community@6.0
```

**Linux:**

```bash
# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/job-tracker-backend.git
cd job-tracker-backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Environment Variables

Create `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

MONGO_DB_NAME=job_tracker
MONGO_HOST=localhost
MONGO_PORT=27017

JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

---

## ▶️ Running the Application

### Start MongoDB

```bash
# If not already running
mongod --dbpath /path/to/data
```

### Start Django Development Server

```bash
python manage.py runserver
```

The API will be available at: **http://127.0.0.1:8000/**

---

## 📚 API Documentation

### Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

### Authentication

1. Register or login to get JWT tokens
2. Click "Authorize" in Swagger UI
3. Enter: `Bearer YOUR_ACCESS_TOKEN`
4. Test any endpoint!

---

## 📁 Project Structure

```
job_tracker_backend/
├── config/                      # Django configuration
│   ├── settings.py             # Main settings
│   ├── urls.py                 # URL routing
│   └── mongodb.py              # MongoDB connection
│
├── apps/                        # Django applications
│   ├── users/                  # User authentication
│   │   ├── models.py           # User model (Django ORM)
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API views
│   │   └── urls.py             # URL patterns
│   │
│   ├── applications/           # Job applications
│   │   ├── services.py         # Business logic
│   │   ├── serializers.py      # Data validation
│   │   ├── views.py            # API endpoints
│   │   ├── file_service.py     # File upload logic
│   │   └── urls.py             # URL patterns
│   │
│   ├── companies/              # Company management
│   │   ├── services.py         # Business logic
│   │   ├── serializers.py      # Data validation
│   │   ├── views.py            # API endpoints
│   │   └── urls.py             # URL patterns
│   │
│   └── analytics/              # Analytics & insights
│       ├── services.py         # Analytics calculations
│       ├── export_service.py   # CSV/PDF export
│       ├── views.py            # API endpoints
│       └── urls.py             # URL patterns
│
├── media/                       # User uploads
│   └── uploads/                # Organized by user
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── seed_data.py                 # Data seeding script
├── test_*.py                    # Test scripts
├── SCHEMAS.md                   # Database schema docs
└── README.md                    # This file
```

---

## 🔌 API Endpoints

### Authentication (`/api/auth/`)

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| POST   | `/register/`        | Register new user         |
| POST   | `/login/`           | Login and get JWT tokens  |
| POST   | `/refresh/`         | Refresh access token      |
| POST   | `/logout/`          | Logout (blacklist token)  |
| GET    | `/user/`            | Get current user profile  |
| PUT    | `/user/`            | Update user profile       |
| POST   | `/change-password/` | Change password           |
| POST   | `/skills/add/`      | Add skill to profile      |
| POST   | `/skills/remove/`   | Remove skill from profile |
| GET    | `/stats/`           | Get user statistics       |

### Applications (`/api/applications/`)

| Method | Endpoint                     | Description             |
| ------ | ---------------------------- | ----------------------- |
| GET    | `/`                          | List all applications   |
| POST   | `/`                          | Create new application  |
| GET    | `/{id}/`                     | Get application details |
| PUT    | `/{id}/`                     | Update application      |
| DELETE | `/{id}/`                     | Delete application      |
| POST   | `/{id}/timeline/`            | Add timeline event      |
| PATCH  | `/{id}/status/`              | Update status           |
| POST   | `/{id}/attach/`              | Attach file             |
| DELETE | `/{id}/attachments/{index}/` | Delete attachment       |
| GET    | `/stats/`                    | Get statistics          |
| GET    | `/search/?q=term`            | Search applications     |
| POST   | `/upload/`                   | Upload file             |
| POST   | `/upload-resume/`            | Upload resume           |

### Companies (`/api/companies/`)

| Method | Endpoint                  | Description                |
| ------ | ------------------------- | -------------------------- |
| GET    | `/`                       | List all companies         |
| POST   | `/`                       | Create new company         |
| GET    | `/{id}/`                  | Get company details        |
| PUT    | `/{id}/`                  | Update company             |
| DELETE | `/{id}/`                  | Delete company             |
| GET    | `/{id}/applications/`     | Get company applications   |
| GET    | `/{id}/stats/`            | Get company statistics     |
| GET    | `/search/?q=term`         | Search companies           |
| GET    | `/autocomplete/?q=prefix` | Autocomplete company names |
| POST   | `/sync/`                  | Sync from applications     |
| GET    | `/industry-breakdown/`    | Industry breakdown         |
| GET    | `/top/`                   | Top companies by apps      |

### Analytics (`/api/analytics/`)

| Method | Endpoint                    | Description               |
| ------ | --------------------------- | ------------------------- |
| GET    | `/dashboard/`               | Dashboard statistics      |
| GET    | `/applications-over-time/`  | Applications timeline     |
| GET    | `/success-rate/`            | Success rate over time    |
| GET    | `/skills/`                  | Skills demand analysis    |
| GET    | `/timeline/`                | Interview stages analysis |
| GET    | `/salary/`                  | Salary insights           |
| GET    | `/response-time/`           | Response time analysis    |
| GET    | `/export/applications/csv/` | Export apps to CSV        |
| GET    | `/export/applications/pdf/` | Export apps to PDF        |
| GET    | `/export/analytics/csv/`    | Export analytics CSV      |
| GET    | `/export/companies/csv/`    | Export companies CSV      |

---

## 🗄️ Database Schema

### MongoDB Collections

#### Applications Collection

```javascript
{
  _id: ObjectId,
  user_id: Integer,
  company: {
    name: String,
    website: String,
    industry: String,
    size: String,
    location: String
  },
  job: {
    title: String,
    description: String,
    employment_type: String,
    work_mode: String,
    salary_min: Number,
    salary_max: Number
  },
  application: {
    applied_date: Date,
    source: String,
    status: String,
    resume_version: String
  },
  requirements: {
    skills_required: [String],
    skills_preferred: [String],
    years_experience: Number
  },
  timeline: [
    {
      date: Date,
      event_type: String,
      title: String,
      notes: String
    }
  ],
  attachments: [...],
  notes: String,
  is_favorite: Boolean,
  created_at: Date,
  updated_at: Date
}
```

See [SCHEMAS.md](SCHEMAS.md) for complete schema documentation.

---

## 🧪 Testing

### Run Test Scripts

```bash
# Test user authentication
python test_applications.py

# Test companies
python test_companies.py

# Test analytics
python test_analytics.py

# Test file upload
python test_file_upload.py

# Test export features
python test_export.py
```

### Using Swagger UI

1. Go to http://127.0.0.1:8000/api/docs/
2. Click "Authorize"
3. Login to get token
4. Paste token with `Bearer ` prefix
5. Test any endpoint interactively!

### Manual Testing with cURL

```bash
# Register user
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass123!","password_confirm":"Pass123!","first_name":"John","last_name":"Doe"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass123!"}'

# Get applications (with token)
curl -X GET http://127.0.0.1:8000/api/applications/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🌱 Data Seeding

Generate sample data for testing and development:

```bash
python seed_data.py
```

This will:

- Create a demo user (`demo@example.com` / `DemoPass123!`)
- Generate 50+ realistic job applications
- Create applications spread over 90 days
- Include various statuses, companies, and timelines
- Add skills, salaries, and interview events

**Customize seeding:**

```bash
# When prompted, enter number of applications
How many applications to create? (default 50): 100
```

---

## 📤 Export Features

### Export to CSV

```bash
# Applications
GET /api/analytics/export/applications/csv/

# With filters
GET /api/analytics/export/applications/csv/?status=interview

# Companies
GET /api/analytics/export/companies/csv/

# Analytics data
GET /api/analytics/export/analytics/csv/
```

### Export to PDF

```bash
# Professional PDF report
GET /api/analytics/export/applications/pdf/

# Includes:
# - Summary statistics
# - Applications list
# - Charts and visualizations
```

### Programmatic Export

```python
import requests

response = requests.get(
    'http://127.0.0.1:8000/api/analytics/export/applications/csv/',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)

with open('applications.csv', 'wb') as f:
    f.write(response.content)
```

---

## 🔮 Future Roadmap (Phase 2: ML & Automation)

### Planned Features

#### 🤖 Machine Learning

- [ ] Job recommendation engine
- [ ] Success probability prediction
- [ ] Salary estimation model
- [ ] Skills gap analysis
- [ ] Interview success prediction
- [ ] Automated insights generation

#### 🕷️ Web Scraping

- [ ] LinkedIn job scraping
- [ ] Indeed integration
- [ ] Company website scraping
- [ ] Auto-populate applications
- [ ] Salary data aggregation

#### 🚀 Automation

- [ ] Auto-apply to jobs (with caution)
- [ ] Resume optimization suggestions
- [ ] Cover letter generation (AI)
- [ ] Interview preparation tips
- [ ] Follow-up reminders
- [ ] Application deadline tracking

#### 📊 Advanced Analytics

- [ ] Predictive analytics dashboard
- [ ] Market trend analysis
- [ ] Skill demand forecasting
- [ ] Company culture insights
- [ ] Interview difficulty ratings

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Keep commits atomic and descriptive

---

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- REST API powered by [Django REST Framework](https://www.django-rest-framework.org/)
- Documentation with [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- Database by [MongoDB](https://www.mongodb.com/)

---
