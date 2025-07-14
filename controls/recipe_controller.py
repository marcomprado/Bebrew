from typing import List, Optional, Dict
from models import Receita, Ingrediente, Etapa
from util.abv_calculator import ABVCalculator

class RecipeController:
    """Controlador para gerenciamento de receitas"""
    
    def __init__(self):
        self.receitas: Dict[str, Receita] = {}
        self.receita_atual: Optional[Receita] = None
        self.abv_calculator = ABVCalculator()
        
    def criar_nova_receita(self, nome: str, tipo: str, volume: float, descricao: Optional[str] = None) -> Receita:
        """Cria uma nova receita"""
        receita = Receita(nome, tipo, volume, descricao)
        self.receitas[receita.id] = receita
        return receita
        
    def carregar_receita(self, receita_id: str) -> Optional[Receita]:
        """Carrega uma receita para edição"""
        if receita_id in self.receitas:
            self.receita_atual = self.receitas[receita_id]
            return self.receita_atual
        return None
        
    def salvar_receita(self, receita: Receita) -> bool:
        """Salva uma receita"""
        self.receitas[receita.id] = receita
        return True
        
    def deletar_receita(self, receita_id: str) -> bool:
        """Deleta uma receita"""
        if receita_id in self.receitas:
            del self.receitas[receita_id]
            if self.receita_atual and self.receita_atual.id == receita_id:
                self.receita_atual = None
            return True
        return False
        
    def duplicar_receita(self, receita_id: str, novo_nome: str) -> Optional[Receita]:
        """Duplica uma receita existente"""
        if receita_id not in self.receitas:
            return None
            
        receita_original = self.receitas[receita_id]
        nova_receita = Receita(novo_nome, receita_original.tipo, receita_original.volume, receita_original.descricao)
        
        # Copiar propriedades técnicas
        nova_receita.og = receita_original.og
        nova_receita.fg = receita_original.fg
        nova_receita.abv = receita_original.abv
        nova_receita.ibu = receita_original.ibu
        nova_receita.srm = receita_original.srm
        nova_receita.ph = receita_original.ph
        nova_receita.temperatura_fermentacao = receita_original.temperatura_fermentacao
        nova_receita.tempo_fermentacao = receita_original.tempo_fermentacao
        nova_receita.dificuldade = receita_original.dificuldade
        
        # Copiar ingredientes
        for ingrediente in receita_original.ingredientes:
            novo_ingrediente = Ingrediente(
                ingrediente.nome, 
                ingrediente.tipo, 
                ingrediente.unidade, 
                ingrediente.quantidade,
                ingrediente.observacoes
            )
            nova_receita.adicionar_ingrediente(novo_ingrediente)
            
        # Copiar etapas
        for etapa in receita_original.etapas:
            nova_etapa = Etapa(
                etapa.nome,
                etapa.descricao,
                etapa.duracao_estimada,
                etapa.temperatura_alvo,
                etapa.observacoes
            )
            nova_etapa.parametros = etapa.parametros.copy()
            nova_receita.adicionar_etapa(nova_etapa)
            
        self.receitas[nova_receita.id] = nova_receita
        return nova_receita
        
    def adicionar_ingrediente(self, receita_id: str, nome: str, tipo: str, unidade: str, quantidade: float, observacoes: Optional[str] = None) -> bool:
        """Adiciona um ingrediente à receita"""
        if receita_id not in self.receitas:
            return False
            
        receita = self.receitas[receita_id]
        ingrediente = Ingrediente(nome, tipo, unidade, quantidade, observacoes)
        receita.adicionar_ingrediente(ingrediente)
        return True
        
    def remover_ingrediente(self, receita_id: str, ingrediente_id: str) -> bool:
        """Remove um ingrediente da receita"""
        if receita_id not in self.receitas:
            return False
            
        receita = self.receitas[receita_id]
        receita.remover_ingrediente(ingrediente_id)
        return True
        
    def editar_ingrediente(self, receita_id: str, ingrediente_id: str, **kwargs) -> bool:
        """Edita um ingrediente existente"""
        if receita_id not in self.receitas:
            return False
            
        receita = self.receitas[receita_id]
        ingrediente = next((ing for ing in receita.ingredientes if ing.id == ingrediente_id), None)
        
        if ingrediente:
            for key, value in kwargs.items():
                if hasattr(ingrediente, key):
                    setattr(ingrediente, key, value)
            return True
        return False
        
    def adicionar_etapa(self, receita_id: str, nome: str, descricao: str, duracao: int, temperatura: Optional[float] = None, observacoes: Optional[str] = None) -> bool:
        """Adiciona uma etapa à receita"""
        if receita_id not in self.receitas:
            return False
            
        receita = self.receitas[receita_id]
        etapa = Etapa(nome, descricao, duracao, temperatura, observacoes)
        receita.adicionar_etapa(etapa)
        return True
        
    def remover_etapa(self, receita_id: str, etapa_id: str) -> bool:
        """Remove uma etapa da receita"""
        if receita_id not in self.receitas:
            return False
            
        receita = self.receitas[receita_id]
        receita.remover_etapa(etapa_id)
        return True
        
    def reordenar_etapas(self, receita_id: str, nova_ordem: List[str]) -> bool:
        """Reordena as etapas da receita"""
        if receita_id not in self.receitas:
            return False
            
        receita = self.receitas[receita_id]
        etapas_dict = {etapa.id: etapa for etapa in receita.etapas}
        
        novas_etapas = []
        for etapa_id in nova_ordem:
            if etapa_id in etapas_dict:
                novas_etapas.append(etapas_dict[etapa_id])
                
        receita.etapas = novas_etapas
        receita._atualizar_tempo_total()
        return True
        
    def calcular_abv_receita(self, receita_id: str) -> Optional[Dict]:
        """Calcula o ABV de uma receita"""
        if receita_id not in self.receitas:
            return None
            
        receita = self.receitas[receita_id]
        if receita.og and receita.fg:
            resultado = self.abv_calculator.calcular(receita.og, receita.fg)
            receita.abv = resultado['abv']
            return resultado
        return None
        
    def validar_receita(self, receita_id: str) -> List[str]:
        """Valida uma receita e retorna lista de problemas"""
        if receita_id not in self.receitas:
            return ["Receita não encontrada"]
            
        receita = self.receitas[receita_id]
        return receita.validar_receita()
        
    def escalar_receita(self, receita_id: str, novo_volume: float) -> Optional[Receita]:
        """Escala uma receita para um novo volume"""
        if receita_id not in self.receitas:
            return None
            
        receita_original = self.receitas[receita_id]
        fator_escala = novo_volume / receita_original.volume
        
        receita_escalada = self.duplicar_receita(receita_id, f"{receita_original.nome} - {novo_volume}L")
        
        if receita_escalada:
            receita_escalada.volume = novo_volume
            receita_escalada.rendimento_esperado = novo_volume
            
            # Escalar ingredientes
            for ingrediente in receita_escalada.ingredientes:
                ingrediente.quantidade *= fator_escala
                
        return receita_escalada
        
    def obter_receitas_por_tipo(self, tipo: str) -> List[Receita]:
        """Obtém todas as receitas de um tipo específico"""
        return [receita for receita in self.receitas.values() if receita.tipo.lower() == tipo.lower()]
        
    def buscar_receitas(self, termo: str) -> List[Receita]:
        """Busca receitas por nome ou descrição"""
        termo = termo.lower()
        resultados = []
        
        for receita in self.receitas.values():
            if (termo in receita.nome.lower() or 
                (receita.descricao and termo in receita.descricao.lower())):
                resultados.append(receita)
                
        return resultados
        
    def obter_estatisticas_receitas(self) -> Dict:
        """Obtém estatísticas das receitas"""
        stats = {
            'total_receitas': len(self.receitas),
            'tipos': {},
            'dificuldades': {},
            'abv_medio': 0,
            'volume_medio': 0
        }
        
        if not self.receitas:
            return stats
            
        abvs = []
        volumes = []
        
        for receita in self.receitas.values():
            # Contagem por tipo
            tipo = receita.tipo
            stats['tipos'][tipo] = stats['tipos'].get(tipo, 0) + 1
            
            # Contagem por dificuldade
            dificuldade = receita.dificuldade
            stats['dificuldades'][dificuldade] = stats['dificuldades'].get(dificuldade, 0) + 1
            
            # ABV para média
            if receita.abv:
                abvs.append(receita.abv)
                
            # Volume para média
            volumes.append(receita.volume)
            
        if abvs:
            stats['abv_medio'] = sum(abvs) / len(abvs)
            
        if volumes:
            stats['volume_medio'] = sum(volumes) / len(volumes)
            
        return stats
        
    def listar_receitas(self, ordenar_por: str = "nome") -> List[Receita]:
        """Lista todas as receitas ordenadas"""
        receitas = list(self.receitas.values())
        
        if ordenar_por == "nome":
            receitas.sort(key=lambda r: r.nome)
        elif ordenar_por == "tipo":
            receitas.sort(key=lambda r: r.tipo)
        elif ordenar_por == "data":
            receitas.sort(key=lambda r: r.data_criacao, reverse=True)
        elif ordenar_por == "abv":
            receitas.sort(key=lambda r: r.abv or 0, reverse=True)
            
        return receitas
        
    def exportar_receita(self, receita_id: str) -> Optional[Dict]:
        """Exporta uma receita para formato JSON"""
        if receita_id not in self.receitas:
            return None
            
        receita = self.receitas[receita_id]
        
        dados = {
            'nome': receita.nome,
            'tipo': receita.tipo,
            'volume': receita.volume,
            'descricao': receita.descricao,
            'og': receita.og,
            'fg': receita.fg,
            'abv': receita.abv,
            'ibu': receita.ibu,
            'srm': receita.srm,
            'ph': receita.ph,
            'temperatura_fermentacao': receita.temperatura_fermentacao,
            'tempo_fermentacao': receita.tempo_fermentacao,
            'dificuldade': receita.dificuldade,
            'ingredientes': [
                {
                    'nome': ing.nome,
                    'tipo': ing.tipo,
                    'unidade': ing.unidade,
                    'quantidade': ing.quantidade,
                    'observacoes': ing.observacoes
                }
                for ing in receita.ingredientes
            ],
            'etapas': [
                {
                    'nome': etapa.nome,
                    'descricao': etapa.descricao,
                    'duracao_estimada': etapa.duracao_estimada,
                    'temperatura_alvo': etapa.temperatura_alvo,
                    'observacoes': etapa.observacoes,
                    'parametros': etapa.parametros
                }
                for etapa in receita.etapas
            ]
        }
        
        return dados
