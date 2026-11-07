from flask import Blueprint, render_template, request, jsonify
from modules.alert_manager import AlertManager
from routes.dashboard import login_required

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/alerts')
@login_required
def alerts_view():
    return render_template('alerts.html', title="SecureLog - Security Alerts")

@alerts_bp.route('/api/alerts', methods=['GET'])
@login_required
def api_get_alerts():
    status = request.args.get('status', 'All')
    severity = request.args.get('severity', 'All')
    alerts = AlertManager.get_alerts(status=status, severity=severity)
    return jsonify(alerts)

@alerts_bp.route('/api/alerts/<int:alert_id>/status', methods=['PATCH'])
@login_required
def api_update_alert_status(alert_id):
    data = request.get_json()
    new_status = data.get('status')
    if new_status not in ['Open', 'Acknowledged', 'Resolved']:
        return jsonify({"success": False, "message": "Invalid status value."}), 400
        
    AlertManager.update_alert_status(alert_id, new_status)
    return jsonify({"success": True, "message": f"Alert {alert_id} updated to {new_status}."})