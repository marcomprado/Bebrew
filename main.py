#!/usr/bin/env python3
"""
Bebrew - Aplicativo para Controle de Produção de Bebidas Fermentadas
Sistema de navegação baseado em grafos com interface CustomTkinter
"""

import customtkinter as ctk
import sys
import os
from typing import Dict, Optional, Any, List
from dataclasses import dataclass

# Importar controladores
from controls.brew_controller import BrewController
from controls.recipe_controller import RecipeController

# Importar views
from view.dashboard_view import DashboardView
from view.base_view import NavigationProtocol

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("dark")

@dataclass
class ViewConfig:
    """Configuração de uma view no grafo de navegação"""
    name: str
    title: str
    icon: str
    view_class: type
    connections: List[str]  # Views que podem ser acessadas desta view

class BebrewNavigator:
    """Sistema de navegação baseado em grafos para o Bebrew"""
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.current_view: Optional[str] = None
        self.view_history: List[str] = []
        self.views: Dict[str, Any] = {}
        
        # Definir o grafo de navegação
        self.setup_navigation_graph()
        
    def setup_navigation_graph(self):
        """Define o grafo de navegação entre as views"""
        self.view_configs = {
            'dashboard': ViewConfig(
                name='dashboard',
                title='Dashboard',
                icon='🏠',
                view_class=DashboardView,
                connections=['nova_receita', 'nova_producao', 'monitoramento', 'receitas', 'historico', 'ingredientes', 'configuracoes']
            ),
            'nova_receita': ViewConfig(
                name='nova_receita',
                title='Nova Receita',
                icon='📝',
                view_class=None,  # Será implementada posteriormente
                connections=['editor_receita', 'dashboard']
            ),
            'editor_receita': ViewConfig(
                name='editor_receita',
                title='Editor de Receita',
                icon='✏️',
                view_class=None,
                connections=['nova_producao', 'receitas', 'dashboard']
            ),
            'nova_producao': ViewConfig(
                name='nova_producao',
                title='Nova Produção',
                icon='🍺',
                view_class=None,
                connections=['monitoramento', 'dashboard']
            ),
            'monitoramento': ViewConfig(
                name='monitoramento',
                title='Monitoramento',
                icon='📊',
                view_class=None,
                connections=['visualizador_producao', 'dashboard']
            ),
            'visualizador_producao': ViewConfig(
                name='visualizador_producao',
                title='Visualizador',
                icon='📈',
                view_class=None,
                connections=['historico', 'dashboard']
            ),
            'historico': ViewConfig(
                name='historico',
                title='Histórico',
                icon='📚',
                view_class=None,
                connections=['visualizador_producao', 'dashboard']
            ),
            'receitas': ViewConfig(
                name='receitas',
                title='Receitas',
                icon='📖',
                view_class=None,
                connections=['editor_receita', 'nova_producao', 'dashboard']
            ),
            'ingredientes': ViewConfig(
                name='ingredientes',
                title='Ingredientes',
                icon='🧪',
                view_class=None,
                connections=['editor_receita', 'dashboard']
            ),
            'configuracoes': ViewConfig(
                name='configuracoes',
                title='Configurações',
                icon='⚙️',
                view_class=None,
                connections=['dashboard']
            )
        }
        
    def can_navigate_to(self, target_view: str) -> bool:
        """Verifica se é possível navegar para a view alvo"""
        # Com menu lateral, sempre é possível navegar
        return target_view in self.view_configs
        
    def navigate_to(self, view_name: str, **kwargs):
        """Navega para uma view específica"""
        if view_name not in self.view_configs:
            print(f"View '{view_name}' não encontrada")
            return False
            
        # Esconder view atual
        if self.current_view and self.current_view in self.views:
            self.views[self.current_view].hide()
            
        # Adicionar à história se não é a mesma view
        if self.current_view and self.current_view != view_name:
            self.view_history.append(self.current_view)
            
        # Criar view se não existe
        if view_name not in self.views:
            config = self.view_configs[view_name]
            if config.view_class:
                self.views[view_name] = config.view_class(
                    self.app.content_frame,
                    self,
                    self.app.brew_controller,
                    self.app.recipe_controller
                )
            else:
                # View não implementada ainda - mostrar placeholder
                self.show_placeholder(view_name)
                return True
                
        # Mostrar nova view
        self.current_view = view_name
        self.views[view_name].show(**kwargs)
        
        # Atualizar sidebar
        self.app.update_sidebar_active(view_name)
        
        return True
        
    def go_back(self):
        """Volta para a view anterior"""
        if not self.view_history:
            # Se não há histórico, vai para o dashboard
            self.navigate_to('dashboard')
            return
            
        previous_view = self.view_history.pop()
        
        # Esconder view atual
        if self.current_view and self.current_view in self.views:
            self.views[self.current_view].hide()
            
        # Mostrar view anterior
        self.current_view = previous_view
        if previous_view in self.views:
            self.views[previous_view].show()
            
        # Atualizar sidebar
        self.app.update_sidebar_active(previous_view)
        
    def show_placeholder(self, view_name: str):
        """Mostra uma tela placeholder para views não implementadas"""
        config = self.view_configs[view_name]
        
        # Criar frame temporário
        temp_frame = ctk.CTkFrame(self.app.content_frame, fg_color='#1a1f2e')
        temp_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ctk.CTkFrame(temp_frame, fg_color='transparent', height=80)
        header_frame.pack(fill='x', padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=config.title,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color='#ffffff'
        )
        title_label.pack(anchor='w', pady=10)
        
        # Conteúdo placeholder
        content_frame = ctk.CTkFrame(temp_frame, fg_color='transparent')
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        placeholder_label = ctk.CTkLabel(
            content_frame,
            text=f"🚧 {config.title}\n\nEsta funcionalidade está em desenvolvimento",
            font=ctk.CTkFont(size=16),
            text_color='#7d8590'
        )
        placeholder_label.pack(expand=True)
        
        # Salvar referência temporária
        self.views[view_name] = type('TempView', (), {
            'frame': temp_frame,
            'hide': lambda: temp_frame.pack_forget(),
            'show': lambda **kwargs: temp_frame.pack(fill='both', expand=True),
            'destroy': lambda: temp_frame.destroy()
        })()
        
        self.current_view = view_name
        self.app.update_sidebar_active(view_name)

