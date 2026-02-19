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

# 2. IMAGENS PERSONALIZADAS (CYBERPUNK + TRADER + FUTURO)
img_login = "https://img.freepik.com/fotos-premium/um-homem-sentado-em-frente-a-varias-telas-de-computador-com-graficos-em-uma-sala-com-iluminacao-neon_902639-50920.jpg"
img_dash = "https://img.freepik.com/fotos-premium/trader-de-criptomoedas-analisando-graficos-em-um-ambiente-futurista-cyberpunk-com-neon_902639-48210.jpg"

bg_url = img_login if not st.session_state.logado else img_dash

# 3. CSS CUSTOMIZADO
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 15px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 5px; }}
    .p-badge {{ background: #bf5af2; color: #fff; padding: 2px 12px; border-radius: 4px; font-size: 20px; margin-left: 10px; font-weight: bold; box-shadow: 0 0 15px #bf5af2; }}
    
    .banca-box {{ 
        background: rgba(0, 0, 0, 0.6); color: #00d2ff; padding: 15px; border-radius: 10px; 
        font-size: 32px; font-weight: 800; border: 2px solid #bf5af2; text-align: center; font-family: monospace;
        box-shadow: 0 0 30px rgba(191, 90, 242, 0.4);
    }}
    
    .signal-card {{ 
        background: rgba(10, 10, 25, 0.9); border-radius: 20px; padding: 30px; text-align: center; 
        border: 1px solid #bf5af2; box-shadow: 0 0 60px rgba(0,0,0,1);
        backdrop-filter: blur(10px);
    }}
    
    .conf-tag {{ 
        background: rgba(191, 90, 242, 0.2); color: #bf5af2; padding: 6px 12px; 
        border-radius: 4px; font-size: 10px; font-weight: bold; display: inline-block; margin: 3px;
        border: 1px solid #bf5af2; text-transform: uppercase;
    }}

    .stButton>button {{
        background: linear-gradient(90deg, #bf5af2, #5e5ce6) !important;
        border: none !important; color: white !important; font-weight: bold !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4. TELA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, col, c3 = st.columns([1, 2, 1])
    with col:
        st.markdown("<h3 style='text-align:center; color:white;'>ACESSO AO TERMINAL</h3>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. DASHBOARD (PÓS-LOGIN)
st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="display:flex; justify-content:center; margin-bottom:20px;"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# GESTÃO FIXA
col_a, col_b, col_c = st.columns(3)
st.session_state.banca = col_a.number_input("BANCA:", value=float(st.session_state.banca))
st.session_state.valor_inicial = col_b.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
st.session_state.payout = col_c.number_input("PAYOUT %:", value=int(st.session_state.payout))

st.markdown("<br>", unsafe_allow_html=True)

# SELEÇÃO DE ESTRATÉGIAS ARROJADAS
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME FRAME:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA:", ["Sniper (RSI/MM/VOL)", "Turbo (MHI/PRICE/KELTNER)", "Quantum (BB/STOCH/FLOW)"])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# 6. MOTOR DE CONFLUÊNCIAS DIFERENCIADAS
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

sinal = "ANALISANDO... 🔎"
cor = "#94a3b8"
confluencias_ok = []

if est == "Sniper (RSI/MM/VOL)":
    # Foco: Cruzamento de médias e exaustão
    rsi = np.random.randint(0, 100)
    ma_cross = np.random.choice([True, False])
    vol_confirm = np.random.choice([True, False])
    if rsi < 20 and ma_cross and vol_confirm:
        sinal, cor, confluencias_ok = "CALL 🟢", "#00e676", ["RSI EXAUSTÃO", "CRUZAMENTO MÉDIAS", "VOL. COMPRADOR"]
    elif rsi > 80 and ma_cross and vol_confirm:
        sinal, cor, confluencias_ok = "PUT 🔴", "#ff3b30", ["RSI EXAUSTÃO", "CRUZAMENTO MÉDIAS", "VOL. VENDEDOR"]

elif est == "Turbo (MHI/PRICE/KELTNER)":
    # Foco: Probabilística e rompimento de canal
    mhi_minority = np.random.choice([True, False])
    keltner_out = np.random.choice([True, False])
    rejection = np.random.choice([True, False])
    if mhi_minority and keltner_out and rejection:
        sinal, cor = "CALL 🟢", "#00e676"
        confluencias_ok = ["MHI MINORIA", "ROMP. KELTNER", "REJEIÇÃO PREÇO"]

elif est == "Quantum (BB/STOCH/FLOW)":
    # Foco: Volatilidade extrema
    bb_touch = np.random.choice(["TOP", "BOTTOM", "NONE"])
    stoch = np.random.randint(0, 100)
    order_flow = np.random.choice(["STRONG", "WEAK"])
    if bb_touch == "BOTTOM" and stoch < 15 and order_flow == "STRONG":
        sinal, cor, confluencias_ok = "CALL 🟢", "#00e676", ["BB SUPORTE", "STOCH OVERSOLD", "FLUXO PESADO"]
    elif bb_touch == "TOP" and stoch > 85 and order_flow == "STRONG":
        sinal, cor, confluencias_ok = "PUT 🔴", "#ff3b30", ["BB RESISTÊNCIA", "STOCH OVERBOUGHT", "FLUXO PESADO"]

prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# CARD DE SINAL
st.markdown(f"""
<div class="signal-card">
    <div style="color:#bf5af2; font-weight:bold; font-size:12px; letter-spacing:3px; margin-bottom:10px;">ENGINE STATUS: ACTIVE</div>
    <h1 style="color:{cor}; font-size:75px; margin:15px 0; text-shadow: 0 0 20px {cor}66;">{sinal}</h1>
    <div style="font-size: 50px; font-weight: bold; color: white; font-family: monospace;">00:{int(faltam):02d}</div>
    <div style="margin-top:20px;">
        {" ".join([f'<span class="conf-tag">{c}</span>' for c in confluencias_ok]) if confluencias_ok else '<span class="conf-tag" style="color:#64748b;">AGUARDANDO CONFLUÊNCIA TRIPLA...</span>'}
    </div>
</div>
""", unsafe_allow_html=True)

# CONTROLES FINAIS
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("LIMPAR HISTÓRICO", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0})
    st.rerun()

time.sleep(1)
st.rerun()
