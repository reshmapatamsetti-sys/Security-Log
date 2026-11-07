from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from database.db import get_db
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/')
@login_required
def dashboard_view():
    return render_template('index.html', title="SecureLog - SOC Dashboard")

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_dashboard_stats():
    db = get_db()
    
    total_events = db.execute("SELECT COUNT(*) FROM security_logs").fetchone()[0]
    successful_logins = db.execute("SELECT COUNT(*) FROM security_logs WHERE event_type = 'Successful Login'").fetchone()[0]
    failed_logins = db.execute("SELECT COUNT(*) FROM security_logs WHERE event_type = 'Failed Login'").fetchone()[0]
    active_alerts = db.execute("SELECT COUNT(*) FROM alerts WHERE status = 'Open'").fetchone()[0]
    critical_alerts = db.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'Critical' AND status = 'Open'").fetchone()[0]
    unique_ips = db.execute("SELECT COUNT(DISTINCT source_ip) FROM security_logs").fetchone()[0]
    
    return jsonify({
        "total_events": total_events,
        "successful_logins": successful_logins,
        "failed_logins": failed_logins,
        "active_alerts": active_alerts,
        "critical_alerts": critical_alerts,
        "unique_ips": unique_ips
    })

@dashboard_bp.route('/api/dashboard/charts', methods=['GET'])
@login_required
def get_dashboard_charts():
    db = get_db()
    
    # Severity distribution
    sev_cursor = db.execute("SELECT severity, COUNT(*) as count FROM security_logs GROUP BY severity")
    severity_data = {row['severity']: row['count'] for row in sev_cursor.fetchall()}
    
    # Event type distribution
    type_cursor = db.execute("SELECT event_type, COUNT(*) as count FROM security_logs GROUP BY event_type")
    event_type_data = {row['event_type']: row['count'] for row in type_cursor.fetchall()}
    
    # Top 5 IP addresses
    ip_cursor = db.execute("SELECT source_ip, COUNT(*) as count FROM security_logs GROUP BY source_ip ORDER BY count DESC LIMIT 5")
    top_ips = [{"source_ip": row['source_ip'], "count": row['count']} for row in ip_cursor.fetchall()]
    
    return jsonify({
        "severity_distribution": severity_data,
        "event_type_distribution": event_type_data,
        "top_ips": top_ips
    })