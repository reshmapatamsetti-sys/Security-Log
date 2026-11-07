from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db
from modules.log_manager import LogManager
from modules.detection_engine import DetectionEngine

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        source_ip = request.remote_addr or '127.0.0.1'
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            # Log Successful Login
            LogManager.add_log(
                source_ip=source_ip,
                username=username,
                event_type="Successful Login",
                description=f"User '{username}' successfully logged into SecureLog dashboard.",
                severity="Informational"
            )
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.dashboard_view'))
        else:
            # Log Failed Login (Crucial for Brute-Force Detection testing!)
            LogManager.add_log(
                source_ip=source_ip,
                username=username if username else "unknown",
                event_type="Failed Login",
                description=f"Invalid credentials provided for user '{username}' from IP {source_ip}.",
                severity="Medium"
            )
            # Automatically run detection engine on failed login
            DetectionEngine.run_detections()
            
            flash("Invalid username or password.", "danger")
            
    return render_template('login.html', title="SecureLog - Login")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('auth.register'))
            
        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            flash("Username already exists.", "danger")
            return redirect(url_for('auth.register'))
            
        hashed_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'analyst')", (username, hashed_pw))
        db.commit()
        
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', title="SecureLog - Register")

@auth_bp.route('/logout')
def logout():
    username = session.get('username', 'system')
    source_ip = request.remote_addr or '127.0.0.1'
    LogManager.add_log(
        source_ip=source_ip,
        username=username,
        event_type="Logout",
        description=f"User '{username}' logged out of the system.",
        severity="Low"
    )
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))