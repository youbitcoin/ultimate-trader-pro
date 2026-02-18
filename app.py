import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime, timedelta

# =========================================================
# 1. CONFIGURAÇÕES E CSS
# =========================================================
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Estilo Visual e Botão Flutuante
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: #e6edf3; }}
    h1, h2, h3 {{ color: #00e676 !important; text-align: center; }}
    .signal-card {{ 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 10px; padding: 25px; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .timer-box {{ font-size: 40px; font-weight: bold; color: #ffffff; margin: 15px 0; font-family: 'monospace'; }}
    
    .float-wpp {{
        position: fixed; width: 60px; height: 60px; bottom: 20px; right: 20px;
        background-color: #25d366; color: #FFF; border-radius: 50px;
        text-align: center; font-size: 30px; box-shadow: 2px 2px 3px #999;
        z-index: 9999; display: flex; align-items: center; justify-content: center; text-decoration: none;
    }}
    
    .entry-now {{ background-color: #00e676; color: #0d1117; padding: 15px; border-radius: 5px; font-weight: 900; animation: blinker 0.6s linear infinite; font-size: 24px; }}
    .entry-put {{ background-color: #ff5252; color: #ffffff; padding: 15px; border-radius: 5px; font-weight: 900; animation: blinker 0.6s linear infinite; font-size: 24px; }}
    @keyframes blinker {{ 50% {{ opacity: 0.2; }} }}
    </style>
    <a href="https://wa.me/{SEU_WHATSAPP}" class="float-wpp" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:35px">
    </a>
    """, unsafe_allow_html=True)

# Inicialização do Estado
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_nome' not in st.session_state:
    st.session_state.usuario_nome = ""

def verificar_acesso():
    try:
        match = re.search(r"/d/([\w-]+)", LINK_PLANILHA)
        SHEET_ID = match.group(1)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
        df = pd.read_csv(url)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame({'usuario': ['teste', 'romildo'], 'senha': ['12345', '12345']})

# =========================================================
# 2. LÓGICA DE TELAS
# =========================================================

# Se NÃO estiver logado, mostra APENAS o login
if not st.session_state.logado:
    st.title("ULTIMATE TRADER LOGIN")
    df_users = verificar_acesso()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.write("---")
        u_input = st.text_input("Usuário / ID", key="user_box")
        p_input = st.text_input("Senha", type="password", key="pass_box")
        
        if st.button("LOGIN", use_container_width=True):
            user_match = df_users[df_users['usuario'].astype(str).str.lower() == str(u_input).lower()]
            if not user_match.empty and str(user_match.iloc[0]['senha']) == str(p_input):
                st.session_state.logado = True
                st.session_state.usuario_nome = u_input
                st.rerun()
            else:
                st.error("Dados incorretos.")
    # Interrompe o script aqui para o terminal não carregar embaixo
    st.stop()

# Se chegou aqui, é porque está logado. Mostra APENAS o terminal.
else:
    st.sidebar.title("MENU")
    st.sidebar.write(f"Trader: {st.session_state.usuario_nome}")
    if st.sidebar.button("SAIR"):
        st.session_state.logado = False
        st.rerun()

    st.title("TERMINAL PRO QUOTEX")

    c1, c2 = st.columns(2)
    with c1:
        tf = st.selectbox("TIMEFRAME:", ["M1 (1 Minuto)", "M5 (5 Minutos)"], key="time_sel")
    with c2:
        par = st.selectbox("PAR DE MOEDAS:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BTC/USD"], key="pair_sel")

    now = datetime.now()
    if "M1" in tf:
        prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        payout = 91
    else:
        prox = now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
        if prox <= now: prox += timedelta(minutes=5)
        payout = 89

    faltam = (prox - now).total_seconds()

    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#00e676; font-weight:bold;'>PAYOUT: {payout}%</span>", unsafe_allow_html=True)
    
    np.random.seed(int(prox.timestamp()))
    analise = np.random.randint(0, 100)
    
    if analise > 85:
        sinal, cor, alert_class = "PUT (VENDA) 🔴", "#ff5252", "entry-put"
    elif analise < 15:
        sinal, cor, alert_class = "CALL (COMPRA) 🟢", "#00e676", "entry-now"
    else:
        sinal, cor, alert_class = "ANALISANDO... 🔎", "#8b949e", ""

    st.markdown(f"<h3>{par}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: {cor} !important; font-size: 38px;'>{sinal}</h1>", unsafe_allow_html=True)

    if "ANALISANDO" not in sinal:
        st.markdown(f"<div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>", unsafe_allow_html=True)
        if 2 < faltam <= 10:
            st.warning("PREPARE A ENTRADA")
        elif faltam <= 2:
            st.markdown(f"<div class='{alert_class}'>CLIQUE AGORA!</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
st.rerun()
    time.sleep(1)
