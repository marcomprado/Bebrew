from typing import List, Optional, Dict, Any
from datetime import datetime
from models import Producao, Receita, EtapaExecucao
from util.abv_calculator import ABVCalculator

class BrewController:
    """Controlador para operações de produção de bebidas"""
    
    def __init__(self):
        self.producoes_ativas: Dict[str, Producao] = {}
        self.producao_atual: Optional[Producao] = None
        self.abv_calculator = ABVCalculator()
        
    def criar_nova_producao(self, receita: Receita, lote: Optional[str] = None) -> Producao:
        """Cria uma nova produção baseada em uma receita"""
        producao = Producao(receita, lote)
        self.producoes_ativas[producao.id] = producao
        return producao
        
    def iniciar_producao(self, producao_id: str) -> bool:
        """Inicia uma produção"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        try:
            producao.iniciar_producao()
            self.producao_atual = producao
            return True
        except ValueError:
            return False
            
    def pausar_producao(self, producao_id: str, motivo: str = "Pausada pelo usuário") -> bool:
        """Pausa uma produção em andamento"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        if producao.status == "Em Andamento":
            producao.adicionar_problema(f"Pausada: {motivo}")
            return True
        return False
        
    def retomar_producao(self, producao_id: str) -> bool:
        """Retoma uma produção pausada"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        producao.adicionar_problema("Produção retomada")
        self.producao_atual = producao
        return True
        
    def iniciar_etapa_atual(self, producao_id: str) -> bool:
        """Inicia a etapa atual da produção"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        try:
            producao.iniciar_etapa_atual()
            return True
        except ValueError:
            return False
            
    def finalizar_etapa_atual(self, producao_id: str) -> bool:
        """Finaliza a etapa atual e avança para a próxima"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        try:
            producao.finalizar_etapa_atual()
            return True
        except ValueError:
            return False
            
    def adicionar_temperatura(self, producao_id: str, temperatura: float) -> bool:
        """Adiciona uma medição de temperatura à etapa atual"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        etapa_atual = producao.obter_etapa_atual()
        
        if etapa_atual:
            etapa_atual.adicionar_temperatura(temperatura)
            return True
        return False
        
    def adicionar_anotacao(self, producao_id: str, anotacao: str) -> bool:
        """Adiciona uma anotação à etapa atual"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        etapa_atual = producao.obter_etapa_atual()
        
        if etapa_atual:
            etapa_atual.adicionar_anotacao(anotacao)
            return True
        return False
        
    def registrar_densidade(self, producao_id: str, densidade: float, tipo: str = "og") -> bool:
        """Registra uma medição de densidade (OG ou FG)"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        
        if tipo.lower() == "og":
            producao.og_medido = densidade
        elif tipo.lower() == "fg":
            producao.fg_medido = densidade
            # Calcular ABV final se ambos OG e FG estão disponíveis
            if producao.og_medido:
                producao.abv_final = self.abv_calculator.calcular(
                    producao.og_medido, producao.fg_medido
                )['abv']
        
        return True
        
    def finalizar_producao(self, producao_id: str, volume_final: Optional[float] = None) -> bool:
        """Finaliza uma produção"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        
        if volume_final:
            producao.volume_final = volume_final
            
        producao.finalizar_producao()
        
        # Remove da lista de produções ativas
        if self.producao_atual and self.producao_atual.id == producao_id:
            self.producao_atual = None
            
        return True
        
    def cancelar_producao(self, producao_id: str, motivo: str) -> bool:
        """Cancela uma produção"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        producao.cancelar_producao(motivo)
        
        # Remove da lista de produções ativas
        del self.producoes_ativas[producao_id]
        
        if self.producao_atual and self.producao_atual.id == producao_id:
            self.producao_atual = None
            
        return True
        
    def obter_status_producao(self, producao_id: str) -> Optional[Dict]:
        """Obtém o status atual de uma produção"""
        if producao_id not in self.producoes_ativas:
            return None
            
        producao = self.producoes_ativas[producao_id]
        return producao.obter_estatisticas()
        
    def obter_temperaturas_etapa_atual(self, producao_id: str) -> List[tuple]:
        """Obtém as temperaturas registradas na etapa atual"""
        if producao_id not in self.producoes_ativas:
            return []
            
        producao = self.producoes_ativas[producao_id]
        etapa_atual = producao.obter_etapa_atual()
        
        if etapa_atual:
            return etapa_atual.temperaturas
        return []
        
    def obter_dados_grafico(self, producao_id: str) -> Dict[str, Any]:
        """Obtém dados formatados para gráficos"""
        if producao_id not in self.producoes_ativas:
            return {}
            
        producao = self.producoes_ativas[producao_id]
        etapa_atual = producao.obter_etapa_atual()
        
        dados = {
            'lote': producao.lote,
            'status': producao.status,
            'progresso': producao.obter_progresso(),
            'receita_nome': producao.receita.nome,
            'etapa_atual': None,
            'temperaturas': [],
            'temperatura_alvo': None,
            'tempo_decorrido': str(producao.duracao_total()) if producao.duracao_total() else "N/A"
        }
        
        if etapa_atual:
            # Encontrar a etapa correspondente na receita
            etapa_receita = next(
                (e for e in producao.receita.etapas if e.id == etapa_atual.etapa_id), 
                None
            )
            
            if etapa_receita:
                dados['etapa_atual'] = etapa_receita.nome
                dados['temperatura_alvo'] = etapa_receita.temperatura_alvo
                
            dados['temperaturas'] = etapa_atual.temperaturas
            
        # Adicionar dados de ABV se disponíveis
        if producao.og_medido and producao.fg_medido:
            resultado_abv = self.abv_calculator.calcular(producao.og_medido, producao.fg_medido)
            dados['abv'] = resultado_abv['abv']
            dados['atenuacao'] = resultado_abv['atenuacao']
        elif producao.receita.og and producao.receita.fg:
            resultado_abv = self.abv_calculator.calcular(producao.receita.og, producao.receita.fg)
            dados['abv'] = resultado_abv['abv']
            dados['atenuacao'] = resultado_abv['atenuacao']
        else:
            dados['abv'] = 0
            dados['atenuacao'] = 0
            
        return dados
        
    def listar_producoes_ativas(self) -> List[Dict]:
        """Lista todas as produções ativas"""
        return [producao.obter_estatisticas() for producao in self.producoes_ativas.values()]
        
    def tem_producao_ativa(self) -> bool:
        """Verifica se há alguma produção ativa"""
        return len(self.producoes_ativas) > 0
        
    def obter_producao_atual(self) -> Optional[Producao]:
        """Retorna a produção atualmente selecionada"""
        return self.producao_atual
        
    def adicionar_problema(self, producao_id: str, problema: str) -> bool:
        """Adiciona um problema à produção"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        producao.adicionar_problema(problema)
        return True
        
    def adicionar_modificacao(self, producao_id: str, modificacao: str) -> bool:
        """Adiciona uma modificação à receita durante a produção"""
        if producao_id not in self.producoes_ativas:
            return False
            
        producao = self.producoes_ativas[producao_id]
        producao.adicionar_modificacao(modificacao)
        return True
