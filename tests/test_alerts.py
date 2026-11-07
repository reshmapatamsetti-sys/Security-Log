import pytest
from app import create_app
from database.db import init_db
from modules.alert_manager import AlertManager

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': ':memory:'
    })
    with app.app_context():
        init_db()
        yield app

def test_alert_status_update(app):
    with app.app_context():
        # Create an alert manually
        AlertManager.create_alert(
            timestamp="2026-03-30 12:00:00",
            alert_type="Brute Force Detection",
            source_ip="10.0.0.99",
            username="root",
            severity="High",
            description="Test alert description",
            detection_reason="Threshold exceeded"
        )

        alerts = AlertManager.get_alerts(status="Open")
        assert len(alerts) == 1
        alert_id = alerts[0]['id']
        assert alerts[0]['status'] == "Open"

        # Update alert status to Acknowledged
        AlertManager.update_alert_status(alert_id, "Acknowledged")
        
        updated_alerts = AlertManager.get_alerts(status="Acknowledged")
        assert len(updated_alerts) == 1
        assert updated_alerts[0]['id'] == alert_id
        assert updated_alerts[0]['status'] == "Acknowledged"