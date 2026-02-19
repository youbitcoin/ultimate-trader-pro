import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. SETUP DA PÁGINA (Layout centrado para parecer mais organizado)
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# FUNDO CYBER TRADER (Vibe mais escura e profissional)
img_background = "https://w0.peakpx.com/wallpaper/705/503/HD-wallpaper-cyberpunk-trading-desk-futuristic-city-view-trading-setup-neon-lights-data-screens-digital-art.jpg"

# 2. CSS REFORMULADO: FOCO EM MINIMALISMO E LEVEZA
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 10, 0.92), rgba(0, 5, 10, 0.92)), url("{img_background}");
        background-size: cover;
        background-position: center;
    }}
    
    /* CABEÇALHO MENOR */
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 10px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 28px; font-family: 'Arial'; font-weight: 700; }}
    .t-text {{ color: #00e676; font-size: 28px; font-family: 'Arial'; font-weight: 700; text-shadow: 0 0 10px #00e676; margin-left: 5px; }}
    .p-badge {{ background: #00d2ff; color: #000; padding: 1px 6px; border-radius: 3px; font-size: 14px; margin-left: 8px; font-weight: bold; }}
    
    /* BOX DE SALDO SLIM */
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.03); color: #00e676; padding: 8px 20px; border-radius: 8px; 
        font-size: 22px; font-weight: 600; border: 1px solid rgba(0, 210, 255, 0.4); text-align: center; font-family: monospace;
        margin-bottom: 20px;
    }}
    
    /* CARD DE SINAL COMPACTO */
    .signal-card {{ 
        background: rgba(5, 10, 20, 0.8); border-radius: 12px; padding: 20px; text-align: center; 
        border: 1px solid rgba(0, 210, 255, 0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    
    /* FONTES DE SINAL REDUZIDAS */
    .signal-text {{ font-size: 50px !important; margin: 5px 0 !important; font-weight: 800; }}
    .timer-text {{ font-size: 35px !important; color: #00d2ff; font-family: monospace; font-weight: bold; }}

    /* BOTÕES AJUSTADOS (TEXTO PRETO, MAIS BAIXOS) */
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000 !important; font-weight: 700 !important; border: none !important;
        height: 38px !important; border-radius: 6px !important; font-size: 14px !important;
    }}
    
    /* INPUTS MAIS DISCRETOS */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(0,0,0,0.3) !important;
        color: #00d2ff !important; border: 1px solid rgba(0, 210, 255, 0.2) !important;
        font-size: 14px !important;
    }}
    label {{ color: rgba(0, 210, 255, 0.7) !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 1px; }}

    /* REMOVE ESPAÇOS DESNECESSÁRIOS DO STREAMLIT */
    .block-container {{ padding-top: 2rem !important; }}
</style>
""", unsafe_allow_html=True)

# 3. LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<p style='text-align:center; color:#00d2ff;'>SECURITY ACCESS</p>", unsafe_allow_html=True)
        u = st.text_input("USER")
        p = st.text_input("PASS", type="password")
        if st.button("ENTER SYSTEM", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD LIMPO
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Saldo Central e Discreto
_, col_banca, _ = st.columns([1, 1.5, 1])
with col_banca:
    st.markdown(f'<div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div>', unsafe_allow_html=True)

# Gestão em linha única para economizar espaço
c1, c2, c3 = st.columns(3)
st.session_state.banca = c1.number_input("BANCA:", value=float(st.session_state.banca))
st.session_state.valor_inicial = c2.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
st.session_state.payout = c3.number_input("PAYOUT %:", value=int(st.session_state.payout))

# Seletores compactos
s1, s2, s3 = st.columns(3)
tf = s1.selectbox("TIME:", ["M1", "M5"])
est = s2.selectbox("ENGINE:", ["Sniper (RSI/MM)", "Turbo (MHI)", "Quantum (BB)"])
at = s3.selectbox("ASSET:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# 5. MOTOR DE ANÁLISE (LÓGICA)
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)
sinal, cor, conf = "ANALISANDO...", "#4b5563", []

# Simulação rápida para o exemplo
if np.random.random() > 0.7:
    sinal, cor, conf = ("CALL 🟢", "#00e676", ["VOL OK", "MA OK"]) if np.random.random() > 0.5 else ("PUT 🔴", "#ff1744", ["VOL OK", "MA OK"])

# Timer Regressivo
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# 6. CARD DE SINAL COMPACTO
st.markdown(f"""
<div class="signal-card">
    <div style="color:rgba(0, 230, 118, 0.7); font-size:11px; font-weight:bold; letter-spacing:2px;">MARKET ANALYSIS: {at}</div>
    <h1 class="signal-text" style="color:{cor};">{sinal}</h1>
    <div class="timer-text">00:{int(faltam):02d}</div>
    <div style="margin-top:10px;">
        {''.join([f'<span style="color:#00e676; border:1px solid #00e676; padding:2px 8px; border-radius:4px; font-size:10px; margin:2px; display:inline-block;">{c}</span>' for c in conf]) if conf else '<span style="color:#4b5563; font-size:10px;">SCANNING...</span>'}
    </div>
</div>
""", unsafe_allow_html=True)

# 7. BOTÕES DE CONTROLE
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
b_col1, b_col2 = st.columns(2)
if b_col1.button("EXIT TERMINAL", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b_col2.button("WIPE DATA", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0})
    st.rerun()

time.sleep(1)
st.rerun()