class BebrewApp:
    """Aplicação principal do Bebrew"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_main_window()
        
        # Cores do tema
        self.colors = {
            'bg_primary': '#1a1f2e',
            'bg_secondary': '#242937',
            'bg_tertiary': '#2e3444',
            'accent_orange': '#ff6b35',
            'accent_blue': '#4dabf7',
            'text_primary': '#ffffff',
            'text_secondary': '#b8bfc6',
            'border': '#404654'
        }
        
        # Criar layout principal
        self.create_main_layout()
        
        # Inicializar controladores
        self.brew_controller = BrewController()
        self.recipe_controller = RecipeController()
        
        # Inicializar sistema de navegação
        self.navigator = BebrewNavigator(self)
        
        # Criar sidebar
        self.create_sidebar()
        
        # Carregar dados iniciais (se existirem)
        self.load_initial_data()
        
    def setup_main_window(self):
        """Configura a janela principal"""
        self.root.title("Bebrew - Controle de Produção de Bebidas Fermentadas")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Centralizar janela
        self.center_window()
        
        # Configurar protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_main_layout(self):
        """Cria o layout principal com sidebar e área de conteúdo"""
        # Container principal
        main_container = ctk.CTkFrame(self.root, fg_color=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(
            main_container,
            fg_color=self.colors['bg_secondary'],
            width=250,
            corner_radius=0
        )
        self.sidebar_frame.pack(side='left', fill='y')
        self.sidebar_frame.pack_propagate(False)
        
        # Área de conteúdo
        self.content_frame = ctk.CTkFrame(
            main_container,
            fg_color=self.colors['bg_primary'],
            corner_radius=0
        )
        self.content_frame.pack(side='right', fill='both', expand=True)
        
    def create_sidebar(self):
        """Cria o menu lateral"""
        # Logo/Título
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color='transparent', height=100)
        logo_frame.pack(fill='x', padx=20, pady=(20, 0))
        logo_frame.pack_propagate(False)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🍺 Bebrew",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['text_primary']
        )
        logo_label.pack(anchor='w', pady=(20, 0))
        
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Controle de Produção",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(anchor='w')
        
        # Separador
        separator = ctk.CTkFrame(self.sidebar_frame, fg_color=self.colors['border'], height=1)
        separator.pack(fill='x', padx=20, pady=20)
        
        # Menu de navegação
        nav_frame = ctk.CTkFrame(self.sidebar_frame, fg_color='transparent')
        nav_frame.pack(fill='both', expand=True, padx=15)
        
        # Botões de navegação
        self.nav_buttons = {}
        
        # Menu principal
        self.create_nav_section(nav_frame, "Menu Principal", [
            ('dashboard', 'Dashboard', '🏠'),
            ('nova_producao', 'Nova Produção', '🍺'),
            ('monitoramento', 'Monitoramento', '📊'),
        ])
        
        # Gerenciamento
        self.create_nav_section(nav_frame, "Gerenciamento", [
            ('receitas', 'Receitas', '📖'),
            ('ingredientes', 'Ingredientes', '🧪'),
            ('historico', 'Histórico', '📚'),
        ])
        
        # Sistema
        self.create_nav_section(nav_frame, "Sistema", [
            ('configuracoes', 'Configurações', '⚙️'),
        ])
        
        # Footer do sidebar
        footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color='transparent', height=60)
        footer_frame.pack(fill='x', padx=20, pady=10)
        footer_frame.pack_propagate(False)
        
        version_label = ctk.CTkLabel(
            footer_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        )
        version_label.pack(side='bottom')
        
    def create_nav_section(self, parent, title, items):
        """Cria uma seção de navegação no sidebar"""
        # Título da seção
        section_label = ctk.CTkLabel(
            parent,
            text=title.upper(),
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors['text_secondary']
        )
        section_label.pack(anchor='w', pady=(15, 5))
        
        # Botões
        for view_name, label, icon in items:
            btn = ctk.CTkButton(
                parent,
                text=f"{icon}  {label}",
                command=lambda v=view_name: self.navigator.navigate_to(v),
                fg_color='transparent',
                hover_color=self.colors['bg_tertiary'],
                text_color=self.colors['text_secondary'],
                anchor='w',
                font=ctk.CTkFont(size=14),
                corner_radius=8,
                height=45
            )
            btn.pack(fill='x', pady=2)
            self.nav_buttons[view_name] = btn
            
    def update_sidebar_active(self, active_view: str):
        """Atualiza o botão ativo no sidebar"""
        for view_name, btn in self.nav_buttons.items():
            if view_name == active_view:
                btn.configure(
                    fg_color=self.colors['bg_tertiary'],
                    text_color=self.colors['text_primary']
                )
                # Adicionar indicador
                if not hasattr(btn, '_indicator'):
                    btn._indicator = ctk.CTkFrame(btn, fg_color=self.colors['accent_orange'], width=3)
                    btn._indicator.place(x=0, y=5, relheight=0.8)
            else:
                btn.configure(
                    fg_color='transparent',
                    text_color=self.colors['text_secondary']
                )
                # Remover indicador
                if hasattr(btn, '_indicator'):
                    btn._indicator.destroy()
                    delattr(btn, '_indicator')
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def load_initial_data(self):
        """Carrega dados iniciais da aplicação"""
        # Aqui você pode carregar receitas salvas, configurações, etc.
        # Por enquanto, criar algumas receitas de exemplo
        self.create_sample_data()
        
    def create_sample_data(self):
        """Cria dados de exemplo para demonstração"""
        # Receita de cerveja exemplo
        cerveja = self.recipe_controller.criar_nova_receita(
            "IPA Tropical",
            "cerveja",
            20.0,
            "Cerveja IPA com lúpulos tropicais"
        )
        cerveja.og = 1.065
        cerveja.fg = 1.012
        cerveja.abv = 6.9
        cerveja.ibu = 45
        cerveja.dificuldade = "Intermediário"
        
        # Adicionar ingredientes
        self.recipe_controller.adicionar_ingrediente(
            cerveja.id, "Malte Pilsen", "malte", "kg", 4.5
        )
        self.recipe_controller.adicionar_ingrediente(
            cerveja.id, "Malte Crystal 60L", "malte", "kg", 0.5
        )
        self.recipe_controller.adicionar_ingrediente(
            cerveja.id, "Lúpulo Citra", "lúpulo", "g", 30
        )
        self.recipe_controller.adicionar_ingrediente(
            cerveja.id, "Lúpulo Mosaic", "lúpulo", "g", 25
        )
        self.recipe_controller.adicionar_ingrediente(
            cerveja.id, "Fermento Safale US-05", "fermento", "un", 1
        )
        
        # Adicionar etapas
        self.recipe_controller.adicionar_etapa(
            cerveja.id, "Mostura", "Mosturação dos maltes", 60, 67.0
        )
        self.recipe_controller.adicionar_etapa(
            cerveja.id, "Fervura", "Fervura do mosto com lúpulos", 60, 100.0
        )
        self.recipe_controller.adicionar_etapa(
            cerveja.id, "Resfriamento", "Resfriar mosto até temperatura de fermentação", 30, 20.0
        )
        self.recipe_controller.adicionar_etapa(
            cerveja.id, "Fermentação Primária", "Fermentação principal", 10080, 18.0  # 7 dias
        )
        
        # Receita de hidromel exemplo
        hidromel = self.recipe_controller.criar_nova_receita(
            "Hidromel Tradicional",
            "hidromel", 
            5.0,
            "Hidromel tradicional com mel de flores silvestres"
        )
        hidromel.og = 1.100
        hidromel.fg = 1.010
        hidromel.abv = 11.8
        hidromel.dificuldade = "Iniciante"
        
        self.recipe_controller.adicionar_ingrediente(
            hidromel.id, "Mel de Flores Silvestres", "mel", "kg", 1.5
        )
        self.recipe_controller.adicionar_ingrediente(
            hidromel.id, "Fermento Lallemand DistilaMax MW", "fermento", "un", 1
        )
        self.recipe_controller.adicionar_ingrediente(
            hidromel.id, "Nutriente de Fermento", "nutriente", "g", 5
        )
        
        self.recipe_controller.adicionar_etapa(
            hidromel.id, "Dissolução", "Dissolver mel em água morna", 30, 40.0
        )
        self.recipe_controller.adicionar_etapa(
            hidromel.id, "Resfriamento", "Resfriar mosto até temperatura de fermentação", 60, 20.0
        )
        self.recipe_controller.adicionar_etapa(
            hidromel.id, "Fermentação", "Fermentação principal", 20160, 18.0  # 14 dias
        )
        
    def on_closing(self):
        """Callback para fechamento da aplicação"""
        # Aqui você pode salvar dados antes de fechar
        self.save_data()
        self.root.quit()
        self.root.destroy()
        
    def save_data(self):
        """Salva dados da aplicação"""
        # Implementar salvamento de receitas, configurações, etc.
        pass
        
    def run(self):
        """Inicia a aplicação"""
        # Navegar para o dashboard inicial
        self.navigator.navigate_to('dashboard')
        
        # Iniciar loop principal
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        # Verificar dependências
        required_modules = ['customtkinter', 'matplotlib', 'numpy']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
                
        if missing_modules:
            print("Módulos necessários não encontrados:")
            for module in missing_modules:
                print(f"  - {module}")
            print("\nInstale os módulos com:")
            print(f"pip install {' '.join(missing_modules)}")
            return 1
            
        # Criar e executar aplicação
        app = BebrewApp()
        app.run()
        
        return 0
        
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário")
        return 0
    except Exception as e:
        print(f"Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
