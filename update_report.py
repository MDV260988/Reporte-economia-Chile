import requests
import json
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
import re

# Zona horaria de Chile
tz_chile = pytz.timezone('America/Santiago')

def obtener_indicadores():
    """Obtiene indicadores del Banco Central via mindicador.cl"""
    try:
        r = requests.get('https://mindicador.cl/api', timeout=10)
        r.raise_for_status()
        data = r.json()
        
        indicadores = {}
        
        # Dólar observado
        if 'dolar' in data:
            indicadores['dolar'] = {
                'valor': f"${data['dolar']['valor']:.0f}",
                'fecha': data['dolar']['fecha'][:10] if data['dolar'].get('fecha') else ''
            }
        
        # UF
        if 'uf' in data:
            indicadores['uf'] = {
                'valor': f"${data['uf']['valor']:.0f}",
                'fecha': data['uf']['fecha'][:10] if data['uf'].get('fecha') else ''
            }
        
        # IPC
        if 'ipc' in data:
            indicadores['ipc'] = {
                'valor': f"{data['ipc']['valor']:.1f}%",
                'fecha': data['ipc']['fecha'][:10] if data['ipc'].get('fecha') else ''
            }
        
        # TPM
        if 'tpm' in data:
            indicadores['tpm'] = {
                'valor': f"{data['tpm']['valor']:.2f}%",
                'fecha': data['tpm']['fecha'][:10] if data['tpm'].get('fecha') else ''
            }
        
        # Cobre
        if 'libra_cobre' in data:
            indicadores['cobre'] = {
                'valor': f"US${data['libra_cobre']['valor']:.2f}",
                'fecha': data['libra_cobre']['fecha'][:10] if data['libra_cobre'].get('fecha') else ''
            }
        
        return indicadores
    
    except Exception as e:
        print(f"Error obteniendo indicadores: {e}")
        return None

def cargar_datos_manuales():
    """Carga datos que se actualizan manualmente (desempleo, Imacec, etc)"""
    try:
        with open('datos_manuales.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Si no existe el archivo, retorna valores por defecto
        return {
            'desempleo': {'valor': '9,5%', 'fecha': 'may–jul 2026'},
            'imacec': {'valor': '-1,5%', 'fecha': 'julio 2026'},
            'crecimiento_proyectado': {'valor': '0,25% a 0,75%', 'fecha': 'proyección 9 sept 2026'}
        }

def actualizar_html(indicadores_auto, datos_manuales):
    """Lee el HTML, actualiza los valores y lo guarda"""
    
    with open('economia-chile-en-simple.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Reemplaza dólar
    if indicadores_auto and 'dolar' in indicadores_auto:
        html = re.sub(
            r'<span class="num" id="v-dolar">[^<]*</span>',
            f'<span class="num" id="v-dolar">{indicadores_auto["dolar"]["valor"]}</span>',
            html
        )
        html = re.sub(
            r'<span class="fch" id="f-dolar">[^<]*</span>',
            f'<span class="fch" id="f-dolar">{indicadores_auto["dolar"]["fecha"]}</span>',
            html
        )
    
    # Reemplaza UF
    if indicadores_auto and 'uf' in indicadores_auto:
        html = re.sub(
            r'<span class="num" id="v-uf">[^<]*</span>',
            f'<span class="num" id="v-uf">{indicadores_auto["uf"]["valor"]}</span>',
            html
        )
        html = re.sub(
            r'<span class="fch" id="f-uf">[^<]*</span>',
            f'<span class="fch" id="f-uf">{indicadores_auto["uf"]["fecha"]}</span>',
            html
        )
    
    # Reemplaza IPC
    if indicadores_auto and 'ipc' in indicadores_auto:
        html = re.sub(
            r'<span class="num" id="v-ipc">[^<]*</span>',
            f'<span class="num" id="v-ipc">{indicadores_auto["ipc"]["valor"]}</span>',
            html
        )
        html = re.sub(
            r'<span class="fch" id="f-ipc">[^<]*</span>',
            f'<span class="fch" id="f-ipc">{indicadores_auto["ipc"]["fecha"]}</span>',
            html
        )
    
    # Reemplaza TPM
    if indicadores_auto and 'tpm' in indicadores_auto:
        html = re.sub(
            r'<span class="num" id="v-tpm">[^<]*</span>',
            f'<span class="num" id="v-tpm">{indicadores_auto["tpm"]["valor"]}</span>',
            html
        )
        html = re.sub(
            r'<span class="fch" id="f-tpm">[^<]*</span>',
            f'<span class="fch" id="f-tpm">{indicadores_auto["tpm"]["fecha"]}</span>',
            html
        )
    
    # Reemplaza Desempleo
    if datos_manuales and 'desempleo' in datos_manuales:
        html = re.sub(
            r'<span class="num" id="v-desempleo">[^<]*</span>',
            f'<span class="num" id="v-desempleo">{datos_manuales["desempleo"]["valor"]}</span>',
            html
        )
        html = re.sub(
            r'<span class="fch" id="f-desempleo">[^<]*</span>',
            f'<span class="fch" id="f-desempleo">{datos_manuales["desempleo"]["fecha"]}</span>',
            html
        )
    
    # Reemplaza Cobre
    if indicadores_auto and 'cobre' in indicadores_auto:
        html = re.sub(
            r'<span class="num" id="v-cobre">[^<]*</span>',
            f'<span class="num" id="v-cobre">{indicadores_auto["cobre"]["valor"]}</span>',
            html
        )
        html = re.sub(
            r'<span class="fch" id="f-cobre">[^<]*</span>',
            f'<span class="fch" id="f-cobre">{indicadores_auto["cobre"]["fecha"]}</span>',
            html
        )
    
    with open('economia-chile-en-simple.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ HTML actualizado correctamente")

if __name__ == '__main__':
    print("🔄 Iniciando actualización de indicadores...")
    
    # Obtener indicadores automáticos
    indicadores = obtener_indicadores()
    if indicadores:
        print(f"✅ Indicadores obtenidos: {list(indicadores.keys())}")
    else:
        print("⚠️  No se pudieron obtener indicadores automáticos")
    
    # Cargar datos manuales
    datos_manuales = cargar_datos_manuales()
    print(f"✅ Datos manuales cargados")
    
    # Actualizar HTML
    actualizar_html(indicadores, datos_manuales)
    
    print("✅ Proceso completado")
