from datetime import datetime, timedelta
from database.db import get_db
from modules.alert_manager import AlertManager

class DetectionEngine:
    @staticmethod
    def get_active_rules():
        db = get_db()
        cursor = db.execute("SELECT * FROM detection_rules WHERE enabled = 1")
        return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def run_detections():
        db = get_db()
        rules = DetectionEngine.get_active_rules()
        alerts_generated = 0

        for rule in rules:
            rule_name = rule['rule_name']
            threshold = rule['threshold']
            time_window_mins = rule['time_window']
            severity = rule['severity']
            
            cutoff_time = datetime.now() - timedelta(minutes=time_window_mins)
            cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')

            if rule_name == 'Brute Force Detection':
                # Query failed logins within the time window grouped by IP and username
                cursor = db.execute(
                    """
                    SELECT source_ip, username, COUNT(*) as failure_count, MAX(id) as latest_log_id
                    FROM security_logs
                    WHERE event_type = 'Failed Login' AND timestamp >= ?
                    GROUP BY source_ip, username
                    HAVING failure_count >= ?
                    """,
                    (cutoff_str, threshold)
                )
                suspicious_groups = cursor.fetchall()

                for row in suspicious_groups:
                    source_ip = row['source_ip']
                    username = row['username']
                    failure_count = row['failure_count']
                    latest_log_id = row['latest_log_id']

                    reason = f"Detected {failure_count} failed login attempts for user '{username}' from IP {source_ip} within {time_window_mins} minutes (Threshold: {threshold})."
                    description = f"Potential brute-force attack targeting account '{username}'."

                    # Check if an alert for this specific IP/username/rule combination already exists and is Open
                    existing = db.execute(
                        """
                        SELECT id FROM alerts 
                        WHERE alert_type = ? AND source_ip = ? AND username = ? AND status = 'Open'
                        """,
                        (rule_name, source_ip, username)
                    ).fetchone()

                    if not existing:
                        AlertManager.create_alert(
                            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            alert_type=rule_name,
                            source_ip=source_ip,
                            username=username,
                            severity=severity,
                            description=description,
                            detection_reason=reason,
                            related_log_id=latest_log_id
                        )
                        alerts_generated += 1

            elif rule_name == 'Multiple Account Lockouts':
                cursor = db.execute(
                    """
                    SELECT source_ip, username, COUNT(*) as lockout_count, MAX(id) as latest_log_id
                    FROM security_logs
                    WHERE event_type = 'Account Lockout' AND timestamp >= ?
                    GROUP BY source_ip, username
                    HAVING lockout_count >= ?
                    """,
                    (cutoff_str, threshold)
                )
                lockout_groups = cursor.fetchall()

                for row in lockout_groups:
                    source_ip = row['source_ip']
                    username = row['username']
                    lockout_count = row['lockout_count']
                    latest_log_id = row['latest_log_id']

                    reason = f"Detected {lockout_count} account lockouts for user '{username}' from IP {source_ip} within {time_window_mins} minutes."
                    description = f"Repeated lockouts indicating aggressive credential stuffing from {source_ip}."

                    existing = db.execute(
                        """
                        SELECT id FROM alerts 
                        WHERE alert_type = ? AND source_ip = ? AND username = ? AND status = 'Open'
                        """,
                        (rule_name, source_ip, username)
                    ).fetchone()

                    if not existing:
                        AlertManager.create_alert(
                            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            alert_type=rule_name,
                            source_ip=source_ip,
                            username=username,
                            severity=severity,
                            description=description,
                            detection_reason=reason,
                            related_log_id=latest_log_id
                        )
                        alerts_generated += 1

        return f"Detection engine ran successfully. Generated {alerts_generated} new alerts."