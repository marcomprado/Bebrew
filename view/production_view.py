import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
from util.mock_data_loader import mock_loader
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class ProductionView(BaseView):
    """View para monitoramento de produção em tempo real"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Monitoramento")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Dados da produção atual
        self.current_production = None
        self.production_id = None
        
        # Widgets principais
        self.status_label = None
        self.progress_bar = None
        self.temp_entry = None
        self.density_entry = None
        self.notes_text = None
        self.temp_canvas = None
        
    def create_widgets(self):
        """Cria os widgets da view de produção"""
        # Header
        self.header_frame = self.create_header(
            self.frame, 
            "Monitoramento de Produção", 
            "Acompanhe sua produção em tempo real"
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
        
        # Seção de status (esquerda superior)
        self.create_status_section()
        
        # Seção de controles (direita superior)
        self.create_controls_section()
        
        # Seção de gráfico (toda largura)
        self.create_chart_section()
        
        # Seção de registros (toda largura)
        self.create_logs_section()
        
    def create_status_section(self):
        """Cria a seção de status da produção"""
        status_card = self.create_card(self.main_scroll, title="Status da Produção", padding=20)
        status_card.grid(row=0, column=0, sticky='ew', padx=(0, 10), pady=(0, 20))
        
        # Container interno
        content = ctk.CTkFrame(status_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Informações da produção
        self.production_info_frame = ctk.CTkFrame(content, fg_color='transparent')
        self.production_info_frame.pack(fill='x', pady=(0, 20))
        
        # Barra de progresso
        progress_label = self.create_label(content, "Progresso Geral:", 'body_secondary')
        progress_label.pack(anchor='w', pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(
            content,
            width=400,
            height=20,
            progress_color=self.colors['accent_orange'],
            fg_color=self.colors['bg_tertiary']
        )
        self.progress_bar.pack(fill='x', pady=(0, 5))
        self.progress_bar.set(0)
        
        self.progress_label = self.create_label(content, "0%", 'heading_sm')
        self.progress_label.pack(anchor='w', pady=(0, 20))
        
        # Etapa atual
        self.current_step_frame = ctk.CTkFrame(content, fg_color='transparent')
        self.current_step_frame.pack(fill='x')
        
        # Botões de controle de etapa
        button_frame = ctk.CTkFrame(content, fg_color='transparent')
        button_frame.pack(fill='x', pady=(20, 0))
        
        self.prev_step_btn = self.create_button(
            button_frame,
            "← Etapa Anterior",
            self.previous_step,
            style='secondary',
            width=150,
            height=40
        )
        self.prev_step_btn.pack(side='left', padx=(0, 10))
        
        self.next_step_btn = self.create_button(
            button_frame,
            "Próxima Etapa →",
            self.next_step,
            style='primary',
            width=150,
            height=40
        )
        self.next_step_btn.pack(side='left')
        
    def create_controls_section(self):
        """Cria a seção de controles e medições"""
        controls_card = self.create_card(self.main_scroll, title="Registrar Medições", padding=20)
        controls_card.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=(0, 20))
        
        # Container interno
        content = ctk.CTkFrame(controls_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Temperatura
        temp_label = self.create_label(content, "Temperatura (°C):", 'body_secondary')
        temp_label.pack(anchor='w', pady=(0, 5))
        
        temp_frame = ctk.CTkFrame(content, fg_color='transparent')
        temp_frame.pack(fill='x', pady=(0, 15))
        
        self.temp_entry = self.create_input(temp_frame, placeholder="Ex: 67.5", width=150)
        self.temp_entry.pack(side='left', padx=(0, 10))
        
        add_temp_btn = self.create_button(
            temp_frame,
            "Registrar",
            self.add_temperature,
            style='solid_primary',
            width=100,
            height=35
        )
        add_temp_btn.pack(side='left')
        
        # Densidade
        density_label = self.create_label(content, "Densidade (SG):", 'body_secondary')
        density_label.pack(anchor='w', pady=(0, 5))
        
        density_frame = ctk.CTkFrame(content, fg_color='transparent')
        density_frame.pack(fill='x', pady=(0, 15))
        
        self.density_entry = self.create_input(density_frame, placeholder="Ex: 1.065", width=150)
        self.density_entry.pack(side='left', padx=(0, 10))
        
        add_density_btn = self.create_button(
            density_frame,
            "Registrar",
            self.add_density,
            style='solid_primary',
            width=100,
            height=35
        )
        add_density_btn.pack(side='left')
        
        # Anotações
        notes_label = self.create_label(content, "Anotações:", 'body_secondary')
        notes_label.pack(anchor='w', pady=(0, 5))
        
        self.notes_text = ctk.CTkTextbox(
            content,
            height=100,
            fg_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_primary'],
            font=self.fonts['body_md']
        )
        self.notes_text.pack(fill='x', pady=(0, 10))
        
        add_note_btn = self.create_button(
            content,
            "Adicionar Anotação",
            self.add_note,
            style='primary',
            width=150,
            height=35
        )
        add_note_btn.pack(anchor='e')
        
    def create_chart_section(self):
        """Cria a seção de gráfico de temperatura"""
        chart_card = self.create_card(self.main_scroll, title="Gráfico de Temperatura", padding=20)
        chart_card.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Container para o gráfico
        self.chart_frame = ctk.CTkFrame(chart_card, fg_color='transparent', height=300)
        self.chart_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
    def create_logs_section(self):
        """Cria a seção de logs e histórico"""
        logs_card = self.create_card(self.main_scroll, title="Histórico de Eventos", padding=20)
        logs_card.grid(row=2, column=0, columnspan=2, sticky='ew')
        
        # Container de logs com scroll
        self.logs_frame = ctk.CTkScrollableFrame(
            logs_card, 
            fg_color='transparent',
            height=200
        )
        self.logs_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
    def load_production(self, production_id: str = None):
        """Carrega os dados da produção"""
        if production_id:
            self.production_id = production_id
            
        # Buscar produção no mock data
        producoes = mock_loader.get_producoes_ativas()
        for prod in producoes:
            if prod.get('id') == self.production_id or prod.get('lote') == self.production_id:
                self.current_production = prod
                break
                
        if not self.current_production:
            # Se não encontrou, pegar a primeira produção ativa
            if producoes:
                self.current_production = producoes[0]
                
        self.update_display()
        
    def update_display(self):
        """Atualiza a exibição com os dados da produção"""
        if not self.current_production:
            return
            
        # Limpar informações antigas
        for widget in self.production_info_frame.winfo_children():
            widget.destroy()
            
        # Informações da produção
        info_text = f"Lote: {self.current_production.get('lote', 'N/A')}\n"
        info_text += f"Receita: {self.current_production.get('receita_nome', 'N/A')}\n"
        info_text += f"Status: {self.current_production.get('status', 'N/A')}\n"
        info_text += f"Início: {self.format_datetime(self.current_production.get('data_inicio', ''))}"
        
        info_label = self.create_label(self.production_info_frame, info_text, 'body')
        info_label.pack(anchor='w')
        
        # Atualizar progresso
        progresso = self.current_production.get('progresso', 0) / 100
        self.progress_bar.set(progresso)
        self.progress_label.configure(text=f"{self.current_production.get('progresso', 0):.0f}%")
        
        # Etapa atual
        for widget in self.current_step_frame.winfo_children():
            widget.destroy()
            
        etapa_info = f"Etapa {self.current_production.get('etapa_atual', 0)} de {self.current_production.get('total_etapas', 0)}"
        etapa_label = self.create_label(self.current_step_frame, etapa_info, 'heading_sm')
        etapa_label.pack(anchor='w')
        
        # Atualizar gráfico
        self.update_temperature_chart()
        
        # Atualizar logs
        self.update_logs()
        
    def update_temperature_chart(self):
        """Atualiza o gráfico de temperatura"""
        # Limpar gráfico anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        if not self.current_production:
            return
            
        temps = self.current_production.get('temperaturas', [])
        if not temps:
            no_data_label = self.create_label(
                self.chart_frame,
                "Nenhuma medição de temperatura registrada",
                'body_secondary'
            )
            no_data_label.pack(expand=True)
            return
            
        # Criar figura
        fig = Figure(figsize=(10, 4), dpi=100)
        fig.patch.set_facecolor(self.colors['bg_secondary'])
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['bg_secondary'])
        
        # Dados
        timestamps = [datetime.fromisoformat(t['timestamp']) for t in temps]
        values = [t['valor'] for t in temps]
        
        # Plot
        ax.plot(timestamps, values, 'o-', color=self.colors['accent_orange'], linewidth=2, markersize=6)
        
        # Configurar eixos
        ax.set_xlabel('Tempo', color=self.colors['text_primary'])
        ax.set_ylabel('Temperatura (°C)', color=self.colors['text_primary'])
        ax.tick_params(colors=self.colors['text_secondary'])
        
        # Formatar datas
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Grid
        ax.grid(True, color=self.colors['border'], alpha=0.3)
        
        # Ajustar layout
        fig.tight_layout()
        
        # Criar canvas
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def update_logs(self):
        """Atualiza o histórico de eventos"""
        # Limpar logs antigos
        for widget in self.logs_frame.winfo_children():
            widget.destroy()
            
        if not self.current_production:
            return
            
        # Adicionar anotações
        anotacoes = self.current_production.get('anotacoes', [])
        for nota in anotacoes:
            timestamp = datetime.fromisoformat(nota['timestamp']).strftime('%H:%M')
            
            log_frame = ctk.CTkFrame(self.logs_frame, fg_color='transparent')
            log_frame.pack(fill='x', pady=5)
            
            time_label = self.create_label(log_frame, f"[{timestamp}]", 'caption')
            time_label.pack(side='left', padx=(0, 10))
            
            text_label = self.create_label(log_frame, nota['texto'], 'body')
            text_label.pack(side='left')
            
    def format_datetime(self, dt_string: str) -> str:
        """Formata uma string de datetime"""
        if not dt_string:
            return "N/A"
        try:
            dt = datetime.fromisoformat(dt_string)
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return dt_string
            
    def add_temperature(self):
        """Adiciona uma medição de temperatura"""
        temp_value = self.temp_entry.get()
        if not temp_value:
            return
            
        try:
            temp = float(temp_value)
            # Aqui seria adicionado ao backend
            self.show_message(f"Temperatura {temp}°C registrada com sucesso!", 'success')
            self.temp_entry.delete(0, 'end')
            # Simular atualização
            self.update_display()
        except ValueError:
            self.show_message("Valor de temperatura inválido", 'error')
            
    def add_density(self):
        """Adiciona uma medição de densidade"""
        density_value = self.density_entry.get()
        if not density_value:
            return
            
        try:
            density = float(density_value)
            # Aqui seria adicionado ao backend
            self.show_message(f"Densidade {density} registrada com sucesso!", 'success')
            self.density_entry.delete(0, 'end')
        except ValueError:
            self.show_message("Valor de densidade inválido", 'error')
            
    def add_note(self):
        """Adiciona uma anotação"""
        note_text = self.notes_text.get("1.0", "end-1c").strip()
        if not note_text:
            return
            
        # Aqui seria adicionado ao backend
        self.show_message("Anotação adicionada com sucesso!", 'success')
        self.notes_text.delete("1.0", "end")
        # Simular atualização
        self.update_logs()
        
    def previous_step(self):
        """Volta para a etapa anterior"""
        self.show_message("Voltando para etapa anterior...", 'info')
        
    def next_step(self):
        """Avança para a próxima etapa"""
        self.show_message("Avançando para próxima etapa...", 'info')
        
    def on_show(self, **kwargs):
        """Callback quando a view é exibida"""
        production_id = kwargs.get('production_id')
        self.load_production(production_id)
        
    def refresh(self):
        """Atualiza os dados da produção"""
        self.load_production()
