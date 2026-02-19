import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. BACKGROUND FUTURISTA (AZUL E VERDE NEON - SEM PESSOAS)
img_background = "https://img.freepik.com/fotos-premium/fundo-de-tecnologia-futurista-com-neons-azuis-e-verdes-setup-trader-vazio_172276-415.jpg?w=1380"

# 3. CSS CUSTOMIZADO (PALETA AZUL & VERDE NEON)
st.markdown(f"""
<style>
    /* FUNDO PRINCIPAL */
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.9), rgba(0, 5, 15, 0.9)), url("{img_background}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO OFICIAL */
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 15px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 40px; font-family: 'Arial Black'; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 40px; font-family: 'Arial Black'; font-weight: 900; text-shadow: 0 0 15px #00e676; margin-left: 5px; }}
    .p-badge {{ 
        background: #00d2ff; color: #000; padding: 2px 10px; border-radius: 4px; 
        font-size: 18px; margin-left: 10px; font-weight: bold; box-shadow: 0 0 10px #00d2ff;
    }}
    
    /* CAIXA DE SALDO (CYBER BLUE) */
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.05); color: #00e676; padding: 15px; border-radius: 10px; 
        font-size: 30px; font-weight: 800; border: 2px solid #00d2ff; text-align: center; font-family: monospace;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
    }}
    
    /* CARD DE SINAL (HIGH PRECISION) */
    .signal-card {{ 
        background: rgba(5, 10, 20, 0.95); border-radius: 15px; padding: 30px; text-align: center; 
        border: 1px solid #00d2ff; box-shadow: 0 0 40px rgba(0, 210, 255, 0.2);
    }}
    
    /* TAGS DE CONFLUÊNCIA VERDE NEON */
    .conf-tag {{ 
        background: rgba(0, 230, 118, 0.1); color: #00e676; padding: 5px 12px; 
        border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; margin: 3px;
        border: 1px solid #00e676; text-transform: uppercase;
    }}
    
    /* INPUTS E BOTÕES */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #050a14 !important;
        color: #00d2ff !important;
        border: 1px solid #00d2ff !important;
    }}
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000 !important; font-weight: bold !important; border: none !important;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 15px #00e676 !important;
    }}
    
    label, p {{ color: #00d2ff !important; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# 4. SISTEMA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, col, c3 = st.columns([1, 2, 1])
    with col:
        st.markdown("<h4 style='text-align:center; color:#00d2ff; letter-spacing:3px;'>SYSTEM ACCESS</h4>", unsafe_allow_html=True)
        u = st.text_input("USER ID")
        p = st.text_input("ACCESS KEY", type="password")
        if st.button("INITIALIZE TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD (LOGADO)
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

st.markdown(f'<div style="display:flex; justify-content:center; margin-bottom:20px;"><div class="banca-box">OPERACIONAL: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# GESTÃO
ca, cb, cc = st.columns(3)
st.session_state.banca = ca.number_input("BANCA:", value=float(st.session_state.banca))
st.session_state.valor_inicial = cb.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
st.session_state.payout = cc.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("<br>", unsafe_allow_html=True)

# CONFIGURAÇÃO DE TESTE (ESTRATÉGIAS DIFERENTES)
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME FRAME:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA:", [
    "Sniper (RSI/MM/VOL)", 
    "Turbo (MHI/PRICE/KELT)", 
    "Quantum (BB/STOCH/FLOW)"
])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# 6. MOTOR DE CONFLUÊNCIA (3 INDICADORES POR ESTRATÉGIA)
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

sinal = "ANALISANDO..."
cor_sinal = "#4b5563"
confluencias = []

# Lógica de Teste
if "Sniper" in est:
    # 3 Confluências: RSI Extremo + Médias Móveis + Volume
    rsi = np.random.randint(0, 100)
    ma_cross = np.random.choice([True, False])
    vol = np.random.choice([True, False])
    if rsi < 20 and ma_cross and vol:
        sinal, cor_sinal, confluencias = "CALL 🟢", "#00e676", ["RSI OVERSOLD", "MA CROSS UP", "VOLUME SPIKE"]
    elif rsi > 80 and ma_cross and vol:
        sinal, cor_sinal, confluencias = "PUT 🔴", "#ff1744", ["RSI OVERBOUGHT", "MA CROSS DOWN", "VOLUME SPIKE"]

elif "Turbo" in est:
    # 3 Confluências: MHI Probabilística + Price Rejection + Keltner Break
    mhi = np.random.choice([True, False])
    rejection = np.random.choice([True, False])
    break_channel = np.random.choice([True, False])
    if mhi and rejection and break_channel:
        tipo = np.random.choice(["CALL 🟢", "PUT 🔴"])
        sinal, cor_sinal = (tipo, "#00e676") if "CALL" in tipo else (tipo, "#ff1744")
        confluencias = ["MHI PATTERN", "PRICE REJECTION", "KELTNER BREAKOUT"]

elif "Quantum" in est:
    # 3 Confluências: Bollinger Touch + Stochastic + Order Flow
    bb_touch = np.random.choice([True, False])
    stoch = np.random.randint(0, 100)
    flow = np.random.choice(["STRONG", "WEAK"])
    if bb_touch and stoch < 15 and flow == "STRONG":
        sinal, cor_sinal, confluencias = "CALL 🟢", "#00e676", ["BB LOWER TOUCH", "STOCH LOW", "FLOW BUY"]
    elif bb_touch and stoch > 85 and flow == "STRONG":
        sinal, cor_sinal, confluencias = "PUT 🔴", "#ff1744", ["BB UPPER TOUCH", "STOCH HIGH", "FLOW SELL"]

# Timer
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# 7. CARD DE SINAL (UI)
st.markdown(f"""
<div class="signal-card">
    <div style="color:#00e676; font-size:12px; letter-spacing:2px; margin-bottom:10px;">PROBABILITY UNIT: {at}</div>
    <h1 style="color:{cor_sinal}; font-size:80px; margin:15px 0; text-shadow: 0 0 30px {cor_sinal}66;">{sinal}</h1>
    <div style="font-size: 55px; font-weight: bold; color: #00d2ff; font-family: monospace;">00:{int(faltam):02d}</div>
    <div style="margin-top:20px;">
        {''.join([f'<span class="conf-tag">{c}</span>' for c in confluencias]) if confluencias else '<span class="conf-tag" style="border-color:#4b5563; color:#4b5563;">SCANNING CONFLUENCES...</span>'}
    </div>
</div>
""", unsafe_allow_html=True)

# 8. AÇÕES
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("EXIT TERMINAL", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("WIPE DATA", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0})
    st.rerun()

time.sleep(1)
st.rerun()
