import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. CONFIGURACOES E DADOS
ARQUIVO_DADOS = "historico_trader.csv"
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            df = pd.read_csv(ARQUIVO_DADOS)
            return int(df['win'][0]), int(df['loss'][0])
        except: return 0, 0
    return 0, 0

def salvar_dados(w, l):
    pd.DataFrame({'win': [w], 'loss': [l]}).to_csv(ARQUIVO_DADOS, index=False)

if 'win' not in st.session_state:
    w, l = carregar_dados()
    st.session_state.update({'win': w, 'loss': l, 'logado': False, 'aguardando': False, 'som_tocado': False})

# 2. CSS - ESTILIZAÇÃO COMPLETA
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 30px; }
    .logo-ultimate { font-family: 'Arial Black'; font-size: 38px; color: white; }
    .logo-trader { font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 20px rgba(0,230,118,0.6); }
    .logo-pro { background: #00e676; color: #020617; padding: 2px 8px; border-radius: 4px; font-size: 18px; vertical-align: middle; margin-left: 5px; }
    
    .dash-container, .signal-card { 
        background: rgba(30, 41, 59, 0.7); border-radius: 20px; 
        padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1);
    }
    .timer-box { font-size: 48px; font-weight: bold; color: white; font-family: monospace; }
    
    /* Estilo do Termo de Uso */
    .footer-terms {
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid rgba(255,255,255,0.05);
        text-align: center;
        color: #64748b;
        font-size: 12px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# 3. TELA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            u = st.text_input("Usuario / ID")
            p = st.text_input("Senha", type="password")
            if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
                if u == "romildo" and p == "12345":
                    st.session_state.logado = True
                    st.rerun()
    st.stop()

# 4. TERMINAL LOGADO
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

total = st.session_state.win + st.session_state.loss
taxa = (st.session_state.win / total * 100) if total > 0 else 0
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white; font-weight: bold;">
        <div>OPS: {total}</div>
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div>ASSERT: {taxa:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.aguardando:
    st.markdown("<div class='signal-card'><h3>RESULTADO DA OPERACAO?</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("WIN", use_container_width=True):
        st.session_state.win += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'som_tocado': False})
        st.rerun()
    if c2.button("LOSS", use_container_width=True):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'som_tocado': False})
        st.rerun()
    if c3.button("GALE", use_container_width=True):
        st.session_state.som_tocado = False
        st.rerun()
    if c4.button("PULAR", use_container_width=True):
        st.session_state.aguardando = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    cols = st.columns([1, 1, 1.5])
    tf = cols[0].selectbox("TEMPO:", ["M1", "M5"])
    est = cols[1].selectbox("ESTRATEGIA:", ["Turbo", "Moderada", "Sniper"])
    
    lista_ativos = [
        "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/CAD (OTC)", 
        "EUR/GBP (OTC)", "USD/CHF (OTC)", "AUD/USD (OTC)", "NZD/USD (OTC)",
        "EUR/JPY (OTC)", "GBP/JPY (OTC)", "CAD/JPY (OTC)", "USD/CAD (OTC)",
        "EUR/CAD (OTC)", "GBP/AUD (OTC)", "AUD/JPY (OTC)", "BITCOIN (BTC)",
        "ETHEREUM (ETH)", "SOLANA (SOL)", "LITECOIN (LTC)", "RIPPLE (XRP)"
    ]
    at = cols[2].selectbox("ATIVO DISPONIVEL:", lista_ativos)

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    th = 85 if est == "Turbo" else 98 if est == "Sniper" else 92
    
    if f >= th: sinal, cor = "PUT 🔴", "#ff5252"
    elif f <= (100 - th): sinal, cor = "CALL 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3"></audio>', height=0)
        st.session_state.som_tocado = True

    st.markdown(f"""
    <div class='signal-card'>
        <h2 style='color:white; margin-bottom:5px;'>{at}</h2>
        <h1 style='color:{cor}; font-size:52px; margin-top:0;'>{sinal}</h1>
        <div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.aguardando = True
        st.rerun()

# 5. RODAPE (BOTOES + TERMOS)
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("SAIR DO SISTEMA", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("LIMPAR HISTORICO", use_container_width=True):
    salvar_dados(0, 0)
    st.session_state.update({'win': 0, 'loss': 0})
    st.rerun()

st.markdown("""
<div class="footer-terms">
    <strong>TERMOS DE USO E RESPONSABILIDADE</strong><br>
    O Ultimate Trader Pro é uma ferramenta de auxílio baseada em algoritmos probabilísticos. 
    Negociar opções binárias e criptoativos envolve riscos substanciais e pode resultar na perda de capital. 
    Não garantimos lucros e os resultados passados não garantem ganhos futuros. 
    O uso deste sistema é de sua total responsabilidade. Nunca invista dinheiro que não possa perder.
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
