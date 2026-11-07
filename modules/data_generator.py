import random
from datetime import datetime, timedelta
from database.db import get_db

class DataGenerator:
    IP_POOL = [
        "192.168.1.10", "192.168.1.15", "192.168.1.45", 
        "10.0.0.5", "10.0.0.22", "172.16.0.8", 
        "203.0.113.42", "198.51.100.14" # Suspicious external IPs
    ]
    
    USERS = ["jdoe", "asmith", "root", "admin", "bwayne", "ckent", "test_user"]
    
    EVENT_TYPES = [
        "Successful Login", "Failed Login", "Logout", 
        "Password Change", "Account Lockout", "Suspicious Activity", 
        "Unauthorized Access Attempt (simulated)", "System Activity"
    ]

    @staticmethod
    def seed_database(num_logs=50):
        db = get_db()
        
        # Check if logs already exist
        count = db.execute("SELECT COUNT(*) FROM security_logs").fetchone()[0]
        if count > 0:
            return "Database already contains logs. Clear or reset to regenerate."

        base_time = datetime.now() - timedelta(hours=2)
        
        # 1. Inject a specific Brute-Force attack pattern (5 failed logins within 5 minutes)
        attack_ip = "203.0.113.42"
        attack_user = "admin"
        for i in range(5):
            log_time = base_time + timedelta(seconds=i * 30) # 30 seconds apart
            db.execute(
                """
                INSERT INTO security_logs (timestamp, source_ip, username, event_type, description, severity, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    log_time.strftime('%Y-%m-%d %H:%M:%S'),
                    attack_ip,
                    attack_user,
                    "Failed Login",
                    f"Invalid password provided for user '{attack_user}' from IP {attack_ip}",
                    "High",
                    "Unreviewed"
                )
            )

        # 2. Inject general background logs
        for i in range(num_logs - 5):
            log_time = base_time + timedelta(minutes=random.randint(5, 120))
            ip = random.choice(DataGenerator.IP_POOL)
            user = random.choice(DataGenerator.USERS)
            event_type = random.choice(DataGenerator.EVENT_TYPES)
            
            # Assign appropriate severity and description
            if event_type == "Failed Login":
                severity = "Medium"
                desc = f"Failed authentication attempt for {user} from {ip}"
            elif event_type == "Account Lockout":
                severity = "High"
                desc = f"Account locked due to multiple failures: {user}"
            elif event_type == "Unauthorized Access Attempt (simulated)":
                severity = "Critical"
                desc = f"Unauthorized endpoint probe detected from {ip}"
            elif event_type == "Successful Login":
                severity = "Informational"
                desc = f"User {user} successfully authenticated from {ip}"
            else:
                severity = "Low"
                desc = f"Standard system operation event recorded for {user}"

            db.execute(
                """
                INSERT INTO security_logs (timestamp, source_ip, username, event_type, description, severity, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (log_time.strftime('%Y-%m-%d %H:%M:%S'), ip, user, event_type, desc, severity, "Unreviewed")
            )

        db.commit()
        return f"Successfully generated {num_logs} sample security logs, including a brute-force simulation."

    @staticmethod
    def reset_database():
        db = get_db()
        db.execute("DELETE FROM security_logs")
        db.execute("DELETE FROM alerts")
        db.commit()
        return DataGenerator.seed_database(50)