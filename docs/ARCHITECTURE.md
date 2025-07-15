# 🏗️ Arquitetura do Sistema Bebrew

Este documento detalha a estrutura técnica, padrões arquiteturais e organização do código do sistema Bebrew.

## 🎯 Visão Geral Arquitetural

O Bebrew segue uma arquitetura **MVC (Model-View-Controller)** adaptada para aplicações desktop, com foco em:

- **Separação de Responsabilidades**: Cada camada tem funções específicas
- **Modularidade**: Componentes independentes e reutilizáveis
- **Extensibilidade**: Fácil adição de novas funcionalidades
- **Manutenibilidade**: Código organizado e bem documentado

## 📁 Estrutura de Diretórios

```
bebrew_mvp/
├── models/                 # Camada de Dados
│   ├── __init__.py        # Exportações do módulo
│   ├── bebida.py          # Classe base para bebidas
│   ├── receita.py         # Modelo de receitas
│   ├── ingredient.py      # Modelo de ingredientes
│   ├── etapa.py          # Modelo de etapas de produção
│   └── producao.py       # Modelo de produção ativa
├── controls/              # Camada de Controle
│   ├── brew_controller.py # Controlador de produção
│   └── recipe_controller.py # Controlador de receitas
├── view/                  # Camada de Apresentação
│   ├── base_view.py      # Classe base para views
│   ├── dashboard_view.py # Dashboard principal
│   ├── recipe_view.py    # Gestão de receitas
│   ├── production_view.py # Monitoramento de produção
│   ├── history_view.py   # Histórico de produções
│   ├── settings_view.py  # Configurações
│   ├── new_recipe_view.py # Criação de receitas
│   ├── new_production_view.py # Nova produção
│   └── ingredients_view.py # Gestão de ingredientes
├── util/                  # Utilitários
│   ├── abv_calculator.py # Cálculos de fermentação
│   ├── graph_plotter.py  # Visualizações
│   └── mock_data_loader.py # Dados de exemplo
├── database/              # Dados e configurações
│   └── mock_data.json    # Dados de exemplo
├── assets/               # Recursos estáticos
├── main.py              # Aplicação principal
└── requirements.txt     # Dependências
```

## 🔧 Camadas Arquiteturais

### 📊 **Camada de Dados (Models)**

Responsável pela definição e manipulação dos dados do sistema.

#### **Bebida** (`bebida.py`)
```python
class Bebida:
    """Classe base para bebidas fermentadas"""
    - id: str (UUID único)
    - nome: str
    - tipo: str
    - volume: float
    - descrição: str
    - data_criacao: datetime
```

#### **Receita** (`receita.py`)
```python
class Receita(Bebida):
    """Receita com ingredientes e etapas"""
    - ingredientes: List[Ingrediente]
    - etapas: List[Etapa]
    - og, fg, abv: float (dados técnicos)
    - ibu, srm, ph: float (específicos cerveja)
    - dificuldade: str
    - tempo_total_estimado: int
```

#### **Ingrediente** (`ingredient.py`)
```python
class Ingrediente:
    """Componente das receitas"""
    - id: str
    - nome: str
    - tipo: str (malte, lúpulo, fermento, etc.)
    - quantidade: float
    - unidade: str
    - observacoes: str
```

#### **Etapa** (`etapa.py`)
```python
class Etapa:
    """Fase da produção"""
    - id: str
    - nome: str
    - descrição: str
    - duracao_estimada: int
    - temperatura_alvo: float
    - parametros: Dict

class EtapaExecucao:
    """Execução real da etapa"""
    - etapa_id: str
    - inicio, fim: datetime
    - temperaturas: List[Tuple[datetime, float]]
    - anotacoes: List[Tuple[datetime, str]]
```

#### **Produção** (`producao.py`)
```python
class Producao:
    """Execução de uma receita"""
    - id: str
    - receita: Receita
    - lote: str
    - status: str
    - etapas_execucao: List[EtapaExecucao]
    - og_medido, fg_medido: float
    - problemas_encontrados: List[str]
    - modificacoes_receita: List[str]
```

