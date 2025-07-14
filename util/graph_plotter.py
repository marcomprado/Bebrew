import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTk
from datetime import datetime, timedelta
import numpy as np
from typing import List, Tuple, Optional
import tkinter as tk

class BebrewPlotter:
    """Classe para criar gráficos do Bebrew usando matplotlib"""
    
    def __init__(self, dark_theme: bool = True):
        self.dark_theme = dark_theme
        self.setup_style()
    
    def setup_style(self):
        """Configura o estilo dos gráficos"""
        if self.dark_theme:
            plt.style.use('dark_background')
            self.bg_color = '#2b2b2b'
            self.text_color = 'white'
            self.grid_color = '#404040'
        else:
            plt.style.use('default')
            self.bg_color = 'white'
            self.text_color = 'black'
            self.grid_color = '#cccccc'
    
    def criar_grafico_temperatura(self, temperaturas: List[Tuple[datetime, float]], 
                                temperatura_alvo: Optional[float] = None,
                                titulo: str = "Monitoramento de Temperatura") -> plt.Figure:
        """
        Cria gráfico de temperatura ao longo do tempo
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.bg_color)
        ax.set_facecolor(self.bg_color)
        
        if temperaturas:
            tempos, temps = zip(*temperaturas)
            ax.plot(tempos, temps, 'o-', color='#00ff88', linewidth=2, markersize=4, label='Temperatura Medida')
            
            # Linha de temperatura alvo
            if temperatura_alvo:
                ax.axhline(y=temperatura_alvo, color='#ff6b6b', linestyle='--', 
                          linewidth=2, label=f'Alvo: {temperatura_alvo}°C')
        
        ax.set_xlabel('Tempo', color=self.text_color)
        ax.set_ylabel('Temperatura (°C)', color=self.text_color)
        ax.set_title(titulo, color=self.text_color, fontsize=14, pad=20)
        ax.grid(True, color=self.grid_color, alpha=0.3)
        ax.legend()
        
        # Formatar eixo X para timestamps
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def criar_grafico_progresso_etapas(self, etapas_nomes: List[str], 
                                     etapas_concluidas: int,
                                     titulo: str = "Progresso da Produção") -> plt.Figure:
        """
        Cria gráfico de barras do progresso das etapas
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.bg_color)
        ax.set_facecolor(self.bg_color)
        
        y_pos = np.arange(len(etapas_nomes))
        cores = ['#00ff88' if i < etapas_concluidas else '#404040' for i in range(len(etapas_nomes))]
        
        barras = ax.barh(y_pos, [1] * len(etapas_nomes), color=cores, alpha=0.8)
        
        # Adicionar texto nas barras
        for i, (barra, nome) in enumerate(zip(barras, etapas_nomes)):
            status = "✓" if i < etapas_concluidas else "○"
            ax.text(0.5, barra.get_y() + barra.get_height()/2, 
                   f"{status} {nome}", ha='center', va='center', 
                   color=self.text_color, fontweight='bold')
        
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_title(titulo, color=self.text_color, fontsize=14, pad=20)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_xticks([])
        
        plt.tight_layout()
        return fig
    
    def criar_grafico_densidade(self, medições: List[Tuple[datetime, float]], 
                              og: Optional[float] = None,
                              fg_estimado: Optional[float] = None,
                              titulo: str = "Evolução da Densidade") -> plt.Figure:
        """
        Cria gráfico da evolução da densidade durante fermentação
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.bg_color)
        ax.set_facecolor(self.bg_color)
        
        if medições:
            tempos, densidades = zip(*medições)
            ax.plot(tempos, densidades, 'o-', color='#4dabf7', linewidth=2, 
                   markersize=6, label='Densidade Medida')
        
        # Linhas de referência
        if og:
            ax.axhline(y=og, color='#ff6b6b', linestyle='--', linewidth=2, 
                      label=f'OG: {og:.3f}')
        
        if fg_estimado:
            ax.axhline(y=fg_estimado, color='#51cf66', linestyle='--', linewidth=2, 
                      label=f'FG Estimado: {fg_estimado:.3f}')
        
        ax.set_xlabel('Tempo', color=self.text_color)
        ax.set_ylabel('Densidade Específica', color=self.text_color)
        ax.set_title(titulo, color=self.text_color, fontsize=14, pad=20)
        ax.grid(True, color=self.grid_color, alpha=0.3)
        ax.legend()
        
        # Formatar eixo X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        return fig
    
    def criar_grafico_historico_abv(self, producoes: List[dict],
                                   titulo: str = "Histórico de ABV") -> plt.Figure:
        """
        Cria gráfico do histórico de ABV das produções
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.bg_color)
        ax.set_facecolor(self.bg_color)
        
        if producoes:
            nomes = [p['nome'][:15] + '...' if len(p['nome']) > 15 else p['nome'] for p in producoes]
            abvs = [p.get('abv', 0) for p in producoes]
            tipos = [p.get('tipo', 'Outro') for p in producoes]
            
            # Cores por tipo de bebida
            cores_tipo = {
                'cerveja': '#ffd43b',
                'hidromel': '#fab005',
                'vinho': '#7c2d12',
                'outro': '#868e96'
            }
            
            cores = [cores_tipo.get(tipo.lower(), cores_tipo['outro']) for tipo in tipos]
            
            barras = ax.bar(range(len(nomes)), abvs, color=cores, alpha=0.8)
            
            # Adicionar valores nas barras
            for barra, abv in zip(barras, abvs):
                height = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2., height + 0.1,
                       f'{abv:.1f}%', ha='center', va='bottom', color=self.text_color)
            
            ax.set_xlabel('Produções', color=self.text_color)
            ax.set_ylabel('ABV (%)', color=self.text_color)
            ax.set_title(titulo, color=self.text_color, fontsize=14, pad=20)
            ax.set_xticks(range(len(nomes)))
            ax.set_xticklabels(nomes, rotation=45, ha='right')
            ax.grid(True, axis='y', color=self.grid_color, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def criar_dashboard_resumo(self, dados: dict) -> plt.Figure:
        """
        Cria um dashboard com múltiplos gráficos resumindo dados da produção
        """
        fig = plt.figure(figsize=(15, 10))
        fig.patch.set_facecolor(self.bg_color)
        
        # Gráfico 1: Temperatura (canto superior esquerdo)
        ax1 = plt.subplot(2, 2, 1)
        if dados.get('temperaturas'):
            tempos, temps = zip(*dados['temperaturas'])
            ax1.plot(tempos, temps, 'o-', color='#00ff88', linewidth=2)
        ax1.set_title('Temperatura Atual', color=self.text_color)
        ax1.set_facecolor(self.bg_color)
        
        # Gráfico 2: Progresso (canto superior direito)
        ax2 = plt.subplot(2, 2, 2)
        progresso = dados.get('progresso', 0)
        wedges, texts = ax2.pie([progresso, 100-progresso], 
                               colors=['#00ff88', '#404040'],
                               startangle=90)
        ax2.set_title(f'Progresso: {progresso:.1f}%', color=self.text_color)
        
        # Gráfico 3: Densidade (canto inferior esquerdo)
        ax3 = plt.subplot(2, 2, 3)
        if dados.get('densidades'):
            tempos, densidades = zip(*dados['densidades'])
            ax3.plot(tempos, densidades, 'o-', color='#4dabf7', linewidth=2)
        ax3.set_title('Evolução da Densidade', color=self.text_color)
        ax3.set_facecolor(self.bg_color)
        
        # Gráfico 4: Estatísticas (canto inferior direito)
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        ax4.set_facecolor(self.bg_color)
        
        stats_text = f"""
        ABV Estimado: {dados.get('abv', 0):.1f}%
        Atenuação: {dados.get('atenuacao', 0):.1f}%
        Tempo Decorrido: {dados.get('tempo_decorrido', 'N/A')}
        Status: {dados.get('status', 'N/A')}
        """
        
        ax4.text(0.1, 0.5, stats_text, transform=ax4.transAxes, 
                color=self.text_color, fontsize=12, verticalalignment='center')
        
        plt.tight_layout()
        return fig
    
    def embed_in_tkinter(self, figure: plt.Figure, parent: tk.Widget) -> FigureCanvasTk:
        """
        Embute um gráfico matplotlib em um widget Tkinter
        """
        canvas = FigureCanvasTk(figure, parent)
        canvas.draw()
        return canvas
