import os

class Settings:
    PROJECT_NAME: str = "Mechanical Material Recommendation System"
    VERSION: str = "1.0.0"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "mechanical_materials_db")

settings = Settings()