### 🎮 **Camada de Controle (Controllers)**

Gerencia a lógica de negócio e orquestra as operações.

#### **BrewController** (`brew_controller.py`)
```python
class BrewController:
    """Controlador de produção"""
    - producoes_ativas: Dict[str, Producao]
    - producao_atual: Producao
    - abv_calculator: ABVCalculator
    
    # Métodos principais:
    - criar_nova_producao()
    - iniciar_producao()
    - iniciar_etapa_atual()
    - adicionar_temperatura()
    - registrar_densidade()
    - finalizar_producao()
```

#### **RecipeController** (`recipe_controller.py`)
```python
class RecipeController:
    """Controlador de receitas"""
    - receitas: Dict[str, Receita]
    - receita_atual: Receita
    
    # Métodos principais:
    - criar_nova_receita()
    - adicionar_ingrediente()
    - adicionar_etapa()
    - escalar_receita()
    - validar_receita()
    - exportar_receita()
```

### 🖥️ **Camada de Apresentação (Views)**

Interface do usuário e interação com o sistema.

#### **BaseView** (`base_view.py`)
```python
class BaseView(ABC):
    """Classe base para todas as views"""
    - colors: Dict (sistema de cores)
    - fonts: Dict (tipografia)
    - navigation: NavigationProtocol
    
    # Métodos base:
    - create_button()
    - create_card()
    - create_input()
    - create_label()
    - show_message()
```

#### **Views Específicas**
- **DashboardView**: Painel principal com estatísticas
- **RecipeView**: Listagem e gestão de receitas
- **NewRecipeView**: Criação de novas receitas
- **ProductionView**: Monitoramento de produção
- **NewProductionView**: Iniciar nova produção
- **HistoryView**: Histórico de produções
- **SettingsView**: Configurações do sistema
- **IngredientsView**: Gestão de ingredientes

### 🛠️ **Camada de Utilitários (Utils)**

Funcionalidades auxiliares e cálculos específicos.

#### **ABVCalculator** (`abv_calculator.py`)
```python
class ABVCalculator:
    """Cálculos de fermentação"""
    - calcular_abv_simples()
    - calcular_abv_preciso()
    - calcular_atenuacao()
    - validar_densidades()
    - converter_brix_para_sg()
```

#### **BebrewPlotter** (`graph_plotter.py`)
```python
class BebrewPlotter:
    """Visualizações de dados"""
    - criar_grafico_temperatura()
    - criar_grafico_progresso_etapas()
    - criar_grafico_densidade()
    - criar_dashboard_resumo()
```

## 🔄 Fluxo de Dados

### **Criação de Receita**
```
User Input → NewRecipeView → RecipeController → Receita Model → Storage
```

### **Iniciar Produção**
```
User Selection → NewProductionView → BrewController → Producao Model → Active Storage
```

### **Monitoramento**
```
Sensor Data → ProductionView → BrewController → EtapaExecucao → Real-time Updates
```

### **Visualização**
```
Model Data → Controller → View → BebrewPlotter → Chart Display
```

## 🧭 Sistema de Navegação

### **BebrewNavigator** (`main.py`)
```python
class BebrewNavigator:
    """Sistema de navegação baseado em grafos"""
    - view_configs: Dict[str, ViewConfig]
    - current_view: str
    - view_history: List[str]
    - forward_history: List[str]
    
    # Navegação:
    - navigate_to()
    - go_back()
    - go_forward()
    - can_navigate_to()
```

### **Grafo de Navegação**
```
dashboard ← → nova_receita ← → editor_receita
    ↓              ↓              ↓
nova_producao → monitoramento → visualizador
    ↓              ↓              ↓
historico ← → receitas ← → ingredientes
    ↓              
configuracoes
```

## 🎨 Padrões de Design

### **Factory Pattern**
- Views criadas dinamicamente pelo Navigator
- Componentes UI criados por métodos factory na BaseView

