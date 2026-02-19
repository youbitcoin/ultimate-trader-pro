import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'aguardando': False, 'som_tocado': False,
        'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. FUNDOS PREMIUM
# Login: Cidade Futurista
img_login = "https://img.freepik.com/fotos-premium/uma-sala-com-muitas-telas-e-uma-cidade-ao-fundo-ia-generativa_955841-419.jpg"
# Dashboard: Hi-Tech Cyberpunk (Circuitos/Data Center Neon)
img_dash = "https://wallpapercave.com/wp/wp4337482.jpg" 

bg_url = img_login if not st.session_state.logado else img_dash

# 3. CSS PARA LOGO E INTERFACE
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO PADRÃO SOLICITADO */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 25px;
    }}
    .u-text {{ color: #FFFFFF; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; text-shadow: 0 0 20px rgba(0,230,118,0.8); }}
    .p-badge {{ 
        background: #00e676; color: #000; padding: 2px 10px; border-radius: 5px; 
        font-size: 20px; margin-left: 10px; font-family: Arial, sans-serif; font-weight: bold;
    }}
    
    /* SALDO CENTRALIZADO */
    .banca-wrapper {{ display: flex; justify-content: center; margin-bottom: 20px; }}
    .banca-box {{ 
        background: rgba(0, 230, 118, 0.15); color: #00e676; padding: 12px 50px; 
        border-radius: 15px; font-size: 26px; font-weight: bold; border: 2px solid #00e676; 
        box-shadow: 0 0 25px rgba(0,230,118,0.3); text-align: center;
    }}
    
    /* CARDS HI-TECH */
    .dash-container, .signal-card {{ 
        background: rgba(10, 15, 28, 0.95); border-radius: 20px; 
        padding: 25px; text-align: center; border: 1px solid rgba(0,230,118,0.3);
        backdrop-filter: blur(15px);
    }}
</style>
""", unsafe_allow_html=True)

# 4. TELA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        u = st.text_input("ID DE ACESSO")
        p = st.text_input("CHAVE", type="password")
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD OPERACIONAL
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Placar Hi-Tech
total_ops = st.session_state.win + st.session_state.loss + st.session_state.gales
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white; font-weight: bold;">
        <div>OPERAS: {total_ops}</div>
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div style="color:#fbbf24;">GALES: {st.session_state.gales}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- REAPARECIMENTO DAS OPÇÕES DE GESTÃO ---
st.markdown("<br>", unsafe_allow_html=True)
if not st.session_state.aguardando:
    with st.expander("⚙️ CONFIGURAÇÕES DE GESTÃO", expanded=True):
        col_g1, col_g2, col_g3 = st.columns(3)
        st.session_state.banca = col_g1.number_input("BANCA:", value=float(st.session_state.banca), step=50.0)
        st.session_state.valor_inicial = col_g2.number_input("ENTRADA:", value=float(st.session_state.valor_inicial), step=5.0)
        st.session_state.payout = col_g3.number_input("PAYOUT %:", value=int(st.session_state.payout))

    # Seleção de Ativos
    c1, c2, c3 = st.columns(3)
    tf = c1.selectbox("TIME:", ["M1", "M5"])
    est = c2.selectbox("ESTRATÉGIA:", ["Sniper", "Turbo", "Moderada"])
    at = c3.selectbox("PARIDADE:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

    # Simulação de Sinal
    seed = int(datetime.now().timestamp() / 60)
    np.random.seed(seed)
    f = np.random.randint(0, 100)
    if f > 80: sinal, cor = "PUT 🔴", "#ff5252"
    elif f < 20: sinal, cor = "CALL 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    st.markdown(f"""
    <div class="signal-card">
        <h2 style="color:white; margin:0;">{at}</h2>
        <h1 style="color:{cor}; font-size:65px; margin:15px 0; font-weight: 900;">{sinal}</h1>
        <div style="font-size: 50px; font-weight: bold; color: white; font-family: monospace;">00:{int(faltam):02d}</div>
    </div>
    """, unsafe_allow_html=True)

# Botões de Controle
st.markdown("<br>", unsafe_allow_html=True)
col_b1, col_b2 = st.columns(2)
if col_b1.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if col_b2.button("LIMPAR DADOS", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
