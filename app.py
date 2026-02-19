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
        'banca': 1000.0, 'valor_atual': 10.0, 'payout': 87
    })

# 2. CSS DINÂMICO (IMAGENS DIFERENTES PARA LOGIN E DASHBOARD)
img_login = "https://images.unsplash.com/photo-1605810230434-7631ac76ec81?q=80&w=2070&auto=format&fit=crop" # Cidade Cyberpunk Clara
img_dash = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop"  # Hardware/Matrix Dark

bg_url = img_login if not st.session_state.logado else img_dash

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{bg_url}");
        background-size: cover;
        background-position: center;
    }}
    
    /* LOGO OFICIAL */
    .logo-container {{ text-align: center; margin-bottom: 30px; }}
    .logo-ultimate {{ font-family: 'Arial Black'; font-size: 38px; color: white; }}
    .logo-trader {{ font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 15px rgba(0,230,118,0.8); }}
    .logo-pro {{ background: #00e676; color: #020617; padding: 2px 10px; border-radius: 4px; font-size: 20px; vertical-align: middle; margin-left: 5px; font-weight: bold; }}
    
    /* SALDO CENTRALIZADO */
    .banca-wrapper {{ display: flex; justify-content: center; margin-bottom: 20px; }}
    .banca-box {{ background: rgba(6, 78, 59, 0.9); color: #00e676; padding: 10px 40px; border-radius: 15px; font-size: 24px; font-weight: bold; border: 2px solid #059669; box-shadow: 0 0 20px rgba(0,230,118,0.3); }}
    
    /* CARDS */
    .dash-container, .signal-card {{ 
        background: rgba(15, 23, 42, 0.85); border-radius: 20px; 
        padding: 20px; text-align: center; border: 1px solid rgba(0,230,118,0.3);
        backdrop-filter: blur(10px);
    }}
    .timer-box {{ font-size: 50px; font-weight: bold; color: white; font-family: 'Courier New', monospace; }}
</style>
""", unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span><span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h3 style='text-align:center; color:white;'>TERMINAL DE ACESSO</h3>", unsafe_allow_html=True)
            u = st.text_input("ID de Usuário")
            p = st.text_input("Chave de Segurança", type="password")
            if st.button("INICIAR SISTEMA", use_container_width=True):
                if u == "romildo" and p == "12345":
                    st.session_state.logado = True
                    st.rerun()
    st.stop()

# 4. PAINEL LOGADO
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span><span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Placar
total_ops = st.session_state.win + st.session_state.loss + st.session_state.gales
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white; font-weight: bold;">
        <div>OPS: {total_ops}</div>
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div style="color:#fbbf24;">GALES: {st.session_state.gales}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Seletores e Ativos
if not st.session_state.aguardando:
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    tf = c1.selectbox("TEMPO:", ["M1", "M5"])
    est = c2.selectbox("ESTRATÉGIA:", ["Turbo", "Sniper", "Moderada"])
    at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BITCOIN", "SOLANA"])

    # Simulação de análise técnica
    seed = int(datetime.now().timestamp() / 60)
    np.random.seed(seed)
    f = np.random.randint(0, 100)
    if f > 85: sinal, cor = "PUT 🔴", "#ff5252"
    elif f < 15: sinal, cor = "CALL 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    st.markdown(f"""
    <div class="signal-card">
        <h2 style="color:white; margin:0;">{at}</h2>
        <h1 style="color:{cor}; font-size:60px; margin:20px 0;">{sinal}</h1>
        <div class="timer-box">00:{int(faltam):02d}</div>
    </div>
    """, unsafe_allow_html=True)

# Rodapé
st.markdown("<br>", unsafe_allow_html=True)
col_f1, col_f2 = st.columns(2)
if col_f1.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if col_f2.button("RESETAR", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
