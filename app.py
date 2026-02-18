import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURACOES BASICAS
SEU_WHATSAPP = "5521998203486"
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# 2. ESTILO CSS (BACKGROUND E DASHBOARD)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        background-attachment: fixed;
    }}
    .dash-container, .signal-card {{
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }}
    h1 {{ 
        color: #00e676 !important; 
        text-align: center; 
        font-weight: 800;
        margin-bottom: 20px;
    }}
    .dash-value {{ font-size: 26px; font-weight: bold; color: #fff; }}
    .value-win {{ color: #00e676; }}
    .value-loss {{ color: #ff5252; }}
    .timer-box {{ font-size: 50px; font-weight: bold; color: #ffffff; margin: 15px 0; font-family: monospace; }}
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

# 3. ESTADOS DA SESSAO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'aguardando' not in st.session_state: st.session_state.aguardando = False
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'som' not in st.session_state: st.session_state.som = False

# 4. LOGIN
if not st.session_state.logado:
    st.title("ACESSO VIP")
    u = st.text_input("Usuario")
    p = st.text_input("Senha", type="password")
    if st.button("ENTRAR"):
        if (u == "romildo" or u == "teste") and p == "12345":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# 5. DASHBOARD (NO TOPO)
total = st.session_state.win + st.session_state.loss
taxa = (st.session_state.win / total * 100) if total > 0 else 0

st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around;">
        <div><div style="font-size:12px;color:#94a3b8">OPS</div><div class="dash-value">{total}</div></div>
        <div><div style="font-size:12px;color:#94a3b8">WINS</div><div class="dash-value value-win">{st.session_state.win}</div></div>
        <div><div style="font-size:12px;color:#94a3b8">LOSSES</div><div class="dash-value value-loss">{st.session_state.loss}</div></div>
        <div><div style="font-size:12px;color:#94a3b8">WIN RATE</div><div class="dash-value">{taxa:.1f}%</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1>MONITOR QUOTEX PRO</h1>", unsafe_allow_html=True)

# 6. ANALISE E SINAIS
if st.session_state.aguardando:
    st.markdown("<div class='signal-card'><h3>CONFIRME O RESULTADO</h3>", unsafe_allow_html=True)
    c_w, c_l, c_n = st.columns(3)
    if c_w.button("WIN"):
        st.session_state.win += 1
        st.session_state.aguardando = False
        st.session_state.som = False
        st.rerun()
    if c_l.button("LOSS"):
        st.session_state.loss += 1
        st.session_state.aguardando = False
        st.session_state.som = False
        st.rerun()
    if c_n.button("PULAR"):
        st.session_state.aguardando = False
        st.session_state.som = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    c1, c2 = st.columns(2)
    tf = c1.selectbox("TEMPO:", ["M1", "M5"])
    at = c2.selectbox("ATIVO OTC:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    if f > 92: sinal, cor = "PUT (VENDA)", "#ff5252"
    elif f < 8: sinal, cor = "CALL (COMPRA)", "#00e676"
    else: sinal, cor = "ANALISANDO...", "#94a3b8"

    if "ANALISANDO" not in sinal and not st.session_state.som:
        st.markdown('<iframe src="https://www.soundjay.com/buttons/sounds/button-3.mp3" allow="autoplay" style="display:none"></iframe>', unsafe_allow_html=True)
        st.session_state.som = True

    st.markdown(f"""
    <div class='signal-card'>
        <h3 style="color:#fff !important">{at}</h3>
        <h1 style='color:{cor} !important; font-size:45px;'>{sinal}</h1>
        <div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.aguardando = True
        time.sleep(1)
        st.rerun()

    time.sleep(1)
    st.rerun()
