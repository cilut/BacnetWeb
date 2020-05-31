import os


class Config:
    SECRET_KEY = "prueba"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("USER_GMAIL")
    MAIL_PASSWORD = os.getenv("PASS_GMAIL")
