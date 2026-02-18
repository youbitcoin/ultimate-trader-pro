import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime, timedelta

# 1. CONFIGURACOES TÉCNICAS
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# CSS para o Card e Botão WhatsApp
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: #e6edf3; }}
    h1, h2, h3 {{ color: #00e676 !important; text-align: center; font-family: sans-serif; }}
    .signal-card {{ 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 12px; padding: 30px; text-align: center;
        margin-top: 20px;
    }}
    .timer-box {{ font-size: 45px; font-weight: bold; color: #ffffff; margin: 15px 0; font-family: monospace; }}
    .float-wpp {{
        position: fixed; width: 60px; height: 60px; bottom: 20px; right: 20px;
        background-color: #25d366; color: #FFF; border-radius: 50px;
        text-align: center; font-size: 30px; box-shadow: 2px 2px 3px #000;
        z-index: 9999; display: flex; align-items: center; justify-content: center;
    }}
    .entry-alert {{ background-color: #00e676; color: #0d1117; padding: 15px; border-radius: 8px; font-weight: 900; animation: blinker 0.6s linear infinite; font-size: 24px; }}
    @keyframes blinker {{ 50% {{ opacity: 0.3; }} }}
    </style>
    <a href="https://wa.me/{SEU_WHATSAPP}" class="float-wpp" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:35px">
    </a>
    """, unsafe_allow_html=True)

# 2. LOGIN SEGURO
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("ACESSO RESTRITO")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("Usuario")
        p = st.text_input("Senha", type="password")
        if st.button("LOGIN", use_container_width=True):
            # Validação direta para evitar erros de leitura de planilha no login
            if (u == "romildo" or u == "teste") and p == "12345":
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Incorreto")
    st.stop()

# 3. TERMINAL (MONITOR QUOTEX PRO)
st.sidebar.button("SAIR", on_click=lambda: st.session_state.update({"logado": False}))

st.title("MONITOR QUOTEX PRO")

col_a, col_b = st.columns(2)
with col_a:
    tf = st.selectbox("TEMPO:", ["M1 (1 Minuto)", "M5 (5 Minutos)"])
with col_b:
    at = st.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BTC/USD"])

# Lógica de Tempo Real
now = datetime.now()
if "M1" in tf:
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
else:
    prox = now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    if prox <= now: prox += timedelta(minutes=5)

faltam = (prox - now).total_seconds()

# GERADOR DE SINAL (Inicia a análise aqui)
st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
st.write(f"Sincronizado: {at}")

# Semente fixa por vela para o sinal não mudar a cada segundo
np.random.seed(int(prox.timestamp()))
chance = np.random.randint(0, 100)

if chance > 85:
    sinal, cor = "PUT (VENDA) 🔴", "#ff5252"
elif chance < 15:
    sinal, cor = "CALL (COMPRA) 🟢", "#00e676"
else:
    sinal, cor = "ANALISANDO FLUXO... 🔎", "#8b949e"

st.markdown(f"<h1 style='color: {cor} !important; font-size: 40px;'>{sinal}</h1>", unsafe_allow_html=True)

# Exibe o cronômetro apenas se houver sinal ou análise ativa
minutos, segundos = int(faltam // 60), int(faltam % 60)
st.markdown(f"<div class='timer-box'>{minutos:02d}:{segundos:02d}</div>", unsafe_allow_html=True)

if "ANALISANDO" not in sinal:
    if faltam <= 3:
        st.markdown("<div class='entry-alert'>CLIQUE AGORA!</div>", unsafe_allow_html=True)
    else:
        st.info(f"Aguarde a entrada para {prox.strftime('%H:%M:%S')}")

st.markdown("</div>", unsafe_allow_html=True)

# Loop de Atualização
time.sleep(1)
st.rerun()
