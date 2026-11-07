from database.db import get_db

class AlertManager:
    @staticmethod
    def create_alert(timestamp, alert_type, source_ip, username, severity, description, detection_reason, related_log_id=None):
        db = get_db()
        db.execute(
            """
            INSERT INTO alerts (timestamp, alert_type, source_ip, username, severity, description, detection_reason, status, related_log_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Open', ?)
            """,
            (timestamp, alert_type, source_ip, username, severity, description, detection_reason, related_log_id)
        )
        db.commit()

    @staticmethod
    def get_alerts(status=None, severity=None):
        db = get_db()
        query = "SELECT * FROM alerts WHERE 1=1"
        params = []

        if status and status != 'All':
            query += " AND status = ?"
            params.append(status)

        if severity and severity != 'All':
            query += " AND severity = ?"
            params.append(severity)

        query += " ORDER BY timestamp DESC"
        cursor = db.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def update_alert_status(alert_id, new_status):
        db = get_db()
        db.execute(
            "UPDATE alerts SET status = ? WHERE id = ?",
            (new_status, alert_id)
        )
        db.commit()
        return True