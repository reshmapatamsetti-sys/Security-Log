from database.db import get_db

class IPAnalyzer:
    @staticmethod
    def get_ip_summaries():
        db = get_db()
        # Aggregate statistics per source IP address
        query = """
            SELECT 
                source_ip,
                COUNT(*) as total_events,
                SUM(CASE WHEN event_type = 'Failed Login' THEN 1 ELSE 0 END) as failed_logins,
                COUNT(DISTINCT username) as distinct_users,
                MAX(timestamp) as last_seen
            FROM security_logs
            GROUP BY source_ip
            ORDER BY failed_logins DESC, total_events DESC
        """
        cursor = db.execute(query)
        ips = [dict(row) for row in cursor.fetchall()]
        
        # Enrich IPs with risk classification heuristics
        analyzed_ips = []
        for ip in ips:
            risk_level = "Normal"
            if ip['failed_logins'] >= 5 or ip['distinct_users'] > 2:
                risk_level = "Suspicious"
            if ip['failed_logins'] >= 10:
                risk_level = "High Risk"
            
            ip['risk_level'] = risk_level
            analyzed_ips.append(ip)
            
        return analyzed_ips

    @staticmethod
    def get_ip_details(source_ip):
        db = get_db()
        cursor = db.execute(
            """
            SELECT * FROM security_logs 
            WHERE source_ip = ? 
            ORDER BY timestamp DESC
            """,
            (source_ip,)
        )
        logs = [dict(row) for row in cursor.fetchall()]
        
        # Retrieve security alerts associated with this IP
        alert_cursor = db.execute(
            """
            SELECT * FROM alerts 
            WHERE source_ip = ? 
            ORDER BY timestamp DESC
            """,
            (source_ip,)
        )
        alerts = [dict(row) for row in alert_cursor.fetchall()]
        
        return {
            "source_ip": source_ip,
            "logs": logs,
            "alerts": alerts,
            "total_events": len(logs),
            "total_alerts": len(alerts)
        }