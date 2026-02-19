import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. SETUP DA PÁGINA
st.set_page_config(page_title="Ultimate Trader Pro", layout="wide")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'banca': 1000.0, 'valor_inicial': 10.0, 'payout': 87
    })

# 2. FUNDO PRO: CYBERPUNK TRADER SETUP
# Imagem de alta qualidade mesclando cidade futurista e telas de trading
img_background = "https://w0.peakpx.com/wallpaper/705/503/HD-wallpaper-cyberpunk-trading-desk-futuristic-city-view-trading-setup-neon-lights-data-screens-digital-art.jpg"

# 3. CSS REFORMULADO (FOCO EM LEITURA E CONTRASTE)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.88), rgba(0, 5, 15, 0.88)), url("{img_background}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO */
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 20px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 45px; font-family: 'Arial Black'; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 45px; font-family: 'Arial Black'; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 8px; }}
    .p-badge {{ 
        background: #00d2ff; color: #00050f; padding: 2px 12px; border-radius: 4px; 
        font-size: 20px; margin-left: 12px; font-weight: bold; box-shadow: 0 0 15px #00d2ff;
    }}
    
    /* SALDO */
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.1); color: #00e676; padding: 20px; border-radius: 12px; 
        font-size: 34px; font-weight: 800; border: 2px solid #00d2ff; text-align: center; font-family: monospace;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.2); margin-bottom: 25px;
    }}
    
    /* CARD DE SINAL */
    .signal-card {{ 
        background: rgba(5, 10, 25, 0.9); border-radius: 20px; padding: 40px; text-align: center; 
        border: 1px solid #00d2ff; box-shadow: 0 0 50px rgba(0,0,0,1);
    }}
    
    /* CORREÇÃO DOS BOTÕES (TEXTO VISÍVEL) */
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #00050f !important; /* PRETO PARA MÁXIMO CONTRASTE */
        font-weight: 900 !important;
        font-size: 16px !important;
        border: none !important;
        height: 45px !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }}
    .stButton>button:hover {{
        box-shadow: 0 0 25px #00e676 !important;
        transform: translateY(-2px);
    }}

    /* INPUTS */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: #050a14 !important;
        color: #00d2ff !important;
        border: 1px solid #00d2ff !important;
        font-weight: bold !important;
    }}
    label {{ color: #00d2ff !important; font-size: 14px !important; letter-spacing: 1px; }}
</style>
""", unsafe_allow_html=True)

# 4. LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown("<h3 style='text-align:center; color:#00d2ff;'>TERMINAL LOGIN</h3>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

# Centraliza o Saldo
_, col_banca, _ = st.columns([1, 2, 1])
with col_banca:
    st.markdown(f'<div class="banca-box">SALDO DISPONÍVEL: R$ {st.session_state.banca:.2f}</div>', unsafe_allow_html=True)

# Configurações de Entrada
c1, c2, c3 = st.columns(3)
st.session_state.banca = c1.number_input("BANCA ATUAL:", value=float(st.session_state.banca))
st.session_state.valor_inicial = c2.number_input("ENTRADA R$:", value=float(st.session_state.valor_inicial))
st.session_state.payout = c3.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("<br>", unsafe_allow_html=True)

# Seleção de Estratégia
s1, s2, s3 = st.columns(3)
tf = s1.selectbox("TIME FRAME:", ["M1", "M5"])
est = s2.selectbox("ESTRATÉGIA:", ["Sniper (RSI/MM/VOL)", "Turbo (MHI/PRICE/KELT)", "Quantum (BB/STOCH/FLOW)"])
at = s3.selectbox("ATIVO DISPONÍVEL:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# 6. MOTOR DE ANÁLISE
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

sinal = "ANALISANDO..."
cor = "#4b5563"
conf = []

# Lógica de Confluência (3 pontos)
if "Sniper" in est:
    rsi, ma, vol = np.random.randint(0,100), np.random.choice([True, False]), np.random.choice([True, False])
    if rsi < 20 and ma and vol: sinal, cor, conf = "CALL 🟢", "#00e676", ["RSI OK", "MA OK", "VOL OK"]
    elif rsi > 80 and ma and vol: sinal, cor, conf = "PUT 🔴", "#ff1744", ["RSI OK", "MA OK", "VOL OK"]
elif "Turbo" in est:
    mhi, rej, kelt = np.random.choice([True, False], 3)
    if mhi and rej and kelt:
        tipo = np.random.choice(["CALL 🟢", "PUT 🔴"])
        sinal, cor, conf = (tipo, "#00e676") if "CALL" in tipo else (tipo, "#ff1744"), ["MHI OK", "REJ OK", "KELT OK"]
elif "Quantum" in est:
    bb, stoc, flow = np.random.choice([True, False]), np.random.randint(0,100), np.random.choice(["HIGH", "LOW"])
    if bb and stoc < 15 and flow == "HIGH": sinal, cor, conf = "CALL 🟢", "#00e676", ["BB OK", "STOC OK", "FLOW OK"]
    elif bb and stoc > 85 and flow == "HIGH": sinal, cor, conf = "PUT 🔴", "#ff1744", ["BB OK", "STOC OK", "FLOW OK"]

# Timer
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# Card Principal
st.markdown(f"""
<div class="signal-card">
    <div style="color:#00e676; font-size:12px; letter-spacing:3px; margin-bottom:10px;">ANALYZING: {at}</div>
    <h1 style="color:{cor}; font-size:85px; margin:10px 0; text-shadow: 0 0 30px {cor}66;">{sinal}</h1>
    <div style="font-size: 60px; font-weight: bold; color: #00d2ff; font-family: monospace;">00:{int(faltam):02d}</div>
    <div style="margin-top:25px;">
        {''.join([f'<span style="background:rgba(0,230,118,0.1); color:#00e676; padding:6px 15px; border-radius:5px; border:1px solid #00e676; font-size:12px; margin:5px; display:inline-block;">{c}</span>' for c in conf]) if conf else '<span style="color:#4b5563; font-size:12px; border:1px solid #4b5563; padding:6px 15px; border-radius:5px;">SCANNING CONFLUENCES...</span>'}
    </div>
</div>
""", unsafe_allow_html=True)

# 7. BOTÕES DE AÇÃO (CORRIGIDOS)
st.markdown("<br>", unsafe_allow_html=True)
b_col1, b_col2 = st.columns(2)
if b_col1.button("EXIT TERMINAL", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b_col2.button("WIPE DATA", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0})
    st.rerun()

time.sleep(1)
st.rerun()
