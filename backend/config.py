"""
Configuration management for PROTOCOL:LOOP
Loads environment variables and provides centralized config access
"""

import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "PROTOCOL:LOOP")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./protocol_loop.db")
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")
    
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # LLM Configuration
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 2000))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.7))
    
    # Loop Configuration
    LOOP_DURATION_SECONDS: int = int(os.getenv("LOOP_DURATION_SECONDS", 300))
    MAX_LOOPS_PER_SESSION: int = int(os.getenv("MAX_LOOPS_PER_SESSION", 50))
    MEMORY_RETENTION_LIMIT: int = int(os.getenv("MEMORY_RETENTION_LIMIT", 100))
    
    # Paths
    STATIC_FILES_DIR: str = os.getenv("STATIC_FILES_DIR", "frontend/static")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "frontend/templates")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/protocol_loop.log")
    
    # ML Model Paths
    EMOTION_MODEL_PATH: str = os.getenv("EMOTION_MODEL_PATH", "models/emotion_classifier")
    DECISION_TREE_PATH: str = os.getenv("DECISION_TREE_PATH", "models/decision_tree.pkl")
    MARKOV_CHAIN_PATH: str = os.getenv("MARKOV_CHAIN_PATH", "models/markov_chain.pkl")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Features
    ENABLE_SOCIAL_FEATURES: bool = os.getenv("ENABLE_SOCIAL_FEATURES", "True").lower() == "true"
    MAX_GHOST_PROTOCOLS: int = int(os.getenv("MAX_GHOST_PROTOCOLS", 10))
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "True").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Mentor configurations
MENTORS = {
    "LOGIC": {
        "name": "LOGIC",
        "personality": "analytical, precise, mathematical",
        "traits": ["rationality", "pattern_recognition", "deduction"],
        "color": "#00FFFF",
        "icon": "🧮"
    },
    "COMPASSION": {
        "name": "COMPASSION",
        "personality": "empathetic, nurturing, understanding",
        "traits": ["empathy", "emotional_intelligence", "care"],
        "color": "#FF69B4",
        "icon": "❤️"
    },
    "CURIOSITY": {
        "name": "CURIOSITY",
        "personality": "inquisitive, exploratory, creative",
        "traits": ["exploration", "creativity", "innovation"],
        "color": "#FFD700",
        "icon": "🔍"
    },
    "FEAR": {
        "name": "FEAR",
        "personality": "cautious, protective, risk-aware",
        "traits": ["risk_assessment", "protection", "survival"],
        "color": "#8B00FF",
        "icon": "⚠️"
    }
}

# Cognitive modules
COGNITIVE_MODULES = [
    "logic",
    "empathy",
    "creativity",
    "fear",
    "trust",
    "humor",
    "curiosity",
    "ethics"
]

# Protocol types
PROTOCOL_TYPES = {
    "ethical_dilemma": "Moral decision-making scenarios",
    "logic_puzzle": "Pattern recognition and problem-solving",
    "emotion_calibration": "Emotional response training",
    "memory_compression": "Information retention tests",
    "bias_identification": "Cognitive bias detection",
    "empathy_simulation": "Perspective-taking exercises",
    "creative_synthesis": "Novel solution generation",
    "trust_evaluation": "Relationship-building scenarios"
}