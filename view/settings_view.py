import customtkinter as ctk
from .base_view import BaseView
from typing import Optional, Dict, List
from util.mock_data_loader import mock_loader

class SettingsView(BaseView):
    """View para configurações do sistema"""
    
    def __init__(self, parent, navigation, brew_controller, recipe_controller):
        super().__init__(parent, navigation, "Configurações")
        self.brew_controller = brew_controller
        self.recipe_controller = recipe_controller
        
        # Carregar configurações atuais
        self.settings = mock_loader.get_configuracoes()
        
        # Widgets principais
        self.temp_unit_var = None
        self.volume_unit_var = None
        self.weight_unit_var = None
        self.density_unit_var = None
        self.theme_var = None
        self.language_var = None
        self.alerts_temp_var = None
        self.alerts_time_var = None
        self.sound_var = None
        
    def create_widgets(self):
        """Cria os widgets da view de configurações"""
        # Header
        header = self.create_header(
            self.frame, 
            "Configurações", 
            "Personalize o sistema de acordo com suas preferências"
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
        
        # Seção de unidades (esquerda)
        self.create_units_section()
        
        # Seção de interface (direita)
        self.create_interface_section()
        
        # Seção de notificações (largura total)
        self.create_notifications_section()
        
        # Seção de dados (largura total)
        self.create_data_section()
        
        # Botões de ação (largura total)
        self.create_action_buttons()
        
    def create_units_section(self):
        """Cria a seção de configuração de unidades"""
        units_card = self.create_card(self.main_scroll, title="Unidades de Medida", padding=20)
        units_card.grid(row=0, column=0, sticky='ew', padx=(0, 10), pady=(0, 20))
        
        # Container interno
        content = ctk.CTkFrame(units_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Temperatura
        temp_label = self.create_label(content, "Temperatura:", 'body_secondary')
        temp_label.pack(anchor='w', pady=(0, 5))
        
        self.temp_unit_var = ctk.StringVar(value=self.settings.get('unidades', {}).get('temperatura', 'celsius'))
        temp_frame = ctk.CTkFrame(content, fg_color='transparent')
        temp_frame.pack(fill='x', pady=(0, 15))
        
        celsius_radio = ctk.CTkRadioButton(
            temp_frame,
            text="Celsius (°C)",
            variable=self.temp_unit_var,
            value="celsius",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        celsius_radio.pack(side='left', padx=(0, 20))
        
        fahrenheit_radio = ctk.CTkRadioButton(
            temp_frame,
            text="Fahrenheit (°F)",
            variable=self.temp_unit_var,
            value="fahrenheit",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        fahrenheit_radio.pack(side='left')
        
        # Volume
        volume_label = self.create_label(content, "Volume:", 'body_secondary')
        volume_label.pack(anchor='w', pady=(0, 5))
        
        self.volume_unit_var = ctk.StringVar(value=self.settings.get('unidades', {}).get('volume', 'litros'))
        volume_frame = ctk.CTkFrame(content, fg_color='transparent')
        volume_frame.pack(fill='x', pady=(0, 15))
        
        litros_radio = ctk.CTkRadioButton(
            volume_frame,
            text="Litros (L)",
            variable=self.volume_unit_var,
            value="litros",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        litros_radio.pack(side='left', padx=(0, 20))
        
        galoes_radio = ctk.CTkRadioButton(
            volume_frame,
            text="Galões (gal)",
            variable=self.volume_unit_var,
            value="galoes",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        galoes_radio.pack(side='left')
        
        # Peso
        weight_label = self.create_label(content, "Peso:", 'body_secondary')
        weight_label.pack(anchor='w', pady=(0, 5))
        
        self.weight_unit_var = ctk.StringVar(value=self.settings.get('unidades', {}).get('peso', 'kg'))
        weight_frame = ctk.CTkFrame(content, fg_color='transparent')
        weight_frame.pack(fill='x', pady=(0, 15))
        
        kg_radio = ctk.CTkRadioButton(
            weight_frame,
            text="Quilogramas (kg)",
            variable=self.weight_unit_var,
            value="kg",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        kg_radio.pack(side='left', padx=(0, 20))
        
        lb_radio = ctk.CTkRadioButton(
            weight_frame,
            text="Libras (lb)",
            variable=self.weight_unit_var,
            value="lb",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        lb_radio.pack(side='left')
        
        # Densidade
        density_label = self.create_label(content, "Densidade:", 'body_secondary')
        density_label.pack(anchor='w', pady=(0, 5))
        
        self.density_unit_var = ctk.StringVar(value=self.settings.get('unidades', {}).get('densidade', 'sg'))
        density_frame = ctk.CTkFrame(content, fg_color='transparent')
        density_frame.pack(fill='x')
        
        sg_radio = ctk.CTkRadioButton(
            density_frame,
            text="Specific Gravity (SG)",
            variable=self.density_unit_var,
            value="sg",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        sg_radio.pack(side='left', padx=(0, 20))
        
        brix_radio = ctk.CTkRadioButton(
            density_frame,
            text="Brix",
            variable=self.density_unit_var,
            value="brix",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        brix_radio.pack(side='left')
        
    def create_interface_section(self):
        """Cria a seção de configuração de interface"""
        interface_card = self.create_card(self.main_scroll, title="Interface", padding=20)
        interface_card.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=(0, 20))
        
        # Container interno
        content = ctk.CTkFrame(interface_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tema
        theme_label = self.create_label(content, "Tema:", 'body_secondary')
        theme_label.pack(anchor='w', pady=(0, 5))
        
        self.theme_var = ctk.StringVar(value=self.settings.get('interface', {}).get('tema', 'dark'))
        theme_frame = ctk.CTkFrame(content, fg_color='transparent')
        theme_frame.pack(fill='x', pady=(0, 20))
        
        dark_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Escuro",
            variable=self.theme_var,
            value="dark",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        dark_radio.pack(side='left', padx=(0, 20))
        
        light_radio = ctk.CTkRadioButton(
            theme_frame,
            text="Claro",
            variable=self.theme_var,
            value="light",
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange']
        )
        light_radio.pack(side='left')
        
        # Idioma
        language_label = self.create_label(content, "Idioma:", 'body_secondary')
        language_label.pack(anchor='w', pady=(0, 5))
        
        self.language_var = ctk.StringVar(value=self.settings.get('interface', {}).get('idioma', 'pt-BR'))
        self.language_combo = ctk.CTkComboBox(
            content,
            values=["pt-BR", "en-US", "es-ES"],
            variable=self.language_var,
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            button_color=self.colors['accent_blue'],
            dropdown_fg_color=self.colors['bg_secondary'],
            dropdown_hover_color=self.colors['bg_tertiary'],
            font=self.fonts['body_md'],
            dropdown_font=self.fonts['body_md'],
            width=200
        )
        self.language_combo.pack(anchor='w', pady=(0, 20))
        
        # Mostrar dicas
        self.tips_var = ctk.BooleanVar(value=self.settings.get('interface', {}).get('mostrar_dicas', True))
        tips_check = ctk.CTkCheckBox(
            content,
            text="Mostrar dicas e ajuda",
            variable=self.tips_var,
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange'],
            font=self.fonts['body_md']
        )
        tips_check.pack(anchor='w')
        
    def create_notifications_section(self):
        """Cria a seção de configuração de notificações"""
        notifications_card = self.create_card(self.main_scroll, title="Notificações", padding=20)
        notifications_card.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Container interno
        content = ctk.CTkFrame(notifications_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Grid para organizar checkboxes
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        
        # Alertas de temperatura
        self.alerts_temp_var = ctk.BooleanVar(
            value=self.settings.get('notificacoes', {}).get('alertas_temperatura', True)
        )
        temp_alert_check = ctk.CTkCheckBox(
            content,
            text="Alertas de temperatura",
            variable=self.alerts_temp_var,
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange'],
            font=self.fonts['body_md']
        )
        temp_alert_check.grid(row=0, column=0, sticky='w', pady=5)
        
        # Alertas de tempo
        self.alerts_time_var = ctk.BooleanVar(
            value=self.settings.get('notificacoes', {}).get('alertas_tempo', True)
        )
        time_alert_check = ctk.CTkCheckBox(
            content,
            text="Alertas de tempo/etapas",
            variable=self.alerts_time_var,
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange'],
            font=self.fonts['body_md']
        )
        time_alert_check.grid(row=0, column=1, sticky='w', pady=5)
        
        # Som
        self.sound_var = ctk.BooleanVar(
            value=self.settings.get('notificacoes', {}).get('som', True)
        )
        sound_check = ctk.CTkCheckBox(
            content,
            text="Som nas notificações",
            variable=self.sound_var,
            border_color=self.colors['accent_orange'],
            hover_color=self.colors['accent_orange'],
            font=self.fonts['body_md']
        )
        sound_check.grid(row=1, column=0, sticky='w', pady=5)
        
    def create_data_section(self):
        """Cria a seção de gerenciamento de dados"""
        data_card = self.create_card(self.main_scroll, title="Dados", padding=20)
        data_card.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Container interno
        content = ctk.CTkFrame(data_card, fg_color='transparent')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Informações sobre dados
        info_text = "Gerencie seus dados de receitas e produções"
        info_label = self.create_label(content, info_text, 'body_secondary')
        info_label.pack(anchor='w', pady=(0, 20))
        
        # Botões de ação
        button_frame = ctk.CTkFrame(content, fg_color='transparent')
        button_frame.pack(fill='x')
        
        export_btn = self.create_button(
            button_frame,
            "Exportar Dados",
            self.export_data,
            style='secondary',
            icon="📤",
            width=150,
            height=40
        )
        export_btn.pack(side='left', padx=(0, 10))
        
        import_btn = self.create_button(
            button_frame,
            "Importar Dados",
            self.import_data,
            style='secondary',
            icon="📥",
            width=150,
            height=40
        )
        import_btn.pack(side='left', padx=(0, 10))
        
        backup_btn = self.create_button(
            button_frame,
            "Fazer Backup",
            self.backup_data,
            style='primary',
            icon="💾",
            width=150,
            height=40
        )
        backup_btn.pack(side='left')
        
    def create_action_buttons(self):
        """Cria os botões de ação principais"""
        action_frame = ctk.CTkFrame(self.main_scroll, fg_color='transparent')
        action_frame.grid(row=3, column=0, columnspan=2, sticky='ew')
        
        # Container para centralizar botões
        button_container = ctk.CTkFrame(action_frame, fg_color='transparent')
        button_container.pack(anchor='e')
        
        # Botão cancelar
        cancel_btn = self.create_button(
            button_container,
            "Cancelar",
            self.cancel_changes,
            style='secondary',
            width=120,
            height=40
        )
        cancel_btn.pack(side='left', padx=(0, 10))
        
        # Botão salvar
        save_btn = self.create_button(
            button_container,
            "Salvar Alterações",
            self.save_settings,
            style='primary',
            width=150,
            height=40
        )
        save_btn.pack(side='left')
        
    def save_settings(self):
        """Salva as configurações alteradas"""
        # Coletar valores atuais
        new_settings = {
            'unidades': {
                'temperatura': self.temp_unit_var.get(),
                'volume': self.volume_unit_var.get(),
                'peso': self.weight_unit_var.get(),
                'densidade': self.density_unit_var.get()
            },
            'notificacoes': {
                'alertas_temperatura': self.alerts_temp_var.get(),
                'alertas_tempo': self.alerts_time_var.get(),
                'som': self.sound_var.get()
            },
            'interface': {
                'tema': self.theme_var.get(),
                'idioma': self.language_var.get(),
                'mostrar_dicas': self.tips_var.get()
            }
        }
        
        # Aqui seria salvo no backend
        self.show_message("Configurações salvas com sucesso!", 'success')
        
        # Aplicar tema se mudou
        if self.theme_var.get() != self.settings.get('interface', {}).get('tema'):
            self.show_message("Reinicie o aplicativo para aplicar o novo tema", 'info')
            
    def cancel_changes(self):
        """Cancela as alterações e volta ao dashboard"""
        self.navigation.navigate_to('dashboard')
        
    def export_data(self):
        """Exporta os dados do sistema"""
        self.show_message("Funcionalidade de exportação em desenvolvimento", 'info')
        
    def import_data(self):
        """Importa dados para o sistema"""
        self.show_message("Funcionalidade de importação em desenvolvimento", 'info')
        
    def backup_data(self):
        """Faz backup dos dados"""
        self.show_message("Backup realizado com sucesso!", 'success')
        
    def on_show(self, **kwargs):
        """Callback quando a view é exibida"""
        # Recarregar configurações atuais
        self.settings = mock_loader.get_configuracoes()
        
    def refresh(self):
        """Atualiza as configurações"""
        pass
