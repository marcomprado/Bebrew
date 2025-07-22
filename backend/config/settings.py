"""
Configurações do Backend Bebrew
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Configurações da aplicação usando variáveis de ambiente"""
    
    # Configurações da OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.7
    
    # Configurações do Firebase
    firebase_project_id: str
    firebase_private_key_id: str
    firebase_private_key: str
    firebase_client_email: str
    firebase_client_id: str
    firebase_auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    firebase_token_uri: str = "https://oauth2.googleapis.com/token"
    firebase_auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    firebase_client_x509_cert_url: str
    
    # Configurações do Sistema
    debug: bool = True
    environment: str = "development"
    log_level: str = "INFO"
    
    # Configurações de Segurança
    secret_key: str
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Configurações de API
    api_host: str = "localhost"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # Configurações de Banco de Dados
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global das configurações
settings = Settings()


def get_settings() -> Settings:
    """Retorna as configurações da aplicação"""
    return settings


def get_cors_origins() -> list[str]:
    """Retorna lista de origens CORS permitidas"""
    return [origin.strip() for origin in settings.cors_origins.split(",")] 