import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Inicialização do Estado Global
if 'logado' not in st.session_state:
    st.session_state.update({
        'logado': False, 'banca': 1000.0, 'entrada': 10.0, 
        'payout': 87, 'wins': 0, 'losses': 0
    })

# CSS Minimalista High-Contrast
st.markdown("""
<style>
    .stApp { background-color: #00050a; }
    .brand { text-align: center; padding: 20px; font-family: 'Arial Black'; }
    .u-t { color: #FFF; font-size: 30px; }
    .t-t { color: #00e676; font-size: 30px; text-shadow: 0 0 10px #00e676; }
    
    /* Botões com contraste máximo (Texto Preto) */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000 !important; font-weight: 900 !important; border: none !important;
        height: 42px !important; text-transform: uppercase;
    }
    
    /* Cards de Dados */
    .data-card {
        background: rgba(0, 210, 255, 0.05); border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 15px;
    }
    .signal-box {
        background: #050a14; border: 1px solid #00d2ff; border-radius: 12px;
        padding: 30px; text-align: center; margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SISTEMA DE SEGURANÇA (BLOQUEIO TOTAL) ---
def tela_login():
    st.markdown('<div class="brand"><span class="u-t">ULTIMATE</span><span class="t-t">TRADER</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<p style='text-align:center; color:#00d2ff; font-size:12px;'>ENCRYPTED ACCESS ONLY</p>", unsafe_allow_html=True)
        user = st.text_input("USUÁRIO", key="user_input")
        pw = st.text_input("SENHA", type="password", key="pw_input")
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if user == "romildo" and pw == "12345":
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Acesso Negado")

# Se não estiver logado, mostra o login e PARA a execução aqui
if not st.session_state.logado:
    tela_login()
    st.stop()  # <--- ISSO impede que o resto do sistema apareça nas fotos image_01d282.png

# --- 3. DASHBOARD OPERACIONAL (SÓ APARECE SE LOGADO) ---
st.markdown('<div class="brand"><span class="u-t">ULTIMATE</span><span class="t-t">TRADER</span><span style="background:#00d2ff; color:#000; padding:2px 8px; border-radius:4px; font-size:12px; margin-left:10px;">PRO</span></div>', unsafe_allow_html=True)

# Linha de Status
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<div class="data-card">BANCA ATUAL<br><span style="color:#00e676; font-size:22px; font-weight:bold;">R$ {st.session_state.banca:.2f}</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="data-card">PLACAR<br><span style="color:#00e676;">W: {st.session_state.wins}</span> | <span style="color:#ff1744;">L: {st.session_state.losses}</span></div>', unsafe_allow_html=True)

# Configurações Rápidas
with st.expander("⚙️ AJUSTES DE MERCADO", expanded=False):
    g1, g2, g3 = st.columns(3)
    st.session_state.entrada = g1.number_input("ENTRADA R$:", value=float(st.session_state.entrada))
    st.session_state.payout = g2.number_input("PAYOUT %:", value=int(st.session_state.payout))
    ativo = g3.selectbox("ATIVO:", ["EUR/USD (OTC)", "BTC/USDT", "GBP/JPY"])

# --- 4. ENGINE DE ANÁLISE ---
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

sinal, cor = "ANALISANDO...", "#4b5563"
if np.random.random() > 0.6:
    if np.random.random() > 0.5: sinal, cor = "CALL 🟢", "#00e676"
    else: sinal, cor = "PUT 🔴", "#ff1744"

timer = 60 - now.second

st.markdown(f"""
<div class="signal-box">
    <div style="color:rgba(0, 210, 255, 0.5); font-size:10px; letter-spacing:2px;">ENGINE STATUS: ACTIVE | {ativo}</div>
    <h1 style="color:{cor}; font-size:60px; margin:10px 0; font-weight:900;">{sinal}</h1>
    <div style="font-size:35px; color:#00d2ff; font-family:monospace;">00:{timer:02d}</div>
</div>
""", unsafe_allow_html=True)

# --- 5. CONTROLES DE RESULTADO ---
res1, res2, res3 = st.columns([1.5, 1.5, 1])

if res1.button("✅ REGISTRAR WIN", use_container_width=True):
    st.session_state.wins += 1
    st.session_state.banca += (st.session_state.entrada * (st.session_state.payout / 100))
    st.rerun()

if res2.button("❌ REGISTRAR LOSS", use_container_width=True):
    st.session_state.losses += 1
    st.session_state.banca -= st.session_state.entrada
    st.rerun()

if res3.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

time.sleep(1)
st.rerun()
