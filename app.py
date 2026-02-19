import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO INICIAL DA PÁGINA
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Inicialização das variáveis de estado (Sessão)
if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. IMAGEM DE FUNDO (SETUP TRADER CYBERPUNK ROXO - SEM PESSOAS)
# Uma sala futurista com telas, neons roxos e vista para a cidade, sem humanos.
img_background = "https://img.freepik.com/fotos-premium/quarto-de-jogador-neon-cyberpunk-com-computador-e-telas-fundo-futurista-roxo_172276-373.jpg?w=1380"

# 3. ESTILIZAÇÃO CSS (CYBERPINK THEME)
st.markdown(f"""
<style>
    /* FUNDO GERAL */
    .stApp {{
        background: linear-gradient(rgba(10, 0, 30, 0.85), rgba(10, 0, 30, 0.9)), url("{img_background}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO BLINDADA (NÃO DESFIGURA) */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
        margin-bottom: 10px;
    }}
    .u-text {{ color: #FFFFFF; font-size: 40px; font-family: 'Arial Black', sans-serif; font-weight: 900; letter-spacing: -1px; }}
    .t-text {{ color: #d500f9; font-size: 40px; font-family: 'Arial Black', sans-serif; font-weight: 900; letter-spacing: -1px; text-shadow: 0 0 15px #d500f9; margin-left: 5px; }}
    .p-badge {{ 
        background: #00e676; color: #000; padding: 4px 10px; border-radius: 4px; 
        font-size: 16px; margin-left: 10px; font-family: sans-serif; font-weight: bold;
        box-shadow: 0 0 10px #00e676;
    }}
    
    /* CAIXA DE SALDO (ROXO E NEON) */
    .banca-box {{ 
        background: rgba(20, 0, 40, 0.8); 
        color: #d500f9; 
        padding: 15px 40px; 
        border-radius: 12px; 
        font-size: 28px; 
        font-weight: 800; 
        border: 2px solid #d500f9; 
        text-align: center; 
        font-family: 'Courier New', monospace;
        box-shadow: 0 0 25px rgba(213, 0, 249, 0.3);
        min-width: 300px;
    }}
    
    /* CARD DE SINAL PRINCIPAL */
    .signal-card {{ 
        background: rgba(15, 5, 25, 0.95); 
        border-radius: 20px; 
        padding: 30px; 
        text-align: center; 
        border: 1px solid #d500f9; 
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
        backdrop-filter: blur(5px);
    }}
    
    /* TAGS DE CONFLUÊNCIA */
    .conf-tag {{ 
        background: rgba(213, 0, 249, 0.15); 
        color: #fff; 
        padding: 6px 12px; 
        border-radius: 6px; 
        font-size: 11px; 
        font-weight: bold; 
        display: inline-block; 
        margin: 4px;
        border: 1px solid #d500f9; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* CUSTOMIZAÇÃO DOS INPUTS E BOTÕES */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(10, 0, 20, 0.9) !important;
        color: #d500f9 !important;
        border: 1px solid #d500f9 !important;
        border-radius: 8px !important;
    }}
    
    .stButton>button {{
        background: linear-gradient(90deg, #aa00ff, #d500f9) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 20px #d500f9 !important;
        transform: scale(1.02);
    }}
    
    /* TEXTO BRANCO GERAL */
    label, .stMarkdown, p {{ color: #e0e0e0 !important; }}
</style>
""", unsafe_allow_html=True)

# 4. TELA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    
    c1, col_login, c3 = st.columns([1, 2, 1])
    with col_login:
        st.markdown("<h4 style='text-align:center; color:#d500f9; letter-spacing:2px;'>SYSTEM ACCESS</h4>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD PRINCIPAL
# Topo com Logo
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Saldo Centralizado
st.markdown(f'<div style="display:flex; justify-content:center; margin-bottom:20px;"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# --- PAINEL DE GESTÃO (BANCA / ENTRADA / PAYOUT) ---
col_g1, col_g2, col_g3 = st.columns(3)
st.session_state.banca = col_g1.number_input("BANCA ATUAL:", value=float(st.session_state.banca), step=50.0)
st.session_state.valor_inicial = col_g2.number_input("VALOR ENTRADA:", value=float(st.session_state.valor_inicial), step=5.0)
st.session_state.payout = col_g3.number_input("PAYOUT %:", value=int(st.session_state.payout), step=1)

st.markdown("<hr style='border-color: #d500f9; opacity: 0.3;'>", unsafe_allow_html=True)

# --- SELETORES DE ESTRATÉGIA ---
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME FRAME:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA (MOTOR):", [
    "Sniper Pro (RSI+Médias)", 
    "Turbo V12 (MHI+Fluxo)", 
    "Quantum Max (Bollinger+Stoch)"
])
at = c3.selectbox("ATIVO / PARIDADE:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD", "ETH/USD"])

