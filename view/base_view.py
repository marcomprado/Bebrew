import customtkinter as ctk
import tkinter as tk
from typing import Protocol, Optional, Callable, Any, Union
from abc import ABC, abstractmethod

class NavigationProtocol(Protocol):
    """Protocol para navegação entre telas"""
    def navigate_to(self, view_name: str, **kwargs) -> None: ...
    def go_back(self) -> None: ...

class BaseView(ABC):
    """Classe base para todas as views do Bebrew"""
    
    def __init__(self, parent: ctk.CTk, navigation: NavigationProtocol, title: str = "Bebrew"):
        self.parent = parent
        self.navigation = navigation
        self.title = title
        self.frame: Optional[ctk.CTkFrame] = None
        self.is_created = False
        
        # Configuração do tema escuro
        self.setup_theme()
        
    def setup_theme(self):
        """Configura o tema escuro azul marinho e cores do Bebrew"""
        ctk.set_appearance_mode("dark")
        
        # Cores customizadas do Bebrew - Tema Azul Marinho
        self.colors = {
            'bg_primary': '#1a1f2e',       # Fundo principal azul marinho escuro
            'bg_secondary': '#242937',     # Fundo secundário (cards)
            'bg_tertiary': '#2e3444',      # Fundo terciário (elementos)
            'accent_orange': '#ff6b35',    # Laranja vibrante
            'accent_blue': '#4dabf7',      # Azul vibrante
            'success': '#51cf66',          # Verde sucesso
            'warning': '#ff6b6b',          # Vermelho avisos
            'text_primary': '#ffffff',     # Texto principal
            'text_secondary': '#b8bfc6',   # Texto secundário
            'text_muted': '#7d8590',       # Texto desabilitado
            'border': '#404654',           # Bordas
            'shadow': 'rgba(0,0,0,0.3)'    # Sombras
        }
        
        # Fontes
        self.fonts = {
            'heading_xl': ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            'heading_lg': ctk.CTkFont(family="Helvetica", size=22, weight="bold"),
            'heading_md': ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            'heading_sm': ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            'body_lg': ctk.CTkFont(family="Helvetica", size=15),
            'body_md': ctk.CTkFont(family="Helvetica", size=14),
            'body_sm': ctk.CTkFont(family="Helvetica", size=13),
            'caption': ctk.CTkFont(family="Helvetica", size=12)
        }
        
    def create_frame(self) -> ctk.CTkFrame:
        """Cria o frame principal da view"""
        if self.frame:
            self.frame.destroy()
            
        self.frame = ctk.CTkFrame(self.parent, fg_color=self.colors['bg_primary'])
        self.frame.pack(fill='both', expand=True)
        return self.frame
        
    def create_header(self, parent: Union[ctk.CTkFrame, tk.Widget], title: str, subtitle: str = "") -> ctk.CTkFrame:
        """Cria um cabeçalho moderno para a view"""
        header_frame = ctk.CTkFrame(parent, fg_color='transparent', height=80)
        header_frame.pack(fill='x', padx=30, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Container do título
        title_container = ctk.CTkFrame(header_frame, fg_color='transparent')
        title_container.pack(side='left', fill='y')
        
        # Título
        title_label = ctk.CTkLabel(
            title_container,
            text=title,
            font=self.fonts['heading_xl'],
            text_color=self.colors['text_primary']
        )
        title_label.pack(anchor='w', pady=(10, 0))
        
        # Subtítulo se fornecido
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                title_container,
                text=subtitle,
                font=self.fonts['body_md'],
                text_color=self.colors['text_secondary']
            )
            subtitle_label.pack(anchor='w')
        
        return header_frame
        
    def create_button(self, parent: Union[ctk.CTkFrame, tk.Widget], text: str, command: Callable, 
                     style: str = 'primary', icon: str = "", **kwargs) -> ctk.CTkButton:
        """Cria um botão moderno com outline"""
        # Configurações de estilo
        styles = {
            'primary': {
                'fg_color': 'transparent',
                'border_color': self.colors['accent_orange'],
                'text_color': self.colors['accent_orange'],
                'hover_color': self.colors['accent_orange']
            },
            'secondary': {
                'fg_color': 'transparent',
                'border_color': self.colors['accent_blue'],
                'text_color': self.colors['accent_blue'],
                'hover_color': self.colors['accent_blue']
            },
            'success': {
                'fg_color': 'transparent',
                'border_color': self.colors['success'],
                'text_color': self.colors['success'],
                'hover_color': self.colors['success']
            },
            'warning': {
                'fg_color': 'transparent',
                'border_color': self.colors['warning'],
                'text_color': self.colors['warning'],
                'hover_color': self.colors['warning']
            },
            'solid_primary': {
                'fg_color': self.colors['accent_orange'],
                'border_color': self.colors['accent_orange'],
                'text_color': self.colors['text_primary'],
                'hover_color': '#ff5722'
            },
            'solid_secondary': {
                'fg_color': self.colors['accent_blue'],
                'border_color': self.colors['accent_blue'],
                'text_color': self.colors['text_primary'],
                'hover_color': '#339af0'
            }
        }
        
        config = styles.get(style, styles['primary'])
        
        # Adicionar ícone ao texto se fornecido
        display_text = f"{icon} {text}" if icon else text
        
        button = ctk.CTkButton(
            parent,
            text=display_text,
            command=command,
            fg_color=config['fg_color'],
            border_color=config['border_color'],
            text_color=config['text_color'],
            hover_color=config['hover_color'],
            border_width=2,
            font=self.fonts['body_md'],
            corner_radius=8,
            **kwargs
        )
        
        # Efeito hover customizado para botões outline
        if style in ['primary', 'secondary', 'success', 'warning']:
            def on_enter(e):
                button.configure(fg_color=config['hover_color'], text_color=self.colors['text_primary'])
            
            def on_leave(e):
                button.configure(fg_color='transparent', text_color=config['text_color'])
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        return button
        
    def create_card(self, parent: Union[ctk.CTkFrame, tk.Widget], title: str = "", padding: int = 20, **kwargs) -> ctk.CTkFrame:
        """Cria um card moderno com sombra"""
        # Container com padding para sombra
        shadow_container = ctk.CTkFrame(parent, fg_color='transparent')
        
        # Card principal
        card = ctk.CTkFrame(
            shadow_container,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12,
            **kwargs
        )
        card.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Adicionar título se fornecido
        if title:
            title_frame = ctk.CTkFrame(card, fg_color='transparent', height=50)
            title_frame.pack(fill='x', padx=padding, pady=(padding, 0))
            title_frame.pack_propagate(False)
            
            title_label = ctk.CTkLabel(
                title_frame,
                text=title,
                font=self.fonts['heading_md'],
                text_color=self.colors['text_primary']
            )
            title_label.pack(anchor='w', pady=5)
            
            # Linha separadora
            separator = ctk.CTkFrame(card, fg_color=self.colors['border'], height=1)
            separator.pack(fill='x', padx=padding, pady=(0, padding))
            
        return card
        
    def create_input(self, parent: Union[ctk.CTkFrame, tk.Widget], placeholder: str = "", **kwargs) -> ctk.CTkEntry:
        """Cria um campo de entrada moderno"""
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            fg_color=self.colors['bg_tertiary'],
            border_color=self.colors['border'],
            text_color=self.colors['text_primary'],
            placeholder_text_color=self.colors['text_muted'],
            font=self.fonts['body_md'],
            corner_radius=8,
            border_width=1,
            **kwargs
        )
        
    def create_label(self, parent: Union[ctk.CTkFrame, tk.Widget], text: str, style: str = 'body', **kwargs) -> ctk.CTkLabel:
        """Cria um label com tipografia moderna"""
        styles = {
            'heading_xl': {'font': self.fonts['heading_xl'], 'color': self.colors['text_primary']},
            'heading_lg': {'font': self.fonts['heading_lg'], 'color': self.colors['text_primary']},
            'heading_md': {'font': self.fonts['heading_md'], 'color': self.colors['text_primary']},
            'heading_sm': {'font': self.fonts['heading_sm'], 'color': self.colors['text_primary']},
            'body': {'font': self.fonts['body_md'], 'color': self.colors['text_primary']},
            'body_secondary': {'font': self.fonts['body_md'], 'color': self.colors['text_secondary']},
            'caption': {'font': self.fonts['caption'], 'color': self.colors['text_muted']},
            'success': {'font': self.fonts['body_md'], 'color': self.colors['success']},
            'warning': {'font': self.fonts['body_md'], 'color': self.colors['warning']},
            'accent': {'font': self.fonts['body_md'], 'color': self.colors['accent_orange']}
        }
        
        style_config = styles.get(style, styles['body'])
        
        return ctk.CTkLabel(
            parent,
            text=text,
            font=style_config['font'],
            text_color=style_config['color'],
            **kwargs
        )
        
    def create_sidebar_button(self, parent: Union[ctk.CTkFrame, tk.Widget], text: str, icon: str, 
                            command: Callable, is_active: bool = False) -> ctk.CTkButton:
        """Cria um botão para o menu lateral"""
        button = ctk.CTkButton(
            parent,
            text=f"{icon}  {text}",
            command=command,
            fg_color=self.colors['bg_tertiary'] if is_active else 'transparent',
            hover_color=self.colors['bg_tertiary'],
            text_color=self.colors['text_primary'] if is_active else self.colors['text_secondary'],
            anchor='w',
            font=self.fonts['body_md'],
            corner_radius=8,
            height=45
        )
        
        # Adicionar indicador de ativo
        if is_active:
            indicator = ctk.CTkFrame(button, fg_color=self.colors['accent_orange'], width=3)
            indicator.place(x=0, y=5, relheight=0.8)
        
        return button
        
    def create_stat_card(self, parent: Union[ctk.CTkFrame, tk.Widget], label: str, 
                        value: str, icon: str = "", color: str = None) -> ctk.CTkFrame:
        """Cria um card de estatística moderno"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12,
            height=100
        )
        
        # Container interno
        inner = ctk.CTkFrame(card, fg_color='transparent')
        inner.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Ícone e label
        top_row = ctk.CTkFrame(inner, fg_color='transparent')
        top_row.pack(fill='x')
        
        if icon:
            icon_label = ctk.CTkLabel(
                top_row,
                text=icon,
                font=ctk.CTkFont(size=20),
                text_color=color or self.colors['text_secondary']
            )
            icon_label.pack(side='left', padx=(0, 8))
        
        label_widget = ctk.CTkLabel(
            top_row,
            text=label,
            font=self.fonts['caption'],
            text_color=self.colors['text_secondary']
        )
        label_widget.pack(side='left')
        
        # Valor
        value_widget = ctk.CTkLabel(
            inner,
            text=value,
            font=self.fonts['heading_lg'],
            text_color=color or self.colors['text_primary']
        )
        value_widget.pack(anchor='w', pady=(5, 0))
        
        return card
        
    def show_message(self, message: str, type: str = 'info'):
        """Exibe uma mensagem temporária"""
        # Esta funcionalidade pode ser expandida para mostrar toasts/notificações
        print(f"[{type.upper()}] {message}")
        
    @abstractmethod
    def create_widgets(self):
        """Método abstrato para criar os widgets específicos da view"""
        pass
        
    def show(self, **kwargs):
        """Exibe a view"""
        if not self.is_created:
            self.create_frame()
            self.create_widgets()
            self.is_created = True
        
        # Atualizar dados se necessário
        self.on_show(**kwargs)
        
    def hide(self):
        """Oculta a view"""
        if self.frame:
            self.frame.pack_forget()
            
    def destroy(self):
        """Destrói a view completamente"""
        if self.frame:
            self.frame.destroy()
            self.frame = None
        self.is_created = False
        
    def on_show(self, **kwargs):
        """Callback chamado quando a view é exibida (para ser sobrescrito)"""
        pass
        
    def refresh(self):
        """Atualiza os dados da view (para ser sobrescrito)"""
        pass 