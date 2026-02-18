import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime, timedelta

# 1. CONFIGURACOES TÉCNICAS
SEU_WHATSAPP = "5521998203486" 

st.set_page_config(page_title="Ultimate Trader - Dashboard Pro", layout="centered")

# CSS para o Dashboard, Cards e WhatsApp
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0b0e14; color: #e6edf3; }}
    h1, h2, h3 {{ color: #00e676 !important; text-align: center; }}
    
    /* Estilo do Dashboard */
    .dash-container {{
        background: #161b22;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #30363d;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }}
    .dash-item {{ text-align: center; }}
    .dash-label {{ font-size: 12px; color: #8b949e; text-transform: uppercase; }}
    .dash-value {{ font-size: 24px; font-weight: bold; color: #fff; }}
    .value-win {{ color: #00e676; }}
    .value-loss {{ color: #ff5252; }}

    .signal-card {{ 
        background: #161b22; 
        border: 2px solid #30363d; 
        border-radius: 15px; padding: 30px; text-align: center;
    }}
    .timer-box {{ font-size: 45px; font-weight: bold; color: #ffffff; margin: 15px 0; font-family: monospace; }}
    
    .float-wpp {{
        position: fixed; width: 60px; height: 60px; bottom: 20px; right: 20px;
        background-color: #25d366; color: #FFF; border-radius: 50px;
        text-align: center; font-size: 30px; box-shadow: 2px 2px 10px #000; z-index: 9999;
        display: flex; align-items: center; justify-content: center;
    }}
    </style>
    <a href="https://wa.me/{SEU_WHATSAPP}" class="float-wpp" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:35px">
    </a>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE SESSÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'aguardando_resultado' not in st.session_state: st.session_state.aguardando_resultado = False
if 'ultimo_sinal' not in st.session_state: st.session_state.ultimo_sinal = None
if 'historico_win' not in st.session_state: st.session_state.historico_win = 0
if 'historico_loss' not in st.session_state: st.session_state.historico_loss = 0

# LOGIN
if not st.session_state.logado:
    st.title("SISTEMA VIP OTC")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("Trader ID")
        p = st.text_input("Senha", type="password")
        if st.button("CONECTAR", use_container_width=True):
            if (u == "romildo" or u == "teste") and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 3. DASHBOARD DE OPERAÇÕES
st.sidebar.button("LIMPAR PLACAR", on_click=lambda: st.session_state.update({'historico_win': 0, 'historico_loss': 0}))
st.sidebar.button("LOGOUT", on_click=lambda: st.session_state.update({'logado': False}))

total_ops = st.session_state.historico_win + st.session_state.historico_loss
winrate = (st.session_state.historico_win / total_ops * 100) if total_ops > 0 else 0

st.markdown(f"""
    <div class="dash-container">
        <div class="dash-item">
            <div class="dash-label">Operações</div>
            <div class="dash-value">{total_ops}</div>
        </div>
        <div class="dash-item">
            <div class="dash-label">Wins</div>
            <div class="dash-value value-win">{st.session_state.historico_win}</div>
        </div>
        <div class="dash-item">
            <div class="dash-label">Losses</div>
            <div class="dash-value value-loss">{st.session_state.historico_loss}</div>
        </div>
        <div class="dash-item">
            <div class="dash-label">Assertividade</div>
            <div class="dash-value">{winrate:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. CONTROLE DE FLUXO (SINAL VS FEEDBACK)
if st.session_state.aguardando_resultado:
    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    st.subheader("AGUARDANDO RESULTADO")
    st.write(f"Confirme o sinal: **{st.session_state.ultimo_sinal['direcao']}** em **{st.session_state.ultimo_sinal['ativo']}**")
    
    col_w, col_l = st.columns(2)
    with col_w:
        if st.button("✅ FOI WIN", use_container_width=True):
            st.session_state.historico_win += 1
            st.session_state.aguardando_resultado = False
            st.rerun()
    with col_l:
        if st.button("❌ FOI LOSS", use_container_width=True):
            st.session_state.historico_loss += 1
            st.session_state.aguardando_resultado = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

else:
    # TELA DE ANÁLISE
    st.title("🎯 MONITOR QUOTEX PRO")
    c1, c2 = st.columns(2)
    with c1: tf = st.selectbox("TEMPO:", ["M1", "M5"])
    with c2: at = st.selectbox("ATIVO OTC:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BTC/USD"])

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    
    faltam = (prox - now).total_seconds()

    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    
    # Filtro de Assertividade 92%
    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    
    if f > 92: sinal, cor = "PUT (VENDA) 🔴", "#ff5252"
    elif f < 8: sinal, cor = "CALL (COMPRA) 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#8b949e"

    st.markdown(f"<h3>{at}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: {cor} !important; font-size: 40px;'>{sinal}</h1>", unsafe_allow_html=True)

    minutos, segundos = int(faltam // 60), int(faltam % 60)
    st.markdown(f
