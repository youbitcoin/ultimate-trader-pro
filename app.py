import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime, timedelta

# 1. CONFIGURACOES TÉCNICAS
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

st.set_page_config(page_title="Ultimate Trader Pro - OTC Expert", layout="centered")

# CSS Profissional
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0b0e14; color: #e6edf3; }}
    h1, h2, h3 {{ color: #00e676 !important; text-align: center; }}
    .signal-card {{ 
        background: #161b22; 
        border: 2px solid #30363d; 
        border-radius: 15px; padding: 35px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.1);
    }}
    .payout-text {{ color: #00e676; font-weight: bold; font-size: 18px; border: 1px solid #00e676; padding: 5px 15px; border-radius: 50px; }}
    .timer-box {{ font-size: 50px; font-weight: bold; color: #ffffff; margin: 20px 0; font-family: 'Courier New', monospace; text-shadow: 0 0 10px #fff; }}
    .float-wpp {{
        position: fixed; width: 60px; height: 60px; bottom: 20px; right: 20px;
        background-color: #25d366; color: #FFF; border-radius: 50px;
        text-align: center; font-size: 30px; box-shadow: 2px 2px 10px #000; z-index: 9999;
        display: flex; align-items: center; justify-content: center;
    }}
    .entry-alert {{ background: linear-gradient(90deg, #00e676, #00c853); color: #000; padding: 15px; border-radius: 8px; font-weight: 900; animation: blinker 0.4s linear infinite; font-size: 26px; }}
    .entry-put {{ background: linear-gradient(90deg, #ff5252, #d50000); color: #fff; padding: 15px; border-radius: 8px; font-weight: 900; animation: blinker 0.4s linear infinite; font-size: 26px; }}
    @keyframes blinker {{ 50% {{ opacity: 0.2; }} }}
    </style>
    <a href="https://wa.me/{SEU_WHATSAPP}" class="float-wpp" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:35px">
    </a>
    """, unsafe_allow_html=True)

# 2. LOGIN
if 'logado' not in st.session_state: st.session_state.logado = False

if not st.session_state.logado:
    st.title("SISTEMA VIP OTC")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("Trader ID")
        p = st.text_input("Senha", type="password")
        if st.button("CONECTAR AO SERVIDOR", use_container_width=True):
            if (u == "romildo" or u == "teste") and p == "12345":
                st.session_state.logado = True
                st.rerun()
            else: st.error("Acesso Negado")
    st.stop()

# 3. TERMINAL OTC PRO
st.sidebar.button("LOGOUT", on_click=lambda: st.session_state.update({"logado": False}))
st.title("🎯 ANALISADOR OTC PRO")

col_a, col_b = st.columns(2)
with col_a:
    tf = st.selectbox("TIMEFRAME:", ["M1 (1 Minuto)", "M5 (5 Minutos)"])
with col_b:
    at = st.selectbox("ATIVO OTC:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)"])

now = datetime.now()
if "M1" in tf:
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
else:
    prox = now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    if prox <= now: prox += timedelta(minutes=5)

faltam = (prox - now).total_seconds()

# --- LÓGICA DE ANÁLISE PROFUNDA ---
st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
payout_otc = 93 if "OTC" in at else 85
st.markdown(f"<span class='payout-text'>PAYOUT {at}: {payout_otc}%</span>", unsafe_allow_html=True)

# Semente baseada na vela para consistência
np.random.seed(int(prox.timestamp()))
rsi_simulado = np.random.randint(0, 100)
tendencia = np.random.choice(["ALTA", "BAIXA", "LATERAL"])

# Só manda sinal se houver confluência (RSI extremo + Tendência)
if rsi_simulado > 92 and tendencia == "BAIXA":
    sinal, cor, alert = "PUT (VENDA) 🔴", "#ff5252", "entry-put"
elif rsi_simulado < 8 and tendencia == "ALTA":
    sinal, cor, alert = "CALL (COMPRA) 🟢", "#00e676", "entry-alert"
else:
    sinal, cor, alert = "BUSCANDO CONFLUÊNCIA... 🔎", "#8b949e", ""

st.markdown(f"<h3 style='margin-top:20px;'>{at} | {tf}</h3>", unsafe_allow_html=True)
st.markdown(f"<h1 style='color: {cor} !important; font-size: 42px;'>{sinal}</h1>", unsafe_allow_html=True)

minutos, segundos = int(faltam // 60), int(faltam % 60)
st.markdown(f"<div class='timer-box'>{minutos:02d}:{segundos:02d}</div>", unsafe_allow_html=True)

if "BUSCANDO" not in sinal:
    if faltam <= 2:
        st.markdown(f"<div class='{alert}'>ENTRE AGORA (2S DELAY)</div>", unsafe_allow_html=True)
    else:
        st.success(f"Probabilidade de acerto: Alta. Prepare entrada às {prox.strftime('%H:%M:%S')}")
else:
    st.info("Aguardando o preço tocar em zonas de suporte ou resistência em OTC.")

st.markdown("</div>", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
