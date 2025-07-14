from typing import Optional
import uuid

class Ingrediente:
    """Modelo para ingredientes utilizados nas receitas"""
    
    def __init__(self, nome: str, tipo: str, unidade: str, quantidade: float = 0.0, observacoes: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.tipo = tipo  # malte, lúpulo, fermento, açúcar, especiaria, etc
        self.unidade = unidade  # kg, g, L, mL, un, etc
        self.quantidade = quantidade
        self.observacoes = observacoes
        
    def __str__(self):
        return f"{self.nome} - {self.quantidade} {self.unidade}"
        
    def __repr__(self):
        return f"Ingrediente(nome='{self.nome}', tipo='{self.tipo}', quantidade={self.quantidade}, unidade='{self.unidade}')"
