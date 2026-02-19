import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

if 'logado' not in st.session_state:
    st.session_state.update({
        'win': 0, 'loss': 0, 'gales': 0, 'logado': False, 
        'aguardando': False, 'som_tocado': False,
        'banca': 1000.0, 'valor_atual': 10.0, 'payout': 87
    })

# 2. LINKS DAS IMAGENS (CONFORME SOLICITADO)
# Login: Cyberpunk + Trader + Futuro
img_login = "https://img.freepik.com/fotos-premium/uma-sala-com-muitas-telas-e-uma-cidade-ao-fundo-ia-generativa_955841-419.jpg"
# Dashboard: Fundo Antigo (Técnico/Dark)
img_dash = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop"

bg_url = img_login if not st.session_state.logado else img_dash

# 3. CSS ULTRA DETALHADO (LOGO E FUNDO)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* LOGO BLINDADA (PARA NÃO DESFIGURAR) */
    .logo-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Arial Black', sans-serif;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 30px;
    }}
    .u-text {{ color: #FFFFFF; font-size: 38px; }}
    .t-text {{ color: #00e676; font-size: 38px; text-shadow: 0 0 15px rgba(0,230,118,0.7); margin-left: 2px; }}
    .p-badge {{ 
        background: #00e676; color: #000; padding: 2px 8px; border-radius: 4px; 
        font-size: 18px; margin-left: 8px; font-family: Arial, sans-serif; font-weight: bold;
    }}
    
    /* SALDO CENTRALIZADO */
    .banca-wrapper {{ display: flex; justify-content: center; margin-bottom: 20px; }}
    .banca-box {{ 
        background: rgba(6, 78, 59, 0.9); color: #00e676; padding: 10px 40px; 
        border-radius: 12px; font-size: 24px; font-weight: bold; border: 2px solid #00e676; 
        text-align: center; min-width: 250px;
    }}
    
    /* CARDS E SINAIS */
    .dash-container, .signal-card {{ 
        background: rgba(15, 23, 42, 0.9); border-radius: 20px; 
        padding: 20px; text-align: center; border: 1px solid rgba(0,230,118,0.3);
        backdrop-filter: blur(10px);
    }}
    .timer-box {{ font-size: 52px; font-weight: bold; color: white; font-family: monospace; }}
</style>
""", unsafe_allow_html=True)

# 4. LÓGICA DE TELAS
if not st.session_state.logado:
    # TELA DE LOGIN
    st.markdown("""
        <div class="logo-box">
            <span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h4 style='text-align:center; color:white;'>ACESSO AO TERMINAL</h4>", unsafe_allow_html=True)
            u = st.text_input("USUÁRIO")
            p = st.text_input("SENHA", type="password")
            if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
                if u == "romildo" and p == "12345":
                    st.session_state.logado = True
                    st.rerun()
    st.stop()

# 5. DASHBOARD (SINAL E OPÇÕES)
st.markdown("""
    <div class="logo-box">
        <span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# Placar
total_ops = st.session_state.win + st.session_state.loss + st.session_state.gales
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white; font-weight: bold; font-size: 14px;">
        <div>OPS: {total_ops}</div>
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div style="color:#fbbf24;">GALES: {st.session_state.gales}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# OPÇÕES E ATIVOS (VOLTARAM PARA A TELA)
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("TEMPO:", ["M1", "M5"])
est = c2.selectbox("ESTRATÉGIA:", ["Sniper", "Turbo", "Moderada"])
at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD", "SOLANA"])

# Análise Técnica
seed = int(datetime.now().timestamp() / 60)
np.random.seed(seed)
f = np.random.randint(0, 100)
if f > 80: sinal, cor = "PUT 🔴", "#ff5252"
elif f < 20: sinal, cor = "CALL 🟢", "#00e676"
else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

now = datetime.now()
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
faltam = (prox - now).total_seconds()

st.markdown(f"""
<div class="signal-card">
    <h2 style="color:white; margin:0;">{at}</h2>
    <h1 style="color:{cor}; font-size:60px; margin:15px 0;">{sinal}</h1>
    <div class="timer-box">00:{int(faltam):02d}</div>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("<br>", unsafe_allow_html=True)
col_f1, col_f2 = st.columns(2)
if col_f1.button("SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if col_f2.button("LIMPAR", use_container_width=True):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
