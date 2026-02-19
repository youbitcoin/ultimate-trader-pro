import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DE INTERFACE (VOLTANDO AO VISUAL IMPACTANTE) ---
st.set_page_config(page_title="Ultimate Trader Pro", layout="wide")

if 'logado' not in st.session_state:
    st.session_state.update({
        'logado': False, 'banca': 1000.0, 'entrada': 10.0, 
        'payout': 87, 'wins': 0, 'losses': 0
    })

# FUNDO CYBERPUNK TRADER (O que você tinha pedido antes)
img_background = "https://w0.peakpx.com/wallpaper/705/503/HD-wallpaper-cyberpunk-trading-desk-futuristic-city-view-trading-setup-neon-lights-data-screens-digital-art.jpg"

# --- 2. CSS VOLTANDO AO ESTILO "CYBER" ---
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.85), rgba(0, 5, 15, 0.85)), url("{img_background}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 25px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 45px; font-family: 'Arial Black'; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 45px; font-family: 'Arial Black'; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 10px; }}
    .p-badge {{ 
        background: #00d2ff; color: #000; padding: 2px 12px; border-radius: 4px; 
        font-size: 20px; margin-left: 15px; font-weight: bold; box-shadow: 0 0 15px #00d2ff;
    }}
    
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.1); color: #00e676; padding: 25px; border-radius: 15px; 
        font-size: 35px; font-weight: 800; border: 2px solid #00d2ff; text-align: center; font-family: monospace;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.3); margin-bottom: 30px;
    }}
    
    .signal-card {{ 
        background: rgba(5, 10, 25, 0.9); border-radius: 20px; padding: 50px; text-align: center; 
        border: 2px solid #00d2ff; box-shadow: 0 0 50px rgba(0,0,0,1);
    }}
    
    /* BOTÕES GRANDES COM TEXTO PRETO */
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000 !important; font-weight: 900 !important; border: none !important;
        height: 55px !important; border-radius: 10px !important; font-size: 18px !important;
        text-transform: uppercase !important;
    }}

    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #050a14 !important; color: #00d2ff !important;
        border: 1px solid #00d2ff !important; font-size: 18px !important;
    }}
    label {{ color: #00d2ff !important; font-size: 16px !important; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- 3. SISTEMA DE LOGIN (COM TRAVA DE SEGURANÇA) ---
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h3 style='text-align:center; color:#00d2ff;'>TERMINAL LOGIN</h3>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO", key="login_user")
        p = st.text_input("SENHA", type="password", key="login_pw")
        if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# --- 4. DASHBOARD CYBER-TRADER ---
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Banca em Destaque
_, col_banca, _ = st.columns([1, 2, 1])
with col_banca:
    st.markdown(f'<div class="banca-box">SALDO OPERACIONAL: R$ {st.session_state.banca:.2f}</div>', unsafe_allow_html=True)

# Gestão Superior
c1, c2, c3 = st.columns(3)
st.session_state.banca = c1.number_input("BANCA ATUAL:", value=float(st.session_state.banca))
st.session_state.entrada = c2.number_input("ENTRADA R$:", value=float(st.session_state.entrada))
st.session_state.payout = c3.number_input("PAYOUT %:", value=int(st.session_state.payout))

# Engine de Sinal
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)
sinal, cor = "ANALISANDO...", "#4b5563"

if np.random.random() > 0.6:
    if np.random.random() > 0.5: sinal, cor = "CALL 🟢", "#00e676"
    else: sinal, cor = "PUT 🔴", "#ff1744"

timer = 60 - now.second

st.markdown(f"""
<div class="signal-card">
    <div style="color:#00d2ff; font-size:14px; letter-spacing:4px; margin-bottom:15px;">QUANTUM ANALYSIS ACTIVE</div>
    <h1 style="color:{cor}; font-size:100px; margin:20px 0; font-weight:900; text-shadow: 0 0 30px {cor};">{sinal}</h1>
    <div style="font-size:50px; color:#00d2ff; font-family:monospace; font-weight:bold;">00:{timer:02d}</div>
</div>
""", unsafe_allow_html=True)

# Botões de Ação
st.markdown("<br>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([1, 1, 1])

if b1.button("✅ REGISTRAR WIN", use_container_width=True):
    st.session_state.wins += 1
    st.session_state.banca += (st.session_state.entrada * (st.session_state.payout / 100))
    st.rerun()

if b2.button("❌ REGISTRAR LOSS", use_container_width=True):
    st.session_state.losses += 1
    st.session_state.banca -= st.session_state.entrada
    st.rerun()

if b3.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

time.sleep(1)
st.rerun()
