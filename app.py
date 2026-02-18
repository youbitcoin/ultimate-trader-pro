import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime, timedelta

# 1. CONFIGURACOES E ESTILO
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# CSS para limpeza de interface e Botao WhatsApp
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: #e6edf3; }}
    h1, h2, h3 {{ color: #00e676 !important; text-align: center; }}
    .signal-card {{ 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 10px; padding: 25px; text-align: center;
    }}
    .timer-box {{ font-size: 40px; font-weight: bold; color: #ffffff; margin: 15px 0; font-family: 'monospace'; }}
    .float-wpp {{
        position: fixed; width: 60px; height: 60px; bottom: 20px; right: 20px;
        background-color: #25d366; color: #FFF; border-radius: 50px;
        text-align: center; font-size: 30px; box-shadow: 2px 2px 3px #999;
        z-index: 9999; display: flex; align-items: center; justify-content: center; text-decoration: none;
    }}
    .entry-now {{ background-color: #00e676; color: #0d1117; padding: 15px; border-radius: 5px; font-weight: 900; animation: blinker 0.6s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0.2; }} }}
    </style>
    <a href="https://wa.me/{SEU_WHATSAPP}" class="float-wpp" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:35px">
    </a>
    """, unsafe_allow_html=True)

# 2. SISTEMA DE LOGIN
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'user' not in st.session_state:
    st.session_state.user = ""

def check_login():
    try:
        match = re.search(r"/d/([\w-]+)", LINK_PLANILHA)
        sid = match.group(1)
        url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv&gid=0"
        df = pd.read_csv(url)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame({'usuario': ['teste', 'romildo'], 'senha': ['12345', '12345']})

# TELA DE LOGIN
if not st.session_state.logado:
    st.title("ACESSO VIP")
    df_u = check_login()
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("Usuario / ID", key="main_u")
        p = st.text_input("Senha", type="password", key="main_p")
        if st.button("LOGIN", use_container_width=True):
            match = df_u[df_u['usuario'].astype(str).str.lower() == str(u).lower()]
            if not match.empty and str(match.iloc[0]['senha']) == str(p):
                st.session_state.logado = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Credenciais incorretas")
    st.stop()

# TELA DO TERMINAL (Apos Login)
else:
    st.sidebar.write(f"Trader: {st.session_state.user}")
    if st.sidebar.button("LOGOUT"):
        st.session_state.logado = False
        st.rerun()

    st.title("MONITOR QUOTEX PRO")
    
    col_a, col_b = st.columns(2)
    with col_a:
        tf = st.selectbox("TEMPO:", ["M1 (1 Minuto)", "M5 (5 Minutos)"], key="sel_tf")
    with col_b:
        at = st.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BTC/USD"], key="sel_at")

    now = datetime.now()
    if "M1" in tf:
        prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    else:
        prox = now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
        if prox <= now: prox
