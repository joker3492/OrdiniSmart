import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurazione generale"""

    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Chiave segreta per JWT
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///ordinismart.db"
    )  # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disabilita il tracking delle modifiche
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Durata del token JWT (in secondi)


class DevelopmentConfig(Config):
    """Configurazione per lo sviluppo"""

    DEBUG = True


class ProductionConfig(Config):
    """Configurazione per la produzione"""

    DEBUG = False


# Seleziona la configurazione attiva in base all'ambiente
config_by_name = {"development": DevelopmentConfig, "production": ProductionConfig}
