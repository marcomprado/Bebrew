import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
from util.mock_data_loader import mock_loader
from datetime import datetime
import uuid

class NewProductionView(BaseView):
    """View para iniciar uma nova produção"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Nova Produção")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Dados da produção
        self.selected_recipe = None
        self.production_data = {}
        
        # Widgets principais
        self.recipe_list_frame = None
        self.selected_recipe_frame = None
        self.lote_entry = None
        self.volume_entry = None
        self.notes_text = None
        
    def create_widgets(self):
        """Cria os widgets da view de nova produção"""
        # Header
        header = self.create_header(
            self.frame, 
            "Nova Produção", 
            "Inicie uma nova produção baseada em uma receita"
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
        
        # Seleção de receita (esquerda)
        self.create_recipe_selection_section()
        
        # Detalhes da produção (direita)
        self.create_production_details_section()
        
        # Resumo da receita selecionada (largura total)
        self.create_recipe_summary_section()
        
        # Configurações iniciais (largura total)
        self.create_initial_settings_section()
        
        # Botões de ação
        self.create_action_buttons()
        
    def create_recipe_selection_section(self):
        """Cria a seção de seleção de receita"""
        recipe_card = self.create_card(self.main_scroll, title="Selecione uma Receita", padding=20)
        recipe_card.grid(row=0, column=0, sticky='nsew', padx=(0, 10), pady=(0, 20))
        
        content = ctk.CTkFrame(recipe_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Filtro de busca
        search_frame = ctk.CTkFrame(content, fg_color='transparent')
        search_frame.pack(fill='x', pady=(0, 15))
        
        search_label = self.create_label(search_frame, "Buscar:", 'body_secondary')
        search_label.pack(side='left', padx=(0, 10))
        
        self.search_entry = self.create_input(search_frame, placeholder="Nome da receita...", width=200)
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_recipes())
        
        # Lista de receitas
        self.recipe_list_frame = ctk.CTkScrollableFrame(
            content,
            fg_color='transparent',
            height=300
        )
        self.recipe_list_frame.pack(fill='both', expand=True)
        
        # Carregar receitas
        self.load_recipes()
        
    def create_production_details_section(self):
        """Cria a seção de detalhes da produção"""
        details_card = self.create_card(self.main_scroll, title="Detalhes da Produção", padding=20)
        details_card.grid(row=0, column=1, sticky='nsew', padx=(10, 0), pady=(0, 20))
        
        content = ctk.CTkFrame(details_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Número do lote
        lote_label = self.create_label(content, "Número do Lote:", 'body_secondary')
        lote_label.pack(anchor='w', pady=(0, 5))
        
        # Frame para lote
        lote_frame = ctk.CTkFrame(content, fg_color='transparent')
        lote_frame.pack(fill='x', pady=(0, 15))
        
        self.lote_entry = self.create_input(lote_frame, placeholder="Gerado automaticamente")
        self.lote_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Botão gerar lote
        generate_btn = self.create_button(
            lote_frame,
            "Gerar",
            self.generate_lote_number,
            style='secondary',
            width=80,
            height=35
        )
        generate_btn.pack(side='left')
        
        # Volume
        volume_label = self.create_label(content, "Volume a Produzir (L):", 'body_secondary')
        volume_label.pack(anchor='w', pady=(0, 5))
        
        self.volume_entry = self.create_input(content, placeholder="Ex: 20")
        self.volume_entry.pack(fill='x', pady=(0, 15))
        self.volume_entry.bind("<KeyRelease>", lambda e: self.calculate_scaling())
        
        # Escala
        self.scale_label = self.create_label(content, "Escala: 100%", 'heading_sm')
        self.scale_label.pack(anchor='w', pady=(0, 20))
        
        # Data/hora de início
        date_label = self.create_label(content, "Início Previsto:", 'body_secondary')
        date_label.pack(anchor='w', pady=(0, 5))
        
        date_frame = ctk.CTkFrame(content, fg_color='transparent')
        date_frame.pack(fill='x', pady=(0, 15))
        
        # Mostrar data/hora atual
        now = datetime.now()
        date_text = now.strftime("%d/%m/%Y %H:%M")
        self.date_label = self.create_label(date_frame, date_text, 'body')
        self.date_label.pack(side='left')
        
        # Notas iniciais
        notes_label = self.create_label(content, "Notas Iniciais:", 'body_secondary')
        notes_label.pack(anchor='w', pady=(0, 5))
        
        self.notes_text = ctk.CTkTextbox(
            content,
            height=80,
            fg_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_primary'],
            font=self.fonts['body_md']
        )
        self.notes_text.pack(fill='x')
        
    def create_recipe_summary_section(self):
        """Cria a seção de resumo da receita selecionada"""
        summary_card = self.create_card(
            self.main_scroll, 
            title="Receita Selecionada", 
            padding=20
        )
        summary_card.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        self.selected_recipe_frame = ctk.CTkFrame(summary_card, fg_color='transparent')
        self.selected_recipe_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Placeholder inicial
        self.no_recipe_label = self.create_label(
            self.selected_recipe_frame,
            "Nenhuma receita selecionada",
            'body_secondary'
        )
        self.no_recipe_label.pack(pady=40)
        
    def create_initial_settings_section(self):
        """Cria a seção de configurações iniciais"""
        settings_card = self.create_card(
            self.main_scroll, 
            title="Configurações Iniciais", 
            padding=20
        )
        settings_card.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        content = ctk.CTkFrame(settings_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Grid para organizar campos
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)
        
        # OG inicial
        og_label = self.create_label(content, "OG Medido:", 'body_secondary')
        og_label.grid(row=0, column=0, sticky='w', padx=(0, 20), pady=(0, 5))
        
        self.og_entry = self.create_input(content, placeholder="Ex: 1.065")
        self.og_entry.grid(row=1, column=0, sticky='ew', padx=(0, 20), pady=(0, 15))
        
        # Temperatura inicial
        temp_label = self.create_label(content, "Temperatura Inicial (°C):", 'body_secondary')
        temp_label.grid(row=0, column=1, sticky='w', padx=(0, 20), pady=(0, 5))
        
        self.temp_entry = self.create_input(content, placeholder="Ex: 20")
        self.temp_entry.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=(0, 15))
        
        # pH inicial
        ph_label = self.create_label(content, "pH Inicial:", 'body_secondary')
        ph_label.grid(row=0, column=2, sticky='w', pady=(0, 5))
        
        self.ph_entry = self.create_input(content, placeholder="Ex: 5.2")
        self.ph_entry.grid(row=1, column=2, sticky='ew', pady=(0, 15))
        
        # Checklist inicial
        checklist_label = self.create_label(content, "Checklist Pré-Produção:", 'body_secondary')
        checklist_label.grid(row=2, column=0, columnspan=3, sticky='w', pady=(20, 10))
        
        # Checkboxes
        self.checklist_vars = {}
        checklist_items = [
            "Ingredientes verificados e pesados",
            "Equipamentos sanitizados",
            "Água tratada e aquecida",
            "Fermento ativado (se necessário)",
            "Instrumentos de medição calibrados"
        ]
        
        for idx, item in enumerate(checklist_items):
            var = ctk.BooleanVar()
            self.checklist_vars[item] = var
            
            checkbox = ctk.CTkCheckBox(
                content,
                text=item,
                variable=var,
                border_color=self.colors['accent_orange'],
                hover_color=self.colors['accent_orange'],
                font=self.fonts['body_md']
            )
            checkbox.grid(row=3 + idx // 2, column=idx % 2, sticky='w', padx=(0, 20), pady=5)
            
    def create_action_buttons(self):
        """Cria os botões de ação"""
        action_frame = ctk.CTkFrame(self.main_scroll, fg_color='transparent')
        action_frame.grid(row=3, column=0, columnspan=2, sticky='ew')
        
        button_container = ctk.CTkFrame(action_frame, fg_color='transparent')
        button_container.pack(anchor='e')
        
        cancel_btn = self.create_button(
            button_container,
            "Cancelar",
            self.cancel_production,
            style='secondary',
            width=120,
            height=40
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        self.start_btn = self.create_button(
            button_container,
            "Iniciar Produção",
            self.start_production,
            style='solid_primary',
            width=150,
            height=40
        )
        self.start_btn.pack(side='left')
        self.start_btn.configure(state='disabled')
        
    def load_recipes(self):
        """Carrega as receitas disponíveis"""
        recipes = mock_loader.get_receitas()
        self.display_recipes(recipes)
        
    def display_recipes(self, recipes: List[Dict]):
        """Exibe as receitas na lista"""
        # Limpar lista
        for widget in self.recipe_list_frame.winfo_children():
            widget.destroy()
            
        if not recipes:
            no_recipes = self.create_label(
                self.recipe_list_frame,
                "Nenhuma receita disponível",
                'body_secondary'
            )
            no_recipes.pack(pady=40)
            return
            
        for recipe in recipes:
            self.create_recipe_item(recipe)
            
    def create_recipe_item(self, recipe: Dict):
        """Cria um item de receita na lista"""
        item_frame = ctk.CTkFrame(
            self.recipe_list_frame,
            fg_color=self.colors['bg_tertiary'],
            corner_radius=8,
            height=80,
            cursor="hand2"
        )
        item_frame.pack(fill='x', pady=5)
        item_frame.pack_propagate(False)
        
        # Bind para seleção
        def select_recipe(e=None):
            self.select_recipe(recipe)
            # Destacar item selecionado
            for child in self.recipe_list_frame.winfo_children():
                child.configure(fg_color=self.colors['bg_tertiary'])
            item_frame.configure(fg_color=self.colors['accent_orange'])
            
        item_frame.bind("<Button-1>", select_recipe)
        
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=15, pady=10)
        inner.bind("<Button-1>", select_recipe)
        
        # Nome e tipo
        name_frame = ctk.CTkFrame(inner, fg_color='transparent')
        name_frame.pack(anchor='w')
        name_frame.bind("<Button-1>", select_recipe)
        
        name_label = self.create_label(
            name_frame,
            recipe['nome'],
            'heading_sm'
        )
        name_label.pack(side='left', padx=(0, 10))
        name_label.bind("<Button-1>", select_recipe)
        
        type_badge = ctk.CTkLabel(
            name_frame,
            text=recipe.get('tipo', 'N/A').upper(),
            font=self.fonts['caption'],
            text_color=self.colors['text_primary'],
            fg_color=self.colors['accent_blue'],
            corner_radius=4,
            padx=8,
            pady=2
        )
        type_badge.pack(side='left')
        type_badge.bind("<Button-1>", select_recipe)
        
        # Detalhes
        details_text = f"Volume: {recipe.get('volume', 0)}L  •  ABV: {recipe.get('abv', 0):.1f}%"
        details_label = self.create_label(inner, details_text, 'caption')
        details_label.pack(anchor='w', pady=(5, 0))
        details_label.bind("<Button-1>", select_recipe)
        
    def select_recipe(self, recipe: Dict):
        """Seleciona uma receita para produção"""
        self.selected_recipe = recipe
        self.update_recipe_summary()
        
        # Habilitar botão de iniciar
        self.start_btn.configure(state='normal')
        
        # Atualizar volume padrão
        if not self.volume_entry.get():
            self.volume_entry.delete(0, 'end')
            self.volume_entry.insert(0, str(recipe.get('volume', 20)))
            
        # Gerar número de lote se vazio
        if not self.lote_entry.get():
            self.generate_lote_number()
            
    def update_recipe_summary(self):
        """Atualiza o resumo da receita selecionada"""
        # Limpar frame
        for widget in self.selected_recipe_frame.winfo_children():
            widget.destroy()
            
        if not self.selected_recipe:
            self.no_recipe_label = self.create_label(
                self.selected_recipe_frame,
                "Nenhuma receita selecionada",
                'body_secondary'
            )
            self.no_recipe_label.pack(pady=40)
            return
            
        # Grid para organizar informações
        self.selected_recipe_frame.grid_columnconfigure(0, weight=1)
        self.selected_recipe_frame.grid_columnconfigure(1, weight=1)
        
        # Informações básicas
        info_frame = ctk.CTkFrame(self.selected_recipe_frame, fg_color='transparent')
        info_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 20))
        
        # Nome
        name_label = self.create_label(
            info_frame,
            self.selected_recipe['nome'],
            'heading_md'
        )
        name_label.pack(anchor='w', pady=(0, 10))
        
        # Descrição
        if self.selected_recipe.get('descricao'):
            desc_label = self.create_label(
                info_frame,
                self.selected_recipe['descricao'],
                'body_secondary'
            )
            desc_label.pack(anchor='w', pady=(0, 15))
            
        # Dados técnicos
        tech_text = f"Volume Original: {self.selected_recipe.get('volume', 0)}L\n"
        tech_text += f"ABV Estimado: {self.selected_recipe.get('abv', 0):.1f}%\n"
        tech_text += f"OG: {self.selected_recipe.get('og', 'N/A')}\n"
        tech_text += f"FG: {self.selected_recipe.get('fg', 'N/A')}"
        
        tech_label = self.create_label(info_frame, tech_text, 'body')
        tech_label.pack(anchor='w')
        
        # Ingredientes e etapas
        details_frame = ctk.CTkFrame(self.selected_recipe_frame, fg_color='transparent')
        details_frame.grid(row=0, column=1, sticky='nsew')
        
        # Ingredientes
        ing_title = self.create_label(details_frame, "Ingredientes:", 'heading_sm')
        ing_title.pack(anchor='w', pady=(0, 10))
        
        ing_frame = ctk.CTkFrame(details_frame, fg_color=self.colors['bg_tertiary'], corner_radius=8)
        ing_frame.pack(fill='x', pady=(0, 15))
        
        ing_inner = ctk.CTkFrame(ing_frame, fg_color='transparent')
        ing_inner.pack(padx=15, pady=10)
        
        for ing in self.selected_recipe.get('ingredientes', [])[:5]:  # Mostrar apenas 5 primeiros
            ing_text = f"• {ing['nome']} - {ing['quantidade']} {ing['unidade']}"
            ing_label = self.create_label(ing_inner, ing_text, 'caption')
            ing_label.pack(anchor='w', pady=2)
            
        if len(self.selected_recipe.get('ingredientes', [])) > 5:
            more_label = self.create_label(
                ing_inner, 
                f"... e mais {len(self.selected_recipe['ingredientes']) - 5} ingredientes",
                'caption'
            )
            more_label.pack(anchor='w', pady=(5, 0))
            
        # Etapas
        steps_title = self.create_label(details_frame, "Etapas:", 'heading_sm')
        steps_title.pack(anchor='w', pady=(0, 10))
        
        steps_frame = ctk.CTkFrame(details_frame, fg_color=self.colors['bg_tertiary'], corner_radius=8)
        steps_frame.pack(fill='x')
        
        steps_inner = ctk.CTkFrame(steps_frame, fg_color='transparent')
        steps_inner.pack(padx=15, pady=10)
        
        for idx, etapa in enumerate(self.selected_recipe.get('etapas', [])):
            step_text = f"{idx + 1}. {etapa['nome']} ({etapa['duracao']} min)"
            step_label = self.create_label(steps_inner, step_text, 'caption')
            step_label.pack(anchor='w', pady=2)
            
    def generate_lote_number(self):
        """Gera um número de lote automático"""
        lote = f"L{datetime.now().strftime('%Y%m%d%H%M')}"
        self.lote_entry.delete(0, 'end')
        self.lote_entry.insert(0, lote)
        
    def calculate_scaling(self):
        """Calcula a escala baseada no volume"""
        if not self.selected_recipe:
            return
            
        try:
            new_volume = float(self.volume_entry.get())
            original_volume = self.selected_recipe.get('volume', 20)
            scale = (new_volume / original_volume) * 100
            self.scale_label.configure(text=f"Escala: {scale:.0f}%")
        except:
            self.scale_label.configure(text="Escala: ---%")
            
    def filter_recipes(self):
        """Filtra as receitas baseado na busca"""
        search_term = self.search_entry.get().lower()
        recipes = mock_loader.get_receitas()
        
        if search_term:
            filtered = [r for r in recipes if search_term in r.get('nome', '').lower()]
        else:
            filtered = recipes
            
        self.display_recipes(filtered)
        
    def validate_production(self) -> bool:
        """Valida os dados da produção"""
        errors = []
        
        if not self.selected_recipe:
            errors.append("Selecione uma receita")
            
        if not self.lote_entry.get():
            errors.append("Número do lote é obrigatório")
            
        try:
            volume = float(self.volume_entry.get())
            if volume <= 0:
                errors.append("Volume deve ser maior que zero")
        except:
            errors.append("Volume inválido")
            
        # Verificar checklist
        unchecked = [item for item, var in self.checklist_vars.items() if not var.get()]
        if unchecked:
            errors.append(f"{len(unchecked)} itens do checklist não foram marcados")
            
        if errors:
            error_msg = "Corrija os seguintes itens:\n\n" + "\n".join(errors)
            self.show_message(error_msg, 'error')
            return False
            
        return True
        
    def start_production(self):
        """Inicia a produção"""
        if not self.validate_production():
            return
            
        # Coletar dados
        production_data = {
            'id': str(uuid.uuid4()),
            'lote': self.lote_entry.get(),
            'receita_id': self.selected_recipe['id'],
            'receita_nome': self.selected_recipe['nome'],
            'status': 'Em Andamento',
            'data_inicio': datetime.now().isoformat(),
            'etapa_atual': 1,
            'total_etapas': len(self.selected_recipe.get('etapas', [])),
            'progresso': 0,
            'volume_planejado': float(self.volume_entry.get()),
            'notas_iniciais': self.notes_text.get("1.0", "end-1c").strip()
        }
        
        # Medições iniciais
        try:
            production_data['og_medido'] = float(self.og_entry.get()) if self.og_entry.get() else None
            production_data['temperatura_inicial'] = float(self.temp_entry.get()) if self.temp_entry.get() else None
            production_data['ph_inicial'] = float(self.ph_entry.get()) if self.ph_entry.get() else None
        except:
            pass
            
        # Aqui seria salvo no backend e iniciada a produção
        self.show_message(f"Produção {production_data['lote']} iniciada com sucesso!", 'success')
        
        # Navegar para o monitoramento
        self.navigation.navigate_to('monitoramento', production_id=production_data['lote'])
        
    def cancel_production(self):
        """Cancela a criação da produção"""
        self.navigation.navigate_to('dashboard')
        
    def on_show(self, **kwargs):
        """Callback quando a view é exibida"""
        # Verificar se foi passada uma receita específica
        recipe_id = kwargs.get('recipe_id')
        
        # Limpar seleção anterior
        self.selected_recipe = None
        
        # Limpar campos
        if hasattr(self, 'lote_entry'):
            self.lote_entry.delete(0, 'end')
            self.volume_entry.delete(0, 'end')
            self.notes_text.delete("1.0", "end")
            self.og_entry.delete(0, 'end')
            self.temp_entry.delete(0, 'end')
            self.ph_entry.delete(0, 'end')
            self.search_entry.delete(0, 'end')
            
            # Resetar checklist
            for var in self.checklist_vars.values():
                var.set(False)
                
            # Resetar botão
            self.start_btn.configure(state='disabled')
            
            # Atualizar data/hora
            self.date_label.configure(text=datetime.now().strftime("%d/%m/%Y %H:%M"))
            
            # Atualizar resumo
            self.update_recipe_summary()
            
        # Carregar receitas
        self.load_recipes()
        
        # Se foi passada uma receita, selecioná-la
        if recipe_id:
            recipes = mock_loader.get_receitas()
            for recipe in recipes:
                if recipe.get('id') == recipe_id:
                    self.select_recipe(recipe)
                    break 