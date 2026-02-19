import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. SETUP E PERSISTÊNCIA
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
        'win': w, 'loss': l, 'logado': False, 
        'aguardando': False, 'som_tocado': False,
        'gales': 0, 'valor_inicial': 10.0, 'valor_atual_operacao': 10.0,
        'banca': 1000.0, 'payout': 87
    })

# 2. ESTILO CSS (VISUAL ORIGINAL)
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 20px; padding-top: 10px; }
    .logo-ultimate { font-family: 'Arial Black'; font-size: 38px; color: white; }
    .logo-trader { font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 20px rgba(0,230,118,0.6); }
    .logo-pro { background: #00e676; color: #020617; padding: 2px 8px; border-radius: 4px; font-size: 18px; vertical-align: middle; margin-left: 5px; }
    
    .banca-box { background: #064e3b; color: #00e676; padding: 10px; border-radius: 10px; font-size: 22px; font-weight: bold; text-align: center; border: 1px solid #059669; margin-bottom: 10px; }
    .dash-container { background: rgba(30, 41, 59, 0.7); border-radius: 15px; padding: 10px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
    .signal-card { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 25px; text-align: center; border: 2px solid #00d2ff; }
    
    .timer-box { font-size: 50px; font-weight: bold; color: white; font-family: monospace; }
    .valor-badge { background: #1e293b; color: #fbbf24; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 18px; border: 1px solid #fbbf24; display: inline-block; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.5, 1])
    with col_login:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD PRINCIPAL
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# Placar e Saldo
st.markdown(f"<div class='banca-box'>SALDO: R$ {st.session_state.banca:.2f}</div>", unsafe_allow_html=True)
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white; font-weight: bold; font-size: 12px;">
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div style="color:#fbbf24;">GALES: {st.session_state.gales}</div>
        <div>ASSERT: {taxa:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- LÓGICA DE TRANSIÇÃO DE TELA ---

if st.session_state.aguardando:
    # ---------------------------------------------------------
    # TELA DE RESULTADOS (A QUE TINHA SUMIDO)
    # ---------------------------------------------------------
    st.markdown(f"""
    <div class='signal-card'>
        <div class='valor-badge'>VALOR EM JOGO: R$ {st.session_state.valor_atual_operacao:.2f}</div>
        <h2 style='color:white;'>QUAL FOI O RESULTADO?</h2>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    lucro = st.session_state.valor_atual_operacao * (st.session_state.payout / 100)
    
    if c1.button("WIN ✅", use_container_width=True):
        st.session_state.win += 1
        st.session_state.banca += (st.session_state.valor_atual_operacao + lucro)
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
        st.rerun()
        
    if c2.button("LOSS ❌", use_container_width=True):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
        st.rerun()
        
    if c3.button("GALE 🔄", use_container_width=True):
        nova_entrada = st.session_state.valor_atual_operacao * 2
        if st.session_state.banca >= nova_entrada:
            st.session_state.banca -= nova_entrada
            st.session_state.valor_atual_operacao = nova_entrada
            st.session_state.gales += 1
            st.session_state.som_tocado = False 
            st.rerun()
        else:
            st.error("Sem saldo para Gale!")
            
    if c4.button("PULAR ⏭️", use_container_width=True):
        st.session_state.banca += st.session_state.valor_atual_operacao # Devolve o valor
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # ---------------------------------------------------------
    # TELA DE ANÁLISE / ESPERA (SINAL)
    # ---------------------------------------------------------
    g1, g2, g3 = st.columns(3)
    st.session_state.banca = g1.number_input("BANCA:", value=float(st.session_state.banca))
    st.session_state.valor_inicial = g2.number_input("ENTRADA:", value=float(st.session_state.valor_inicial))
    st.session_state.payout = g3.number_input("PAYOUT %:", value=int(st.session_state.payout))

    # Simulando um sinal para teste (Verde nos primeiros 30 segundos do minuto)
    now = datetime.now()
    if now.second < 30:
        sinal, cor = "CALL 🟢", "#00e676"
    else:
        sinal, cor = "ANALISANDO...", "#94a3b8"
    
    faltam = 60 - now.second

    # Som
    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"></audio>', height=0)
        st.session_state.som_tocado = True

    st.markdown(f"""
    <div class='signal-card'>
        <div class='valor-badge'>ENTRADA: R$ {st.session_state.valor_inicial:.2f}</div>
        <h1 style='color:{cor}; font-size:55px; margin:10px 0;'>{sinal}</h1>
        <div class='timer-box'>00:{faltam:02d}</div>
    </div>
    """, unsafe_allow_html=True)

    # GATILHO: Quando faltar 2 segundos para o sinal acabar, ele "trava" a tela nos botões
    if "ANALISANDO" not in sinal and faltam <= 2:
        if st.session_state.banca >= st.session_state.valor_inicial:
            st.session_state.banca -= st.session_state.valor_inicial
            st.session_state.valor_atual_operacao = st.session_state.valor_inicial
            st.session_state.aguardando = True
            st.rerun()

    # Só faz o rerun automático aqui para não bugar os botões lá de cima
    time.sleep(1)
    st.rerun()

# 5. RODAPÉ (LOGOUT)
st.markdown("<br>", unsafe_allow_html=True)
if st.button("SAIR DO SISTEMA", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
