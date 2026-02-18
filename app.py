import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. PERSISTENCIA E CONFIGURACOES
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

# Inicializacao de estados (Session State)
if 'win' not in st.session_state:
    w, l = carregar_dados()
    st.session_state.update({'win': w, 'loss': l, 'logado': False, 'aguardando': False, 'som_tocado': False})

# 2. ESTILO CSS PARA EVITAR QUEBRA DE LAYOUT
st.markdown("""
<style>
    .stApp { background: #020617; }
    .dash-container, .signal-card { 
        background: rgba(30, 41, 59, 0.7); 
        border-radius: 15px; padding: 20px; text-align: center; border: 1px solid #334155;
    }
    .timer-box { font-size: 45px; font-weight: bold; color: white; }
    .stSelectbox label { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# 3. LOGICA DE LOGIN
if not st.session_state.logado:
    st.markdown("<h1 style='text-align:center; color:white;'>ULTIMATE TRADER PRO</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("Usuario")
        p = st.text_input("Senha", type="password")
        if st.button("ENTRAR", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. TERMINAL (SO EXECUTA SE LOGADO)
st.markdown("<h2 style='text-align:center; color:#00e676;'>ULTIMATE TRADER PRO</h2>", unsafe_allow_html=True)

# Placar
total = st.session_state.win + st.session_state.loss
taxa = (st.session_state.win / total * 100) if total > 0 else 0
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white;">
        <div>OPS: {total}</div>
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div>ASSERT: {taxa:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Lógica de Sinais
if st.session_state.aguardando:
    st.markdown("<div class='signal-card'><h3>RESULTADO?</h3>", unsafe_allow_html=True)
    cols = st.columns(4)
    if cols[0].button("WIN"):
        st.session_state.win += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'som_tocado': False})
        st.rerun()
    if cols[1].button("LOSS"):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'som_tocado': False})
        st.rerun()
    if cols[2].button("GALE"):
        st.session_state.som_tocado = False
        st.rerun()
    if cols[3].button("PULAR"):
        st.session_state.aguardando = False
        st.rerun()
else:
    c1, c2, c3 = st.columns([1, 1, 2])
    tf = c1.selectbox("TEMPO:", ["M1", "M5"])
    est = c2.selectbox("ESTRATEGIA:", ["Turbo", "Moderada", "Sniper"])
    at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BITCOIN", "SOLANA"])

    # Temporizador e Sinal
    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    th = 85 if est == "Turbo" else 98 if est == "Sniper" else 92
    
    if f >= th: sinal, cor = "PUT", "#ff5252"
    elif f <= (100 - th): sinal, cor = "CALL", "#00e676"
    else: sinal, cor = "ANALISANDO...", "#94a3b8"

    # --- CORRECAO DO SOM ---
    if sinal != "ANALISANDO..." and not st.session_state.som_tocado:
        # Usando link direto de som curto e limpo
        st.components.v1.html("""
            <audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3"></audio>
        """, height=0)
        st.session_state.som_tocado = True

    st.markdown(f"""
    <div class='signal-card'>
        <h2 style='color:white;'>{at}</h2>
        <h1 style='color:{cor}; font-size:50px;'>{sinal}</h1>
        <div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if sinal != "ANALISANDO..." and faltam <= 2:
        st.session_state.aguardando = True
        st.rerun()

# Botões de Controle Final (Garantindo que apareçam uma só vez)
st.markdown("<br>", unsafe_allow_html=True)
cb1, cb2 = st.columns(2)
if cb1.button("SAIR DO SISTEMA", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if cb2.button("LIMPAR HISTORICO", use_container_width=True):
    salvar_dados(0, 0)
    st.session_state.update({'win': 0, 'loss': 0})
    st.rerun()

time.sleep(1)
st.rerun()
