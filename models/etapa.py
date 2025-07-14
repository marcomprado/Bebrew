from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid

class Etapa:
    """Representa uma fase da produção (mostura, fervura, fermentação, etc)"""
    
    def __init__(self, nome: str, descricao: str, duracao_estimada: int, temperatura_alvo: Optional[float] = None, observacoes: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.descricao = descricao
        self.duracao_estimada = duracao_estimada  # em minutos
        self.temperatura_alvo = temperatura_alvo  # em Celsius
        self.observacoes = observacoes
        self.parametros = {}  # parâmetros específicos da etapa
        
    def adicionar_parametro(self, chave: str, valor: Any):
        """Adiciona um parâmetro específico à etapa"""
        self.parametros[chave] = valor
        
    def __str__(self):
        temp_info = f" ({self.temperatura_alvo}°C)" if self.temperatura_alvo else ""
        return f"{self.nome}{temp_info} - {self.duracao_estimada}min"
        
    def __repr__(self):
        return f"Etapa(nome='{self.nome}', duracao={self.duracao_estimada}min)"


class EtapaExecucao:
    """Dados medidos durante a execução de uma etapa"""
    
    def __init__(self, etapa_id: str, inicio: Optional[datetime] = None):
        self.id = str(uuid.uuid4())
        self.etapa_id = etapa_id
        self.inicio = inicio or datetime.now()
        self.fim = None
        self.temperaturas = []  # lista de (timestamp, temperatura)
        self.anotacoes = []  # lista de (timestamp, anotação)
        self.parametros_medidos = {}
        self.concluida = False
        
    def adicionar_temperatura(self, temperatura: float, timestamp: Optional[datetime] = None):
        """Registra uma medição de temperatura"""
        timestamp = timestamp or datetime.now()
        self.temperaturas.append((timestamp, temperatura))
        
    def adicionar_anotacao(self, anotacao: str, timestamp: Optional[datetime] = None):
        """Adiciona uma anotação com timestamp"""
        timestamp = timestamp or datetime.now()
        self.anotacoes.append((timestamp, anotacao))
        
    def finalizar_etapa(self):
        """Marca a etapa como concluída"""
        self.fim = datetime.now()
        self.concluida = True
        
    def duracao_real(self) -> Optional[timedelta]:
        """Retorna a duração real da etapa"""
        if self.fim:
            return self.fim - self.inicio
        return None
        
    def __str__(self):
        status = "Concluída" if self.concluida else "Em andamento"
        return f"Execução {self.etapa_id} - {status}" 