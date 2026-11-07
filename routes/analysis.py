from flask import Blueprint, render_template, request, jsonify
from modules.ip_analyzer import IPAnalyzer
from modules.detection_engine import DetectionEngine
from routes.dashboard import login_required

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analysis')
@login_required
def analysis_view():
    return render_template('analysis.html', title="SecureLog - IP & Threat Analysis")

@analysis_bp.route('/api/ip-analysis', methods=['GET'])
@login_required
def api_ip_summaries():
    summaries = IPAnalyzer.get_ip_summaries()
    return jsonify(summaries)

@analysis_bp.route('/api/ip-analysis/<path:source_ip>', methods=['GET'])
@login_required
def api_ip_details(source_ip):
    details = IPAnalyzer.get_ip_details(source_ip)
    return jsonify(details)

@analysis_bp.route('/api/detections/run', methods=['POST'])
@login_required
def api_run_detections():
    result_msg = DetectionEngine.run_detections()
    return jsonify({"success": True, "message": result_msg})