# 6. MOTOR DE CONFLUÊNCIA TRIPLA (SIMULAÇÃO LÓGICA)
# Gera aleatoriedade baseada no minuto atual para simular análise em tempo real
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

sinal = "AGUARDANDO..."
cor_sinal = "#64748b" # Cinza
tags_confluencia = []
analise_txt = "ESCANEANDO MERCADO..."

# Lógica Individual para cada Estratégia
if "Sniper" in est:
    # Requer: RSI Extremo + Cruzamento de Médias + Volume
    rsi = np.random.randint(0, 100)
    media_cross = np.random.choice([True, False])
    volume = np.random.choice(["ALTO", "BAIXO"])
    
    if rsi < 25 and media_cross and volume == "ALTO":
        sinal = "CALL 🟢"
        cor_sinal = "#00e676"
        tags_confluencia = ["RSI SOBREVENDA (OK)", "CRUZAMENTO EMA (OK)", "VOLUME COMPRADOR (OK)"]
    elif rsi > 75 and media_cross and volume == "ALTO":
        sinal = "PUT 🔴"
        cor_sinal = "#ff1744"
        tags_confluencia = ["RSI SOBRECOMPRA (OK)", "CRUZAMENTO EMA (OK)", "VOLUME VENDEDOR (OK)"]

elif "Turbo" in est:
    # Requer: Padrão Probabilístico + Suporte/Resistência + Fluxo
    padrao = np.random.choice(["MHI-1", "MHI-2", "NENHUM"])
    zona = np.random.choice(["ROMPIMENTO", "RETRAÇÃO", "NEUTRO"])
    fluxo = np.random.choice(["FAVOR", "CONTRA"])
    
    if padrao != "NENHUM" and zona == "RETRAÇÃO" and fluxo == "FAVOR":
        tipo = "CALL 🟢" if np.random.random() > 0.5 else "PUT 🔴"
        sinal = tipo
        cor_sinal = "#00e676" if "CALL" in tipo else "#ff1744"
        tags_confluencia = [f"PADRÃO {padrao} (OK)", "ZONA RETRAÇÃO (OK)", "FLUXO A FAVOR (OK)"]

elif "Quantum" in est:
    # Requer: Bandas de Bollinger + Estocástico + Price Action
    bb = np.random.choice(["TOPO", "FUNDO", "MEIO"])
    stoch = np.random.randint(0, 100)
    candle = np.random.choice(["MARTELO", "ENGOLFO", "DOJI"])
    
    if bb == "FUNDO" and stoch < 20 and candle != "DOJI":
        sinal = "CALL 🟢"
        cor_sinal = "#00e676"
        tags_confluencia = ["BB TOQUE INF (OK)", "STOCH 20% (OK)", "PADRÃO REVERSÃO (OK)"]
    elif bb == "TOPO" and stoch > 80 and candle != "DOJI":
        sinal = "PUT 🔴"
        cor_sinal = "#ff1744"
        tags_confluencia = ["BB TOQUE SUP (OK)", "STOCH 80% (OK)", "PADRÃO REVERSÃO (OK)"]

# Se não bateu as 3 confluências
if not tags_confluencia:
    analise_txt = "BUSCANDO PADRÃO DE ALTA PRECISÃO..."
else:
    analise_txt = "CONFLUÊNCIA TRIPLA CONFIRMADA"

# Timer Regressivo
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# 7. EXIBIÇÃO DO SINAL (CARD)
st.markdown(f"""
<div class="signal-card">
    <div style="color:#d500f9; font-weight:bold; font-size:12px; letter-spacing:2px; margin-bottom:5px;">SISTEMA: {est}</div>
    <div style="color:#ffffff; font-size:14px; opacity:0.8; margin-bottom:15px;">{analise_txt}</div>
    
    <h1 style="color:{cor_sinal}; font-size:75px; margin:10px 0; text-shadow: 0 0 30px {cor_sinal}66;">{sinal}</h1>
    
    <div style="font-size: 50px; font-weight: bold; color: white; font-family: monospace;">00:{int(faltam):02d}</div>
    
    <div style="margin-top:20px;">
        {''.join([f'<span class="conf-tag">{tag}</span>' for tag in tags_confluencia])}
    </div>
</div>
""", unsafe_allow_html=True)

# 8. RODAPÉ (AÇÕES)
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("LOGOUT / SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("LIMPAR PLACAR", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0})
    st.rerun()

# Atualização automática
time.sleep(1)
st.rerun()
