import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
from util.mock_data_loader import mock_loader

class RecipeView(BaseView):
    """View para gerenciamento de receitas"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Receitas")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Widgets principais
        self.search_entry = None
        self.type_filter = None
        self.recipe_list_frame = None
        self.recipes_data = []
        
    def create_widgets(self):
        """Cria os widgets da view de receitas"""
        # Header
        header = self.create_header(self.frame, "Receitas", "Gerencie suas receitas de bebidas fermentadas")
        
        # Botão nova receita no header
        new_recipe_btn = self.create_button(
            header,
            "Nova Receita",
            self.on_new_recipe,
            style='solid_primary',
            icon="➕",
            width=140,
            height=40
        )
        new_recipe_btn.pack(side='right', padx=(0, 30))
        
        # Container principal com scroll
        self.main_scroll = ctk.CTkScrollableFrame(
            self.frame, 
            fg_color='transparent'
        )
        self.main_scroll.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Seção de filtros
        self.create_filter_section()
        
        # Lista de receitas
        self.create_recipe_list_section()
        
    def create_filter_section(self):
        """Cria a seção de filtros e busca"""
        filter_card = self.create_card(self.main_scroll, padding=20)
        filter_card.pack(fill='x', pady=(0, 20))
        
        # Container de filtros
        filter_container = ctk.CTkFrame(filter_card, fg_color='transparent')
        filter_container.pack(fill='x', padx=20, pady=20)
        
        # Grid para organizar filtros
        filter_container.grid_columnconfigure(0, weight=3)  # Busca
        filter_container.grid_columnconfigure(1, weight=1)  # Tipo
        filter_container.grid_columnconfigure(2, weight=1)  # Dificuldade
        filter_container.grid_columnconfigure(3, weight=0)  # Botão
        
        # Campo de busca
        search_label = self.create_label(filter_container, "Buscar receita:", 'body_secondary')
        search_label.grid(row=0, column=0, sticky='w', padx=(0, 10), pady=(0, 5))
        
        self.search_entry = self.create_input(
            filter_container,
            placeholder="Nome da receita...",
            width=300
        )
        self.search_entry.grid(row=1, column=0, sticky='ew', padx=(0, 20))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_recipes())
        
        # Filtro por tipo
        type_label = self.create_label(filter_container, "Tipo:", 'body_secondary')
        type_label.grid(row=0, column=1, sticky='w', padx=(0, 10), pady=(0, 5))
        
        tipos = ["Todos"] + mock_loader.get_tipos_bebida()
        self.type_filter = ctk.CTkComboBox(
            filter_container,
            values=tipos,
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md'],
            command=self.on_filter_change
        )
        self.type_filter.grid(row=1, column=1, sticky='ew', padx=(0, 20))
        self.type_filter.set("Todos")
        
        # Filtro por dificuldade
        diff_label = self.create_label(filter_container, "Dificuldade:", 'body_secondary')
        diff_label.grid(row=0, column=2, sticky='w', padx=(0, 10), pady=(0, 5))
        
        self.diff_filter = ctk.CTkComboBox(
            filter_container,
            values=["Todas", "Iniciante", "Intermediário", "Avançado"],
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md'],
            command=self.on_filter_change
        )
        self.diff_filter.grid(row=1, column=2, sticky='ew', padx=(0, 20))
        self.diff_filter.set("Todas")
        
        # Botão limpar filtros
        clear_btn = self.create_button(
            filter_container,
            "Limpar",
            self.clear_filters,
            style='secondary',
            width=100,
            height=35
        )
        clear_btn.grid(row=1, column=3, padx=(0, 0))
        
    def create_recipe_list_section(self):
        """Cria a seção de lista de receitas"""
        # Container da lista
        list_card = self.create_card(self.main_scroll, title="Minhas Receitas", padding=0)
        list_card.pack(fill='both', expand=True)
        
        # Frame para a lista
        self.recipe_list_frame = ctk.CTkFrame(list_card, fg_color='transparent')
        self.recipe_list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Carregar receitas
        self.load_recipes()
        
    def create_recipe_item(self, parent, recipe_data: Dict):
        """Cria um item de receita na lista"""
        # Container do item
        item_frame = ctk.CTkFrame(
            parent, 
            fg_color=self.colors['bg_tertiary'],
            corner_radius=12,
            height=120
        )
        item_frame.pack(fill='x', pady=8)
        item_frame.pack_propagate(False)
        
        # Container interno com padding
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Grid para organizar conteúdo
        inner.grid_columnconfigure(0, weight=1)  # Info
        inner.grid_columnconfigure(1, weight=0)  # Ações
        
        # Container de informações
        info_frame = ctk.CTkFrame(inner, fg_color='transparent')
        info_frame.grid(row=0, column=0, sticky='ew')
        
        # Primeira linha: Nome e badges
        top_row = ctk.CTkFrame(info_frame, fg_color='transparent')
        top_row.pack(fill='x', pady=(0, 8))
        
        # Nome da receita
        name_label = self.create_label(
            top_row,
            recipe_data.get('nome', 'N/A'),
            'heading_sm'
        )
        name_label.pack(side='left', padx=(0, 15))
        
        # Badge do tipo
        type_badge = ctk.CTkLabel(
            top_row,
            text=recipe_data.get('tipo', 'N/A').upper(),
            font=self.fonts['caption'],
            text_color=self.colors['text_primary'],
            fg_color=self.colors['accent_blue'],
            corner_radius=4,
            padx=10,
            pady=3
        )
        type_badge.pack(side='left', padx=(0, 10))
        
        # Badge de dificuldade
        diff_colors = {
            'Iniciante': self.colors['success'],
            'Intermediário': self.colors['accent_orange'],
            'Avançado': self.colors['warning']
        }
        diff_color = diff_colors.get(recipe_data.get('dificuldade', ''), self.colors['text_muted'])
        
        diff_badge = ctk.CTkLabel(
            top_row,
            text=recipe_data.get('dificuldade', 'N/A'),
            font=self.fonts['caption'],
            text_color=self.colors['text_primary'],
            fg_color=diff_color,
            corner_radius=4,
            padx=10,
            pady=3
        )
        diff_badge.pack(side='left')
        
        # Segunda linha: Descrição
        if recipe_data.get('descricao'):
            desc_label = self.create_label(
                info_frame,
                recipe_data.get('descricao', ''),
                'body_secondary'
            )
            desc_label.pack(anchor='w', pady=(0, 8))
        
        # Terceira linha: Detalhes técnicos
        details_frame = ctk.CTkFrame(info_frame, fg_color='transparent')
        details_frame.pack(anchor='w')
        
        details_text = f"Volume: {recipe_data.get('volume', 0)}L  •  "
        details_text += f"ABV: {recipe_data.get('abv', 0):.1f}%  •  "
        
        if recipe_data.get('ibu'):
            details_text += f"IBU: {recipe_data.get('ibu', 0)}  •  "
        
        details_text += f"Ingredientes: {len(recipe_data.get('ingredientes', []))}  •  "
        details_text += f"Etapas: {len(recipe_data.get('etapas', []))}"
        
        details_label = self.create_label(details_frame, details_text, 'caption')
        details_label.pack(side='left')
        
        # Container de ações
        actions_frame = ctk.CTkFrame(inner, fg_color='transparent')
        actions_frame.grid(row=0, column=1, padx=(20, 0))
        
        # Botões de ação
        view_btn = self.create_button(
            actions_frame,
            "Visualizar",
            lambda: self.on_view_recipe(recipe_data['id']),
            style='secondary',
            width=100,
            height=35
        )
        view_btn.pack(pady=(0, 5))
        
        edit_btn = self.create_button(
            actions_frame,
            "Editar",
            lambda: self.on_edit_recipe(recipe_data['id']),
            style='primary',
            width=100,
            height=35
        )
        edit_btn.pack(pady=(0, 5))
        
        brew_btn = self.create_button(
            actions_frame,
            "Produzir",
            lambda: self.on_brew_recipe(recipe_data['id']),
            style='solid_primary',
            width=100,
            height=35
        )
        brew_btn.pack()
        
    def load_recipes(self):
        """Carrega as receitas do mock data"""
        self.recipes_data = mock_loader.get_receitas()
        self.display_recipes(self.recipes_data)
        
    def display_recipes(self, recipes: List[Dict]):
        """Exibe as receitas na lista"""
        # Limpar lista atual
        for widget in self.recipe_list_frame.winfo_children():
            widget.destroy()
            
        if not recipes:
            no_recipes_label = self.create_label(
                self.recipe_list_frame,
                "Nenhuma receita encontrada",
                'body_secondary'
            )
            no_recipes_label.pack(pady=40)
        else:
            for recipe in recipes:
                self.create_recipe_item(self.recipe_list_frame, recipe)
                
    def filter_recipes(self):
        """Filtra as receitas baseado nos critérios"""
        search_term = self.search_entry.get().lower()
        type_filter = self.type_filter.get()
        diff_filter = self.diff_filter.get()
        
        filtered = self.recipes_data
        
        # Filtro por busca
        if search_term:
            filtered = [r for r in filtered if search_term in r.get('nome', '').lower()]
        
        # Filtro por tipo
        if type_filter != "Todos":
            filtered = [r for r in filtered if r.get('tipo') == type_filter]
        
        # Filtro por dificuldade
        if diff_filter != "Todas":
            filtered = [r for r in filtered if r.get('dificuldade') == diff_filter]
        
        self.display_recipes(filtered)
        
    def on_filter_change(self, value):
        """Callback para mudança nos filtros"""
        self.filter_recipes()
        
    def clear_filters(self):
        """Limpa todos os filtros"""
        self.search_entry.delete(0, 'end')
        self.type_filter.set("Todos")
        self.diff_filter.set("Todas")
        self.filter_recipes()
        
    def on_new_recipe(self):
        """Navega para criar nova receita"""
        self.navigation.navigate_to('nova_receita')
        
    def on_view_recipe(self, recipe_id: str):
        """Visualiza detalhes da receita"""
        self.navigation.navigate_to('visualizar_receita', recipe_id=recipe_id)
        
    def on_edit_recipe(self, recipe_id: str):
        """Edita uma receita"""
        self.navigation.navigate_to('editor_receita', recipe_id=recipe_id)
        
    def on_brew_recipe(self, recipe_id: str):
        """Inicia produção com a receita"""
        self.navigation.navigate_to('nova_producao', recipe_id=recipe_id)
        
    def on_show(self, **kwargs):
        """Callback quando a view é exibida"""
        self.load_recipes()
        
    def refresh(self):
        """Atualiza a lista de receitas"""
        self.load_recipes()
