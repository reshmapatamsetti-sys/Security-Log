import pytest
from app import create_app
from database.db import init_db
from modules.log_manager import LogManager
from modules.detection_engine import DetectionEngine
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

def test_failed_login_brute_force_detection(app):
    with app.app_context():
        # Inject 5 failed logins within threshold window for the same IP and user
        ip = "192.168.1.200"
        user = "admin"
        for _ in range(5):
            LogManager.add_log(
                source_ip=ip,
                username=user,
                event_type="Failed Login",
                description="Invalid password",
                severity="Medium"
            )

        # Run detection engine
        DetectionEngine.run_detections()

        # Verify an alert was generated
        alerts = AlertManager.get_alerts(status="Open")
        assert len(alerts) == 1
        assert alerts[0]['alert_type'] == 'Brute Force Detection'
        assert alerts[0]['source_ip'] == ip
        assert alerts[0]['username'] == user

        # Run detection engine again to test duplicate alert prevention
        DetectionEngine.run_detections()
        alerts_after_second_run = AlertManager.get_alerts(status="Open")
        assert len(alerts_after_second_run) == 1  # No duplicate alert should be created