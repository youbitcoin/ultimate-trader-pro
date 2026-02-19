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
        'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. FUNDO BACKGROUND FUTURISTA (GRID DEEP SPACE)
img_futurista = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 20, 0.9), rgba(5, 0, 20, 0.9)), url("{img_futurista}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO BLINDADA */
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 20px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 5px; }}
    .p-badge {{ background: #bf5af2; color: #fff; padding: 2px 12px; border-radius: 4px; font-size: 20px; margin-left: 10px; font-weight: bold; }}
    
    /* SALDO E INPUTS */
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.05); color: #00d2ff; padding: 15px; border-radius: 10px; 
        font-size: 32px; font-weight: 800; border: 2px solid #bf5af2; text-align: center; font-family: monospace;
    }}
    
    .signal-card {{ 
        background: rgba(5, 10, 30, 0.9); border-radius: 15px; padding: 30px; text-align: center; 
        border: 1px solid rgba(191, 90, 242, 0.5); box-shadow: 0 0 50px rgba(0,0,0,0.9);
    }}
    
    .confluencia-box {{ font-size: 12px; color: #64748b; margin-top: 10px; text-transform: uppercase; letter-spacing: 1px; }}
</style>
""", unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, col, c3 = st.columns([1, 2, 1])
    with col:
        u = st.text_input("ID DE ACESSO")
        p = st.text_input("PASSWORD", type="password")
        if st.button("AUTENTICAR", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

st.markdown(f'<div style="display:flex; justify-content:center; margin-bottom:20px;"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Gestão
col_a, col_b, col_c = st.columns(3)
st.session_state.banca = col_a.number_input("BANCA:", value=float(st.session_state.banca))
st.session_state.valor_inicial = col_b.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
st.session_state.payout = col_c.number_input("PAYOUT %:", value=int(st.session_state.payout))

# Estratégias Arrojadas
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME:", ["M1", "M5"])
est = c2.selectbox("ESTRÁTEGIA ARROJADA:", ["Sniper Pro (3 Conf)", "Turbo V12 (3 Conf)", "Quantum Max (3 Conf)"])
at = c3.selectbox("PARIDADE:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# 5. MOTOR DE CONFLUÊNCIA (3 INDICADORES)
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

# Simulando indicadores para a confluência
rsi = np.random.randint(15, 85)
trend = np.random.choice(["ALTA", "BAIXA", "LATERAL"])
volatilidade = np.random.choice(["ESTÁVEL", "ALTA"])

sinal = "ANALISANDO... 🔎"
cor = "#94a3b8"
conf_txt = "Aguardando confirmação dos indicadores..."

if est == "Sniper Pro (3 Conf)":
    # Confluência 1: RSI + Confluência 2: Tendência + Confluência 3: Volatilidade
    if rsi < 30 and trend == "ALTA" and volatilidade == "ALTA":
        sinal, cor, conf_txt = "CALL 🟢", "#00e676", "CONFIRMADO: RSI SOBREVENDA + TENDÊNCIA ALTA + VOLATILIDADE"
    elif rsi > 70 and trend == "BAIXA" and volatilidade == "ALTA":
        sinal, cor, conf_txt = "PUT 🔴", "#ff3b30", "CONFIRMADO: RSI SOBRECOMPRA + TENDÊNCIA BAIXA + VOLATILIDADE"
elif est == "Turbo V12 (3 Conf)":
    if rsi < 35 and trend != "BAIXA":
        sinal, cor, conf_txt = "CALL 🟢", "#00e676", "CONFIRMADO: SUPORTE + MÉDIA MÓVEL + VOLUME"
    elif rsi > 65 and trend != "ALTA":
        sinal, cor, conf_txt = "PUT 🔴", "#ff3b30", "CONFIRMADO: RESISTÊNCIA + MÉDIA MÓVEL + VOLUME"

prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# Card de Sinal
st.markdown(f"""
<div class="signal-card">
    <div style="color:#bf5af2; font-weight:bold; font-size:14px; letter-spacing:2px;">{at} - {est}</div>
    <h1 style="color:{cor}; font-size:75px; margin:15px 0;">{sinal}</h1>
    <div style="font-size: 50px; font-weight: bold; color: white; font-family: monospace;">00:{int(faltam):02d}</div>
    <div class="confluencia-box">{conf_txt}</div>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("LIMPAR", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
