#!/usr/bin/env python3
"""
Script para iniciar a API do Bebrew
"""
import uvicorn
from backend.config.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    print("🍺 Iniciando Bebrew API...")
    print(f"📡 Servidor: http://{settings.api_host}:{settings.api_port}")
    print(f"📚 Documentação: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"🔧 Modo Debug: {settings.debug}")
    print("-" * 50)
    
    uvicorn.run(
        "backend.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 