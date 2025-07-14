def calcular_abv_simples(og: float, fg: float) -> float:
    """
    Calcula ABV usando a fórmula simples
    ABV = (OG - FG) * 131.25
    """
    return (og - fg) * 131.25

def calcular_abv_preciso(og: float, fg: float) -> float:
    """
    Calcula ABV usando a fórmula mais precisa
    ABV = (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)
    """
    return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794)

def calcular_abv_alternativo(og: float, fg: float) -> float:
    """
    Fórmula alternativa para ABV
    ABV = ((1.05 * (og - fg)) / fg) / 0.79 * 100
    """
    return ((1.05 * (og - fg)) / fg) / 0.79 * 100

def calcular_atenuacao(og: float, fg: float) -> float:
    """
    Calcula a atenuação aparente
    Atenuação = ((OG - FG) / (OG - 1)) * 100
    """
    return ((og - fg) / (og - 1)) * 100

def calcular_calorias(og: float, fg: float, volume_ml: float) -> float:
    """
    Calcula as calorias aproximadas por 100ml
    """
    abv = calcular_abv_simples(og, fg)
    # Fórmula aproximada: (6.9 * ABV) + (4.0 * (RE - 0.1))
    # RE = Real Extract = 0.1808 * OP + 0.8192 * FG
    re = 0.1808 * og + 0.8192 * fg
    calorias_por_100ml = (6.9 * abv) + (4.0 * (re - 0.1))
    return calorias_por_100ml

def estimar_fg_por_atenuacao(og: float, atenuacao_esperada: float) -> float:
    """
    Estima o FG baseado na atenuação esperada do fermento
    """
    return og - ((og - 1) * (atenuacao_esperada / 100))

def validar_densidades(og: float, fg: float) -> list:
    """
    Valida se as densidades estão em faixas aceitáveis
    Retorna lista de problemas encontrados
    """
    problemas = []
    
    if og < 1.020:
        problemas.append("OG muito baixo (< 1.020)")
    elif og > 1.150:
        problemas.append("OG muito alto (> 1.150)")
        
    if fg < 0.990:
        problemas.append("FG muito baixo (< 0.990)")
    elif fg > 1.030:
        problemas.append("FG muito alto (> 1.030)")
        
    if fg >= og:
        problemas.append("FG deve ser menor que OG")
        
    atenuacao = calcular_atenuacao(og, fg)
    if atenuacao > 90:
        problemas.append("Atenuação muito alta (> 90%)")
    elif atenuacao < 30:
        problemas.append("Atenuação muito baixa (< 30%)")
        
    return problemas

def converter_brix_para_sg(brix: float) -> float:
    """
    Converte Brix para Specific Gravity
    SG = 1 + (Brix / (258.6 - ((Brix / 258.2) * 227.1)))
    """
    return 1 + (brix / (258.6 - ((brix / 258.2) * 227.1)))

def converter_sg_para_brix(sg: float) -> float:
    """
    Converte Specific Gravity para Brix
    Brix = (((182.4601 * SG - 775.6821) * SG + 1262.7794) * SG - 669.5622)
    """
    return (((182.4601 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622)

def calcular_pontos_gravity(og: float, volume_litros: float) -> float:
    """
    Calcula os pontos de gravity para uma receita
    Usado para escalar receitas
    """
    return (og - 1) * 1000 * volume_litros

class ABVCalculator:
    """Classe para cálculos relacionados ao ABV e densidades"""
    
    def __init__(self):
        self.metodos_abv = {
            'simples': calcular_abv_simples,
            'preciso': calcular_abv_preciso,
            'alternativo': calcular_abv_alternativo
        }
    
    def calcular(self, og: float, fg: float, metodo: str = 'simples') -> dict:
        """
        Calcula ABV e outras métricas
        """
        if metodo not in self.metodos_abv:
            metodo = 'simples'
            
        resultado = {
            'og': og,
            'fg': fg,
            'abv': self.metodos_abv[metodo](og, fg),
            'atenuacao': calcular_atenuacao(og, fg),
            'calorias_100ml': calcular_calorias(og, fg, 100),
            'validacao': validar_densidades(og, fg)
        }
        
        return resultado
