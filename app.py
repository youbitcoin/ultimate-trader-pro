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

# 2. FUNDOS DE ALTA PERFORMANCE
# Login: Cidade Futurista / Dashboard: Digital Grid Hi-Tech
img_login = "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?q=80&w=1974&auto=format&fit=crop"
img_dash = "https://images.unsplash.com/photo-1510511459019-5dee224ffb8b?q=80&w=2070&auto=format&fit=crop"

bg_url = img_login if not st.session_state.logado else img_dash

# 3. CSS CUSTOMIZADO (LOGO BLINDADA + GRID FUTURISTA)
st.markdown(f"""
<style>
    /* FUNDO COM OVERLAY PARA LEITURA */
    .stApp {{
        background: linear-gradient(rgba(0, 8, 20, 0.85), rgba(0, 8, 20, 0.85)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO OFICIAL - FORMATO TRAVADO */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
        filter: drop-shadow(0 0 10px rgba(0, 230, 118, 0.3));
    }}
    .u-text {{ color: #FFFFFF; font-size: 40px; font-family: 'Arial Black', sans-serif; font-weight: 900; letter-spacing: -1px; }}
    .t-text {{ color: #00e676; font-size: 40px; font-family: 'Arial Black', sans-serif; font-weight: 900; letter-spacing: -1px; margin-left: 4px; }}
    .p-badge {{ 
        background: #00e676; color: #000; padding: 2px 10px; border-radius: 6px; 
        font-size: 18px; margin-left: 10px; font-family: sans-serif; font-weight: bold;
    }}
    
    /* SALDO CENTRALIZADO HI-TECH */
    .banca-wrapper {{ display: flex; justify-content: center; margin: 20px 0; }}
    .banca-box {{ 
        background: rgba(0, 230, 118, 0.1); 
        color: #00e676; 
        padding: 15px 60px; 
        border-radius: 4px; 
        font-size: 28px; 
        font-weight: bold; 
        border-left: 5px solid #00e676;
        border-right: 5px solid #00e676;
        box-shadow: 0 0 30px rgba(0,230,118,0.2);
    }}
    
    /* CARDS DE SINAIS */
    .signal-card {{ 
        background: rgba(13, 17, 23, 0.95); 
        border-radius: 15px; 
        padding: 30px; 
        text-align: center; 
        border: 1px solid rgba(0,230,118,0.4);
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
    }}
    
    .timer {{ font-size: 55px; font-weight: bold; color: #fff; font-family: 'Courier New', monospace; }}
    
    /* AJUSTE INPUTS */
    .stNumberInput input {{ background-color: #0d1117 !important; color: #00e676 !important; border: 1px solid #00e676 !important; }}
</style>
""", unsafe_allow_html=True)

# 4. SISTEMA DE ACESSO
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div style='text-align:center; color:#64748b; margin-bottom:10px;'>CYBERNETIC INTERFACE V2.0</div>", unsafe_allow_html=True)
        u = st.text_input("ID DE ACESSO")
        p = st.text_input("CHAVE CRIPTOGRÁFICA", type="password")
        if st.button("AUTENTICAR NO TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD OPERACIONAL
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Saldo em destaque
st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Painel de Gestão e Parâmetros
with st.container():
    col_a, col_b, col_c = st.columns(3)
    st.session_state.banca = col_a.number_input("BANCA ATUAL:", value=float(st.session_state.banca))
    st.session_state.valor_inicial = col_b.number_input("ENTRADA R$:", value=float(st.session_state.valor_inicial))
    st.session_state.payout = col_c.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("---")

# Seleção de Mercado
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME FRAME:", ["M1", "M5", "M15"])
est = c2.selectbox("ALGORITMO:", ["Sniper V2", "Turbo Neon", "Quantum"])
at = c3.selectbox("ATIVO DISPONÍVEL:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD", "ETH/USD"])

# Motor de Decisão
seed = int(datetime.now().timestamp() / 60)
np.random.seed(seed)
res = np.random.randint(0, 100)
if res > 82: sinal, cor = "PUT 🔴", "#ff5252"
elif res < 18: sinal, cor = "CALL 🟢", "#00e676"
else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

now = datetime.now()
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# Card de Sinal Futurista
st.markdown(f"""
<div class="signal-card">
    <div style="color:#64748b; font-size:14px; letter-spacing:3px;">SYSTEM ANALYSIS: {at}</div>
    <h1 style="color:{cor}; font-size:70px; margin:20px 0; text-shadow: 0 0 20px {cor}44;">{sinal}</h1>
    <div class="timer">00:{int(faltam):02d}</div>
</div>
""", unsafe_allow_html=True)

# Rodapé de Ações
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("ENCERRAR CONEXÃO", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("RESETAR TERMINAL", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
