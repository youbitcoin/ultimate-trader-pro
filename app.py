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

# 2. FUNDO BACKGROUND FUTURISTA (CYBER NEURAL GRID)
img_futurista = "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2070&auto=format&fit=crop"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(5, 0, 20, 0.92), rgba(0, 10, 30, 0.92)), url("{img_futurista}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .logo-box {{ display: flex; align-items: center; justify-content: center; padding: 15px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 42px; font-family: 'Arial Black'; font-weight: 900; text-shadow: 0 0 20px #00e676; margin-left: 5px; }}
    .p-badge {{ background: #bf5af2; color: #fff; padding: 2px 12px; border-radius: 4px; font-size: 20px; margin-left: 10px; font-weight: bold; }}
    
    .banca-box {{ 
        background: rgba(0, 210, 255, 0.05); color: #00d2ff; padding: 15px; border-radius: 10px; 
        font-size: 32px; font-weight: 800; border: 2px solid #bf5af2; text-align: center; font-family: monospace;
        box-shadow: 0 0 20px rgba(191, 90, 242, 0.3);
    }}
    
    .signal-card {{ 
        background: rgba(5, 5, 20, 0.95); border-radius: 15px; padding: 30px; text-align: center; 
        border: 1px solid #bf5af2; box-shadow: 0 0 50px rgba(0,0,0,1);
    }}
    
    .conf-tag {{ 
        background: rgba(191, 90, 242, 0.1); color: #bf5af2; padding: 5px 10px; 
        border-radius: 5px; font-size: 11px; font-weight: bold; display: inline-block; margin: 2px;
        border: 1px solid rgba(191, 90, 242, 0.3);
    }}
</style>
""", unsafe_allow_html=True)

# 3. LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
    c1, col, c3 = st.columns([1, 2, 1])
    with col:
        u = st.text_input("USUÁRIO")
        p = st.text_input("SENHA", type="password")
        if st.button("AUTENTICAR SISTEMA", use_container_width=True):
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

st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TIME:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA:", ["Sniper (RSI/Tend/Volume)", "Turbo (MHI/Canais/Price)", "Quantum (BBands/Stoch/Fluxo)"])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# 5. MOTOR DE CONFLUÊNCIA DIFERENCIADO
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

sinal = "ANALISANDO... 🔎"
cor = "#94a3b8"
confluencias_ok = []

# Simulação de Indicadores para teste
if est == "Sniper (RSI/Tend/Volume)":
    # Lógica: RSI extremo + Tendência confirmada + Volume acima da média
    rsi = np.random.randint(0, 100)
    vol = np.random.choice([True, False])
    tend = np.random.choice(["ALTA", "BAIXA"])
    
    if rsi < 25 and tend == "ALTA" and vol:
        sinal, cor = "CALL 🟢", "#00e676"
        confluencias_ok = ["RSI SOBREVENDA", "TENDÊNCIA DE ALTA", "VOLUME COMPRADOR"]
    elif rsi > 75 and tend == "BAIXA" and vol:
        sinal, cor = "PUT 🔴", "#ff3b30"
        confluencias_ok = ["RSI SOBRECOMPRA", "TENDÊNCIA DE BAIXA", "VOLUME VENDEDOR"]

elif est == "Turbo (MHI/Canais/Price)":
    # Lógica: Ciclo MHI + Canal de Keltner + Rejeição de Preço
    mhi = np.random.choice(["MINORIA", "MAJORIA"])
    canal = np.random.choice(["ROMPIDO", "DENTRO"])
    price_action = np.random.choice(["REJEIÇÃO", "CONTINUIDADE"])
    
    if mhi == "MINORIA" and canal == "ROMPIDO" and price_action == "REJEIÇÃO":
        # Atribuindo Call ou Put baseado no candle anterior simulado
        tipo = np.random.choice(["CALL 🟢", "PUT 🔴"])
        sinal, cor = (tipo, "#00e676") if "CALL" in tipo else (tipo, "#ff3b30")
        confluencias_ok = ["MHI MINORIA", "CANAL ROMPIDO", "REJEIÇÃO DE PREÇO"]

elif est == "Quantum (BBands/Stoch/Fluxo)":
    # Lógica: Bollinger Bands + Estocástico + Fluxo de Ordens
    bb = np.random.choice(["TOPO", "FUNDO", "MEIO"])
    stoch = np.random.randint(0, 100)
    fluxo = np.random.choice(["FORTE", "FRACO"])
    
    if bb == "FUNDO" and stoch < 20 and fluxo == "FORTE":
        sinal, cor = "CALL 🟢", "#00e676"
        confluencias_ok = ["BOLLINGER FUNDO", "STOCH OVERSOLD", "FLUXO COMPRADOR"]
    elif bb == "TOPO" and stoch > 80 and fluxo == "FORTE":
        sinal, cor = "PUT 🔴", "#ff3b30"
        confluencias_ok = ["BOLLINGER TOPO", "STOCH OVERBOUGHT", "FLUXO VENDEDOR"]

# Timer
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

# Card de Sinal
st.markdown(f"""
<div class="signal-card">
    <div style="color:#00d2ff; font-weight:bold; font-size:14px; letter-spacing:2px; margin-bottom:10px;">{at} - PROBABILITY UNIT</div>
    <h1 style="color:{cor}; font-size:75px; margin:15px 0; text-shadow: 0 0 20px {cor}66;">{sinal}</h1>
    <div style="font-size: 50px; font-weight: bold; color: white; font-family: monospace;">00:{int(faltam):02d}</div>
    <div style="margin-top:15px;">
        {" ".join([f'<span class="conf-tag">{c}</span>' for c in confluencias_ok]) if confluencias_ok else '<span class="conf-tag" style="color:#64748b;">AGUARDANDO CONFLUÊNCIA TRIPLA...</span>'}
    </div>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("ZERAR DADOS", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
