import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
from util.mock_data_loader import mock_loader
import uuid

class IngredientsView(BaseView):
    """View para gerenciamento de ingredientes"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Ingredientes")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Dados de ingredientes
        self.ingredients_data = {}
        self.selected_category = "Todos"
        
        # Widgets principais
        self.search_entry = None
        self.category_buttons = {}
        self.ingredients_list_frame = None
        
    def create_widgets(self):
        """Cria os widgets da view de ingredientes"""
        # Header
        header = self.create_header(
            self.frame, 
            "Ingredientes", 
            "Gerencie os ingredientes disponíveis para suas receitas"
        )
        
        # Botão adicionar no header
        add_btn = self.create_button(
            header,
            "Adicionar Ingrediente",
            self.show_add_ingredient_dialog,
            style='solid_primary',
            icon="➕",
            width=160,
            height=40
        )
        add_btn.pack(side='right', padx=(0, 30))
        
        # Container principal
        main_container = ctk.CTkFrame(self.frame, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Grid principal
        main_container.grid_columnconfigure(0, weight=0)  # Categorias
        main_container.grid_columnconfigure(1, weight=1)  # Lista
        main_container.grid_rowconfigure(0, weight=1)
        
        # Seção de categorias (esquerda)
        self.create_categories_section(main_container)
        
        # Seção principal (direita)
        self.create_main_section(main_container)
        
    def create_categories_section(self, parent):
        """Cria a seção de categorias"""
        categories_card = self.create_card(parent, title="Categorias", padding=20)
        categories_card.grid(row=0, column=0, sticky='nsew', padx=(0, 20))
        
        content = ctk.CTkFrame(categories_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Categorias disponíveis
        categories = [
            ("Todos", "📦", None),
            ("Maltes", "🌾", "malte"),
            ("Lúpulos", "🌿", "lúpulo"),
            ("Fermentos", "🧫", "fermento"),
            ("Açúcares", "🍯", "açúcar"),
            ("Mel", "🍯", "mel"),
            ("Especiarias", "🌶️", "especiaria"),
            ("Adjuntos", "🌽", "adjunto"),
            ("Nutrientes", "💊", "nutriente"),
            ("Outros", "📦", "outro")
        ]
        
        for label, icon, category in categories:
            btn = self.create_category_button(content, label, icon, category)
            btn.pack(fill='x', pady=5)
            self.category_buttons[category or "Todos"] = btn
            
        # Destacar categoria inicial
        self.highlight_category("Todos")
        
    def create_category_button(self, parent, label: str, icon: str, category: Optional[str]):
        """Cria um botão de categoria"""
        btn = ctk.CTkButton(
            parent,
            text=f"{icon}  {label}",
            command=lambda: self.select_category(category or "Todos"),
            fg_color='transparent',
            hover_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_secondary'],
            anchor='w',
            font=self.fonts['body_md'],
            corner_radius=8,
            height=40,
            width=180
        )
        return btn
        
    def create_main_section(self, parent):
        """Cria a seção principal com busca e lista"""
        main_container = ctk.CTkFrame(parent, fg_color='transparent')
        main_container.grid(row=0, column=1, sticky='nsew')
        
        # Card de busca
        search_card = self.create_card(main_container, padding=20)
        search_card.pack(fill='x', pady=(0, 20))
        
        search_content = ctk.CTkFrame(search_card, fg_color='transparent')
        search_content.pack(fill='x', padx=20, pady=20)
        
        # Campo de busca
        search_frame = ctk.CTkFrame(search_content, fg_color='transparent')
        search_frame.pack(fill='x')
        
        search_label = self.create_label(search_frame, "Buscar ingrediente:", 'body_secondary')
        search_label.pack(side='left', padx=(0, 10))
        
        self.search_entry = self.create_input(
            search_frame, 
            placeholder="Nome do ingrediente...",
            width=300
        )
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_ingredients())
        
        # Card da lista
        list_card = self.create_card(main_container, title="Lista de Ingredientes", padding=0)
        list_card.pack(fill='both', expand=True)
        
        # Lista de ingredientes
        self.ingredients_list_frame = ctk.CTkScrollableFrame(
            list_card,
            fg_color='transparent'
        )
        self.ingredients_list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Carregar ingredientes
        self.load_ingredients()
        
    def highlight_category(self, category: str):
        """Destaca a categoria selecionada"""
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.configure(
                    fg_color=self.colors['bg_tertiary'],
                    text_color=self.colors['text_primary']
                )
            else:
                btn.configure(
                    fg_color='transparent',
                    text_color=self.colors['text_secondary']
                )
                
    def select_category(self, category: str):
        """Seleciona uma categoria"""
        self.selected_category = category
        self.highlight_category(category)
        self.filter_ingredients()
        
    def load_ingredients(self):
        """Carrega os ingredientes dos dados mock"""
        # Obter ingredientes únicos de todas as receitas
        self.ingredients_data = mock_loader.get_ingredientes_unicos()
        
        # Adicionar alguns ingredientes extras para demonstração
        extra_ingredients = {
            'malte': ['Malte Vienna', 'Malte Caramelo 120L', 'Malte Torrado', 'Malte de Trigo'],
            'lúpulo': ['Lúpulo Cascade', 'Lúpulo Centennial', 'Lúpulo Simcoe', 'Lúpulo Amarillo'],
            'fermento': ['Fermento Lallemand BRY-97', 'Fermento SafLager W-34/70', 'Fermento Red Star Premier Rouge'],
            'especiaria': ['Canela em Pau', 'Gengibre Fresco', 'Pimenta da Jamaica', 'Cardamomo']
        }
        
        for tipo, ingredientes in extra_ingredients.items():
            if tipo in self.ingredients_data:
                self.ingredients_data[tipo].extend(ingredientes)
                self.ingredients_data[tipo] = sorted(list(set(self.ingredients_data[tipo])))
            else:
                self.ingredients_data[tipo] = sorted(ingredientes)
                
        self.display_ingredients()
        
    def display_ingredients(self):
        """Exibe os ingredientes filtrados"""
        # Limpar lista
        for widget in self.ingredients_list_frame.winfo_children():
            widget.destroy()
            
        # Filtrar por categoria
        if self.selected_category == "Todos":
            filtered_data = self.ingredients_data
        else:
            filtered_data = {
                k: v for k, v in self.ingredients_data.items() 
                if k == self.selected_category
            }
            
        # Filtrar por busca
        search_term = self.search_entry.get().lower() if hasattr(self, 'search_entry') else ""
        
        if not filtered_data:
            no_ingredients = self.create_label(
                self.ingredients_list_frame,
                "Nenhum ingrediente encontrado",
                'body_secondary'
            )
            no_ingredients.pack(pady=40)
            return
            
        # Exibir por categoria
        for categoria, ingredientes in sorted(filtered_data.items()):
            # Filtrar ingredientes por busca
            if search_term:
                ingredientes = [i for i in ingredientes if search_term in i.lower()]
                
            if not ingredientes:
                continue
                
            # Título da categoria
            cat_frame = ctk.CTkFrame(self.ingredients_list_frame, fg_color='transparent')
            cat_frame.pack(fill='x', pady=(0, 10))
            
            cat_label = self.create_label(
                cat_frame,
                categoria.upper(),
                'heading_sm'
            )
            cat_label.pack(anchor='w', pady=(10, 5))
            
            # Grid de ingredientes
            grid_frame = ctk.CTkFrame(cat_frame, fg_color='transparent')
            grid_frame.pack(fill='x')
            
            # Configurar grid com 3 colunas
            for i in range(3):
                grid_frame.grid_columnconfigure(i, weight=1, uniform="ingredients")
                
            # Adicionar ingredientes
            for idx, ingrediente in enumerate(ingredientes):
                self.create_ingredient_item(grid_frame, ingrediente, categoria, idx)
                
    def create_ingredient_item(self, parent, ingredient: str, category: str, index: int):
        """Cria um item de ingrediente"""
        row = index // 3
        col = index % 3
        
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_tertiary'],
            corner_radius=8,
            height=50
        )
        item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Nome do ingrediente
        name_label = self.create_label(inner, ingredient, 'body')
        name_label.pack(side='left')
        
        # Botões de ação
        action_frame = ctk.CTkFrame(inner, fg_color='transparent')
        action_frame.pack(side='right')
        
        # Botão editar
        edit_btn = ctk.CTkButton(
            action_frame,
            text="✏️",
            command=lambda: self.edit_ingredient(ingredient, category),
            fg_color='transparent',
            hover_color=self.colors['bg_secondary'],
            width=30,
            height=30
        )
        edit_btn.pack(side='left', padx=(0, 5))
        
    def show_add_ingredient_dialog(self):
        """Mostra diálogo para adicionar ingrediente"""
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Adicionar Ingrediente")
        dialog.geometry("450x350")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Container principal
        main_frame = ctk.CTkFrame(dialog, fg_color=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = self.create_label(main_frame, "Novo Ingrediente", 'heading_md')
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Nome
        name_label = self.create_label(main_frame, "Nome:*", 'body_secondary')
        name_label.pack(anchor='w', pady=(0, 5))
        
        name_entry = self.create_input(main_frame, placeholder="Ex: Malte Pilsen Premium")
        name_entry.pack(fill='x', pady=(0, 15))
        
        # Categoria
        cat_label = self.create_label(main_frame, "Categoria:*", 'body_secondary')
        cat_label.pack(anchor='w', pady=(0, 5))
        
        categories = ["malte", "lúpulo", "fermento", "açúcar", "mel", "especiaria", "adjunto", "nutriente", "outro"]
        cat_combo = ctk.CTkComboBox(
            main_frame,
            values=categories,
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md']
        )
        cat_combo.pack(fill='x', pady=(0, 15))
        cat_combo.set("malte")
        
        # Observações
        obs_label = self.create_label(main_frame, "Observações:", 'body_secondary')
        obs_label.pack(anchor='w', pady=(0, 5))
        
        obs_text = ctk.CTkTextbox(
            main_frame,
            height=60,
            fg_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_primary'],
            font=self.fonts['body_md']
        )
        obs_text.pack(fill='x', pady=(0, 20))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        button_frame.pack(fill='x')
        
        def save_ingredient():
            nome = name_entry.get()
            categoria = cat_combo.get()
            
            if nome:
                # Adicionar à lista
                if categoria not in self.ingredients_data:
                    self.ingredients_data[categoria] = []
                    
                if nome not in self.ingredients_data[categoria]:
                    self.ingredients_data[categoria].append(nome)
                    self.ingredients_data[categoria].sort()
                    
                self.display_ingredients()
                self.show_message(f"Ingrediente '{nome}' adicionado com sucesso!", 'success')
                dialog.destroy()
            else:
                self.show_message("Nome do ingrediente é obrigatório", 'error')
                
        cancel_btn = self.create_button(
            button_frame,
            "Cancelar",
            dialog.destroy,
            style='secondary',
            width=100,
            height=35
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        save_btn = self.create_button(
            button_frame,
            "Salvar",
            save_ingredient,
            style='solid_primary',
            width=100,
            height=35
        )
        save_btn.pack(side='left')
        
    def edit_ingredient(self, ingredient: str, category: str):
        """Edita um ingrediente existente"""
        # Por enquanto, apenas mostrar mensagem
        self.show_message(f"Edição de '{ingredient}' em desenvolvimento", 'info')
        
    def filter_ingredients(self):
        """Filtra os ingredientes baseado na busca"""
        self.display_ingredients()
        
    def on_show(self, **kwargs):
        """Callback quando a view é exibida"""
        self.load_ingredients()
        
    def refresh(self):
        """Atualiza a lista de ingredientes"""
        self.load_ingredients() 