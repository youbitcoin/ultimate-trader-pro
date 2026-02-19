import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAÇÃO DE INTERFACE & ENGINE ---
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Inicialização de Estado Robusta
if 'logado' not in st.session_state:
    st.session_state.update({
        'logado': False, 
        'banca': 1000.0, 
        'entrada': 10.0, 
        'payout': 87, 
        'wins': 0, 
        'losses': 0
    })

# CSS Profissional (Contraste Total e Sem Vazamentos)
st.markdown("""
<style>
    /* Fundo Escuro Profissional */
    .stApp { background-color: #000408; }
    
    /* Branding */
    .brand { text-align: center; padding: 15px; }
    .u-t { color: #FFF; font-size: 28px; font-weight: 800; font-family: 'Arial'; }
    .t-t { color: #00e676; font-size: 28px; font-weight: 800; text-shadow: 0 0 12px #00e676; margin-left: 5px; }
    
    /* Cards de Informação Estilo 'Glass' */
    .data-card {
        background: rgba(0, 210, 255, 0.03); 
        border: 1px solid rgba(0, 210, 255, 0.15);
        padding: 12px; border-radius: 10px; text-align: center;
    }
    
    /* Signal Box (Foco Central) */
    .signal-box {
        background: rgba(5, 10, 20, 0.8); 
        border: 1px solid #00d2ff; 
        border-radius: 15px;
        padding: 25px; text-align: center; 
        margin: 15px 0;
        box-shadow: 0 0 30px rgba(0,0,0,0.5);
    }

    /* BOTÕES: Texto Preto sobre Neon para Leitura Perfeita */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000000 !important; 
        font-weight: 900 !important; 
        border: none !important;
        height: 45px !important;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px #00e676 !important;
        transform: scale(1.02);
    }
    
    /* Ajuste de Inputs para não poluir o visual */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0a0e14 !important;
        color: #00d2ff !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNÇÃO DE SEGURANÇA (LOGIN ISOLADO) ---
def render_login():
    st.markdown('<div class="brand"><span class="u-t">ULTIMATE</span><span class="t-t">TRADER</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<p style='text-align:center; color:#00d2ff; font-size:11px; letter-spacing:2px;'>SYSTEM LOCKED</p>", unsafe_allow_html=True)
        user = st.text_input("USUÁRIO", key="auth_user")
        pw = st.text_input("SENHA", type="password", key="auth_pw")
        if st.button("UNLOCK TERMINAL", use_container_width=True):
            if user == "romildo" and pw == "12345":
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Credenciais Inválidas")

# Bloqueio de Execução
if not st.session_state.logado:
    render_login()
    st.stop()

# --- 3. DASHBOARD PRINCIPAL (SÓ EXECUTA APÓS LOGIN) ---

# Cabeçalho Compacto
st.markdown('<div class="brand"><span class="u-t">ULTIMATE</span><span class="t-t">TRADER</span><span style="background:#00d2ff; color:#000; padding:2px 8px; border-radius:4px; font-size:12px; margin-left:10px; vertical-align:middle;">PRO</span></div>', unsafe_allow_html=True)

# Linha de Métricas (Banca e Placar)
m1, m2 = st.columns(2)
with m1:
    st.markdown(f'<div class="data-card"><small>CURRENT BALANCE</small><br><span style="color:#00e676; font-size:20px; font-weight:bold;">R$ {st.session_state.banca:.2f}</span></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="data-card"><small>SCOREBOARD</small><br><span style="color:#00e676;">W: {st.session_state.wins}</span> | <span style="color:#ff1744;">L: {st.session_state.losses}</span></div>', unsafe_allow_html=True)

# Configurações Escondidas (Clean Look)
with st.expander("⚙️ CONFIGURE TRADE SETTINGS", expanded=False):
    g1, g2, g3 = st.columns(3)
    st.session_state.entrada = g1.number_input("ENTRADA R$:", value=float(st.session_state.entrada))
    st.session_state.payout = g2.number_input("PAYOUT %:", value=int(st.session_state.payout))
    ativo = g3.selectbox("ASSET:", ["EUR/USD (OTC)", "BTC/USDT", "GBP/JPY"])

# --- 4. ENGINE DE SINAL (LÓGICA BASEADA NO MINUTO) ---
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

sinal, cor = "SCANNING...", "#4b5563"
# Probabilidade baseada em confluência simulada
prob = np.random.random()
if prob > 0.65:
    sinal, cor = ("CALL 🟢", "#00e676") if np.random.random() > 0.5 else ("PUT 🔴", "#ff1744")

# Timer de 60 segundos exato
timer = 60 - now.second

st.markdown(f"""
<div class="signal-box">
    <div style="color:rgba(0, 210, 255, 0.5); font-size:10px; letter-spacing:2px; font-weight:bold;">MARKET ANALYZER V4.0</div>
    <h1 style="color:{cor}; font-size:55px; margin:10px 0; font-weight:900; letter-spacing:-2px;">{sinal}</h1>
    <div style="font-size:35px; color:#00d2ff; font-family:monospace; font-weight:bold;">00:{timer:02d}</div>
</div>
""", unsafe_allow_html=True)

# --- 5. CONTROLES DE RESULTADO (Ação Rápida) ---
st.markdown("<br>", unsafe_allow_html=True)
res1, res2, res3 = st.columns([1.5, 1.5, 1])

if res1.button("✅ WIN", use_container_width=True):
    st.session_state.wins += 1
    st.session_state.banca += (st.session_state.entrada * (st.session_state.payout / 100))
    st.rerun()

if res2.button("❌ LOSS", use_container_width=True):
    st.session_state.losses += 1
    st.session_state.banca -= st.session_state.entrada
    st.rerun()

if res3.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

# Loop de atualização (1s)
time.sleep(1)
st.rerun()
