from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME = "Library Management API"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    JWT_ALGORITHM = "HS256"
    JWT_EXP_MINUTES = 60

settings = Settings()
