import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. SETUP DA PÁGINA (Layout Centrado para um visual mais "Clean")
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'logado': False, 'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# IMAGEM DE FUNDO (SETUP TRADER CYBERPUNK)
img_background = "https://w0.peakpx.com/wallpaper/705/503/HD-wallpaper-cyberpunk-trading-desk-futuristic-city-view-trading-setup-neon-lights-data-screens-digital-art.jpg"

# 2. CSS REFORMULADO (MINIMALISTA + CONTRASTE ALTO)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 10, 0.94), rgba(0, 5, 10, 0.94)), url("{img_background}");
        background-size: cover;
        background-position: center;
    }}
    
    /* CABEÇALHO COMPACTO */
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 10px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 26px; font-family: 'Arial'; font-weight: 700; }}
    .t-text {{ color: #00e676; font-size: 26px; font-family: 'Arial'; font-weight: 700; text-shadow: 0 0 10px #00e676; margin-left: 5px; }}
    .p-badge {{ background: #00d2ff; color: #000; padding: 1px 6px; border-radius: 3px; font-size: 13px; margin-left: 8px; font-weight: bold; }}
    
    /* SALDO SLIM */
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.05); color: #00e676; padding: 10px; border-radius: 8px; 
        font-size: 20px; font-weight: 600; border: 1px solid rgba(0, 210, 255, 0.3); text-align: center;
        margin-bottom: 20px; font-family: monospace;
    }}
    
    /* CARD DE SINAL DISCRETO */
    .signal-card {{ 
        background: rgba(5, 10, 20, 0.85); border-radius: 12px; padding: 25px; text-align: center; 
        border: 1px solid rgba(0, 210, 255, 0.2); box-shadow: 0 8px 32px rgba(0,0,0,0.6);
    }}
    
    .signal-text {{ font-size: 48px !important; margin: 10px 0 !important; font-weight: 800; letter-spacing: 2px; }}
    .timer-text {{ font-size: 32px !important; color: #00d2ff; font-family: monospace; font-weight: bold; }}

    /* BOTÕES (TEXTO PRETO PARA MÁXIMA LEITURA) */
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000000 !important; font-weight: 800 !important; border: none !important;
        height: 40px !important; border-radius: 6px !important; font-size: 14px !important;
        text-transform: uppercase !important;
    }}
    
    /* INPUTS E SELECTS */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(0,0,0,0.4) !important;
        color: #00d2ff !important; border: 1px solid rgba(0, 210, 255, 0.2) !important;
        font-size: 14px !important;
    }}
    label {{ color: rgba(0, 210, 255, 0.8) !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }}

    .block-container {{ padding-top: 2rem !important; }}
</style>
""", unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<p style='text-align:center; color:#00d2ff; font-size:12px;'>SECURITY CHECK REQUIRED</p>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("ACESSAR TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD (LOGADO)
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Bloco de Saldo
_, col_banca, _ = st.columns([1, 1.5, 1])
with col_banca:
    st.markdown(f'<div class="banca-box">SALDO ATUAL: R$ {st.session_state.banca:.2f}</div>', unsafe_allow_html=True)

# Linha de Gestão
c1, c2, c3 = st.columns(3)
st.session_state.banca = c1.number_input("BANCA:", value=float(st.session_state.banca))
st.session_state.valor_inicial = c2.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
st.session_state.payout = c3.number_input("PAYOUT %:", value=int(st.session_state.payout))

# Linha de Estratégia
s1, s2, s3 = st.columns(3)
tf = s1.selectbox("TIME:", ["M1", "M5"])
est = s2.selectbox("ENGINE:", ["Sniper V2", "Turbo MHI", "Quantum BB"])
at = s3.selectbox("ASSET:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# 5. MOTOR DE ANÁLISE
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)
sinal, cor, conf = "ANALISANDO...", "#4b5563", []

# Simulação de sinal baseada no tempo
if np.random.random() > 0.6:
    if np.random.random() > 0.5:
        sinal, cor, conf = "CALL 🟢", "#00e676", ["VOL OK", "TREND UP"]
    else:
        sinal, cor, conf = "PUT 🔴", "#ff1744", ["VOL OK", "TREND DOWN"]

# Timer
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# 6. CARD DE SINAL (VISUAL CLEAN)
st.markdown(f"""
<div class="signal-card">
    <div style="color:rgba(0, 230, 118, 0.7); font-size:10px; font-weight:bold; letter-spacing:2px;">ENGINE STATUS: ACTIVE | {at}</div>
    <h1 class="signal-text" style="color:{cor};">{sinal}</h1>
    <div class="timer-text">00:{int(faltam):02d}</div>
    <div style="margin-top:12px;">
        {''.join([f'<span style="color:#00e676; border:1px solid #00e676; padding:2px 10px; border-radius:4px; font-size:10px; margin:3px; display:inline-block;">{c}</span>' for c in conf]) if conf else '<span style="color:#4b5563; font-size:10px;">SCANNING MARKET...</span>'}
    </div>
</div>
""", unsafe_allow_html=True)

# 7. BOTÕES DE CONTROLE (APENAS UMA VEZ)
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
b_col1, b_col2 = st.columns(2)

if b_col1.button("SAIR DO SISTEMA", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

if b_col2.button("LIMPAR DADOS", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0})
    st.rerun()

# Atualização automática suave
time.sleep(1)
st.rerun()
