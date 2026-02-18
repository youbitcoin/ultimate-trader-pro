import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES BÁSICAS
SEU_WHATSAPP = "5521998203486"
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# 2. ESTILO CSS (BACKGROUND, LOGO E VIDRO)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        background-attachment: fixed;
    }}
    
    /* Estilo do Logo */
    .logo-text {{
        font-family: 'Arial Black', sans-serif;
        font-size: 42px;
        letter-spacing: -2px;
        text-align: center;
        margin-bottom: 10px;
    }}
    .logo-ultimate {{ color: #ffffff; }}
    .logo-trader {{ color: #00e676; text-shadow: 0 0 15px rgba(0,230,118,0.6); }}
    .logo-pro {{ 
        font-size: 18px; 
        background: #00e676; 
        color: #020617; 
        padding: 2px 8px; 
        border-radius: 4px; 
        vertical-align: middle;
        margin-left: 5px;
    }}

    .dash-container, .signal-card {{
        background: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }}

    h1 {{ color: #00e676 !important; text-align: center; font-weight: 800; }}
    .dash-value {{ font-size: 26px; font-weight: bold; color: #fff; }}
    .value-win {{ color: #00e676; }}
    .value-loss {{ color: #ff5252; }}
    .timer-box {{ font-size: 55px; font-weight: bold; color: #ffffff; margin: 10px 0; font-family: monospace; }}
    
    .float-wpp {{
        position: fixed; width: 60px; height: 60px; bottom: 25px; right: 25px;
        background-color: #25d366; border-radius: 50px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4); z-index: 9999;
    }}
</style>
<a href="https://wa.me/{SEU_WHATSAPP}" class="float-wpp" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:35px">
</a>
""", unsafe_allow_html=True)

# 3. ESTADOS DA SESSÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'aguardando' not in st.session_state: st.session_state.aguardando = False
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'som' not in st.session_state: st.session_state.som = False

# 4. PAGINA DE LOGIN (COM LOGO)
if not st.session_state.logado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="logo-text"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="signal-card">', unsafe_allow_html=True)
        u = st.text_input("Usuário / ID")
        p = st.text_input("Senha de Acesso", type="password")
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if (u == "romildo" or u == "teste") and p == "12345":
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 5. DASHBOARD DE PERFORMANCE
total = st.session_state.win + st.session_state.loss
taxa = (st.session_state.win / total * 100) if total > 0 else 0

st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around;">
        <div><div style="font-size:11px;color:#94a3b8">OPS</div><div class="dash-value">{total}</div></div>
        <div><div style="font-size:11px;color:#94a3b8">WINS</div><div class="dash-value value-win">{st.session_state.win}</div></div>
        <div><div style="font-size:11px;color:#94a3b8">LOSSES</div><div class="dash-value value-loss">{st.session_state.loss}</div></div>
        <div><div style="font-size:11px;color:#94a3b8">WIN RATE</div><div class="dash-value">{taxa:.1f}%</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# LOGO NO TOPO DO TERMINAL
st.markdown('<div class="logo-text" style="font-size:28px;"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# 6. ANALISE E SINAIS
if st.session_state.aguardando:
    st.markdown("<div class='signal-card'><h3>RESULTADO DO SINAL?</h3>", unsafe_allow_html=True)
    c_w, c_l, c_n = st.columns(3)
    if c_w.button("✅ WIN"):
        st.session_state.win += 1
        st.session_state.aguardando = False
        st.session_state.som = False
        st.rerun()
    if c_l.button("❌ LOSS"):
        st.session_state.loss += 1
        st.session_state.aguardando = False
        st.session_state.som = False
        st.rerun()
    if c_n.button("⚪ PULAR"):
        st.session_state.aguardando = False
        st.session_state.som = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    c1, c2 = st.columns(2)
    tf = c1.selectbox("TEMPO:", ["M1", "M5"])
    
    # LISTA EXPANDIDA DE PARES
    lista_ativos = [
        "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", 
        "AUD/CAD (OTC)", "EUR/GBP (OTC)", "USD/CHF (OTC)",
        "AUD/USD (OTC)", "NZD/USD (OTC)", "EUR/JPY (OTC)",
        "BITCOIN (BTC)", "ETHEREUM (ETH)", "SOLANA (SOL)"
    ]
    at = c2.selectbox("ATIVO DISPONÍVEL:", lista_ativos)

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    
    if f > 91: sinal, cor = "PUT (VENDA) 🔴", "#ff5252"
    elif f < 9: sinal, cor = "CALL (COMPRA) 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

    # SOM DE ALERTA
    if "ANALISANDO" not in sinal and not st.session_state.som:
        st.markdown('<iframe src="https://www.soundjay.com/buttons/sounds/button-3.mp3" allow="autoplay" style="display:none"></iframe>', unsafe_allow_html=True)
        st.session_state.som = True

    st.markdown(f"""
    <div class='signal-card'>
        <h2 style="color:#fff !important; margin-bottom:0;">{at}</h2>
        <h1 style='color:{cor} !important; font-size:45px; margin:10px 0;'>{sinal}</h1>
        <div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.aguardando = True
        time.sleep(1)
        st.rerun()

    time.sleep(1)
    st.rerun()
