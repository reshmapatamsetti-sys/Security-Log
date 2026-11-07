from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from modules.log_manager import LogManager
from routes.dashboard import login_required
from database.db import get_db

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs')
@login_required
def logs_view():
    return render_template('logs.html', title="SecureLog - Security Logs")

@logs_bp.route('/api/logs', methods=['GET'])
@login_required
def api_get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)
    event_type = request.args.get('event_type', 'All')
    severity = request.args.get('severity', 'All')
    search = request.args.get('search', '')
    
    result = LogManager.get_logs(page=page, per_page=per_page, event_type=event_type, severity=severity, search=search)
    return jsonify(result)

@logs_bp.route('/api/logs/import', methods=['POST'])
@login_required
def api_import_logs():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part in request."}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected."}), 400
        
    success, message = LogManager.import_csv(file)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

@logs_bp.route('/api/logs/clear', methods=['POST'])
@login_required
def api_clear_logs():
    db = get_db()
    db.execute("DELETE FROM security_logs")
    db.execute("DELETE FROM alerts")
    db.commit()
    return jsonify({"success": True, "message": "All security logs and alerts have been cleared."})