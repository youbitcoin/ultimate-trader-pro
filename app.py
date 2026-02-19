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

# Inicialização do estado
if 'win' not in st.session_state:
    w, l = carregar_dados()
    st.session_state.update({
        'win': w, 'loss': l, 'logado': False, 'aguardando': False, 
        'som_tocado': False, 'gales': 0, 'banca': 1000.0, 
        'entrada': 10.0, 'payout': 87, 'valor_operacao': 10.0
    })

# 2. ESTILO CSS (VOLTANDO AO DESIGN DAS IMAGENS)
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-ultimate { font-family: 'Arial Black'; font-size: 38px; color: white; }
    .logo-trader { font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 15px #00e676; }
    .logo-pro { background: #00d2ff; color: #020617; padding: 2px 8px; border-radius: 4px; font-size: 18px; vertical-align: middle; }
    
    .banca-card { background: #064e3b; color: #00e676; padding: 15px; border-radius: 12px; font-size: 24px; font-weight: bold; text-align: center; border: 1px solid #059669; margin-bottom: 10px; }
    .stats-container { background: rgba(30, 41, 59, 0.5); border-radius: 10px; padding: 8px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); }
    .signal-box { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 30px; text-align: center; border: 2px solid #00d2ff; }
    
    .timer-text { font-size: 60px; font-weight: bold; color: white; font-family: monospace; }
    .entrada-badge { background: #1e293b; color: #fbbf24; padding: 5px 20px; border-radius: 50px; font-weight: bold; border: 1px solid #fbbf24; display: inline-block; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. TELA DE LOGIN (ESTILO image_0171bd.png)
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span> <span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<h3 style='text-align:center; color:#bf40bf;'>SYSTEM ACCESS</h3>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO", placeholder="Seu usuário")
        p = st.text_input("SENHA", type="password", placeholder="Sua senha")
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD PRINCIPAL
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span> <span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# Exibição do Saldo e Stats
st.markdown(f"<div class='banca-card'>SALDO OPERACIONAL: R$ {st.session_state.banca:.2f}</div>", unsafe_allow_html=True)
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0

st.markdown(f"""
<div class="stats-container">
    <div style="display: flex; justify-content: space-around; font-weight: bold; font-size: 14px;">
        <span style="color:#00e676;">WINS: {st.session_state.win}</span>
        <span style="color:#ff5252;">LOSSES: {st.session_state.loss}</span>
        <span style="color:#fbbf24;">GALES: {st.session_state.gales}</span>
        <span style="color:white;">ASSERT: {taxa:.1f}%</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Inputs de Gestão (Sempre visíveis mas desabilitados em operação)
c1, c2, c3 = st.columns(3)
nova_banca = c1.number_input("BANCA ATUAL:", value=float(st.session_state.banca), disabled=st.session_state.aguardando)
nova_entrada = c2.number_input("ENTRADA R$:", value=float(st.session_state.entrada), disabled=st.session_state.aguardando)
novo_payout = c3.number_input("PAYOUT %:", value=int(st.session_state.payout), disabled=st.session_state.aguardando)

if not st.session_state.aguardando:
    st.session_state.banca = nova_banca
    st.session_state.entrada = nova_entrada
    st.session_state.payout = novo_payout

# --- ÁREA DINÂMICA (SINAL OU RESULTADO) ---
placeholder = st.empty()

with placeholder.container():
    if st.session_state.aguardando:
        # TELA DE CONFIRMAÇÃO (RESTAURADA)
        st.markdown(f"""
        <div class='signal-box'>
            <div class='entrada-badge'>EM OPERAÇÃO: R$ {st.session_state.valor_operacao:.2f}</div>
            <h2 style='color:white;'>CONFIRME O RESULTADO ABAIXO:</h2>
        """, unsafe_allow_html=True)
        
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        lucro = st.session_state.valor_operacao * (st.session_state.payout / 100)
        
        if res_col1.button("WIN ✅", use_container_width=True):
            st.session_state.win += 1
            st.session_state.banca += (st.session_state.valor_operacao + lucro)
            salvar_dados(st.session_state.win, st.session_state.loss)
            st.session_state.update({'aguardando': False, 'valor_operacao': st.session_state.entrada, 'som_tocado': False})
            st.rerun()
            
        if res_col2.button("LOSS ❌", use_container_width=True):
            st.session_state.loss += 1
            salvar_dados(st.session_state.win, st.session_state.loss)
            st.session_state.update({'aguardando': False, 'valor_operacao': st.session_state.entrada, 'som_tocado': False})
            st.rerun()
            
        if res_col3.button("GALE 🔄", use_container_width=True):
            st.session_state.valor_operacao *= 2
            st.session_state.gales += 1
            st.session_state.som_tocado = False
            st.rerun()
            
        if res_col4.button("PULAR ⏭️", use_container_width=True):
            st.session_state.banca += st.session_state.valor_operacao
            st.session_state.update({'aguardando': False, 'valor_operacao': st.session_state.entrada})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        # TELA DE ANÁLISE (CRONÔMETRO)
        sel1, sel2, sel3 = st.columns(3)
        tf = sel1.selectbox("TIME FRAME:", ["M1", "M5"])
        est = sel2.selectbox("ESTRATÉGIA:", ["Turbo V2", "Sniper (RSI/MM)"])
        at = sel3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/JPY (OTC)"])

        now = datetime.now()
        sinal, cor = ("CALL 🟢", "#00e676") if now.second < 30 else ("ANALISANDO...", "#94a3b8")
        faltam = 60 - now.second

        if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
            st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"></audio>', height=0)
            st.session_state.som_tocado = True

        st.markdown(f"""
        <div class='signal-box'>
            <div class='entrada-badge'>PRÓXIMA ENTRADA: R$ {st.session_state.entrada:.2f}</div>
            <h1 style='color:{cor}; font-size:55px; margin:10px 0;'>{sinal}</h1>
            <div class='timer-text'>00:{faltam:02d}</div>
        </div>
        """, unsafe_allow_html=True)

        # Gatilho de Operação
        if "ANALISANDO" not in sinal and faltam <= 2:
            st.session_state.banca -= st.session_state.entrada
            st.session_state.valor_operacao = st.session_state.entrada
            st.session_state.aguardando = True
            st.rerun()

# 5. RODAPÉ (LIMPANDO OS BOTÕES DUPLICADOS DA image_01cea2.png)
st.markdown("<br>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
if f1.button("SAIR DO TERMINAL", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if f2.button("ZERAR HISTÓRICO", use_container_width=True):
    salvar_dados(0, 0)
    st.session_state.update({'win':0, 'loss':0, 'gales':0})
    st.rerun()

# Loop de atualização (Só roda se NÃO estiver aguardando resultado)
if not st.session_state.aguardando:
    time.sleep(1)
    st.rerun()
