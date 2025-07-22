"""
Serviço de IA para Bebrew usando OpenAI
"""
import openai
from typing import Dict, List, Optional, Any
from loguru import logger
from ..config.settings import get_settings


class AIService:
    """Serviço de IA para funcionalidades inteligentes do Bebrew"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = openai.OpenAI(api_key=self.settings.openai_api_key)
        self.model = self.settings.openai_model
        
    async def analyze_recipe(self, recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa uma receita e fornece insights e sugestões
        
        Args:
            recipe_data: Dados da receita (ingredientes, etapas, etc.)
            
        Returns:
            Análise da receita com insights e sugestões
        """
        try:
            prompt = self._create_recipe_analysis_prompt(recipe_data)
            
            response = await self._get_completion(prompt)
            
            return {
                "analysis": response,
                "suggestions": self._extract_suggestions(response),
                "quality_score": self._calculate_quality_score(recipe_data),
                "potential_issues": self._identify_potential_issues(recipe_data)
            }
            
        except Exception as e:
            logger.error(f"Erro ao analisar receita: {e}")
            return {"error": "Erro ao analisar receita"}
    
    async def optimize_recipe(self, recipe_data: Dict[str, Any], target_style: str) -> Dict[str, Any]:
        """
        Otimiza uma receita para um estilo específico
        
        Args:
            recipe_data: Dados da receita atual
            target_style: Estilo desejado (IPA, Stout, etc.)
            
        Returns:
            Receita otimizada
        """
        try:
            prompt = self._create_optimization_prompt(recipe_data, target_style)
            
            response = await self._get_completion(prompt)
            
            return {
                "optimized_recipe": response,
                "changes_made": self._extract_changes(recipe_data, response),
                "expected_improvements": self._predict_improvements(response)
            }
            
        except Exception as e:
            logger.error(f"Erro ao otimizar receita: {e}")
            return {"error": "Erro ao otimizar receita"}
    
    async def predict_fermentation(self, recipe_data: Dict[str, Any], 
                                 initial_gravity: float, temperature: float) -> Dict[str, Any]:
        """
        Prediz o comportamento da fermentação
        
        Args:
            recipe_data: Dados da receita
            initial_gravity: Densidade inicial
            temperature: Temperatura de fermentação
            
        Returns:
            Previsões de fermentação
        """
        try:
            prompt = self._create_fermentation_prediction_prompt(
                recipe_data, initial_gravity, temperature
            )
            
            response = await self._get_completion(prompt)
            
            return {
                "prediction": response,
                "estimated_final_gravity": self._extract_final_gravity(response),
                "fermentation_time": self._extract_fermentation_time(response),
                "abv_estimate": self._calculate_abv_estimate(initial_gravity, response)
            }
            
        except Exception as e:
            logger.error(f"Erro ao prever fermentação: {e}")
            return {"error": "Erro ao prever fermentação"}
    
    async def suggest_improvements(self, production_data: Dict[str, Any]) -> List[str]:
        """
        Sugere melhorias baseadas em dados de produção
        
        Args:
            production_data: Dados de produção (temperaturas, tempos, etc.)
            
        Returns:
            Lista de sugestões de melhorias
        """
        try:
            prompt = self._create_improvement_prompt(production_data)
            
            response = await self._get_completion(prompt)
            
            return self._extract_suggestions(response)
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {e}")
            return ["Erro ao gerar sugestões"]
    
    async def _get_completion(self, prompt: str) -> str:
        """Obtém resposta da OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um especialista em brassagem artesanal com vasto conhecimento em cerveja, hidromel e vinho."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.settings.openai_max_tokens,
                temperature=self.settings.openai_temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Erro na comunicação com OpenAI: {e}")
            raise
    
    def _create_recipe_analysis_prompt(self, recipe_data: Dict[str, Any]) -> str:
        """Cria prompt para análise de receita"""
        return f"""
        Analise esta receita de brassagem e forneça insights detalhados:
        
        Receita: {recipe_data}
        
        Por favor, analise:
        1. Balanceamento de ingredientes
        2. Potenciais problemas
        3. Sugestões de melhoria
        4. Estilo esperado
        5. Características sensoriais previstas
        
        Forneça uma análise estruturada e prática.
        """
    
    def _create_optimization_prompt(self, recipe_data: Dict[str, Any], target_style: str) -> str:
        """Cria prompt para otimização de receita"""
        return f"""
        Otimize esta receita para o estilo {target_style}:
        
        Receita atual: {recipe_data}
        
        Forneça:
        1. Receita otimizada
        2. Justificativas para mudanças
        3. Impacto esperado nas características
        4. Considerações de processo
        
        Mantenha a estrutura original mas otimize para o estilo desejado.
        """
    
    def _create_fermentation_prediction_prompt(self, recipe_data: Dict[str, Any], 
                                             initial_gravity: float, temperature: float) -> str:
        """Cria prompt para previsão de fermentação"""
        return f"""
        Prediga o comportamento da fermentação:
        
        Receita: {recipe_data}
        Densidade inicial: {initial_gravity}
        Temperatura: {temperature}°C
        
        Forneça:
        1. Densidade final esperada
        2. Tempo de fermentação
        3. Comportamento do fermento
        4. Potenciais problemas
        5. Recomendações de controle
        
        Base suas previsões em dados científicos de fermentação.
        """
    
    def _create_improvement_prompt(self, production_data: Dict[str, Any]) -> str:
        """Cria prompt para sugestões de melhoria"""
        return f"""
        Analise estes dados de produção e sugira melhorias:
        
        Dados: {production_data}
        
        Forneça sugestões práticas para:
        1. Otimização de processo
        2. Melhoria de qualidade
        3. Eficiência de produção
        4. Controle de qualidade
        
        Foque em melhorias implementáveis e mensuráveis.
        """
    
    def _extract_suggestions(self, response: str) -> List[str]:
        """Extrai sugestões da resposta da IA"""
        # Implementação básica - pode ser melhorada com parsing mais sofisticado
        lines = response.split('\n')
        suggestions = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['sugestão', 'recomendo', 'considere', 'melhore']):
                suggestions.append(line.strip())
        
        return suggestions[:5]  # Limita a 5 sugestões
    
    def _calculate_quality_score(self, recipe_data: Dict[str, Any]) -> float:
        """Calcula score de qualidade da receita"""
        # Implementação básica - pode ser expandida
        score = 7.0  # Score base
        
        # Ajustes baseados em critérios
        if 'ingredients' in recipe_data and len(recipe_data['ingredients']) > 3:
            score += 0.5
        
        if 'steps' in recipe_data and len(recipe_data['steps']) > 5:
            score += 0.5
        
        return min(score, 10.0)
    
    def _identify_potential_issues(self, recipe_data: Dict[str, Any]) -> List[str]:
        """Identifica potenciais problemas na receita"""
        issues = []
        
        # Análise básica - pode ser expandida
        if 'ingredients' in recipe_data:
            if len(recipe_data['ingredients']) < 2:
                issues.append("Poucos ingredientes podem resultar em sabor limitado")
        
        return issues
    
    def _extract_changes(self, original: Dict[str, Any], optimized: str) -> List[str]:
        """Extrai mudanças feitas na otimização"""
        # Implementação básica
        return ["Mudanças identificadas na otimização"]
    
    def _predict_improvements(self, optimized_recipe: str) -> List[str]:
        """Prediz melhorias esperadas"""
        return ["Melhorias esperadas na receita otimizada"]
    
    def _extract_final_gravity(self, response: str) -> float:
        """Extrai densidade final da resposta"""
        # Implementação básica
        return 1.010  # Valor padrão
    
    def _extract_fermentation_time(self, response: str) -> int:
        """Extrai tempo de fermentação da resposta"""
        # Implementação básica
        return 14  # Dias padrão
    
    def _calculate_abv_estimate(self, initial_gravity: float, response: str) -> float:
        """Calcula estimativa de ABV"""
        # Fórmula básica de ABV
        final_gravity = self._extract_final_gravity(response)
        abv = (initial_gravity - final_gravity) * 131.25
        return round(abv, 2)


# Instância global do serviço
ai_service = AIService() 