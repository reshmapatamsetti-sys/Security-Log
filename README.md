# SecureLog: Intelligent Security Log Monitoring and Threat Detection System

SecureLog is a SIEM-inspired (Security Information and Event Monitoring) cybersecurity application designed to collect, process, analyze, and visualize security telemetry. Built with Python, Flask, and SQLite, it features automated brute-force detection, IP risk analysis, alert lifecycle management, and a responsive Security Operations Center (SOC) dashboard.

---

## 1. Project Introduction & Problem Statement
Modern digital infrastructure generates millions of log events daily. Security teams struggle to manually sift through disparate logs to spot sophisticated threats such as brute-force attacks, credential stuffing, and unauthorized access attempts. 

SecureLog solves this by centralizing security log collection, applying rule-based anomaly detection in real time, and presenting actionable security intelligence through a professional SOC dashboard.

## 2. Project Objectives
- Provide a centralized platform for security event ingestion and monitoring.
- Automate the detection of repeated failed authentication attempts and brute-force attacks using configurable sliding time windows.
- Track network origin intelligence and classify IP risk levels.
- Manage security alerts through an incident lifecycle (*Open*, *Acknowledged*, *Resolved*).
- Demonstrate clean, modular, and maintainable software engineering principles suitable for technical interviews.

## 3. Key Features
- **User Authentication Portal:** Secure registration and login portal where authentication attempts (successful and failed) are recorded into security logs.
- **Security Log Management:** Paginated, searchable, and filterable log table with CSV import validation.
- **Automated Threat Detection Engine:** Scans logs for configurable thresholds (e.g., 5 failed logins within 5 minutes) and prevents duplicate active alerts.
- **IP Activity & Risk Analysis:** Aggregates event metrics per source IP address and applies heuristic risk scoring (*Normal*, *Suspicious*, *High Risk*).
- **Interactive SOC Dashboard:** Real-time statistics cards and live telemetry feeds.
- **Automated Testing:** Comprehensive `pytest` suite covering database initialization, log management, and detection rules.

## 4. Technology Stack
- **Backend:** Python 3, Flask, Flask Blueprints, Werkzeug (Password Hashing)
- **Database:** SQLite, Python `sqlite3` (with parameterized queries)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **Testing:** Pytest
- **Environment:** Visual Studio Code, Git, Python Virtual Environment (`venv`)

## 5. System Architecture & Folder Structure
SecureLog follows a modular MVC-inspired architecture:
```text
SecureLog/
│
├── app.py                      # Flask application factory and entry point
├── config.py                   # Application configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git exclusion rules
│
├── database/
│   ├── __init__.py             # Database package marker
│   ├── db.py                   # SQLite connection and initialization handlers
│   └── schema.sql              # Database tables and default seeding data
│
├── modules/
│   ├── __init__.py             # Modules package marker
│   ├── log_manager.py          # Log creation, querying, pagination, and CSV import
│   ├── detection_engine.py     # Rule-based threat detection and alert triggering
│   ├── alert_manager.py        # Alert lifecycle and status management
│   ├── ip_analyzer.py          # IP telemetry aggregation and risk scoring
│   └── data_generator.py       # Simulated sample data and brute-force injection
│
├── routes/
│   ├── __init__.py             # Routes package marker
│   ├── auth.py                 # Authentication, registration, and login telemetry
│   ├── dashboard.py            # Dashboard views and JSON statistics APIs
│   ├── logs.py                 # Log viewer and CSV import API endpoints
│   ├── alerts.py               # Alert management and status patching endpoints
│   └── analysis.py             # IP analysis views and manual detection triggers
│
├── templates/                  # HTML5 Jinja2 Templates
│   ├── base.html
│   ├── index.html
│   ├── logs.html
│   ├── alerts.html
│   ├── analysis.html
│   └── settings.html
│
├── static/                     # Frontend Assets
│   ├── css/
│   │   └── style.css           # Dark navy SOC theme stylesheet
│   └── js/
│       ├── dashboard.js
│       ├── logs.js
│       ├── alerts.js
│       └── analysis.js
│
└── tests/                      # Automated Test Suite
    ├── test_logs.py
    ├── test_detection.py
    └── test_alerts.py