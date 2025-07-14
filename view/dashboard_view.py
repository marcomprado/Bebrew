import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class DashboardView(BaseView):
    """View principal do dashboard do Bebrew"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Dashboard")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Widgets principais
        self.stats_cards = {}
        self.production_list = None
        self.recipe_list = None
        
    def create_widgets(self):
        """Cria os widgets do dashboard"""
        # Header
        self.create_header(self.frame, "Dashboard", "Visão geral do sistema")
        
        # Container principal com scroll
        self.main_scroll = ctk.CTkScrollableFrame(
            self.frame, 
            fg_color='transparent'
        )
        self.main_scroll.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Cards de estatísticas
        self.create_stats_section()
        
        # Seção de produções ativas
        self.create_active_productions_section()
        
        # Seção de receitas recentes
        self.create_recent_recipes_section()
        
        # Gráfico de resumo
        self.create_summary_chart_section()
        
    def create_stats_section(self):
        """Cria a seção de cards de estatísticas"""
        stats_container = ctk.CTkFrame(self.main_scroll, fg_color='transparent')
        stats_container.pack(fill='x', pady=(0, 20))
        
        # Grid de estatísticas
        stats_grid = ctk.CTkFrame(stats_container, fg_color='transparent')
        stats_grid.pack(fill='x')
        
        # Configurar grid com 4 colunas
        for i in range(4):
            stats_grid.grid_columnconfigure(i, weight=1, uniform="stats")
        
        # Cards de estatísticas
        stats_data = [
            ("Produções Ativas", "0", "🍺", self.colors['accent_orange']),
            ("Receitas Salvas", "0", "📖", self.colors['accent_blue']),
            ("ABV Médio", "0.0%", "📊", self.colors['success']),
            ("Última Produção", "Nenhuma", "⏰", self.colors['text_secondary'])
        ]
        
        for idx, (label, value, icon, color) in enumerate(stats_data):
            card = self.create_stat_card(stats_grid, label, value, icon, color)
            card.grid(row=0, column=idx, padx=10, sticky='ew')
            self.stats_cards[label] = card
            
    def create_active_productions_section(self):
        """Cria a seção de produções ativas"""
        # Título da seção
        section_header = ctk.CTkFrame(self.main_scroll, fg_color='transparent')
        section_header.pack(fill='x', pady=(0, 10))
        
        title_label = self.create_label(
            section_header, 
            "Produções Ativas", 
            'heading_md'
        )
        title_label.pack(side='left')
        
        new_production_btn = self.create_button(
            section_header,
            "Nova Produção",
            lambda: self.navigation.navigate_to('nova_producao'),
            style='primary',
            icon="➕",
            width=140,
            height=35
        )
        new_production_btn.pack(side='right')
        
        # Card container
        card_container = self.create_card(self.main_scroll, padding=0)
        card_container.pack(fill='x', pady=(0, 20))
        
        # Lista de produções
        self.production_list = ctk.CTkFrame(card_container, fg_color='transparent')
        self.production_list.pack(fill='both', expand=True, padx=20, pady=20)
        
    def create_recent_recipes_section(self):
        """Cria a seção de receitas recentes"""
        # Título da seção
        section_header = ctk.CTkFrame(self.main_scroll, fg_color='transparent')
        section_header.pack(fill='x', pady=(0, 10))
        
        title_label = self.create_label(
            section_header, 
            "Receitas Recentes", 
            'heading_md'
        )
        title_label.pack(side='left')
        
        new_recipe_btn = self.create_button(
            section_header,
            "Nova Receita",
            lambda: self.navigation.navigate_to('nova_receita'),
            style='secondary',
            icon="➕",
            width=130,
            height=35
        )
        new_recipe_btn.pack(side='right')
        
        # Card container
        card_container = self.create_card(self.main_scroll, padding=0)
        card_container.pack(fill='x', pady=(0, 20))
        
        # Lista de receitas
        self.recipe_list = ctk.CTkFrame(card_container, fg_color='transparent')
        self.recipe_list.pack(fill='both', expand=True, padx=20, pady=20)
        
    def create_summary_chart_section(self):
        """Cria a seção de gráfico resumo"""
        # Título da seção
        title_label = self.create_label(
            self.main_scroll, 
            "Resumo de Atividades", 
            'heading_md'
        )
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Card para o gráfico
        chart_card = self.create_card(self.main_scroll, padding=20)
        chart_card.pack(fill='x')
        
        # Placeholder para gráfico
        chart_placeholder = ctk.CTkLabel(
            chart_card,
            text="📈 Gráfico de resumo será exibido aqui",
            font=self.fonts['body_md'],
            text_color=self.colors['text_muted'],
            height=200
        )
        chart_placeholder.pack(expand=True)
        
    def create_production_item(self, parent, production_data: Dict):
        """Cria um item de produção na lista"""
        # Container do item
        item_frame = ctk.CTkFrame(
            parent, 
            fg_color=self.colors['bg_tertiary'],
            corner_radius=8,
            height=80
        )
        item_frame.pack(fill='x', pady=5)
        item_frame.pack_propagate(False)
        
        # Container interno
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Informações
        info_frame = ctk.CTkFrame(inner, fg_color='transparent')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Nome e lote
        name_label = self.create_label(
            info_frame,
            f"{production_data.get('receita_nome', 'N/A')} - Lote {production_data.get('lote', 'N/A')}",
            'heading_sm'
        )
        name_label.pack(anchor='w')
        
        # Status
        status_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        status_frame.pack(anchor='w', pady=(5, 0))
        
        status_label = self.create_label(
            status_frame,
            f"Status: {production_data.get('status', 'N/A')}",
            'body_secondary'
        )
        status_label.pack(side='left', padx=(0, 15))
        
        # Barra de progresso
        progress_value = production_data.get('progresso', 0) / 100
        progress_bar = ctk.CTkProgressBar(
            status_frame,
            width=100,
            height=8,
            progress_color=self.colors['accent_orange'],
            fg_color=self.colors['bg_secondary']
        )
        progress_bar.pack(side='left', padx=(0, 10))
        progress_bar.set(progress_value)
        
        progress_label = self.create_label(
            status_frame,
            f"{production_data.get('progresso', 0):.0f}%",
            'caption'
        )
        progress_label.pack(side='left')
        
        # Botões
        actions_frame = ctk.CTkFrame(inner, fg_color='transparent')
        actions_frame.pack(side='right')
        
        monitor_btn = self.create_button(
            actions_frame,
            "Monitorar",
            lambda: self.navigation.navigate_to('monitoramento', production_id=production_data.get('lote')),
            style='primary',
            width=100,
            height=35
        )
        monitor_btn.pack()
        
    def create_recipe_item(self, parent, recipe_data: Dict):
        """Cria um item de receita na lista"""
        # Container do item
        item_frame = ctk.CTkFrame(
            parent, 
            fg_color=self.colors['bg_tertiary'],
            corner_radius=8,
            height=80
        )
        item_frame.pack(fill='x', pady=5)
        item_frame.pack_propagate(False)
        
        # Container interno
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Informações
        info_frame = ctk.CTkFrame(inner, fg_color='transparent')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Nome e tipo
        name_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        name_frame.pack(anchor='w')
        
        name_label = self.create_label(
            name_frame,
            recipe_data.get('nome', 'N/A'),
            'heading_sm'
        )
        name_label.pack(side='left', padx=(0, 10))
        
        # Badge do tipo
        type_badge = ctk.CTkLabel(
            name_frame,
            text=recipe_data.get('tipo', 'N/A').upper(),
            font=self.fonts['caption'],
            text_color=self.colors['text_primary'],
            fg_color=self.colors['accent_blue'],
            corner_radius=4,
            padx=8,
            pady=2
        )
        type_badge.pack(side='left')
        
        # Detalhes
        details_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        details_frame.pack(anchor='w', pady=(5, 0))
        
        details_text = f"Volume: {recipe_data.get('volume', 0)}L  •  ABV: {recipe_data.get('abv', 0):.1f}%"
        details_label = self.create_label(details_frame, details_text, 'body_secondary')
        details_label.pack(side='left')
        
        # Botões
        actions_frame = ctk.CTkFrame(inner, fg_color='transparent')
        actions_frame.pack(side='right')
        
        # Container horizontal para botões
        buttons_row = ctk.CTkFrame(actions_frame, fg_color='transparent')
        buttons_row.pack()
        
        edit_btn = self.create_button(
            buttons_row,
            "Editar",
            lambda: self.navigation.navigate_to('editor_receita', recipe_id=recipe_data.get('id')),
            style='secondary',
            width=80,
            height=35
        )
        edit_btn.pack(side='left', padx=(0, 5))
        
        brew_btn = self.create_button(
            buttons_row,
            "Produzir",
            lambda: self.navigation.navigate_to('nova_producao', recipe_id=recipe_data.get('id')),
            style='solid_primary',
            width=90,
            height=35
        )
        brew_btn.pack(side='left')
        
    def update_stats(self):
        """Atualiza as estatísticas do dashboard"""
        # Produções ativas
        active_count = len(self.brew_controller.producoes_ativas)
        self.update_stat_card("Produções Ativas", str(active_count))
        
        # Receitas salvas
        recipe_count = len(self.recipe_controller.receitas)
        self.update_stat_card("Receitas Salvas", str(recipe_count))
        
        # ABV médio
        stats = self.recipe_controller.obter_estatisticas_receitas()
        abv_medio = f"{stats.get('abv_medio', 0):.1f}%"
        self.update_stat_card("ABV Médio", abv_medio)
        
        # Última produção
        last_production = "Nenhuma"
        if self.brew_controller.producao_atual:
            last_production = self.brew_controller.producao_atual.lote
        self.update_stat_card("Última Produção", last_production)
        
    def update_stat_card(self, label: str, new_value: str):
        """Atualiza o valor de um card de estatística"""
        if label in self.stats_cards:
            card = self.stats_cards[label]
            # Encontrar o label de valor dentro do card
            for widget in card.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkLabel) and child.cget("font") == self.fonts['heading_lg']:
                            child.configure(text=new_value)
                            break
                            
    def update_active_productions(self):
        """Atualiza a lista de produções ativas"""
        # Limpar lista atual
        for widget in self.production_list.winfo_children():
            widget.destroy()
            
        # Obter produções ativas
        productions = self.brew_controller.listar_producoes_ativas()
        
        if not productions:
            no_productions_label = self.create_label(
                self.production_list,
                "Nenhuma produção ativa no momento",
                'body_secondary'
            )
            no_productions_label.pack(pady=40)
        else:
            for production in productions:
                # Adicionar nome da receita aos dados
                if production.get('lote') in self.brew_controller.producoes_ativas:
                    producao_obj = self.brew_controller.producoes_ativas[production.get('lote')]
                    production['receita_nome'] = producao_obj.receita.nome
                    
                self.create_production_item(self.production_list, production)
                
    def update_recent_recipes(self):
        """Atualiza a lista de receitas recentes"""
        # Limpar lista atual
        for widget in self.recipe_list.winfo_children():
            widget.destroy()
            
        # Obter receitas recentes (últimas 5)
        recipes = self.recipe_controller.listar_receitas("data")[:5]
        
        if not recipes:
            no_recipes_label = self.create_label(
                self.recipe_list,
                "Nenhuma receita cadastrada ainda",
                'body_secondary'
            )
            no_recipes_label.pack(pady=40)
        else:
            for recipe in recipes:
                recipe_data = {
                    'id': recipe.id,
                    'nome': recipe.nome,
                    'tipo': recipe.tipo,
                    'volume': recipe.volume,
                    'abv': recipe.abv or 0
                }
                self.create_recipe_item(self.recipe_list, recipe_data)
                
    def on_show(self, **kwargs):
        """Callback chamado quando a view é exibida"""
        self.refresh()
        
    def refresh(self):
        """Atualiza todos os dados do dashboard"""
        self.update_stats()
        self.update_active_productions()
        self.update_recent_recipes()
