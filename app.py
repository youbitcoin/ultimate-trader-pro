import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'aguardando': False, 'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. IMAGENS DE FUNDO (CYBERPUNK CITY)
img_login = "https://wallpaperaccess.com/full/2653258.jpg" # Cidade Neon
img_dash = "https://images.wallpapersden.com/image/download/cyberpunk-city-street-night-art_bGxtZ2mUmZqaraWkpJRmbmdlrWZnZWU.jpg"

bg_url = img_login if not st.session_state.logado else img_dash

# 3. CSS ESTILO CYBERPUNK (ROXO, AZUL E NEON)
st.markdown(f"""
<style>
    /* FUNDO DINÂMICO */
    .stApp {{
        background: linear-gradient(rgba(10, 0, 30, 0.8), rgba(0, 5, 25, 0.85)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO OFICIAL COM BRILHO NEON */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
        text-shadow: 0 0 10px rgba(191, 90, 242, 0.5);
    }}
    .u-text {{ color: #FFFFFF; font-size: 42px; font-family: 'Arial Black', sans-serif; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 42px; font-family: 'Arial Black', sans-serif; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 5px; }}
    .p-badge {{ 
        background: #bf5af2; color: #fff; padding: 2px 12px; border-radius: 4px; 
        font-size: 20px; margin-left: 10px; font-weight: bold; box-shadow: 0 0 15px #bf5af2;
    }}
    
    /* SALDO COM GRADIENTE CYBER */
    .banca-wrapper {{ display: flex; justify-content: center; margin: 25px 0; }}
    .banca-box {{ 
        background: rgba(15, 0, 30, 0.8); 
        color: #00d2ff; 
        padding: 15px 70px; 
        border-radius: 10px; 
        font-size: 30px; 
        font-weight: bold; 
        border: 2px solid #bf5af2;
        box-shadow: 0 0 25px rgba(191, 90, 242, 0.4), inset 0 0 15px rgba(0, 210, 255, 0.2);
        text-align: center;
    }}
    
    /* CARDS E INPUTS CUSTOMIZADOS */
    .signal-card {{ 
        background: rgba(10, 0, 20, 0.9); 
        border-radius: 20px; 
        padding: 35px; 
        text-align: center; 
        border: 1px solid #00d2ff;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.2);
    }}
    
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(20, 0, 40, 0.9) !important;
        color: #00d2ff !important;
        border: 1px solid #bf5af2 !important;
        border-radius: 8px !important;
    }}

    .timer-text {{ 
        font-size: 55px; 
        font-weight: bold; 
        color: #ffffff; 
        font-family: 'Courier New', monospace; 
        text-shadow: 0 0 15px #bf5af2; 
    }}
    
    /* BOTÕES NEON */
    .stButton>button {{
        background: linear-gradient(90deg, #bf5af2, #5e5ce6) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: 0.4s;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 25px #bf5af2 !important;
        transform: translateY(-2px);
    }}

    hr {{ border: 0; height: 1px; background: linear-gradient(90deg, transparent, #bf5af2, transparent); margin: 30px 0; }}
</style>
""", unsafe_allow_html=True)

# 4. TELA DE LOGIN CYBERPUNK
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div style='text-align:center; color:#00d2ff; font-weight:bold; letter-spacing:3px; margin-bottom:15px;'>SYSTEM AUTHENTICATION</div>", unsafe_allow_html=True)
        u = st.text_input("USER ID")
        p = st.text_input("ACCESS KEY", type="password")
        if st.button("CONNECT TO NEURAL NET", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD OPERACIONAL
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Exibição do Saldo
st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Painel de Gestão
with st.container():
    col_a, col_b, col_c = st.columns(3)
    st.session_state.banca = col_a.number_input("BANCA:", value=float(st.session_state.banca))
    st.session_state.valor_inicial = col_b.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
    st.session_state.payout = col_c.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("<hr>", unsafe_allow_html=True)

# Seleção de Parâmetros
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME:", ["M1", "M5"])
est = c2.selectbox("STRATEGY:", ["Cyber Sniper", "Neon Turbo", "Quantum Pulse"])
at = c3.selectbox("ASSET:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# Lógica de Sinal (Simulada)
seed = int(datetime.now().timestamp() / 60)
np.random.seed(seed)
res = np.random.randint(0, 100)
if res > 80: sinal, cor = "PUT 🔴", "#ff3b30"
elif res < 20: sinal, cor = "CALL 🟢", "#00e676"
else: sinal, cor = "ANALYZING... 🔎", "#00d2ff"

now = datetime.now()
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# Card de Sinal Cyber
st.markdown(f"""
<div class="signal-card">
    <div style="color:#bf5af2; font-size:14px; font-weight:bold; letter-spacing:4px; margin-bottom:10px;">PROBABILITY ENGINE</div>
    <h1 style="color:{cor}; font-size:75px; margin:15px 0; text-shadow: 0 0 20px {cor}88;">{sinal}</h1>
    <div class="timer-text">00:{int(faltam):02d}</div>
</div>
""", unsafe_allow_html=True)

# Ações de Controle
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("DISCONNECT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("WIPE DATA", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
