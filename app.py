import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. SETUP E DADOS
ARQUIVO_DADOS = "historico_trader.csv"
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            df = pd.read_csv(ARQUIVO_DADOS)
            return int(df.get('win', [0])[0]), int(df.get('loss', [0])[0])
        except: return 0, 0
    return 0, 0

def salvar_dados(w, l):
    pd.DataFrame({'win': [w], 'loss': [l]}).to_csv(ARQUIVO_DADOS, index=False)

if 'win' not in st.session_state:
    w, l = carregar_dados()
    st.session_state.update({
        'win': w, 'loss': l, 'logado': False, 'aguardando': False, 
        'som_tocado': False, 'gales': 0, 'banca': 1000.0, 'payout': 87
    })

# 2. ESTILO CSS (FOCO EM COMPACTAR TUDO)
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-mini { font-family: 'Arial Black'; font-size: 20px; color: white; text-align: center; margin-bottom: 5px; }
    .logo-trader { color: #00e676; }
    
    /* Barra de Saldo Ultra Fina */
    .status-bar { 
        background: #064e3b; color: #00e676; padding: 4px 12px; border-radius: 6px; 
        font-size: 14px; font-weight: bold; border: 1px solid #059669;
        display: flex; justify-content: space-between; margin-bottom: 8px;
    }

    .card-sinal { 
        background: rgba(30, 41, 59, 0.5); border-radius: 12px; padding: 12px; 
        text-align: center; border: 1px solid rgba(255,255,255,0.1); 
    }

    .timer-text { font-size: 34px; font-weight: bold; color: white; font-family: monospace; }
    
    /* Remove espaços inúteis */
    .block-container { padding-top: 1rem !important; }
    div[data-testid="stVerticalBlock"] > div { margin-top: -10px; }
</style>
""", unsafe_allow_html=True)

# 3. LOGIN LADO A LADO (BEM PEQUENO)
if not st.session_state.logado:
    st.markdown('<div class="logo-mini">ULTIMATE <span class="logo-trader">TRADER</span> PRO</div>', unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 3, 1])
    with col_login:
        c1, c2, c3 = st.columns([1.5, 1.5, 1])
        u = c1.text_input("U:", placeholder="Usuário", label_visibility="collapsed")
        p = c2.text_input("S:", type="password", placeholder="Senha", label_visibility="collapsed")
        if c3.button("ENTRAR", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD OPERACIONAL
st.markdown('<div class="logo-mini">ULTIMATE <span class="logo-trader">TRADER</span> PRO</div>', unsafe_allow_html=True)

# Barra de Status e Placar em uma linha só
total_gales = st.session_state.get('gales', 0)
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0

st.markdown(f"""
<div class='status-bar'>
    <span>SALDO: R$ {st.session_state.banca:.2f}</span>
    <span>W: {st.session_state.win} | L: {st.session_state.loss} | G: {total_gales} | {taxa:.1f}%</span>
</div>
""", unsafe_allow_html=True)

# Inputs de Gestão
if not st.session_state.aguardando:
    i1, i2, i3 = st.columns(3)
    st.session_state.banca = i1.number_input("BANCA:", value=float(st.session_state.banca), format="%.2f")
    st.session_state.valor_inicial = i2.number_input("ENTRADA:", value=10.0)
    st.session_state.payout = i3.number_input("PAYOUT %:", value=87)
    if 'valor_atual_operacao' not in st.session_state:
        st.session_state.valor_atual_operacao = st.session_state.valor_inicial

# Card de Sinal
if st.session_state.aguardando:
    st.markdown("<div class='card-sinal'>", unsafe_allow_html=True)
    st.write(f"⚠️ OPERAÇÃO: R$ {st.session_state.valor_atual_operacao:.2f}")
    b1, b2, b3 = st.columns(3)
    lucro = st.session_state.valor_atual_operacao * (st.session_state.payout / 100)
    
    if b1.button("WIN ✅", use_container_width=True):
        st.session_state.win += 1
        st.session_state.banca += (st.session_state.valor_atual_operacao + lucro)
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
        st.rerun()
    if b2.button("LOSS ❌", use_container_width=True):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
        st.rerun()
    if b3.button("GALE 🔄", use_container_width=True):
        st.session_state.valor_atual_operacao *= 2
        st.session_state.gales += 1
        st.session_state.som_tocado = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Seletores e Sinal
    s1, s2, s3 = st.columns(3)
    tf = s1.selectbox("T:", ["M1", "M5"], label_visibility="collapsed")
    est = s2.selectbox("E:", ["Turbo", "Moderada"], label_visibility="collapsed")
    at = s3.selectbox("A:", ["EUR/USD (OTC)", "BTC"], label_visibility="collapsed")

    # Simulação de Sinal (Lógica que você gostou)
    sinal, cor = ("CALL 🟢", "#00e676") if datetime.now().second % 10 < 5 else ("ANALISANDO...", "#94a3b8")
    faltam = 60 - datetime.now().second

    st.markdown(f"""
    <div class='card-sinal'>
        <h1 style='color:{cor}; font-size:38px; margin:0;'>{sinal}</h1>
        <div class='timer-text'>00:{faltam:02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.banca -= st.session_state.valor_inicial
        st.session_state.aguardando = True
        st.rerun()

# --- 5. RODAPÉ (ÚNICO E SEM DUPLICATAS) ---
st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
footer_1, footer_2 = st.columns(2)

if footer_1.button("LOGOUT / SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

if footer_2.button("ZERAR HISTÓRICO", use_container_width=True):
    salvar_dados(0, 0)
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
