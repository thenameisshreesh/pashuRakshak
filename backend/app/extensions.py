"""
Flask extensions initialized here and shared across the application.
PyMongo, JWT Manager, and GridFS instances.
"""
from datetime import timedelta

from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from gridfs import GridFS

# Global extension instances – populated during create_app()
mongo_client: MongoClient = None  # type: ignore
db = None  # pymongo Database object
jwt = JWTManager()
fs: GridFS = None  # type: ignore


def init_extensions(app):
    """Initialize all extensions with the Flask app."""
    global mongo_client, db, fs

    # MongoDB
    mongo_uri = app.config["MONGO_URI"]
    db_name = app.config["DB_NAME"]
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[db_name]

    # GridFS
    fs = GridFS(db)

    # JWT
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
        seconds=app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 86400)
    )
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
        seconds=app.config.get("JWT_REFRESH_TOKEN_EXPIRES", 2592000)
    )
    jwt.init_app(app)

    # Ensure indexes
    _ensure_indexes()


def get_db():
    """Get the MongoDB database instance."""
    return db


def get_fs():
    """Get the GridFS instance."""
    return fs


def _ensure_indexes():
    """Create MongoDB indexes for performance."""
    db.users.create_index("mobile", unique=True, sparse=True)
    db.users.create_index("username", unique=True, sparse=True)
    db.users.create_index("role")
    db.schemes.create_index("name")
    db.applications.create_index("farmer_id")
    db.applications.create_index("scheme_id")
    db.applications.create_index("status")
    db.rfid_tags.create_index("tag_id", unique=True)
    db.rfid_tags.create_index("farmer_id")
    db.scan_sessions.create_index("session_id", unique=True)
    db.notifications.create_index("user_id")
    db.notifications.create_index([("user_id", 1), ("read", 1)])
    db.audit_logs.create_index("user_id")
    db.audit_logs.create_index("action")
    db.audit_logs.create_index("timestamp")
    db.raids.create_index("status")
