import json
import os
from typing import Dict, List, Any
from datetime import datetime

class MockDataLoader:
    """Carregador de dados mock para desenvolvimento"""
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'mock_data.json')
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Carrega os dados do arquivo JSON"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Arquivo de dados mock não encontrado: {self.data_path}")
            return {
                "receitas": [],
                "producoes": [],
                "historico": [],
                "configuracoes": {}
            }
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return {
                "receitas": [],
                "producoes": [],
                "historico": [],
                "configuracoes": {}
            }
    
    def get_receitas(self) -> List[Dict[str, Any]]:
        """Retorna todas as receitas"""
        return self.data.get("receitas", [])
    
    def get_receita_by_id(self, receita_id: str) -> Dict[str, Any]:
        """Retorna uma receita específica pelo ID"""
        receitas = self.get_receitas()
        for receita in receitas:
            if receita.get("id") == receita_id:
                return receita
        return None
    
    def get_producoes_ativas(self) -> List[Dict[str, Any]]:
        """Retorna produções em andamento ou fermentando"""
        producoes = self.data.get("producoes", [])
        return [p for p in producoes if p.get("status") in ["Em Andamento", "Fermentando"]]
    
    def get_producao_by_id(self, producao_id: str) -> Dict[str, Any]:
        """Retorna uma produção específica pelo ID"""
        producoes = self.data.get("producoes", [])
        for producao in producoes:
            if producao.get("id") == producao_id:
                return producao
        return None
    
    def get_historico(self) -> List[Dict[str, Any]]:
        """Retorna o histórico de produções concluídas"""
        return self.data.get("historico", [])
    
    def get_configuracoes(self) -> Dict[str, Any]:
        """Retorna as configurações do sistema"""
        return self.data.get("configuracoes", {})
    
    def get_estatisticas(self) -> Dict[str, Any]:
        """Calcula estatísticas gerais"""
        receitas = self.get_receitas()
        producoes = self.data.get("producoes", [])
        historico = self.get_historico()
        
        # Calcular ABV médio
        abvs = []
        for receita in receitas:
            if receita.get("abv"):
                abvs.append(receita["abv"])
        for hist in historico:
            if hist.get("abv"):
                abvs.append(hist["abv"])
        
        abv_medio = sum(abvs) / len(abvs) if abvs else 0
        
        # Última produção
        ultima_producao = "Nenhuma"
        if producoes:
            ultima_producao = producoes[-1].get("lote", "Nenhuma")
        
        return {
            "total_receitas": len(receitas),
            "producoes_ativas": len(self.get_producoes_ativas()),
            "abv_medio": abv_medio,
            "ultima_producao": ultima_producao,
            "total_historico": len(historico)
        }
    
    def get_tipos_bebida(self) -> List[str]:
        """Retorna os tipos únicos de bebida"""
        tipos = set()
        for receita in self.get_receitas():
            tipo = receita.get("tipo")
            if tipo:
                tipos.add(tipo)
        return sorted(list(tipos))
    
    def get_ingredientes_unicos(self) -> Dict[str, List[str]]:
        """Retorna ingredientes únicos por tipo"""
        ingredientes_por_tipo = {}
        
        for receita in self.get_receitas():
            for ingrediente in receita.get("ingredientes", []):
                tipo = ingrediente.get("tipo", "outro")
                nome = ingrediente.get("nome")
                
                if tipo not in ingredientes_por_tipo:
                    ingredientes_por_tipo[tipo] = set()
                
                if nome:
                    ingredientes_por_tipo[tipo].add(nome)
        
        # Converter sets para listas ordenadas
        for tipo in ingredientes_por_tipo:
            ingredientes_por_tipo[tipo] = sorted(list(ingredientes_por_tipo[tipo]))
        
        return ingredientes_por_tipo

# Instância global para uso em toda a aplicação
mock_loader = MockDataLoader() 