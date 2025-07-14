from datetime import datetime
from typing import List, Optional
import uuid

class Bebida:
    """Classe base para bebidas fermentadas"""
    
    def __init__(self, nome: str, tipo: str, volume: float, descricao: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.tipo = tipo  # cerveja, hidromel, vinho, etc
        self.volume = volume  # em litros
        self.descricao = descricao
        self.data_criacao = datetime.now()
        
    def __str__(self):
        return f"{self.nome} ({self.tipo}) - {self.volume}L"
        
    def __repr__(self):
        return f"Bebida(nome='{self.nome}', tipo='{self.tipo}', volume={self.volume})" 