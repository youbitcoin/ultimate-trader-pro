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

# 2. FUNDOS CYBERPINK VIBRANTES
img_login = "https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070&auto=format&fit=crop" # Roxo & Azul Hi-tech
img_dash = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2070&auto=format&fit=crop" # Abstrato Cyber Dark

bg_url = img_login if not st.session_state.logado else img_dash

# 3. CSS CUSTOMIZADO (PALETA ROXO + AZUL)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(10, 0, 20, 0.85), rgba(0, 5, 20, 0.85)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO OFICIAL */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
    }}
    .u-text {{ color: #FFFFFF; font-size: 40px; font-family: 'Arial Black', sans-serif; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 40px; font-family: 'Arial Black', sans-serif; font-weight: 900; text-shadow: 0 0 15px #00e676; margin-left: 5px; }}
    .p-badge {{ 
        background: #bf5af2; color: #fff; padding: 2px 10px; border-radius: 6px; 
        font-size: 18px; margin-left: 10px; font-weight: bold; box-shadow: 0 0 10px #bf5af2;
    }}
    
    /* SALDO CENTRALIZADO (ROXO + AZUL) */
    .banca-wrapper {{ display: flex; justify-content: center; margin: 20px 0; }}
    .banca-box {{ 
        background: rgba(191, 90, 242, 0.1); 
        color: #00d2ff; 
        padding: 15px 60px; 
        border-radius: 4px; 
        font-size: 28px; 
        font-weight: bold; 
        border-left: 5px solid #bf5af2;
        border-right: 5px solid #00d2ff;
        box-shadow: 0 0 30px rgba(191, 90, 242, 0.2);
    }}
    
    /* CARDS E INPUTS */
    .signal-card {{ 
        background: rgba(15, 0, 30, 0.9); 
        border-radius: 15px; 
        padding: 30px; 
        text-align: center; 
        border: 1px solid #bf5af2;
        box-shadow: 0 0 40px rgba(191, 90, 242, 0.1);
    }}
    
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #0a0014 !important;
        color: #00d2ff !important;
        border: 1px solid #bf5af2 !important;
    }}

    .timer {{ font-size: 55px; font-weight: bold; color: #fff; font-family: 'Courier New', monospace; text-shadow: 0 0 10px #bf5af2; }}
    
    /* BOTÕES */
    .stButton>button {{
        background: linear-gradient(45deg, #bf5af2, #5e5ce6);
        color: white;
        border: none;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 20px #bf5af2;
        transform: scale(1.02);
    }}
</style>
""", unsafe_allow_html=True)

# 4. LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div style='text-align:center; color:#bf5af2; margin-bottom:10px;'>CYBERNETIC ACCESS PORTAL</div>", unsafe_allow_html=True)
        u = st.text_input("USER ID")
        p = st.text_input("ENCRYPTED KEY", type="password")
        if st.button("INITIALIZE INTERFACE", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# GESTÃO
with st.container():
    col_a, col_b, col_c = st.columns(3)
    st.session_state.banca = col_a.number_input("BANCA:", value=float(st.session_state.banca))
    st.session_state.valor_inicial = col_b.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
    st.session_state.payout = col_c.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("<hr style='border-color: #bf5af2;'>", unsafe_allow_html=True)

# MERCADO
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA:", ["Sniper V2", "Turbo Purple", "Quantum Blue"])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# ANÁLISE
seed = int(datetime.now().timestamp() / 60)
np.random.seed(seed)
res = np.random.randint(0, 100)
if res > 80: sinal, cor = "PUT 🔴", "#ff3b30"
elif res < 20: sinal, cor = "CALL 🟢", "#00e676"
else: sinal, cor = "ANALISANDO... 🔎", "#00d2ff"

now = datetime.now()
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

st.markdown(f"""
<div class="signal-card">
    <div style="color:#bf5af2; font-size:14px; letter-spacing:2px;">CYBERPINK ENGINE ACTIVE</div>
    <h1 style="color:{cor}; font-size:70px; margin:20px 0;">{sinal}</h1>
    <div class="timer">00:{int(faltam):02d}</div>
</div>
""", unsafe_allow_html=True)

# AÇÕES
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("RESET", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
