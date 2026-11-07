import sqlite3
import os
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        # Auto-create database if it doesn't exist
        db_path = app.config['DATABASE']
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        if not os.path.exists(db_path):
            init_db()
            print("Database initialized successfully!")