from database.db import get_db
import csv
import io
from datetime import datetime

class LogManager:
    @staticmethod
    def add_log(source_ip, username, event_type, description, severity, status="Unreviewed", timestamp=None):
        db = get_db()
        if not timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        db.execute(
            """
            INSERT INTO security_logs (timestamp, source_ip, username, event_type, description, severity, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (timestamp, source_ip, username, event_type, description, severity, status)
        )
        db.commit()
        return db.execute("SELECT last_insert_rowid()").fetchone()[0]

    @staticmethod
    def get_logs(page=1, per_page=15, event_type=None, severity=None, search=None):
        db = get_db()
        query = "SELECT * FROM security_logs WHERE 1=1"
        params = []

        if event_type and event_type != 'All':
            query += " AND event_type = ?"
            params.append(event_type)

        if severity and severity != 'All':
            query += " AND severity = ?"
            params.append(severity)

        if search:
            query += " AND (username LIKE ? OR source_ip LIKE ? OR description LIKE ?)"
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])

        # Get total count for pagination
        count_query = f"SELECT COUNT(*) FROM ({query})"
        total_count = db.execute(count_query, params).fetchone()[0]

        # Add sorting and pagination
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        offset = (page - 1) * per_page
        params.extend([per_page, offset])

        cursor = db.execute(query, params)
        logs = [dict(row) for row in cursor.fetchall()]

        return {
            "logs": logs,
            "total": total_count,
            "page": page,
            "per_page": per_page,
            "total_pages": (total_count + per_page - 1) // per_page if total_count > 0 else 1
        }

    @staticmethod
    def import_csv(file_storage):
        try:
            stream = io.TextIOWrapper(file_storage.stream, encoding="utf-8")
            reader = csv.DictReader(stream)
            imported_count = 0
            
            for row in reader:
                LogManager.add_log(
                    source_ip=row.get('source_ip', '127.0.0.1'),
                    username=row.get('username', 'system'),
                    event_type=row.get('event_type', 'System Activity'),
                    description=row.get('description', 'Imported log event'),
                    severity=row.get('severity', 'Low'),
                    status=row.get('status', 'Unreviewed'),
                    timestamp=row.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                )
                imported_count += 1
            return True, f"Successfully imported {imported_count} logs."
        except Exception as e:
            return False, str(e)