-- SecureLog Database Schema

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS security_logs;
DROP TABLE IF EXISTS alerts;
DROP TABLE IF EXISTS detection_rules;
DROP TABLE IF EXISTS system_settings;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'analyst',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE security_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    source_ip TEXT NOT NULL,
    username TEXT NOT NULL,
    event_type TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT DEFAULT 'Unreviewed'
);

CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    source_ip TEXT NOT NULL,
    username TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    detection_reason TEXT NOT NULL,
    status TEXT DEFAULT 'Open',
    related_log_id INTEGER,
    FOREIGN KEY (related_log_id) REFERENCES security_logs (id)
);

CREATE TABLE detection_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    threshold INTEGER NOT NULL,
    time_window INTEGER NOT NULL, -- in minutes
    severity TEXT NOT NULL,
    enabled BOOLEAN DEFAULT 1
);

CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_name TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL
);

-- Insert Default Detection Rules
INSERT INTO detection_rules (rule_name, description, threshold, time_window, severity, enabled)
VALUES 
('Brute Force Detection', 'Multiple failed login attempts from same user/IP within time window', 5, 5, 'High', 1),
('Suspicious After-Hours Access', 'Login activity detected outside standard operational hours', 1, 1, 'Medium', 1),
('Multiple Account Lockouts', 'Repeated account lockouts originating from the same source IP', 3, 10, 'Critical', 1);

-- Insert Default System Settings
INSERT INTO system_settings (setting_name, setting_value)
VALUES 
('auto_refresh_interval', '15'),
('log_retention_days', '30'),
('alert_email_notifications', 'disabled');

-- Insert Default Admin User (Password: admin123 - hashed using Werkzeug)
-- Hash generated for 'admin123': scrypt:32768:8:1$K... (handled in code or seeded securely)