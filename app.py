import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. SETUP DA PÁGINA
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'aguardando': False, 'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. FUNDOS DE TRADING (GRÁFICOS E CANDLES)
# Login: Gráficos de alta tecnologia
img_login = "https://images.unsplash.com/photo-1611974717482-480928d19c4a?q=80&w=2070&auto=format&fit=crop" 
# Dashboard: Interface de trading dark com candles
img_dash = "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=2070&auto=format&fit=crop"

bg_url = img_login if not st.session_state.logado else img_dash

# 3. CSS "MASTER TRADER" (ROXO + AZUL + GRÁFICOS)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(10, 0, 30, 0.9), rgba(0, 5, 25, 0.92)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO BLINDADA */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
    }}
    .u-text {{ color: #FFFFFF; font-size: 42px; font-family: 'Arial Black', sans-serif; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 42px; font-family: 'Arial Black', sans-serif; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 5px; }}
    .p-badge {{ 
        background: #bf5af2; color: #fff; padding: 2px 12px; border-radius: 4px; 
        font-size: 20px; margin-left: 10px; font-weight: bold; box-shadow: 0 0 15px #bf5af2;
    }}
    
    /* SALDO EM MODO TERMINAL */
    .banca-wrapper {{ display: flex; justify-content: center; margin: 25px 0; }}
    .banca-box {{ 
        background: rgba(15, 0, 30, 0.8); 
        color: #00d2ff; 
        padding: 15px 70px; 
        border-radius: 10px; 
        font-size: 32px; 
        font-weight: 800; 
        border: 2px solid #bf5af2;
        box-shadow: 0 0 25px rgba(191, 90, 242, 0.4);
        text-align: center;
        font-family: 'Courier New', monospace;
    }}
    
    /* CARDS DE TRADING */
    .signal-card {{ 
        background: rgba(10, 15, 30, 0.95); 
        border-radius: 8px; 
        padding: 30px; 
        text-align: center; 
        border-top: 4px solid #00d2ff;
        border-bottom: 4px solid #bf5af2;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
    }}
    
    .timer-text {{ 
        font-size: 60px; 
        font-weight: bold; 
        color: #ffffff; 
        font-family: monospace; 
        letter-spacing: 5px;
    }}
    
    /* INPUTS ESTILO BLOOMBERG */
    .stNumberInput input {{
        background-color: #050510 !important;
        color: #00d2ff !important;
        border: 1px solid #bf5af2 !important;
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #5e5ce6, #bf5af2) !important;
        border: none !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 4px !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, col_login, c3 = st.columns([1, 2, 1])
    with col_login:
        st.markdown("<h4 style='text-align:center; color:#00d2ff;'>TRADING TERMINAL ACCESS</h4>", unsafe_allow_html=True)
        u = st.text_input("USER ID")
        p = st.text_input("PASSKEY", type="password")
        if st.button("CONNECT TO MARKET", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD OPERACIONAL
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Saldo Principal
st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Painel de Gestão (Banca, Entrada, Payout)
with st.container():
    col_a, col_b, col_c = st.columns(3)
    st.session_state.banca = col_a.number_input("BANCA:", value=float(st.session_state.banca))
    st.session_state.valor_inicial = col_b.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
    st.session_state.payout = col_c.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("<br>", unsafe_allow_html=True)

# Parâmetros de Mercado
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA:", ["Price Action", "Fibonacci Quantum", "MHI High"])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# Lógica de Sinal (Probabilidade)
seed = int(datetime.now().timestamp() / 60)
np.random.seed(seed)
res = np.random.randint(0, 100)
if res > 80: sinal, cor = "PUT 🔴", "#ff3b30"
elif res < 20: sinal, cor = "CALL 🟢", "#00e676"
else: sinal, cor = "ANALISANDO... 🔎", "#00d2ff"

now = datetime.now()
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# Card Principal de Sinal
st.markdown(f"""
<div class="signal-card">
    <div style="color:#00d2ff; font-weight:bold; letter-spacing:2px; margin-bottom:10px;">MARKET ANALYSIS: {at}</div>
    <h1 style="color:{cor}; font-size:80px; margin:10px 0; text-shadow: 0 0 30px {cor}66;">{sinal}</h1>
    <div class="timer-text">00:{int(faltam):02d}</div>
</div>
""", unsafe_allow_html=True)

# Botões Finais
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("WIPE HISTORY", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
