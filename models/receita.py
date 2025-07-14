from typing import List, Optional
from .bebida import Bebida
from .ingredient import Ingrediente
from .etapa import Etapa

class Receita(Bebida):
    """Receita de bebida fermentada com ingredientes, etapas e dados técnicos"""
    
    def __init__(self, nome: str, tipo: str, volume: float, descricao: Optional[str] = None):
        super().__init__(nome, tipo, volume, descricao)
        self.ingredientes: List[Ingrediente] = []
        self.etapas: List[Etapa] = []
        
        # Dados técnicos
        self.og = None  # Original Gravity (densidade inicial)
        self.fg = None  # Final Gravity (densidade final)
        self.abv = None  # Alcohol by Volume
        self.ibu = None  # International Bitterness Units (para cerveja)
        self.srm = None  # Standard Reference Method (cor para cerveja)
        self.ph = None
        
        # Configurações de fermentação
        self.temperatura_fermentacao = None
        self.tempo_fermentacao = None  # em dias
        
        # Metadados
        self.dificuldade = "Iniciante"  # Iniciante, Intermediário, Avançado
        self.rendimento_esperado = volume
        self.tempo_total_estimado = 0  # em minutos
        
    def adicionar_ingrediente(self, ingrediente: Ingrediente):
        """Adiciona um ingrediente à receita"""
        self.ingredientes.append(ingrediente)
        
    def remover_ingrediente(self, ingrediente_id: str):
        """Remove um ingrediente da receita"""
        self.ingredientes = [ing for ing in self.ingredientes if ing.id != ingrediente_id]
        
    def adicionar_etapa(self, etapa: Etapa):
        """Adiciona uma etapa à receita"""
        self.etapas.append(etapa)
        self._atualizar_tempo_total()
        
    def remover_etapa(self, etapa_id: str):
        """Remove uma etapa da receita"""
        self.etapas = [etapa for etapa in self.etapas if etapa.id != etapa_id]
        self._atualizar_tempo_total()
        
    def _atualizar_tempo_total(self):
        """Atualiza o tempo total estimado baseado nas etapas"""
        self.tempo_total_estimado = sum(etapa.duracao_estimada for etapa in self.etapas)
        
    def calcular_abv(self):
        """Calcula o ABV baseado no OG e FG"""
        if self.og and self.fg:
            self.abv = (self.og - self.fg) * 131.25
            return self.abv
        return None
        
    def obter_ingredientes_por_tipo(self, tipo: str) -> List[Ingrediente]:
        """Retorna todos os ingredientes de um tipo específico"""
        return [ing for ing in self.ingredientes if ing.tipo.lower() == tipo.lower()]
        
    def validar_receita(self) -> List[str]:
        """Valida a receita e retorna lista de problemas encontrados"""
        problemas = []
        
        if not self.ingredientes:
            problemas.append("Receita não possui ingredientes")
            
        if not self.etapas:
            problemas.append("Receita não possui etapas definidas")
            
        if self.volume <= 0:
            problemas.append("Volume deve ser maior que zero")
            
        # Verificações específicas por tipo
        if self.tipo.lower() == "cerveja":
            maltes = self.obter_ingredientes_por_tipo("malte")
            if not maltes:
                problemas.append("Cerveja deve ter pelo menos um malte")
                
        return problemas
        
    def __str__(self):
        return f"Receita: {self.nome} ({self.tipo}) - {len(self.ingredientes)} ingredientes, {len(self.etapas)} etapas" 