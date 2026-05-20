"""
Application configuration loaded from environment variables.
"""
import os


class Config:
    """Base configuration."""
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://shreeshpitambare084_db_user:GPaqBT9gPNdCJvnW@cluster1.wjc2yyt.mongodb.net/?appName=Cluster1",
    )
    DB_NAME = os.getenv("DB_NAME", "pashuRakshak")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "pashurakshak-super-secret-jwt-key-2024")
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 24 hours in seconds
    JWT_REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 30  # 30 days in seconds
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB upload limit
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
