from flask import Flask, redirect, url_for
from config import Config
from database import init_app, get_db
from modules.data_generator import DataGenerator
from werkzeug.security import generate_password_hash

# Import Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.logs import logs_bp
from routes.alerts import alerts_bp
from routes.analysis import analysis_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.update(test_config)

    # Initialize Database
    init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(analysis_bp)

    with app.app_context():
        db = get_db()
        # Seed default admin user if none exists (username: admin, password: admin123)
        admin_check = db.execute("SELECT id FROM users WHERE username = 'admin'").fetchone()
        if not admin_check:
            hashed_pw = generate_password_hash('admin123')
            db.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')", ('admin', hashed_pw))
            db.commit()
            print("Default admin user created (Username: admin, Password: admin123).")

        # Seed initial logs if empty
        log_check = db.execute("SELECT COUNT(*) FROM security_logs").fetchone()[0]
        if log_check == 0:
            DataGenerator.seed_database(50)
            print("Initial sample security logs generated!")

    @app.route('/settings')
    def settings_view():
        return app.view_functions['dashboard.dashboard_view']() # Placeholder for settings

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)