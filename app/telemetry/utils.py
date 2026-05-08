import matplotlib
matplotlib.use('Agg')  # Usa backend non-interattivo
import matplotlib.pyplot as plt
import os
from datetime import datetime

def generate_telemetry_charts(telemetry, upload_folder):
    """Genera i grafici di telemetria con matplotlib."""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    telemetry_folder = os.path.join(upload_folder, 'telemetry')
    os.makedirs(telemetry_folder, exist_ok=True)
    
    charts = {}
    
    # Grafico Velocità
    if telemetry.velocita:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(telemetry.velocita, label='Velocità (km/h)', color='blue', linewidth=2)
        ax.set_xlabel('Tempo')
        ax.set_ylabel('Velocità (km/h)')
        ax.set_title('Telemetria: Velocità')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        filename = f'velocita_{telemetry.id}_{timestamp}.png'
        filepath = os.path.join(telemetry_folder, filename)
        fig.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close(fig)
        charts['velocita'] = f'telemetry/{filename}'
    
    # Grafico RPM
    if telemetry.rpm:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(telemetry.rpm, label='RPM', color='red', linewidth=2)
        ax.set_xlabel('Tempo')
        ax.set_ylabel('RPM')
        ax.set_title('Telemetria: RPM')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        filename = f'rpm_{telemetry.id}_{timestamp}.png'
        filepath = os.path.join(telemetry_folder, filename)
        fig.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close(fig)
        charts['rpm'] = f'telemetry/{filename}'
    
    # Grafico Temperatura Freni
    if telemetry.temperatura_freni:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(telemetry.temperatura_freni, label='Temperatura Freni (°C)', color='orange', linewidth=2)
        ax.set_xlabel('Tempo')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Telemetria: Temperatura Freni')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        filename = f'temp_freni_{telemetry.id}_{timestamp}.png'
        filepath = os.path.join(telemetry_folder, filename)
        fig.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close(fig)
        charts['temperatura_freni'] = f'telemetry/{filename}'
    
    # Grafico Temperatura Gomme
    if telemetry.temperatura_gomme:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(telemetry.temperatura_gomme, label='Temperatura Gomme (°C)', color='green', linewidth=2)
        ax.set_xlabel('Tempo')
        ax.set_ylabel('Temperatura (°C)')
        ax.set_title('Telemetria: Temperatura Gomme')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        filename = f'temp_gomme_{telemetry.id}_{timestamp}.png'
        filepath = os.path.join(telemetry_folder, filename)
        fig.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close(fig)
        charts['temperatura_gomme'] = f'telemetry/{filename}'
    
    # Grafico Multi-Dati
    if telemetry.velocita and telemetry.rpm:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        ax1.plot(telemetry.velocita, color='blue', linewidth=2)
        ax1.set_ylabel('Velocità (km/h)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(telemetry.rpm, color='red', linewidth=2)
        ax2.set_ylabel('RPM', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax2.set_xlabel('Tempo')
        ax2.grid(True, alpha=0.3)
        
        fig.suptitle('Telemetria: Velocità + RPM', fontsize=14, fontweight='bold')
        
        filename = f'combined_{telemetry.id}_{timestamp}.png'
        filepath = os.path.join(telemetry_folder, filename)
        fig.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close(fig)
        charts['combined'] = f'telemetry/{filename}'
    
    return charts


def generate_pedal_charts(telemetry, upload_folder):
    """Genera grafici per gas, freno, sterzo."""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    telemetry_folder = os.path.join(upload_folder, 'telemetry')
    os.makedirs(telemetry_folder, exist_ok=True)
    
    charts = {}
    
    if telemetry.gas and telemetry.freno:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        ax1.fill_between(range(len(telemetry.gas)), telemetry.gas, alpha=0.5, color='green')
        ax1.set_ylabel('Gas (%)')
        ax1.set_title('Telemetria: Posizione Gas')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 100)
        
        ax2.fill_between(range(len(telemetry.freno)), telemetry.freno, alpha=0.5, color='red')
        ax2.set_ylabel('Freno (%)')
        ax2.set_xlabel('Tempo')
        ax2.set_title('Telemetria: Pressione Freno')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 100)
        
        filename = f'pedals_{telemetry.id}_{timestamp}.png'
        filepath = os.path.join(telemetry_folder, filename)
        fig.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close(fig)
        charts['pedals'] = f'telemetry/{filename}'
    
    return charts
