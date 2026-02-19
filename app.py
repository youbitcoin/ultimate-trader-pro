import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta

# --- 1. SETUP DA INTERFACE CYBERPUNK ---
st.set_page_config(page_title="Ultimate Trader Pro", layout="wide")

if 'logado' not in st.session_state:
    st.session_state.update({
        'logado': False, 'banca': 1000.0, 'entrada': 10.0, 
        'payout': 87, 'wins': 0, 'losses': 0, 'm_gale': 0
    })

# Fundo original de alta performance
img_background = "https://w0.peakpx.com/wallpaper/705/503/HD-wallpaper-cyberpunk-trading-desk-futuristic-city-view-trading-setup-neon-lights-data-screens-digital-art.jpg"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.85), rgba(0, 5, 15, 0.85)), url("{img_background}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 20px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 45px; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 45px; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 10px; }}
    .p-badge {{ background: #00d2ff; color: #000; padding: 2px 12px; border-radius: 4px; font-size: 20px; margin-left: 15px; font-weight: 800; box-shadow: 0 0 15px #00d2ff; }}
    
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.1); color: #00e676; padding: 20px; border-radius: 15px; 
        font-size: 32px; font-weight: 800; border: 2px solid #00d2ff; text-align: center; font-family: monospace;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.2);
    }}
    
    .signal-card {{ 
        background: rgba(5, 10, 25, 0.95); border-radius: 20px; padding: 40px; text-align: center; 
        border: 2px solid #00d2ff; box-shadow: 0 0 50px rgba(0,0,0,1); margin-top: 20px;
    }}
    
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000 !important; font-weight: 900 !important; border: none !important;
        height: 55px !important; border-radius: 10px !important; font-size: 18px !important;
    }}

    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #050a14 !important; color: #00d2ff !important;
        border: 1px solid #00d2ff !important; font-size: 18px !important;
    }}
    label {{ color: #00d2ff !important; font-size: 15px !important; font-weight: bold; text-transform: uppercase; }}
</style>
""", unsafe_allow_html=True)

# --- 2. SISTEMA DE LOGIN (O ÚNICO BLOQUEIO QUE MANTIVEMOS PARA NÃO VAZAR) ---
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h3 style='text-align:center; color:#00d2ff;'>ACCESS TERMINAL</h3>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# --- 3. DASHBOARD OPERACIONAL ---
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Linha de Status
c_b1, c_b2 = st.columns([2, 1])
with c_b1:
    st.markdown(f'<div class="banca-box">SALDO DISPONÍVEL: R$ {st.session_state.banca:.2f}</div>', unsafe_allow_html=True)
with c_b2:
    st.markdown(f'<div class="banca-box" style="border-color:#00e676; color:#fff;">W: {st.session_state.wins} | L: {st.session_state.losses}</div>', unsafe_allow_html=True)

# Gestão de Martingale e Entradas
st.markdown("<br>", unsafe_allow_html=True)
g1, g2, g3, g4 = st.columns(4)
st.session_state.entrada = g1.number_input("ENTRADA R$:", value=float(st.session_state.entrada))
st.session_state.payout = g2.number_input("PAYOUT %:", value=int(st.session_state.payout))
ativo = g3.selectbox("ATIVO:", ["EUR/USD (OTC)", "BTC/USDT", "GBP/JPY"])
m_nivel = g4.selectbox("MARTINGALE:", ["Nenhum", "Gale 1", "Gale 2"])

# Cálculo de Martingale sugerido
valor_gale = st.session_state.entrada * 2.2 if m_nivel != "Nenhum" else st.session_state.entrada

# --- 4. ENGINE DE ANÁLISE ---
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
    <div style="color:#00d2ff; font-size:14px; letter-spacing:4px;">QUANTUM ANALYSIS ACTIVE | {ativo}</div>
    <h1 style="color:{cor}; font-size:110px; margin:15px 0; font-weight:900; text-shadow: 0 0 30px {cor};">{sinal}</h1>
    <div style="font-size:45px; color:#00d2ff; font-family:monospace; font-weight:bold;">00:{timer:02d}</div>
    <div style="margin-top:20px; font-size:18px; color:#aaa;">
        SUGESTÃO: <span style="color:#00d2ff; font-weight:bold;">{m_nivel}</span> | 
        VALOR: <span style="color:#00e676; font-weight:bold;">R$ {valor_gale:.2f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. CONTROLES DE RESULTADO ---
st.markdown("<br>", unsafe_allow_html=True)
res1, res2, res3 = st.columns([1.5, 1.5, 1])

if res1.button("✅ REGISTRAR WIN", use_container_width=True):
    st.session_state.wins += 1
    st.session_state.banca += (st.session_state.entrada * (st.session_state.payout / 100))
    st.rerun()

if res2.button("❌ REGISTRAR LOSS", use_container_width=True):
    st.session_state.losses += 1
    st.session_state.banca -= st.session_state.entrada
    st.rerun()

if res3.button("LOGOUT / SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

time.sleep(1)
st.rerun()
