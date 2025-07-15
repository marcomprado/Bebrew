import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
from util.mock_data_loader import mock_loader
import uuid
from datetime import datetime

class NewRecipeView(BaseView):
    """View para criação de novas receitas"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Nova Receita")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Dados da receita sendo criada
        self.recipe_data = {
            'ingredientes': [],
            'etapas': []
        }
        
        # Widgets principais
        self.nome_entry = None
        self.tipo_combo = None
        self.volume_entry = None
        self.descricao_text = None
        self.dificuldade_combo = None
        
        # Widgets técnicos
        self.og_entry = None
        self.fg_entry = None
        self.ibu_entry = None
        self.srm_entry = None
        
        # Listas
        self.ingredientes_frame = None
        self.etapas_frame = None
        
    def create_widgets(self):
        """Cria os widgets da view de nova receita"""
        # Header
        header = self.create_header(
            self.frame, 
            "Nova Receita", 
            "Crie uma nova receita para suas bebidas fermentadas"
        )
        
        # Container principal com scroll
        self.main_scroll = ctk.CTkScrollableFrame(
            self.frame, 
            fg_color='transparent'
        )
        self.main_scroll.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Grid principal
        self.main_scroll.grid_columnconfigure(0, weight=1)
        self.main_scroll.grid_columnconfigure(1, weight=1)
        
        # Informações básicas (esquerda)
        self.create_basic_info_section()
        
        # Dados técnicos (direita)
        self.create_technical_section()
        
        # Ingredientes (largura total)
        self.create_ingredients_section()
        
        # Etapas (largura total)
        self.create_steps_section()
        
        # Botões de ação
        self.create_action_buttons()
        
    def create_basic_info_section(self):
        """Cria a seção de informações básicas"""
        basic_card = self.create_card(self.main_scroll, title="Informações Básicas", padding=20)
        basic_card.grid(row=0, column=0, sticky='ew', padx=(0, 10), pady=(0, 20))
        
        content = ctk.CTkFrame(basic_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Nome da receita
        nome_label = self.create_label(content, "Nome da Receita:*", 'body_secondary')
        nome_label.pack(anchor='w', pady=(0, 5))
        
        self.nome_entry = self.create_input(content, placeholder="Ex: IPA Tropical")
        self.nome_entry.pack(fill='x', pady=(0, 15))
        
        # Tipo
        tipo_label = self.create_label(content, "Tipo de Bebida:*", 'body_secondary')
        tipo_label.pack(anchor='w', pady=(0, 5))
        
        tipos = mock_loader.get_tipos_bebida()
        if not tipos:
            tipos = ["Cerveja", "Hidromel", "Vinho"]
            
        self.tipo_combo = ctk.CTkComboBox(
            content,
            values=tipos,
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md']
        )
        self.tipo_combo.pack(fill='x', pady=(0, 15))
        self.tipo_combo.set(tipos[0])
        
        # Volume
        volume_label = self.create_label(content, "Volume (L):*", 'body_secondary')
        volume_label.pack(anchor='w', pady=(0, 5))
        
        self.volume_entry = self.create_input(content, placeholder="Ex: 20")
        self.volume_entry.pack(fill='x', pady=(0, 15))
        
        # Dificuldade
        diff_label = self.create_label(content, "Dificuldade:", 'body_secondary')
        diff_label.pack(anchor='w', pady=(0, 5))
        
        self.dificuldade_combo = ctk.CTkComboBox(
            content,
            values=["Iniciante", "Intermediário", "Avançado"],
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md']
        )
        self.dificuldade_combo.pack(fill='x', pady=(0, 15))
        self.dificuldade_combo.set("Intermediário")
        
        # Descrição
        desc_label = self.create_label(content, "Descrição:", 'body_secondary')
        desc_label.pack(anchor='w', pady=(0, 5))
        
        self.descricao_text = ctk.CTkTextbox(
            content,
            height=100,
            fg_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_primary'],
            font=self.fonts['body_md']
        )
        self.descricao_text.pack(fill='x')
        
    def create_technical_section(self):
        """Cria a seção de dados técnicos"""
        tech_card = self.create_card(self.main_scroll, title="Dados Técnicos", padding=20)
        tech_card.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=(0, 20))
        
        content = ctk.CTkFrame(tech_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # OG
        og_label = self.create_label(content, "OG (Original Gravity):", 'body_secondary')
        og_label.pack(anchor='w', pady=(0, 5))
        
        self.og_entry = self.create_input(content, placeholder="Ex: 1.065")
        self.og_entry.pack(fill='x', pady=(0, 15))
        
        # FG
        fg_label = self.create_label(content, "FG (Final Gravity):", 'body_secondary')
        fg_label.pack(anchor='w', pady=(0, 5))
        
        self.fg_entry = self.create_input(content, placeholder="Ex: 1.012")
        self.fg_entry.pack(fill='x', pady=(0, 15))
        
        # ABV calculado
        self.abv_label = self.create_label(content, "ABV Estimado: ---%", 'heading_sm')
        self.abv_label.pack(anchor='w', pady=(0, 20))
        
        # Bind para calcular ABV automaticamente
        self.og_entry.bind("<KeyRelease>", lambda e: self.calculate_abv())
        self.fg_entry.bind("<KeyRelease>", lambda e: self.calculate_abv())
        
        # IBU (para cerveja)
        ibu_label = self.create_label(content, "IBU (para cervejas):", 'body_secondary')
        ibu_label.pack(anchor='w', pady=(0, 5))
        
        self.ibu_entry = self.create_input(content, placeholder="Ex: 45")
        self.ibu_entry.pack(fill='x', pady=(0, 15))
        
        # SRM (para cerveja)
        srm_label = self.create_label(content, "SRM (cor para cervejas):", 'body_secondary')
        srm_label.pack(anchor='w', pady=(0, 5))
        
        self.srm_entry = self.create_input(content, placeholder="Ex: 8")
        self.srm_entry.pack(fill='x')
        
    def create_ingredients_section(self):
        """Cria a seção de ingredientes"""
        ingredients_card = self.create_card(
            self.main_scroll, 
            title="Ingredientes", 
            padding=20
        )
        ingredients_card.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        content = ctk.CTkFrame(ingredients_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Botão adicionar ingrediente
        add_frame = ctk.CTkFrame(content, fg_color='transparent')
        add_frame.pack(fill='x', pady=(0, 20))
        
        add_btn = self.create_button(
            add_frame,
            "Adicionar Ingrediente",
            self.show_add_ingredient_dialog,
            style='primary',
            icon="➕",
            width=180,
            height=35
        )
        add_btn.pack(anchor='w')
        
        # Lista de ingredientes
        self.ingredientes_frame = ctk.CTkScrollableFrame(
            content,
            fg_color='transparent',
            height=200
        )
        self.ingredientes_frame.pack(fill='both', expand=True)
        
        # Placeholder
        self.no_ingredients_label = self.create_label(
            self.ingredientes_frame,
            "Nenhum ingrediente adicionado ainda",
            'body_secondary'
        )
        self.no_ingredients_label.pack(pady=40)
        
    def create_steps_section(self):
        """Cria a seção de etapas"""
        steps_card = self.create_card(
            self.main_scroll, 
            title="Etapas de Produção", 
            padding=20
        )
        steps_card.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        content = ctk.CTkFrame(steps_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Botão adicionar etapa
        add_frame = ctk.CTkFrame(content, fg_color='transparent')
        add_frame.pack(fill='x', pady=(0, 20))
        
        add_btn = self.create_button(
            add_frame,
            "Adicionar Etapa",
            self.show_add_step_dialog,
            style='primary',
            icon="➕",
            width=150,
            height=35
        )
        add_btn.pack(anchor='w')
        
        # Lista de etapas
        self.etapas_frame = ctk.CTkScrollableFrame(
            content,
            fg_color='transparent',
            height=200
        )
        self.etapas_frame.pack(fill='both', expand=True)
        
        # Placeholder
        self.no_steps_label = self.create_label(
            self.etapas_frame,
            "Nenhuma etapa adicionada ainda",
            'body_secondary'
        )
        self.no_steps_label.pack(pady=40)
        
    def create_action_buttons(self):
        """Cria os botões de ação"""
        action_frame = ctk.CTkFrame(self.main_scroll, fg_color='transparent')
        action_frame.grid(row=3, column=0, columnspan=2, sticky='ew')
        
        button_container = ctk.CTkFrame(action_frame, fg_color='transparent')
        button_container.pack(anchor='e')
        
        cancel_btn = self.create_button(
            button_container,
            "Cancelar",
            self.cancel_recipe,
            style='secondary',
            width=120,
            height=40
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        save_btn = self.create_button(
            button_container,
            "Salvar Receita",
            self.save_recipe,
            style='solid_primary',
            width=150,
            height=40
        )
        save_btn.pack(side='left')
        
    def calculate_abv(self):
        """Calcula o ABV baseado em OG e FG"""
        try:
            og = float(self.og_entry.get())
            fg = float(self.fg_entry.get())
            abv = (og - fg) * 131.25
            self.abv_label.configure(text=f"ABV Estimado: {abv:.1f}%")
        except:
            self.abv_label.configure(text="ABV Estimado: ---%")
            
    def show_add_ingredient_dialog(self):
        """Mostra diálogo para adicionar ingrediente"""
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Adicionar Ingrediente")
        dialog.geometry("500x400")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Container principal
        main_frame = ctk.CTkFrame(dialog, fg_color=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Nome do ingrediente
        nome_label = self.create_label(main_frame, "Nome:*", 'body_secondary')
        nome_label.pack(anchor='w', pady=(0, 5))
        
        nome_entry = self.create_input(main_frame, placeholder="Ex: Malte Pilsen")
        nome_entry.pack(fill='x', pady=(0, 15))
        
        # Tipo
        tipo_label = self.create_label(main_frame, "Tipo:*", 'body_secondary')
        tipo_label.pack(anchor='w', pady=(0, 5))
        
        tipo_combo = ctk.CTkComboBox(
            main_frame,
            values=["malte", "lúpulo", "fermento", "açúcar", "mel", "especiaria", "adjunto", "nutriente", "outro"],
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md']
        )
        tipo_combo.pack(fill='x', pady=(0, 15))
        tipo_combo.set("malte")
        
        # Quantidade e unidade
        qty_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        qty_frame.pack(fill='x', pady=(0, 15))
        
        qty_label = self.create_label(qty_frame, "Quantidade:*", 'body_secondary')
        qty_label.pack(anchor='w', pady=(0, 5))
        
        qty_container = ctk.CTkFrame(qty_frame, fg_color='transparent')
        qty_container.pack(fill='x')
        
        qty_entry = self.create_input(qty_container, placeholder="Ex: 4.5", width=200)
        qty_entry.pack(side='left', padx=(0, 10))
        
        unit_combo = ctk.CTkComboBox(
            qty_container,
            values=["kg", "g", "L", "mL", "un"],
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md'],
            width=100
        )
        unit_combo.pack(side='left')
        unit_combo.set("kg")
        
        # Observações
        obs_label = self.create_label(main_frame, "Observações:", 'body_secondary')
        obs_label.pack(anchor='w', pady=(0, 5))
        
        obs_text = ctk.CTkTextbox(
            main_frame,
            height=80,
            fg_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_primary'],
            font=self.fonts['body_md']
        )
        obs_text.pack(fill='x', pady=(0, 20))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        button_frame.pack(fill='x')
        
        def add_ingredient():
            nome = nome_entry.get()
            tipo = tipo_combo.get()
            try:
                quantidade = float(qty_entry.get())
                unidade = unit_combo.get()
                obs = obs_text.get("1.0", "end-1c").strip()
                
                if nome and quantidade > 0:
                    ingrediente = {
                        'id': str(uuid.uuid4()),
                        'nome': nome,
                        'tipo': tipo,
                        'quantidade': quantidade,
                        'unidade': unidade,
                        'observacoes': obs
                    }
                    self.recipe_data['ingredientes'].append(ingrediente)
                    self.update_ingredients_list()
                    dialog.destroy()
                else:
                    self.show_message("Preencha todos os campos obrigatórios", 'error')
            except ValueError:
                self.show_message("Quantidade inválida", 'error')
        
        cancel_btn = self.create_button(
            button_frame,
            "Cancelar",
            dialog.destroy,
            style='secondary',
            width=100,
            height=35
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        add_btn = self.create_button(
            button_frame,
            "Adicionar",
            add_ingredient,
            style='solid_primary',
            width=100,
            height=35
        )
        add_btn.pack(side='left')
        
    def show_add_step_dialog(self):
        """Mostra diálogo para adicionar etapa"""
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Adicionar Etapa")
        dialog.geometry("500x450")
        dialog.transient(self.frame)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Container principal
        main_frame = ctk.CTkFrame(dialog, fg_color=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Nome da etapa
        nome_label = self.create_label(main_frame, "Nome da Etapa:*", 'body_secondary')
        nome_label.pack(anchor='w', pady=(0, 5))
        
        nome_entry = self.create_input(main_frame, placeholder="Ex: Mostura")
        nome_entry.pack(fill='x', pady=(0, 15))
        
        # Duração
        duracao_label = self.create_label(main_frame, "Duração (minutos):*", 'body_secondary')
        duracao_label.pack(anchor='w', pady=(0, 5))
        
        duracao_entry = self.create_input(main_frame, placeholder="Ex: 60")
        duracao_entry.pack(fill='x', pady=(0, 15))
        
        # Temperatura
        temp_label = self.create_label(main_frame, "Temperatura Alvo (°C):", 'body_secondary')
        temp_label.pack(anchor='w', pady=(0, 5))
        
        temp_entry = self.create_input(main_frame, placeholder="Ex: 67")
        temp_entry.pack(fill='x', pady=(0, 15))
        
        # Descrição
        desc_label = self.create_label(main_frame, "Descrição:*", 'body_secondary')
        desc_label.pack(anchor='w', pady=(0, 5))
        
        desc_text = ctk.CTkTextbox(
            main_frame,
            height=100,
            fg_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_primary'],
            font=self.fonts['body_md']
        )
        desc_text.pack(fill='x', pady=(0, 20))
        
        # Botões
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        button_frame.pack(fill='x')
        
        def add_step():
            nome = nome_entry.get()
            desc = desc_text.get("1.0", "end-1c").strip()
            try:
                duracao = int(duracao_entry.get())
                temp = float(temp_entry.get()) if temp_entry.get() else None
                
                if nome and duracao > 0 and desc:
                    etapa = {
                        'id': str(uuid.uuid4()),
                        'nome': nome,
                        'descricao': desc,
                        'duracao': duracao,
                        'temperatura': temp
                    }
                    self.recipe_data['etapas'].append(etapa)
                    self.update_steps_list()
                    dialog.destroy()
                else:
                    self.show_message("Preencha todos os campos obrigatórios", 'error')
            except ValueError:
                self.show_message("Valores inválidos", 'error')
        
        cancel_btn = self.create_button(
            button_frame,
            "Cancelar",
            dialog.destroy,
            style='secondary',
            width=100,
            height=35
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        add_btn = self.create_button(
            button_frame,
            "Adicionar",
            add_step,
            style='solid_primary',
            width=100,
            height=35
        )
        add_btn.pack(side='left')
        
    def update_ingredients_list(self):
        """Atualiza a lista de ingredientes"""
        # Limpar lista
        for widget in self.ingredientes_frame.winfo_children():
            widget.destroy()
            
        if not self.recipe_data['ingredientes']:
            self.no_ingredients_label = self.create_label(
                self.ingredientes_frame,
                "Nenhum ingrediente adicionado ainda",
                'body_secondary'
            )
            self.no_ingredients_label.pack(pady=40)
            return
            
        # Adicionar ingredientes
        for idx, ing in enumerate(self.recipe_data['ingredientes']):
            self.create_ingredient_item(ing, idx)
            
    def create_ingredient_item(self, ingredient: Dict, index: int):
        """Cria um item de ingrediente na lista"""
        item_frame = ctk.CTkFrame(
            self.ingredientes_frame,
            fg_color=self.colors['bg_tertiary'],
            corner_radius=8,
            height=60
        )
        item_frame.pack(fill='x', pady=5)
        item_frame.pack_propagate(False)
        
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Info
        info_text = f"{ingredient['nome']} - {ingredient['quantidade']} {ingredient['unidade']}"
        info_label = self.create_label(inner, info_text, 'body')
        info_label.pack(side='left')
        
        # Tipo badge
        type_badge = ctk.CTkLabel(
            inner,
            text=ingredient['tipo'].upper(),
            font=self.fonts['caption'],
            text_color=self.colors['text_primary'],
            fg_color=self.colors['accent_blue'],
            corner_radius=4,
            padx=8,
            pady=2
        )
        type_badge.pack(side='left', padx=(10, 0))
        
        # Botão remover
        def remove_ingredient():
            self.recipe_data['ingredientes'].pop(index)
            self.update_ingredients_list()
            
        remove_btn = self.create_button(
            inner,
            "Remover",
            remove_ingredient,
            style='warning',
            width=80,
            height=30
        )
        remove_btn.pack(side='right')
        
    def update_steps_list(self):
        """Atualiza a lista de etapas"""
        # Limpar lista
        for widget in self.etapas_frame.winfo_children():
            widget.destroy()
            
        if not self.recipe_data['etapas']:
            self.no_steps_label = self.create_label(
                self.etapas_frame,
                "Nenhuma etapa adicionada ainda",
                'body_secondary'
            )
            self.no_steps_label.pack(pady=40)
            return
            
        # Adicionar etapas
        for idx, etapa in enumerate(self.recipe_data['etapas']):
            self.create_step_item(etapa, idx)
            
    def create_step_item(self, step: Dict, index: int):
        """Cria um item de etapa na lista"""
        item_frame = ctk.CTkFrame(
            self.etapas_frame,
            fg_color=self.colors['bg_tertiary'],
            corner_radius=8,
            height=80
        )
        item_frame.pack(fill='x', pady=5)
        item_frame.pack_propagate(False)
        
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Info
        info_frame = ctk.CTkFrame(inner, fg_color='transparent')
        info_frame.pack(side='left', fill='both', expand=True)
        
        # Nome e duração
        name_text = f"{index + 1}. {step['nome']} ({step['duracao']} min)"
        if step.get('temperatura'):
            name_text += f" - {step['temperatura']}°C"
            
        name_label = self.create_label(info_frame, name_text, 'heading_sm')
        name_label.pack(anchor='w')
        
        # Descrição
        desc_label = self.create_label(info_frame, step['descricao'], 'caption')
        desc_label.pack(anchor='w', pady=(5, 0))
        
        # Botões
        button_frame = ctk.CTkFrame(inner, fg_color='transparent')
        button_frame.pack(side='right')
        
        # Mover para cima
        if index > 0:
            up_btn = self.create_button(
                button_frame,
                "↑",
                lambda: self.move_step(index, -1),
                style='secondary',
                width=30,
                height=30
            )
            up_btn.pack(side='left', padx=(0, 5))
        
        # Mover para baixo
        if index < len(self.recipe_data['etapas']) - 1:
            down_btn = self.create_button(
                button_frame,
                "↓",
                lambda: self.move_step(index, 1),
                style='secondary',
                width=30,
                height=30
            )
            down_btn.pack(side='left', padx=(0, 5))
        
        # Remover
        def remove_step():
            self.recipe_data['etapas'].pop(index)
            self.update_steps_list()
            
        remove_btn = self.create_button(
            button_frame,
            "Remover",
            remove_step,
            style='warning',
            width=80,
            height=30
        )
        remove_btn.pack(side='left')
        
    def move_step(self, index: int, direction: int):
        """Move uma etapa para cima ou para baixo"""
        new_index = index + direction
        self.recipe_data['etapas'][index], self.recipe_data['etapas'][new_index] = \
            self.recipe_data['etapas'][new_index], self.recipe_data['etapas'][index]
        self.update_steps_list()
        
    def validate_recipe(self) -> bool:
        """Valida os dados da receita"""
        errors = []
        
        if not self.nome_entry.get():
            errors.append("Nome da receita é obrigatório")
            
        try:
            volume = float(self.volume_entry.get())
            if volume <= 0:
                errors.append("Volume deve ser maior que zero")
        except:
            errors.append("Volume inválido")
            
        if not self.recipe_data['ingredientes']:
            errors.append("Adicione pelo menos um ingrediente")
            
        if not self.recipe_data['etapas']:
            errors.append("Adicione pelo menos uma etapa")
            
        if errors:
            error_msg = "Corrija os seguintes erros:\n\n" + "\n".join(errors)
            self.show_message(error_msg, 'error')
            return False
            
        return True
        
    def save_recipe(self):
        """Salva a receita"""
        if not self.validate_recipe():
            return
            
        # Coletar dados
        recipe_data = {
            'id': str(uuid.uuid4()),
            'nome': self.nome_entry.get(),
            'tipo': self.tipo_combo.get(),
            'volume': float(self.volume_entry.get()),
            'descricao': self.descricao_text.get("1.0", "end-1c").strip(),
            'dificuldade': self.dificuldade_combo.get(),
            'data_criacao': datetime.now().strftime('%Y-%m-%d'),
            'ingredientes': self.recipe_data['ingredientes'],
            'etapas': self.recipe_data['etapas']
        }
        
        # Dados técnicos opcionais
        try:
            recipe_data['og'] = float(self.og_entry.get()) if self.og_entry.get() else None
            recipe_data['fg'] = float(self.fg_entry.get()) if self.fg_entry.get() else None
            
            if recipe_data['og'] and recipe_data['fg']:
                recipe_data['abv'] = (recipe_data['og'] - recipe_data['fg']) * 131.25
                
            recipe_data['ibu'] = int(self.ibu_entry.get()) if self.ibu_entry.get() else None
            recipe_data['srm'] = int(self.srm_entry.get()) if self.srm_entry.get() else None
        except:
            pass
            
        # Aqui seria salvo no backend/banco de dados
        self.show_message(f"Receita '{recipe_data['nome']}' salva com sucesso!", 'success')
        
        # Navegar para a lista de receitas
        self.navigation.navigate_to('receitas')
        
    def cancel_recipe(self):
        """Cancela a criação da receita"""
        # Confirmar cancelamento se houver dados
        if (self.nome_entry.get() or self.recipe_data['ingredientes'] or self.recipe_data['etapas']):
            # Aqui poderia mostrar um diálogo de confirmação
            pass
            
        self.navigation.navigate_to('receitas')
        
    def on_show(self, **kwargs):
        """Callback quando a view é exibida"""
        # Limpar formulário
        self.recipe_data = {
            'ingredientes': [],
            'etapas': []
        }
        
        # Limpar campos
        if hasattr(self, 'nome_entry'):
            self.nome_entry.delete(0, 'end')
            self.volume_entry.delete(0, 'end')
            self.descricao_text.delete("1.0", "end")
            self.og_entry.delete(0, 'end')
            self.fg_entry.delete(0, 'end')
            self.ibu_entry.delete(0, 'end')
            self.srm_entry.delete(0, 'end')
            
            # Resetar combos
            tipos = mock_loader.get_tipos_bebida()
            if tipos:
                self.tipo_combo.set(tipos[0])
            self.dificuldade_combo.set("Intermediário")
            
            # Limpar listas
            self.update_ingredients_list()
            self.update_steps_list() 