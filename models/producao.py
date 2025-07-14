from datetime import datetime, timedelta
from typing import List, Optional, Dict
from .receita import Receita
from .etapa import EtapaExecucao
import uuid

class Producao:
    """Execução prática de uma receita com dados registrados"""
    
    def __init__(self, receita: Receita, lote: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.receita = receita
        self.lote = lote or f"L{datetime.now().strftime('%Y%m%d%H%M')}"
        
        # Controle de execução
        self.data_inicio = None
        self.data_fim = None
        self.status = "Planejada"  # Planejada, Em Andamento, Fermentando, Concluída, Cancelada
        self.etapas_execucao: List[EtapaExecucao] = []
        self.etapa_atual_index = 0
        
        # Dados medidos
        self.og_medido = None
        self.fg_medido = None
        self.abv_final = None
        self.volume_final = None
        self.rendimento_real = None
        
        # Notas e observações
        self.notas_gerais = ""
        self.problemas_encontrados = []
        self.modificacoes_receita = []
        
        # Qualidade
        self.avaliacao_visual = None
        self.avaliacao_aroma = None
        self.avaliacao_sabor = None
        self.nota_final = None
        
    def iniciar_producao(self):
        """Inicia a produção"""
        if self.status != "Planejada":
            raise ValueError("Produção já foi iniciada")
            
        self.data_inicio = datetime.now()
        self.status = "Em Andamento"
        
        # Cria as execuções das etapas baseadas na receita
        for etapa in self.receita.etapas:
            etapa_exec = EtapaExecucao(etapa.id)
            self.etapas_execucao.append(etapa_exec)
            
    def iniciar_etapa_atual(self):
        """Inicia a etapa atual"""
        if self.etapa_atual_index >= len(self.etapas_execucao):
            raise ValueError("Todas as etapas já foram concluídas")
            
        etapa_atual = self.etapas_execucao[self.etapa_atual_index]
        etapa_atual.inicio = datetime.now()
        
    def finalizar_etapa_atual(self):
        """Finaliza a etapa atual e avança para a próxima"""
        if self.etapa_atual_index >= len(self.etapas_execucao):
            raise ValueError("Todas as etapas já foram concluídas")
            
        etapa_atual = self.etapas_execucao[self.etapa_atual_index]
        etapa_atual.finalizar_etapa()
        self.etapa_atual_index += 1
        
        # Verifica se todas as etapas foram concluídas
        if self.etapa_atual_index >= len(self.etapas_execucao):
            self.status = "Fermentando"
            
    def finalizar_producao(self):
        """Finaliza a produção"""
        self.data_fim = datetime.now()
        self.status = "Concluída"
        
        # Calcula rendimento
        if self.volume_final and self.receita.rendimento_esperado:
            self.rendimento_real = (self.volume_final / self.receita.rendimento_esperado) * 100
            
        # Calcula ABV final
        if self.og_medido and self.fg_medido:
            self.abv_final = (self.og_medido - self.fg_medido) * 131.25
            
    def cancelar_producao(self, motivo: str):
        """Cancela a produção"""
        self.status = "Cancelada"
        self.problemas_encontrados.append(f"Cancelada: {motivo}")
        
    def obter_etapa_atual(self) -> Optional[EtapaExecucao]:
        """Retorna a etapa atual em execução"""
        if self.etapa_atual_index < len(self.etapas_execucao):
            return self.etapas_execucao[self.etapa_atual_index]
        return None
        
    def obter_progresso(self) -> float:
        """Retorna o progresso da produção (0-100%)"""
        if not self.etapas_execucao:
            return 0.0
        return (self.etapa_atual_index / len(self.etapas_execucao)) * 100
        
    def duracao_total(self) -> Optional[timedelta]:
        """Retorna a duração total da produção"""
        if self.data_inicio and self.data_fim:
            return self.data_fim - self.data_inicio
        elif self.data_inicio:
            return datetime.now() - self.data_inicio
        return None
        
    def adicionar_problema(self, problema: str):
        """Adiciona um problema encontrado durante a produção"""
        self.problemas_encontrados.append(f"{datetime.now().strftime('%H:%M')} - {problema}")
        
    def adicionar_modificacao(self, modificacao: str):
        """Adiciona uma modificação feita na receita"""
        self.modificacoes_receita.append(f"{datetime.now().strftime('%H:%M')} - {modificacao}")
        
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas da produção"""
        stats = {
            'lote': self.lote,
            'status': self.status,
            'progresso': self.obter_progresso(),
            'etapas_concluidas': self.etapa_atual_index,
            'total_etapas': len(self.etapas_execucao),
            'duracao': str(self.duracao_total()) if self.duracao_total() else None,
            'rendimento': self.rendimento_real,
            'abv_final': self.abv_final
        }
        return stats
        
    def __str__(self):
        return f"Produção {self.lote} - {self.receita.nome} ({self.status})" 