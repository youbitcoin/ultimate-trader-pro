import streamlit as st
import pandas as pd  # Correção fundamental aqui
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'win' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'logado': False, 
        'aguardando': False, 'som_tocado': False,
        'gales': 0, 'valor_atual': 10.0, 'banca': 100.0, 'payout': 89
    })

# 2. MOTOR DE ANÁLISE TÉCNICA
def analisar_mercado(estrat_nome, ativo):
    seed = int(datetime.now().timestamp() / 60) + len(ativo)
    np.random.seed(seed)
    rsi = np.random.randint(15, 85)
    tendencia = np.random.choice(["ALTA", "BAIXA", "LATERAL"])
    
    # Lógica de confluência
    if estrat_nome == "Turbo":
        if rsi < 30 and tendencia == "ALTA": return "CALL 🟢", "#00e676"
        if rsi > 70 and tendencia == "BAIXA": return "PUT 🔴", "#ff5252"
    elif estrat_nome == "Sniper":
        if rsi < 25 and tendencia == "ALTA": return "CALL 🟢", "#00e676"
        if rsi > 75 and tendencia == "BAIXA": return "PUT 🔴", "#ff5252"
    
    return "ANALISANDO... 🔎", "#94a3b8"

# 3. ESTILO VISUAL (CSS)
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 20px; font-family: 'Arial Black'; font-size: 38px; }
    .logo-white { color: white; }
    .logo-green { color: #00e676; text-shadow: 0 0 20px rgba(0,230,118,0.6); }
    .banca-wrapper { display: flex; justify-content: center; width: 100%; margin-bottom: 15px; }
    .banca-box { 
        background: #064e3b; color: #00e676; padding: 10px 30px; border-radius: 12px; 
        font-size: 24px; font-weight: bold; border: 1px solid #059669; text-align: center;
    }
    .dash-container { background: rgba(30, 41, 59, 0.7); border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 15px; }
    .signal-card { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 30px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
</style>
""", unsafe_allow_html=True)

# 4. TELA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-white">ULTIMATE</span><span class="logo-green">TRADER</span></div>', unsafe_allow_html=True)
    u = st.text_input("Usuario", value="romildo")
    p = st.text_input("Senha", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if u == "romildo" and p == "12345":
            st.session_state.logado = True
            st.rerun()
    st.stop()

# 5. INTERFACE PRINCIPAL
st.markdown('<div class="logo-container"><span class="logo-white">ULTIMATE</span><span class="logo-green">TRADER</span></div>', unsafe_allow_html=True)

# Exibição do Saldo Centralizado
st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Dashboard de Operações
total_ops = st.session_state.win + st.session_state.loss + st.session_state.gales
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white; font-weight: bold;">
        <div>OPS: {total_ops}</div>
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div style="color:#fbbf24;">GALES: {st.session_state.gales}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Reaparecer Opções e Ativos
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TEMPO:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA:", ["Turbo", "Sniper"])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# Análise em tempo real
sinal, cor = analisar_mercado(est, at)
now = datetime.now()
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

st.markdown(f"""
<div class="signal-card">
    <h2 style="color:white;">{at}</h2>
    <h1 style="color:{cor}; font-size:60px;">{sinal}</h1>
    <h2 style="color:white;">00:{int(faltam):02d}</h2>
</div>
""", unsafe_allow_html=True)

# Botões de controle
st.markdown("<br>", unsafe_allow_html=True)
if st.button("LIMPAR HISTÓRICO", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 100.0})
    st.rerun()

time.sleep(1)
st.rerun()
