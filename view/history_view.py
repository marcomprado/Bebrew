import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
from util.mock_data_loader import mock_loader
from datetime import datetime

class HistoryView(BaseView):
    """View para histórico de produções concluídas"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Histórico")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Widgets principais
        self.search_entry = None
        self.type_filter = None
        self.history_list_frame = None
        self.history_data = []
        
    def create_widgets(self):
        """Cria os widgets da view de histórico"""
        # Header
        header = self.create_header(
            self.frame, 
            "Histórico de Produções", 
            "Análise de produções concluídas"
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
        
        # Seção de estatísticas (topo)
        self.create_stats_section()
        
        # Seção de filtros
        self.create_filter_section()
        
        # Lista de histórico
        self.create_history_list_section()
        
    def create_stats_section(self):
        """Cria a seção de estatísticas gerais"""
        # Container de estatísticas
        stats_container = ctk.CTkFrame(self.main_scroll, fg_color='transparent')
        stats_container.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Grid de cards
        stats_container.grid_columnconfigure(0, weight=1, uniform="stats")
        stats_container.grid_columnconfigure(1, weight=1, uniform="stats")
        stats_container.grid_columnconfigure(2, weight=1, uniform="stats")
        stats_container.grid_columnconfigure(3, weight=1, uniform="stats")
        
        # Calcular estatísticas
        historico = mock_loader.get_historico()
        total_producoes = len(historico)
        
        # ABV médio
        abvs = [h.get('abv', 0) for h in historico if h.get('abv')]
        abv_medio = sum(abvs) / len(abvs) if abvs else 0
        
        # Taxa de sucesso
        concluidas = len([h for h in historico if h.get('status') == 'Concluída'])
        taxa_sucesso = (concluidas / total_producoes * 100) if total_producoes > 0 else 0
        
        # Avaliação média
        avaliacoes = [h.get('avaliacao', 0) for h in historico if h.get('avaliacao')]
        avaliacao_media = sum(avaliacoes) / len(avaliacoes) if avaliacoes else 0
        
        # Cards de estatísticas
        stats_data = [
            ("Total de Produções", str(total_producoes), "📊", self.colors['accent_blue']),
            ("ABV Médio", f"{abv_medio:.1f}%", "🍺", self.colors['accent_orange']),
            ("Taxa de Sucesso", f"{taxa_sucesso:.0f}%", "✅", self.colors['success']),
            ("Avaliação Média", f"{avaliacao_media:.1f}/5", "⭐", self.colors['warning'])
        ]
        
        for idx, (label, value, icon, color) in enumerate(stats_data):
            card = self.create_stat_card(stats_container, label, value, icon, color)
            card.grid(row=0, column=idx, padx=10, sticky='ew')
            
    def create_filter_section(self):
        """Cria a seção de filtros"""
        filter_card = self.create_card(self.main_scroll, padding=20)
        filter_card.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Container de filtros
        filter_container = ctk.CTkFrame(filter_card, fg_color='transparent')
        filter_container.pack(fill='x', padx=20, pady=20)
        
        # Grid para organizar filtros
        filter_container.grid_columnconfigure(0, weight=2)  # Busca
        filter_container.grid_columnconfigure(1, weight=1)  # Tipo
        filter_container.grid_columnconfigure(2, weight=1)  # Período
        filter_container.grid_columnconfigure(3, weight=0)  # Botão
        
        # Campo de busca
        search_label = self.create_label(filter_container, "Buscar:", 'body_secondary')
        search_label.grid(row=0, column=0, sticky='w', padx=(0, 10), pady=(0, 5))
        
        self.search_entry = self.create_input(
            filter_container,
            placeholder="Nome da receita ou lote...",
            width=300
        )
        self.search_entry.grid(row=1, column=0, sticky='ew', padx=(0, 20))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_history())
        
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
        
        # Filtro por período
        period_label = self.create_label(filter_container, "Período:", 'body_secondary')
        period_label.grid(row=0, column=2, sticky='w', padx=(0, 10), pady=(0, 5))
        
        self.period_filter = ctk.CTkComboBox(
            filter_container,
            values=["Todos", "Última Semana", "Último Mês", "Últimos 3 Meses", "Último Ano"],
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md'],
            command=self.on_filter_change
        )
        self.period_filter.grid(row=1, column=2, sticky='ew', padx=(0, 20))
        self.period_filter.set("Todos")
        
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
        
    def create_history_list_section(self):
        """Cria a seção de lista de histórico"""
        # Container da lista
        list_card = self.create_card(self.main_scroll, title="Produções Concluídas", padding=0)
        list_card.grid(row=2, column=0, columnspan=2, sticky='ew')
        
        # Frame para a lista
        self.history_list_frame = ctk.CTkFrame(list_card, fg_color='transparent')
        self.history_list_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Carregar histórico
        self.load_history()
        
    def create_history_item(self, parent, history_data: Dict):
        """Cria um item de histórico na lista"""
        # Container do item
        item_frame = ctk.CTkFrame(
            parent, 
            fg_color=self.colors['bg_tertiary'],
            corner_radius=12,
            height=140
        )
        item_frame.pack(fill='x', pady=8)
        item_frame.pack_propagate(False)
        
        # Container interno com padding
        inner = ctk.CTkFrame(item_frame, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Grid para organizar conteúdo
        inner.grid_columnconfigure(0, weight=1)  # Info
        inner.grid_columnconfigure(1, weight=0)  # Métricas
        
        # Container de informações
        info_frame = ctk.CTkFrame(inner, fg_color='transparent')
        info_frame.grid(row=0, column=0, sticky='ew')
        
        # Primeira linha: Nome e badges
        top_row = ctk.CTkFrame(info_frame, fg_color='transparent')
        top_row.pack(fill='x', pady=(0, 8))
        
        # Nome da receita
        name_label = self.create_label(
            top_row,
            history_data.get('receita_nome', 'N/A'),
            'heading_sm'
        )
        name_label.pack(side='left', padx=(0, 15))
        
        # Badge do tipo
        type_badge = ctk.CTkLabel(
            top_row,
            text=history_data.get('tipo', 'N/A').upper(),
            font=self.fonts['caption'],
            text_color=self.colors['text_primary'],
            fg_color=self.colors['accent_blue'],
            corner_radius=4,
            padx=10,
            pady=3
        )
        type_badge.pack(side='left', padx=(0, 10))
        
        # Badge de status
        status_color = self.colors['success'] if history_data.get('status') == 'Concluída' else self.colors['warning']
        status_badge = ctk.CTkLabel(
            top_row,
            text=history_data.get('status', 'N/A'),
            font=self.fonts['caption'],
            text_color=self.colors['text_primary'],
            fg_color=status_color,
            corner_radius=4,
            padx=10,
            pady=3
        )
        status_badge.pack(side='left')
        
        # Segunda linha: Detalhes
        details_text = f"Lote: {history_data.get('lote', 'N/A')}  •  "
        details_text += f"Período: {self.format_date(history_data.get('data_inicio', ''))} - "
        details_text += f"{self.format_date(history_data.get('data_fim', ''))}"
        
        details_label = self.create_label(info_frame, details_text, 'body_secondary')
        details_label.pack(anchor='w', pady=(0, 8))
        
        # Terceira linha: Notas
        if history_data.get('notas'):
            notes_label = self.create_label(
                info_frame,
                f'"{history_data.get("notas", "")}"',
                'caption'
            )
            notes_label.pack(anchor='w')
        
        # Container de métricas
        metrics_frame = ctk.CTkFrame(inner, fg_color='transparent')
        metrics_frame.grid(row=0, column=1, padx=(20, 0))
        
        # Métricas
        metrics_container = ctk.CTkFrame(metrics_frame, fg_color=self.colors['bg_secondary'], corner_radius=8)
        metrics_container.pack()
        
        metrics_inner = ctk.CTkFrame(metrics_container, fg_color='transparent')
        metrics_inner.pack(padx=15, pady=10)
        
        # ABV
        abv_label = self.create_label(metrics_inner, "ABV", 'caption')
        abv_label.pack()
        abv_value = self.create_label(
            metrics_inner, 
            f"{history_data.get('abv', 0):.1f}%", 
            'heading_sm'
        )
        abv_value.pack(pady=(0, 10))
        
        # Volume
        vol_label = self.create_label(metrics_inner, "Volume", 'caption')
        vol_label.pack()
        vol_value = self.create_label(
            metrics_inner, 
            f"{history_data.get('volume_final', 0):.1f}L", 
            'body'
        )
        vol_value.pack(pady=(0, 10))
        
        # Avaliação
        if history_data.get('avaliacao'):
            rating_label = self.create_label(metrics_inner, "Avaliação", 'caption')
            rating_label.pack()
            
            # Estrelas
            stars = "⭐" * int(history_data.get('avaliacao', 0))
            stars_label = self.create_label(metrics_inner, stars, 'body')
            stars_label.pack()
            
    def load_history(self):
        """Carrega o histórico do mock data"""
        self.history_data = mock_loader.get_historico()
        self.display_history(self.history_data)
        
    def display_history(self, history: List[Dict]):
        """Exibe o histórico na lista"""
        # Limpar lista atual
        for widget in self.history_list_frame.winfo_children():
            widget.destroy()
            
        if not history:
            no_history_label = self.create_label(
                self.history_list_frame,
                "Nenhuma produção concluída encontrada",
                'body_secondary'
            )
            no_history_label.pack(pady=40)
        else:
            for item in history:
                self.create_history_item(self.history_list_frame, item)
                
    def filter_history(self):
        """Filtra o histórico baseado nos critérios"""
        search_term = self.search_entry.get().lower()
        type_filter = self.type_filter.get()
        period_filter = self.period_filter.get()
        
        filtered = self.history_data
        
        # Filtro por busca
        if search_term:
            filtered = [h for h in filtered if 
                       search_term in h.get('receita_nome', '').lower() or
                       search_term in h.get('lote', '').lower()]
        
        # Filtro por tipo
        if type_filter != "Todos":
            filtered = [h for h in filtered if h.get('tipo') == type_filter]
        
        # Filtro por período (simplificado para o mock)
        # Em produção, seria feito com datas reais
        if period_filter == "Última Semana":
            filtered = filtered[:2]
        elif period_filter == "Último Mês":
            filtered = filtered[:5]
        
        self.display_history(filtered)
        
    def on_filter_change(self, value):
        """Callback para mudança nos filtros"""
        self.filter_history()
        
    def clear_filters(self):
        """Limpa todos os filtros"""
        self.search_entry.delete(0, 'end')
        self.type_filter.set("Todos")
        self.period_filter.set("Todos")
        self.filter_history()
        
    def format_date(self, date_string: str) -> str:
        """Formata uma string de data"""
        if not date_string:
            return "N/A"
        try:
            if 'T' in date_string:
                dt = datetime.fromisoformat(date_string)
            else:
                dt = datetime.strptime(date_string, '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except:
            return date_string
            
    def on_show(self, **kwargs):
        """Callback quando a view é exibida"""
        self.load_history()
        
    def refresh(self):
        """Atualiza o histórico"""
        self.load_history()
