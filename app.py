import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from faker import Faker
import time
from streamlit_option_menu import option_menu
import random

st.set_page_config(
    page_title="Aurum - Dashboard Starter",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

fake = Faker('pt_BR')

# Inicializar estado da sessão
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'theme' not in st.session_state:
    st.session_state.theme = 'pastel'
if 'hide_tutorial' not in st.session_state:
    st.session_state.hide_tutorial = False

def get_theme_colors():
    themes = {
        'pastel': {
            'primary': '#87CEEB',
            'secondary': '#98FB98', 
            'accent': '#F0A3C9',
            'background': '#F8F8FF',
            'text': '#4A4A4A',
            'gradients': ['#87CEEB', '#98FB98', '#DDA0DD', '#F0E68C', '#FFB6C1']
        },
        'neon': {
            'primary': '#00FFFF',
            'secondary': '#FF1493',
            'accent': '#FFD700',
            'background': '#1A1A1A',
            'text': '#FFFFFF',
            'gradients': ['#00FFFF', '#FF1493', '#00FF00', '#FFD700', '#FF4500']
        },
        'glass': {
            'primary': '#6366F1',
            'secondary': '#8B5CF6',
            'accent': '#EC4899',
            'background': '#F1F5F9',
            'text': '#334155',
            'gradients': ['#6366F1', '#8B5CF6', '#EC4899', '#F59E0B', '#10B981']
        }
    }
    return themes[st.session_state.theme]

def generate_fake_data():
    np.random.seed(42)
    random.seed(42)
    
    # Dados de vendas mensais
    months = pd.date_range(start='2023-01-01', end='2024-12-31', freq='ME')
    vendas_mensais = []
    base_value = 1000000
    
    for i, month in enumerate(months):
        trend = base_value + (i * 50000)
        seasonal = np.sin(i * np.pi / 6) * 200000
        noise = np.random.normal(0, 100000)
        value = max(trend + seasonal + noise, 500000)
        vendas_mensais.append({
            'data': month,
            'vendas': value,
            'meta': trend * 1.1
        })
    
    df_vendas = pd.DataFrame(vendas_mensais)
    
    # Top produtos
    produtos = ['Aurum Premium', 'Aurum Standard', 'Aurum Starter', 'Aurum Enterprise', 'Aurum Pro']
    vendas_produtos = [np.random.randint(500000, 2000000) for _ in produtos]
    
    # Top vendedores
    vendedores = []
    for i in range(10):
        vendedores.append({
            'nome': fake.name(),
            'vendas': np.random.randint(100000, 500000),
            'meta': np.random.randint(120000, 600000),
            'regiao': random.choice(['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Paraná', 'Rio Grande do Sul'])
        })
    
    # Últimas transações
    transacoes = []
    for i in range(50):
        transacoes.append({
            'data': fake.date_between(start_date='-30d', end_date='today'),
            'cliente': fake.company(),
            'produto': random.choice(produtos),
            'valor': np.random.randint(10000, 200000),
            'status': random.choice(['Concluída', 'Pendente', 'Processando'])
        })
    
    return df_vendas, produtos, vendas_produtos, vendedores, transacoes

def inject_theme_css():
    colors = get_theme_colors()
    
    if st.session_state.theme == 'neon':
        css = f"""
        <style>
        .main {{
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        }}
        
        /* Sidebar Neon */
        .css-1d391kg {{
            background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 100%);
            border-right: 2px solid {colors['primary']};
            box-shadow: 5px 0 20px rgba(0, 255, 255, 0.3);
        }}
        
        .css-1d391kg .stSelectbox > div > div {{
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(255, 20, 147, 0.1) 100%);
            border: 1px solid {colors['primary']};
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }}
        
        .css-1d391kg .stButton > button {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: bold;
            padding: 12px 24px;
            transition: all 0.3s ease;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.4), 0 4px 15px rgba(0, 0, 0, 0.3);
        }}
        
        .css-1d391kg .stButton > button:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.6), 0 8px 25px rgba(0, 0, 0, 0.4);
            text-shadow: 0 0 20px rgba(255, 255, 255, 1);
        }}
        
        .css-1d391kg .stButton > button:active {{
            transform: translateY(-1px) scale(1.02);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(255, 20, 147, 0.1) 100%);
            border: 2px solid {colors['primary']};
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
            color: {colors['text']};
        }}
        .section-header {{
            color: {colors['primary']};
            text-shadow: 0 0 10px {colors['primary']};
            font-weight: bold;
        }}
        .vendedor-card {{
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.15) 0%, rgba(255, 20, 147, 0.15) 100%);
            border: 1px solid {colors['primary']};
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
            color: {colors['text']};
        }}
        
        /* Botões premium gerais - Neon */
        .stButton > button {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: bold;
            padding: 12px 24px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.4), 0 4px 15px rgba(0, 0, 0, 0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.6s ease;
        }}
        
        .stButton > button:hover:before {{
            left: 100%;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-5px) scale(1.08);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.7), 0 10px 30px rgba(0, 0, 0, 0.5);
            text-shadow: 0 0 20px rgba(255, 255, 255, 1);
        }}
        
        .stButton > button:active {{
            transform: translateY(-2px) scale(1.04);
            transition: all 0.1s ease;
        }}
        
        /* Animações extras premium - Neon */
        @keyframes pulse-neon {{
            0% {{ box-shadow: 0 0 15px rgba(0, 255, 255, 0.4); }}
            50% {{ box-shadow: 0 0 25px rgba(0, 255, 255, 0.8); }}
            100% {{ box-shadow: 0 0 15px rgba(0, 255, 255, 0.4); }}
        }}
        
        .stButton > button[data-testid="primary-button"] {{
            animation: pulse-neon 2s infinite;
        }}
        
        .stSelectbox > div > div > div {{
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(255, 20, 147, 0.1) 100%);
            border: 1px solid {colors['primary']};
            color: {colors['text']};
        }}
        
        /* Estilo menu navegação - Neon */
        .nav-link {{
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.15) 0%, rgba(255, 20, 147, 0.15) 100%) !important;
            border: 2px solid {colors['primary']} !important;
            border-radius: 12px !important;
            color: {colors['text']} !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
            text-shadow: 0 0 8px rgba(255, 255, 255, 0.6) !important;
        }}
        
        .nav-link:hover {{
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.6) !important;
            border-color: {colors['secondary']} !important;
            text-shadow: 0 0 15px rgba(255, 255, 255, 1) !important;
        }}
        
        .nav-link-selected {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%) !important;
            border: 2px solid {colors['accent']} !important;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.8) !important;
            animation: pulse-neon 1.5s infinite !important;
        }}
        </style>
        """
    elif st.session_state.theme == 'glass':
        css = f"""
        <style>
        .main {{
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        }}
        
        /* Sidebar Glass */
        .css-1d391kg {{
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
            backdrop-filter: blur(20px);
            border-right: 2px solid rgba(99, 102, 241, 0.3);
            box-shadow: 5px 0 25px rgba(99, 102, 241, 0.2);
        }}
        
        .css-1d391kg .stSelectbox > div > div {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 15px;
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
        }}
        
        .css-1d391kg .stButton > button {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(99, 102, 241, 0.2) 100%);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 15px;
            color: {colors['primary']};
            font-weight: bold;
            padding: 12px 24px;
            transition: all 0.3s ease;
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
        }}
        
        .css-1d391kg .stButton > button:hover {{
            transform: translateY(-4px) scale(1.06);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.6) 0%, rgba(99, 102, 241, 0.3) 100%);
            box-shadow: 0 12px 35px rgba(99, 102, 241, 0.25);
            border: 1px solid rgba(99, 102, 241, 0.6);
        }}
        
        .css-1d391kg .stButton > button:active {{
            transform: translateY(-2px) scale(1.03);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            border: 2px solid {colors['primary']};
            border-radius: 20px;
            padding: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
            color: #ffffff;
            font-weight: 700;
        }}
        .section-header {{
            color: {colors['primary']};
            font-weight: bold;
        }}
        .vendedor-card {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
            border: 2px solid {colors['secondary']};
            border-radius: 20px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(15px);
            box-shadow: 0 8px 32px rgba(139, 92, 246, 0.15);
            color: #ffffff;
            font-weight: 600;
        }}
        
        /* Botões premium gerais - Glass */
        .stButton > button {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(99, 102, 241, 0.2) 100%);
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 15px;
            color: {colors['primary']};
            font-weight: bold;
            padding: 12px 24px;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: left 0.7s ease;
        }}
        
        .stButton > button:hover:before {{
            left: 100%;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-6px) scale(1.08);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.6) 0%, rgba(99, 102, 241, 0.3) 100%);
            box-shadow: 0 15px 40px rgba(99, 102, 241, 0.3);
            border: 1px solid rgba(99, 102, 241, 0.6);
        }}
        
        .stButton > button:active {{
            transform: translateY(-3px) scale(1.04);
            transition: all 0.1s ease;
        }}
        
        /* Animações extras premium - Glass */
        @keyframes pulse-glass {{
            0% {{ box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15); }}
            50% {{ box-shadow: 0 12px 35px rgba(99, 102, 241, 0.35); }}
            100% {{ box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15); }}
        }}
        
        .stButton > button[data-testid="primary-button"] {{
            animation: pulse-glass 2.5s infinite;
        }}
        
        .stSelectbox > div > div > div {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.4);
            backdrop-filter: blur(10px);
            color: {colors['primary']};
        }}
        
        /* Estilo menu navegação - Glass */
        .nav-link {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(99, 102, 241, 0.15) 100%) !important;
            border: 2px solid rgba(99, 102, 241, 0.4) !important;
            border-radius: 15px !important;
            color: {colors['primary']} !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15) !important;
        }}
        
        .nav-link:hover {{
            transform: translateY(-4px) scale(1.06) !important;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.4) 0%, rgba(99, 102, 241, 0.25) 100%) !important;
            box-shadow: 0 12px 35px rgba(99, 102, 241, 0.3) !important;
            border-color: rgba(99, 102, 241, 0.6) !important;
        }}
        
        .nav-link-selected {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.25) 100%) !important;
            border: 2px solid {colors['accent']} !important;
            box-shadow: 0 15px 40px rgba(99, 102, 241, 0.4) !important;
            animation: pulse-glass 2s infinite !important;
        }}
        </style>
        """
    else:  # pastel
        css = f"""
        <style>
        .main {{
            background: linear-gradient(135deg, {colors['background']} 0%, #F0F8FF 100%);
        }}
        
        /* Títulos sempre visíveis - Pastel */
        .section-header, h3, .stMarkdown h3 {{
            color: {colors['primary']} !important;
            font-weight: bold !important;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8) !important;
        }}
        
        /* AURUM sempre dourado */
        h1, .stMarkdown h1, h2, .stMarkdown h2 {{
            color: #DAA520 !important;
            font-weight: bold !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        }}
        
        /* Força cor dourada para qualquer texto AURUM */
        *:contains("AURUM"), [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2 {{
            color: #DAA520 !important;
        }}
        
        /* Sidebar Pastel */
        .css-1d391kg {{
            background: linear-gradient(180deg, rgba(248, 248, 255, 0.9) 0%, rgba(240, 248, 255, 0.85) 100%);
            border-right: 3px solid {colors['primary']};
            box-shadow: 5px 0 20px rgba(135, 206, 235, 0.3);
            backdrop-filter: blur(5px);
        }}
        
        .css-1d391kg h1 {{
            color: #DAA520 !important;
        }}
        
        .css-1d391kg h2 {{
            color: #DAA520 !important;
        }}
        
        .css-1d391kg h3 {{
            color: {colors['primary']} !important;
        }}
        
        .css-1d391kg .stSelectbox label {{
            color: #FFFFFF !important;
            font-weight: bold !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        }}
        
        .css-1d391kg .stSelectbox > div > div {{
            background: linear-gradient(135deg, rgba(135, 206, 235, 0.15) 0%, rgba(152, 251, 152, 0.15) 100%);
            border: 2px solid {colors['primary']};
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(135, 206, 235, 0.2);
        }}
        
        .css-1d391kg .stButton > button {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: bold;
            padding: 12px 24px;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(135, 206, 235, 0.4);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        .css-1d391kg .stButton > button:hover {{
            transform: translateY(-4px) scale(1.05);
            box-shadow: 0 10px 30px rgba(135, 206, 235, 0.6);
            background: linear-gradient(135deg, {colors['accent']} 0%, {colors['primary']} 100%);
        }}
        
        .css-1d391kg .stButton > button:active {{
            transform: translateY(-2px) scale(1.02);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, rgba(135, 206, 235, 0.15) 0%, rgba(152, 251, 152, 0.15) 100%);
            border: 2px solid {colors['primary']};
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(135, 206, 235, 0.3);
            color: #ffffff;
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        .section-header {{
            color: {colors['primary']};
            font-weight: bold;
        }}
        .vendedor-card {{
            background: linear-gradient(135deg, rgba(135, 206, 235, 0.12) 0%, rgba(152, 251, 152, 0.12) 100%);
            border: 2px solid {colors['accent']};
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(152, 251, 152, 0.25);
            color: #ffffff;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        /* Botões premium gerais - Pastel */
        .stButton > button {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: bold;
            padding: 12px 24px;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            box-shadow: 0 6px 20px rgba(135, 206, 235, 0.4);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: left 0.5s ease;
        }}
        
        .stButton > button:hover:before {{
            left: 100%;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-6px) scale(1.1);
            box-shadow: 0 12px 35px rgba(135, 206, 235, 0.6);
            background: linear-gradient(135deg, {colors['accent']} 0%, {colors['primary']} 100%);
        }}
        
        .stButton > button:active {{
            transform: translateY(-3px) scale(1.05);
            transition: all 0.1s ease;
        }}
        
        /* Animações extras premium - Pastel */
        @keyframes pulse-pastel {{
            0% {{ box-shadow: 0 6px 20px rgba(135, 206, 235, 0.4); }}
            50% {{ box-shadow: 0 10px 30px rgba(135, 206, 235, 0.7); }}
            100% {{ box-shadow: 0 6px 20px rgba(135, 206, 235, 0.4); }}
        }}
        
        .stButton > button[data-testid="primary-button"] {{
            animation: pulse-pastel 2s infinite;
        }}
        
        .stSelectbox > div > div > div {{
            background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, rgba(152, 251, 152, 0.1) 100%);
            border: 2px solid {colors['primary']};
            color: {colors['text']};
        }}
        
        .stMultiSelect > div > div > div {{
            background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, rgba(152, 251, 152, 0.1) 100%);
            border: 1px solid {colors['secondary']};
            border-radius: 8px;
        }}
        
        /* Filtros com texto branco - Pastel */
        .stSelectbox label, .stMultiSelect label {{
            color: #FFFFFF !important;
            font-weight: bold !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        }}
        
        .stSelectbox > div > div > div, .stMultiSelect > div > div {{
            color: #FFFFFF !important;
            font-weight: bold !important;
        }}
        
        /* Estilo menu navegação - Pastel */
        .nav-link {{
            background: linear-gradient(135deg, rgba(135, 206, 235, 0.2) 0%, rgba(152, 251, 152, 0.15) 100%) !important;
            border: 3px solid {colors['primary']} !important;
            border-radius: 12px !important;
            color: {colors['primary']} !important;
            font-weight: bold !important;
            transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
            box-shadow: 0 6px 20px rgba(135, 206, 235, 0.3) !important;
        }}
        
        .nav-link:hover {{
            transform: translateY(-5px) scale(1.08) !important;
            background: linear-gradient(135deg, {colors['accent']} 0%, {colors['secondary']} 100%) !important;
            box-shadow: 0 10px 30px rgba(135, 206, 235, 0.5) !important;
            border-color: {colors['accent']} !important;
            color: white !important;
        }}
        
        .nav-link-selected {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%) !important;
            border: 3px solid {colors['accent']} !important;
            color: white !important;
            box-shadow: 0 8px 25px rgba(135, 206, 235, 0.6) !important;
            animation: pulse-pastel 1.8s infinite !important;
        }}
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

def show_login():
    # CSS premium para tela de login
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #18181b 0%, #1f1f23 100%);
    }
    
    .login-container {
        max-width: 450px;
        margin: 2rem auto;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
        border-radius: 25px;
        backdrop-filter: blur(20px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .login-title {
        text-align: center;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(251, 191, 36, 0.5)); }
        to { filter: drop-shadow(0 0 20px rgba(251, 191, 36, 0.8)); }
    }
    
    .login-subtitle {
        text-align: center;
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    
    .version-info {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Tutorial de modo escuro no login
    st.error("""
    💡 **DICA IMPORTANTE:** Para a melhor experiência visual, ative o modo escuro do seu navegador:
    
    🌙 **Chrome/Edge:** Clique nas **3 bolinhas (⋮)** → **Configurações** → **Aparência** → **Tema Escuro**
    🦊 **Firefox:** Clique nas **3 linhas (≡)** → **Configurações** → **Geral** → **Tema Escuro**
    🧭 **Safari:** Menu **Safari** → **Preferências** → **Aparência** → **Escuro**
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Container principal com glassmorphism
        st.markdown("""
        <div class="login-container">
            <h1 class="login-title">🏆 AURUM</h1>
            <p class="login-subtitle">Dashboard Starter</p>
        </div>
        """, unsafe_allow_html=True)
        
        
        # Informações da versão
        st.markdown("""
        <div class="version-info">
            🚀 Versão Starter | v1.0.0
        </div>
        """, unsafe_allow_html=True)
        
        # Aviso sobre dados fictícios
        st.warning("""
        **⚠️ IMPORTANTE:** Este é um dashboard de demonstração. Todos os dados apresentados são **FICTÍCIOS** e gerados automaticamente para fins de apresentação.
        """)
        
        # Credenciais visíveis
        st.info("""
        **🔑 Credenciais de Acesso Demo:**
        
        👤 **Usuário:** `aurum`
        🔐 **Senha:** `aurum`
        
        *Basta clicar em "ENTRAR" - os campos já estão preenchidos*
        """)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário", placeholder="Digite: aurum", value="aurum")
            password = st.text_input("🔐 Senha", type="password", placeholder="Digite: aurum", value="aurum")
            
            submitted = st.form_submit_button("🚀 ENTRAR NO DASHBOARD", use_container_width=True, type="primary")
            
            if submitted:
                if username == "aurum" and password == "aurum":
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.success("✨ Login realizado com sucesso! Redirecionando...")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas! Use: **aurum** / **aurum**")
        
        # Call to action no final
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: white; padding: 20px;">
            <h3>🚀</h3>
            <p>Starter <strong>AURUM</strong></p>
        </div>
        """, unsafe_allow_html=True)

def create_kpi_card(title, value, delta, delta_label, icon):
    colors = get_theme_colors()
    
    # Cor do título específica para temas pastel e glass
    if st.session_state.theme in ['pastel', 'glass']:
        title_color = "#FFFFFF"
        title_shadow = "2px 2px 4px rgba(0,0,0,0.8)"
    else:
        title_color = colors['text']
        title_shadow = "1px 1px 2px rgba(0,0,0,0.3)"
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; margin-bottom: 10px;">
            <span style="font-size: 1.5rem; margin-right: 10px;">{icon}</span>
            <span style="font-size: 0.9rem; color: {title_color}; font-weight: bold; text-shadow: {title_shadow};">{title}</span>
        </div>
        <div style="font-size: 2rem; font-weight: bold; margin: 10px 0; color: #FFFFFF; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{value}</div>
        <div style="color: {'#00FF00' if delta >= 0 else '#FF4500'}; font-size: 0.9rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            {'📈' if delta >= 0 else '📉'} {delta:+.1f}% {delta_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_vendedor_card(vendedor):
    colors = get_theme_colors()
    initial = vendedor['nome'].split()[0][0]
    performance_color = "#00FF00" if vendedor['performance'] >= 100 else "#FFD700" if vendedor['performance'] >= 80 else "#FF6B6B"
    
    # Ajustar cor do texto baseado no tema
    if st.session_state.theme == 'neon':
        text_color = colors['text']  # Branco para tema escuro
    elif st.session_state.theme == 'glass':
        text_color = '#ffffff'  # Branco para contraste no fundo escuro
    else:  # pastel
        text_color = '#ffffff'  # Branco com sombra para contraste
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div class="vendedor-card">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center; 
                            color: white; font-size: 24px; font-weight: bold; margin-right: 20px;">
                    {initial}
                </div>
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: {text_color}; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{vendedor['nome']}</h4>
                    <p style="margin: 5px 0; opacity: 0.8; color: {text_color}; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">📍 {vendedor['regiao']}</p>
                </div>
                <div style="text-align: right;">
                    <div style="color: {performance_color}; font-size: 20px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                        {vendedor['performance']:.1f}%
                    </div>
                    <div style="opacity: 0.8; font-size: 12px; color: {text_color}; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Performance</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas em colunas separadas do Streamlit
        col_vendas, col_meta, col_diff = st.columns(3)
        
        with col_vendas:
            st.metric("💰 Vendas", f"R$ {vendedor['vendas']:,.0f}")
        
        with col_meta:
            st.metric("🎯 Meta", f"R$ {vendedor['meta']:,.0f}")
        
        with col_diff:
            diff = vendedor['vendas'] - vendedor['meta']
            st.metric("📊 Diferença", f"R$ {abs(diff):,.0f}", 
                     delta=f"{'Acima' if diff > 0 else 'Abaixo'} da meta")
        
        # Progress bar
        progress_pct = min(vendedor['performance'] / 100, 1.0)
        st.progress(progress_pct)
        
        st.markdown("<br>", unsafe_allow_html=True)

def create_chart(chart_type, data, title):
    colors = get_theme_colors()
    
    if chart_type == 'line':
        fig = px.line(data, x='data', y='vendas', title=title)
        fig.add_scatter(x=data['data'], y=data['meta'], mode='lines', name='Meta', line=dict(dash='dash'))
        fig.update_traces(line=dict(color=colors['primary'], width=3))
        
    elif chart_type == 'bar':
        produtos = ['Aurum Premium', 'Aurum Standard', 'Aurum Starter', 'Aurum Enterprise', 'Aurum Pro']
        valores = [np.random.randint(500000, 2000000) for _ in produtos]
        
        fig = go.Figure(data=[
            go.Bar(x=produtos, y=valores, 
                  marker=dict(color=colors['gradients'][:len(produtos)]))
        ])
        fig.update_layout(title=title)
        
    elif chart_type == 'pie':
        regioes = ['São Paulo', 'Rio de Janeiro', 'Minas Gerais', 'Paraná', 'Outros']
        valores = [30, 25, 20, 15, 10]
        
        fig = px.pie(values=valores, names=regioes, title=title, 
                     color_discrete_sequence=colors['gradients'])
        
    elif chart_type == 'gauge':
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = 87,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            delta = {'reference': 100},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': colors['primary']},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': colors['secondary']},
                    {'range': [80, 100], 'color': colors['accent']}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=colors['text'])
    )
    
    return fig

def show_mandatory_dark_mode_guide():
    """Mostra guia obrigatório de modo escuro com botão para ocultar"""
    if not st.session_state.hide_tutorial:
        st.error("""
        🌟 **EXPERIÊNCIA STARTER COMPLETA** 🌟
        
        **Para aproveitar 100% dos efeitos visuais, ative o MODO ESCURO do seu navegador:**
        
        🌙 **Chrome/Edge:** Clique nas **3 bolinhas (⋮)** no canto superior direito → **Configurações** → **Aparência** → **Tema Escuro**
        
        🦊 **Firefox:** Clique nas **3 linhas (≡)** no canto superior direito → **Configurações** → **Geral** → **Tema Escuro**
        
        🧭 **Safari:** Menu **Safari** → **Preferências** → **Aparência** → **Escuro**
        
        ✨ **Os temas NEON LED e GLASS ficam ESPETACULARES no modo escuro!** ✨
        """)
        
        st.warning("""
        💡 **DICA STARTER:** Após ativar o modo escuro, teste os 3 temas no sidebar e veja a diferença impressionante nos efeitos visuais!
        """)
        
        # Botão para ocultar o tutorial
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("✅ Entendi, não mostrar mais", type="primary", use_container_width=True):
                st.session_state.hide_tutorial = True
                st.success("✨ Tutorial ocultado! Você pode reativá-lo no sidebar.")
                st.rerun()

def create_premium_sidebar():
    """Cria um sidebar premium e estiloso com controles principais"""
    colors = get_theme_colors()
    
    with st.sidebar:
        # Logo e título no sidebar
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0; margin-bottom: 30px;">
            <h1 style="color: #DAA520; font-size: 2.5rem; margin: 0;">🏆</h1>
            <h2 style="color: #DAA520 !important; font-size: 1.5rem; margin: 5px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">AURUM</h2>
            <p style="color: {colors['text']}; opacity: 0.8; margin: 0;">Dashboard Starter</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Seletor de tema premium
        st.markdown(f"<h3 style='color: {colors['primary']}; margin-bottom: 15px;'>🎨 Personalização</h3>", unsafe_allow_html=True)
        
        theme_names = {'pastel': '🎨 Pastel Sofisticado', 'neon': '💡 Neon LED Vibrante', 'glass': '🔮 Glass Futurista'}
        selected_theme = st.selectbox(
            "Selecione o tema:", 
            options=['pastel', 'neon', 'glass'],
            format_func=lambda x: theme_names[x],
            key="theme_selector"
        )
        if selected_theme != st.session_state.theme:
            st.session_state.theme = selected_theme
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Informações do usuário
        st.markdown(f"<h3 style='color: {colors['primary']}; margin-bottom: 15px;'>👤 Usuário</h3>", unsafe_allow_html=True)
        st.markdown(f"**Bem-vindo:** {st.session_state.user}")
        st.markdown(f"**Sessão ativa desde:** {datetime.now().strftime('%H:%M')}")
        st.markdown(f"**Última sync:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Status do sistema
        st.markdown(f"<h3 style='color: {colors['primary']}; margin-bottom: 15px;'>⚡ Status Sistema</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🚀 Performance", "98%", "2%")
        with col2:
            st.metric("📡 Conexão", "Ativo", "0ms")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Actions premium
        st.markdown(f"<h3 style='color: {colors['primary']}; margin-bottom: 15px;'>⚡ Ações Rápidas</h3>", unsafe_allow_html=True)
        
        if st.button("📊 Atualizar Dados", use_container_width=True):
            st.success("✨ Dados atualizados!")
            time.sleep(0.5)
            st.rerun()
        
        if st.button("📁 Exportar Relatório", use_container_width=True):
            st.info("📤 Preparando relatório...")
            
        if st.button("📧 Enviar por Email", use_container_width=True):
            st.info("📬 Enviando relatório...")
        
        # Botão para reativar tutorial se estiver oculto
        if st.session_state.hide_tutorial:
            if st.button("💡 Mostrar Tutorial Modo Escuro", use_container_width=True):
                st.session_state.hide_tutorial = False
                st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Logout button premium
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.rerun()
        
        # Footer do sidebar
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; opacity: 0.7; font-size: 0.8rem;">
            <p style="color: {colors['text']};">🚀 Aurum Starter</p>
            <p style="color: {colors['text']};">v1.0.0 | 2024</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    if not st.session_state.logged_in:
        show_login()
        return
    
    inject_theme_css()
    create_premium_sidebar()
    
    # Header principal (mais clean agora)
    colors = get_theme_colors()
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0; margin-bottom: 30px;">
        <h1 style="color: #DAA520 !important; font-size: 3rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🏆 AURUM</h1>
        <h2 style="color: {colors['primary']}; margin: 10px 0;">Dashboard Starter</h2>
        <p style="color: {colors['text']}; opacity: 0.8;">Bem-vindo, {st.session_state.user}! | Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tutorial obrigatório de modo escuro
    show_mandatory_dark_mode_guide()
    
    st.markdown("---")
    
    # Gerar dados
    df_vendas, produtos, vendas_produtos, vendedores, transacoes = generate_fake_data()
    
    # Navegação
    menu = option_menu(
        menu_title=None,
        options=["📊 Overview", "💰 Vendas", "👥 Clientes", "⚙️ Operacional"],
        icons=["graph-up", "currency-dollar", "people", "gear"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px"},
        }
    )
    
    if menu == "📊 Overview":
        st.markdown("<h2 class='section-header'>📊 Visão Geral Executiva</h2>", unsafe_allow_html=True)
        
        # KPIs
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            create_kpi_card("Receita Total", "R$ 12,5M", 8.5, "vs mês anterior", "💰")
        
        with col2:
            create_kpi_card("Vendas do Mês", "1.847", 12.3, "vs meta", "📈")
        
        with col3:
            create_kpi_card("Clientes Ativos", "15.234", -2.1, "vs mês anterior", "👥")
        
        with col4:
            create_kpi_card("Ticket Médio", "R$ 6.789", 15.7, "vs mês anterior", "🎯")
        
        with col5:
            create_kpi_card("Taxa Conversão", "14.8%", 3.2, "vs mês anterior", "⚡")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        
        with col1:
            fig_line = create_chart('line', df_vendas.tail(12), '📈 Evolução de Vendas Aurum (12 meses)')
            st.plotly_chart(fig_line, use_container_width=True)
            
            fig_gauge = create_chart('gauge', None, '🎯 Meta vs Realizado')
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            fig_bar = create_chart('bar', None, '🏆 Top 5 Produtos Aurum')
            st.plotly_chart(fig_bar, use_container_width=True)
            
            fig_pie = create_chart('pie', None, '🗺️ Distribuição por Região')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    elif menu == "💰 Vendas":
        st.markdown("<h2 class='section-header'>💰 Análise de Vendas Detalhada</h2>", unsafe_allow_html=True)
        
        # KPIs específicos de vendas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_kpi_card("Meta Mensal", "R$ 8.2M", 15.3, "vs mês anterior", "🎯")
        
        with col2:
            create_kpi_card("Realizado", "R$ 9.1M", 22.8, "acima da meta", "🚀")
        
        with col3:
            create_kpi_card("Pipeline", "R$ 15.6M", 8.9, "oportunidades", "⏳")
        
        with col4:
            create_kpi_card("Conversão", "18.5%", 5.2, "vs trimestre", "⚡")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos de vendas
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de performance por produto
            fig_produtos = create_chart('bar', None, '📊 Performance por Produto')
            st.plotly_chart(fig_produtos, use_container_width=True)
        
        with col2:
            # Gráfico de evolução de vendas
            fig_evolucao = create_chart('line', df_vendas.tail(6), '📈 Evolução Vendas (6 meses)')
            st.plotly_chart(fig_evolucao, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filtros para o Hall da Fama
        st.markdown(f"<h3 class='section-header'>🔍 Filtros Hall da Fama</h3>", unsafe_allow_html=True)
        
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            periodo = st.selectbox(
                "📅 Período:",
                ["Hoje", "Esta Semana", "Este Mês", "Últimos 3 Meses", "Este Ano"],
                index=2
            )
        
        with col_filtro2:
            regiao = st.multiselect(
                "🌍 Região:",
                ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Paraná", "Todos"],
                default=["Todos"]
            )
            
        with col_filtro3:
            produto_filtro = st.selectbox(
                "📦 Produto:",
                ["Todos", "Aurum Premium", "Aurum Standard", "Aurum Starter", "Aurum Enterprise", "Aurum Pro"],
                index=0
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Top Vendedores com cards visuais impressionantes
        st.markdown("<h3 class='section-header'>🏆 Hall da Fama - Top Vendedores</h3>", unsafe_allow_html=True)
        
        df_vendedores = pd.DataFrame(vendedores)
        df_vendedores['performance'] = (df_vendedores['vendas'] / df_vendedores['meta'] * 100).round(1)
        top_vendedores = df_vendedores.nlargest(5, 'vendas')
        
        for idx, vendedor in top_vendedores.iterrows():
            create_vendedor_card(vendedor)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Últimas Transações com cards visuais
        st.markdown("<h3 class='section-header'>💳 Últimas Transações VIP</h3>", unsafe_allow_html=True)
        
        df_transacoes = pd.DataFrame(transacoes).head(6)
        
        col1, col2, col3 = st.columns(3)
        
        for idx, (i, transacao) in enumerate(df_transacoes.iterrows()):
            col = [col1, col2, col3][idx % 3]
            
            status_icon = {"Concluída": "✅", "Pendente": "⏳", "Processando": "🔄"}
            status_color = {"Concluída": "#00FF00", "Pendente": "#FFD700", "Processando": "#00BFFF"}
            
            with col:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); border-radius: 15px; padding: 15px; margin-bottom: 15px; 
                            border: 1px solid {get_theme_colors()['primary']};">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 10px;">
                        <div style="color: {status_color[transacao['status']]}; font-size: 20px;">
                            {status_icon[transacao['status']]}
                        </div>
                        <div style="color: {status_color[transacao['status']]}; font-size: 12px; font-weight: bold;">
                            {transacao['status']}
                        </div>
                    </div>
                    <div style="font-weight: bold; margin-bottom: 8px; color: {get_theme_colors()['text']};">
                        {transacao['cliente'][:25]}{'...' if len(transacao['cliente']) > 25 else ''}
                    </div>
                    <div style="color: {get_theme_colors()['accent']}; font-size: 14px; margin-bottom: 8px;">
                        📦 {transacao['produto']}
                    </div>
                    <div style="font-size: 18px; font-weight: bold; color: #00FF00;">
                        💰 R$ {transacao['valor']:,.0f}
                    </div>
                    <div style="font-size: 12px; opacity: 0.8; margin-top: 8px; color: {get_theme_colors()['text']};">
                        📅 {transacao['data'].strftime('%d/%m/%Y')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif menu == "👥 Clientes":
        st.markdown("<h2 class='section-header'>👥 Análise de Clientes & Marketing</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            create_kpi_card("Novos Clientes", "1.234", 18.5, "este mês", "👤")
        
        with col2:
            create_kpi_card("Taxa Retenção", "89.5%", 2.1, "vs mês anterior", "🔄")
        
        with col3:
            create_kpi_card("LTV Médio", "R$ 45.6K", 12.8, "vs trimestre", "💎")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Simulação de funil de vendas
        st.subheader("🎯 Funil de Conversão Aurum")
        
        funil_data = {
            'Etapa': ['Visitantes', 'Leads', 'Oportunidades', 'Propostas', 'Fechamentos'],
            'Quantidade': [10000, 3500, 1200, 450, 180],
            'Taxa Conversão': [100, 35, 34.3, 37.5, 40]
        }
        
        df_funil = pd.DataFrame(funil_data)
        
        colors = get_theme_colors()
        fig_funil = px.funnel(df_funil, x='Quantidade', y='Etapa', 
                             title="Funil de Vendas Aurum",
                             color_discrete_sequence=[colors['primary']])
        st.plotly_chart(fig_funil, use_container_width=True)
    
    elif menu == "⚙️ Operacional":
        st.markdown("<h2 class='section-header'>⚙️ Indicadores Operacionais</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_kpi_card("Produtividade", "127%", 8.2, "vs meta", "⚡")
        
        with col2:
            create_kpi_card("Eficiência", "94.2%", 5.1, "vs mês anterior", "🎯")
        
        with col3:
            create_kpi_card("Margem", "34.8%", -1.2, "vs trimestre", "📊")
        
        with col4:
            create_kpi_card("Custos", "R$ 2.1M", -3.5, "vs orçado", "💸")
        
        # Mapa interativo de infraestrutura operacional
        st.subheader("🏢 Mapa de Infraestrutura Operacional")
        
        # Dados simulados de infraestrutura operacional
        infraestrutura = {
            'Local': ['Centro SP', 'Filial RJ', 'CD Campinas', 'Escritório BH', 'Hub Curitiba', 
                     'Base Floripa', 'Centro GO', 'Filial Salvador', 'Hub Recife', 'Base Fortaleza'],
            'Tipo': ['Sede', 'Filial', 'Centro de Distribuição', 'Escritório', 'Hub Logístico',
                    'Base Operacional', 'Centro Regional', 'Filial', 'Hub Logístico', 'Base Operacional'],
            'Status': ['Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Manutenção', 'Ativo', 'Ativo'],
            'Funcionarios': [350, 180, 45, 85, 120, 65, 95, 140, 110, 75],
            'Cobertura_KM': [500, 400, 300, 350, 450, 280, 380, 420, 390, 320],
            'Lat': [-23.5505, -22.9068, -22.9056, -19.9167, -25.2521, -27.2423, -16.6864, -12.9714, -8.0476, -3.7319],
            'Lon': [-46.6333, -43.1729, -47.0608, -43.9345, -49.2908, -48.2619, -49.2643, -38.5014, -34.8770, -38.5267]
        }
        
        df_infra = pd.DataFrame(infraestrutura)
        
        # Criar mapa com diferentes símbolos por tipo
        fig_mapa = go.Figure()
        
        # Definir cores e símbolos por tipo
        tipo_config = {
            'Sede': {'color': '#DAA520', 'symbol': 'star', 'size': 20},
            'Filial': {'color': '#00BFFF', 'symbol': 'circle', 'size': 15},
            'Centro de Distribuição': {'color': '#FF6347', 'symbol': 'square', 'size': 18},
            'Escritório': {'color': '#32CD32', 'symbol': 'triangle-up', 'size': 12},
            'Hub Logístico': {'color': '#FF1493', 'symbol': 'diamond', 'size': 16},
            'Base Operacional': {'color': '#9370DB', 'symbol': 'cross', 'size': 14},
            'Centro Regional': {'color': '#FF8C00', 'symbol': 'hexagon', 'size': 15}
        }
        
        for tipo in df_infra['Tipo'].unique():
            df_tipo = df_infra[df_infra['Tipo'] == tipo]
            config = tipo_config[tipo]
            
            fig_mapa.add_trace(go.Scattergeo(
                lon=df_tipo['Lon'],
                lat=df_tipo['Lat'],
                text=df_tipo['Local'],
                mode='markers+text',
                name=tipo,
                marker=dict(
                    size=config['size'],
                    color=config['color'],
                    symbol=config['symbol'],
                    line=dict(width=2, color='white')
                ),
                textposition="top center",
                textfont=dict(size=10, color=config['color']),
                hovertemplate=
                '<b>%{text}</b><br>' +
                'Tipo: ' + tipo + '<br>' +
                'Funcionários: %{customdata[0]}<br>' +
                'Cobertura: %{customdata[1]} km<br>' +
                'Status: %{customdata[2]}' +
                '<extra></extra>',
                customdata=df_tipo[['Funcionarios', 'Cobertura_KM', 'Status']].values
            ))
        
        fig_mapa.update_geos(
            projection_type="natural earth",
            showland=True, landcolor='#F0F0F0',
            showocean=True, oceancolor='#E6F3FF',
            showcountries=True, countrycolor='#CCCCCC',
            showlakes=True, lakecolor='#E6F3FF',
            fitbounds="locations",
            bgcolor="rgba(0,0,0,0)"
        )
        
        fig_mapa.update_layout(
            title="📍 Rede de Infraestrutura Aurum",
            geo=dict(
                center=dict(lat=-15.0, lon=-50.0),
                projection_scale=2.5
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=get_theme_colors()['text']),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_mapa, use_container_width=True)
        
        # Tabela resumo da infraestrutura
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<h4 class='section-header'>📊 Status da Rede</h4>", unsafe_allow_html=True)
            status_summary = df_infra['Status'].value_counts()
            fig_status = px.pie(
                values=status_summary.values, 
                names=status_summary.index,
                title="Status das Unidades",
                color_discrete_sequence=get_theme_colors()['gradients']
            )
            fig_status.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=get_theme_colors()['text'])
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            st.markdown(f"<h4 class='section-header'>👥 Funcionários por Unidade</h4>", unsafe_allow_html=True)
            df_funcionarios = df_infra[['Local', 'Funcionarios', 'Tipo']].sort_values('Funcionarios', ascending=False)
            st.dataframe(df_funcionarios, use_container_width=True, hide_index=True)
    
    # Call-to-Actions no final
    st.markdown("---")
    st.markdown("<h3 class='section-header'>🚀 Acelere Seus Resultados com Aurum</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Upgrade para Pro", type="primary", use_container_width=True):
            st.success("✨ Entraremos em contato em breve!")
    
    with col2:
        if st.button("📱 Falar no WhatsApp", use_container_width=True):
            st.info("💬 Redirecionando para WhatsApp...")
    
    with col3:
        if st.button("🔗 Links Úteis", use_container_width=True):
            st.info("📚 Acesse nossa documentação!")

if __name__ == "__main__":
    main()