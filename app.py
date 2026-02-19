import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. SETUP DA PÁGINA
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'aguardando': False, 'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. FUNDO FUTURISTA HIGH-TECH
# Uma malha digital de alta tecnologia que combina azul e roxo
img_futurista = "https://images.hdqwalls.com/download/cyberpunk-city-street-4k-yo-2560x1440.jpg"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.85), rgba(0, 5, 15, 0.85)), url("{img_futurista}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO BLINDADA */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
    }}
    .u-text {{ color: #FFFFFF; font-size: 42px; font-family: 'Arial Black', sans-serif; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 42px; font-family: 'Arial Black', sans-serif; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 5px; }}
    .p-badge {{ 
        background: #bf5af2; color: #fff; padding: 2px 12px; border-radius: 4px; 
        font-size: 20px; margin-left: 10px; font-weight: bold; box-shadow: 0 0 15px #bf5af2;
    }}
    
    /* SALDO FUTURISTA */
    .banca-wrapper {{ display: flex; justify-content: center; margin: 25px 0; }}
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.05); 
        color: #00d2ff; 
        padding: 15px 70px; 
        border-radius: 4px; 
        font-size: 32px; 
        font-weight: 800; 
        border: 2px solid #bf5af2;
        box-shadow: 0 0 20px rgba(191, 90, 242, 0.3);
        text-align: center;
        font-family: 'Courier New', monospace;
    }}
    
    /* CARD DE SINAL */
    .signal-card {{ 
        background: rgba(5, 10, 25, 0.95); 
        border-radius: 12px; 
        padding: 30px; 
        text-align: center; 
        border: 1px solid #00d2ff;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.7);
    }}
    
    /* AJUSTE DE CORES DOS INPUTS */
    .stNumberInput input {{ background-color: #0a0a20 !important; color: #00d2ff !important; border: 1px solid #bf5af2 !important; }}
    .stSelectbox div[data-baseweb="select"] {{ background-color: #0a0a20 !important; color: white !important; border: 1px solid #bf5af2 !important; }}
</style>
""", unsafe_allow_html=True)

# 3. LOGIN (FUTURISTA)
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, col_log, c3 = st.columns([1, 2, 1])
    with col_log:
        st.markdown("<h4 style='text-align:center; color:#00d2ff;'>SECURE ACCESS TERMINAL</h4>", unsafe_allow_html=True)
        u = st.text_input("ID")
        p = st.text_input("CHAVE", type="password")
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD OPERACIONAL
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Saldo
st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Painel de Gestão (Sempre Visível)
col_a, col_b, col_c = st.columns(3)
st.session_state.banca = col_a.number_input("BANCA ATUAL:", value=float(st.session_state.banca))
st.session_state.valor_inicial = col_b.number_input("ENTRADA R$:", value=float(st.session_state.valor_inicial))
st.session_state.payout = col_c.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("<br>", unsafe_allow_html=True)

# Mercado e ESTRATÉGIAS RESTAURADAS
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TEMPO:", ["M1", "M5"])
# RESTAURADO: Sniper, Turbo e Moderada
est = c2.selectbox("ESTRATÉGIA:", ["Sniper", "Turbo", "Moderada"])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# Analisador de Sinais
seed = int(datetime.now().timestamp() / 60)
np.random.seed(seed)
res = np.random.randint(0, 100)
if res > 80: sinal, cor = "PUT 🔴", "#ff3b30"
elif res < 20: sinal, cor = "CALL 🟢", "#00e676"
else: sinal, cor = "ANALISANDO... 🔎", "#00d2ff"

now = datetime.now()
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# Card de Sinal Futurista
st.markdown(f"""
<div class="signal-card">
    <div style="color:#bf5af2; font-weight:bold; letter-spacing:2px; margin-bottom:10px;">PROBABILITY ENGINE: {at}</div>
    <h1 style="color:{cor}; font-size:75px; margin:10px 0; text-shadow: 0 0 30px {cor}66;">{sinal}</h1>
    <div style="font-size: 55px; font-weight: bold; color: white; font-family: monospace;">00:{int(faltam):02d}</div>
</div>
""", unsafe_allow_html=True)

# Controle Final
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("LIMPAR HISTÓRICO", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
