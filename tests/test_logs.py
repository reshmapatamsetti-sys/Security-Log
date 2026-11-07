import pytest
from app import create_app
from database.db import get_db, init_db
from modules.log_manager import LogManager

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': ':memory:'
    })
    with app.app_context():
        init_db()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_log_creation_and_retrieval(app):
    with app.app_context():
        # Add a test log
        LogManager.add_log(
            source_ip="192.168.1.100",
            username="test_user",
            event_type="Successful Login",
            description="Unit test login successful",
            severity="Informational"
        )
        
        # Retrieve logs
        result = LogManager.get_logs(page=1, per_page=10)
        logs = result['logs']
        
        assert len(logs) == 1
        assert logs[0]['username'] == "test_user"
        assert logs[0]['event_type'] == "Successful Login"
        assert logs[0]['severity'] == "Informational"