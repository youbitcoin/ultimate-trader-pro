import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES E DADOS
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
        'gales': 0, 'valor_atual': 10.0, 'banca': 1000.0, 'payout': 87
    })

# 2. ESTILO CSS (O DESIGN QUE VOCÊ GOSTOU)
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 20px; padding-top: 20px; }
    .logo-ultimate { font-family: 'Arial Black'; font-size: 38px; color: white; }
    .logo-trader { font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 20px rgba(0,230,118,0.6); }
    .logo-pro { background: #00e676; color: #020617; padding: 2px 8px; border-radius: 4px; font-size: 18px; vertical-align: middle; margin-left: 5px; }
    
    /* Cards e Boxes */
    .banca-box { background: #064e3b; color: #00e676; padding: 15px; border-radius: 12px; font-size: 24px; font-weight: bold; text-align: center; border: 1px solid #059669; margin-bottom: 15px; }
    .dash-container { background: rgba(30, 41, 59, 0.7); border-radius: 15px; padding: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
    .signal-card { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 25px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
    
    .timer-box { font-size: 48px; font-weight: bold; color: white; font-family: monospace; }
    .valor-badge { background: #1e293b; color: #fbbf24; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 18px; border: 1px solid #fbbf24; display: inline-block; margin-bottom: 15px; }
    
    /* Botões */
    .stButton>button { border-radius: 8px !important; height: 45px !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# Container principal para evitar sobreposição
main_ui = st.empty()

# 3. HOME DE LOGIN (RECONFIGURADA)
if not st.session_state.logado:
    with main_ui.container():
        st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
        _, col_login, _ = st.columns([1, 2, 1])
        with col_login:
            st.markdown("<div style='background:rgba(30,41,59,0.5); padding:25px; border-radius:15px; border:1px solid #00d2ff;'>", unsafe_allow_html=True)
            u = st.text_input("Usuário", placeholder="Digite seu usuário")
            p = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            if st.button("ACESSAR TERMINAL", use_container_width=True):
                if u == "romildo" and p == "12345":
                    st.session_state.logado = True
                    st.rerun()
                else:
                    st.error("Dados incorretos!")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. DASHBOARD (SÓ CARREGA SE LOGADO)
with main_ui.container():
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

    # Status de Banca e Placar
    total_gales = st.session_state.get('gales', 0)
    taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0
    
    st.markdown(f"<div class='banca-box'>SALDO ATUAL: R$ {st.session_state.banca:.2f}</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="dash-container">
        <div style="display: flex; justify-content: space-around; color: white; font-weight: bold; font-size: 13px;">
            <div style="color:#00e676;">WINS: {st.session_state.win}</div>
            <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
            <div style="color:#fbbf24;">GALES: {total_gales}</div>
            <div>ASSERT: {taxa:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Configurações de Gestão
    if not st.session_state.aguardando:
        c1, c2, c3 = st.columns(3)
        st.session_state.banca = c1.number_input("BANCA:", value=float(st.session_state.banca))
        st.session_state.valor_inicial = c2.number_input("ENTRADA:", value=10.0)
        st.session_state.payout = c3.number_input("PAYOUT %:", value=87)
        if 'valor_atual_operacao' not in st.session_state:
            st.session_state.valor_atual_operacao = st.session_state.valor_inicial

    # Card de Operação / Sinal
    if st.session_state.aguardando:
        st.markdown(f"""
        <div class='signal-card'>
            <div class='valor-badge'>EM OPERAÇÃO: R$ {st.session_state.valor_atual_operacao:.2f}</div>
            <h3 style='color:white;'>CONFIRMAR RESULTADO?</h3>
        """, unsafe_allow_html=True)
        res_cols = st.columns(4)
        lucro = st.session_state.valor_atual_operacao * (st.session_state.payout / 100)
        
        if res_cols[0].button("WIN ✅", use_container_width=True):
            st.session_state.win += 1
            st.session_state.banca += (st.session_state.valor_atual_operacao + lucro)
            salvar_dados(st.session_state.win, st.session_state.loss)
            st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
            st.rerun()
        if res_cols[1].button("LOSS ❌", use_container_width=True):
            st.session_state.loss += 1
            salvar_dados(st.session_state.win, st.session_state.loss)
            st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
            st.rerun()
        if res_cols[2].button("GALE 🔄", use_container_width=True):
            st.session_state.valor_atual_operacao *= 2
            st.session_state.gales += 1
            st.session_state.som_tocado = False
            st.rerun()
        if res_cols[3].button("SKIP ⏭️", use_container_width=True):
            st.session_state.banca += st.session_state.valor_atual_operacao
            st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Modo Análise
        sel_cols = st.columns([1, 1, 1.5])
        tf = sel_cols[0].selectbox("TEMPO:", ["M1", "M5"])
        est = sel_cols[1].selectbox("ESTRAT:", ["Turbo", "Sniper"])
        at = sel_cols[2].selectbox("ATIVO:", ["EUR/USD (OTC)", "BITCOIN"])

        # Lógica de sinal simplificada para o exemplo
        sinal, cor = ("CALL 🟢", "#00e676") if datetime.now().second % 10 < 5 else ("ANALISANDO...", "#94a3b8")
        faltam = 60 - datetime.now().second

        st.markdown(f"""
        <div class='signal-card'>
            <div class='valor-badge'>ENTRADA: R$ {st.session_state.valor_inicial:.2f}</div>
            <h2 style='color:white; margin:0;'>{at}</h2>
            <h1 style='color:{cor}; font-size:52px; margin:10px 0;'>{sinal}</h1>
            <div class='timer-box'>00:{faltam:02d}</div>
        </div>
        """, unsafe_allow_html=True)

        if "ANALISANDO" not in sinal and faltam <= 2:
            st.session_state.banca -= st.session_state.valor_inicial
            st.session_state.aguardando = True
            st.rerun()

    # Rodapé único
    st.markdown("<br>", unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    if f1.button("LOGOUT / SAIR", use_container_width=True):
        st.session_state.logado = False
        st.rerun()
    if f2.button("ZERAR HISTÓRICO", use_container_width=True):
        salvar_dados(0, 0)
        st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
        st.rerun()

time.sleep(1)
st.rerun()