### **Observer Pattern**
- Views observam mudanças nos Controllers
- Atualizações em tempo real de dados

### **Strategy Pattern**
- Múltiplas fórmulas de cálculo de ABV
- Diferentes tipos de bebida com comportamentos específicos

### **Template Method**
- BaseView define template para todas as views
- Métodos abstratos implementados pelas views específicas

## 📊 Gerenciamento de Estado

### **Estado da Aplicação**
```python
BebrewApp:
    - navigator: BebrewNavigator
    - brew_controller: BrewController  
    - recipe_controller: RecipeController
    - current_view: BaseView
```

### **Estado das Views**
```python
BaseView:
    - is_created: bool
    - frame: CTkFrame
    - navigation: NavigationProtocol
```

### **Estado dos Dados**
```python
Controllers:
    - Dados ativos em memória
    - Cache de objetos frequentemente acessados
    - Sincronização com storage
```

## 🔧 Configuração e Personalização

### **Configurações de Sistema**
```python
Settings:
    - unidades: Dict (temperatura, volume, peso)
    - interface: Dict (tema, idioma)
    - notificacoes: Dict (alertas, som)
```

### **Temas e Estilos**
```python
BaseView.colors:
    - bg_primary, bg_secondary, bg_tertiary
    - accent_orange, accent_blue
    - text_primary, text_secondary
    - success, warning, border
```

## 🚀 Extensibilidade

### **Adicionando Novas Views**
1. Herdar de `BaseView`
2. Implementar `create_widgets()`
3. Registrar no `BebrewNavigator`
4. Definir conexões no grafo

### **Novos Tipos de Bebida**
1. Criar classe herdando de `Bebida`
2. Implementar cálculos específicos
3. Adicionar views especializadas
4. Configurar controladores

### **Integração Externa**
1. Criar adaptadores na camada de utils
2. Implementar interfaces padronizadas
3. Manter compatibilidade com models existentes

## 🔒 Segurança e Validação

### **Validação de Dados**
- Modelos com validação interna
- Controllers verificam integridade
- Views mostram feedback visual

### **Tratamento de Erros**
- Try-catch em operações críticas
- Fallbacks para dados corrompidos
- Logs de erro para debugging

## 📈 Performance

### **Otimizações**
- Lazy loading de views
- Cache de dados frequentes
- Atualizações incrementais
- Garbage collection adequado

### **Memória**
- Destruição de views não utilizadas
- Limpeza de referências circulares
- Gestão eficiente de objetos temporários

## 🧪 Testabilidade

### **Separação de Responsabilidades**
- Lógica de negócio isolada nos Controllers
- Views testáveis independentemente
- Mocks para dependências externas

### **Injeção de Dependências**
- Controllers recebem dependências via construtor
- Views recebem controllers como parâmetros
- Facilita testes unitários

## 📚 Documentação da API

### **Interfaces Públicas**
```python
NavigationProtocol:
    - navigate_to(view_name: str, **kwargs)
    - go_back()

BrewController:
    - criar_nova_producao(receita: Receita) -> Producao
    - iniciar_producao(producao_id: str) -> bool
    - adicionar_temperatura(producao_id: str, temp: float) -> bool

RecipeController:
    - criar_nova_receita(nome: str, tipo: str, volume: float) -> Receita
    - adicionar_ingrediente(receita_id: str, ingrediente: Ingrediente) -> bool
    - escalar_receita(receita_id: str, novo_volume: float) -> Receita
```

## 🔮 Evolução da Arquitetura

### **Melhorias Planejadas**
- **Persistência**: Banco de dados SQLite
- **Networking**: API REST para sincronização
- **Plugins**: Sistema de extensões
- **Microservices**: Divisão em serviços especializados

### **Refatorações Futuras**
- **Dependency Injection**: Container IoC
- **Event Bus**: Comunicação assíncrona
- **State Management**: Redux-like pattern
- **Reactive Programming**: Observables para dados

---

*Arquitetura projetada para crescer e evoluir com as necessidades da comunidade de produtores artesanais.* 