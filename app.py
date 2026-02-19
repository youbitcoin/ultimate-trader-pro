import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DE TELA (WIDE PARA CABER TUDO)
st.set_page_config(page_title="Ultimate Trader Pro", layout="wide", initial_sidebar_state="collapsed")

# Inicialização Blindada
if 'logado' not in st.session_state:
    st.session_state.update({
        'logado': False, 'banca': 1000.0, 'entrada': 10.0, 
        'payout': 87, 'wins': 0, 'losses': 0
    })

# FUNDO CYBERPUNK ORIGINAL
img_background = "https://w0.peakpx.com/wallpaper/705/503/HD-wallpaper-cyberpunk-trading-desk-futuristic-city-view-trading-setup-neon-lights-data-screens-digital-art.jpg"

# 2. CSS RESTAURADO (ELEMENTOS GRANDES)
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.9), rgba(0, 5, 15, 0.9)), url("{img_background}");
        background-size: cover; background-attachment: fixed;
    }}
    .logo-box {{ text-align: center; padding: 20px 0; }}
    .u-text {{ color: #FFFFFF; font-size: 45px; font-weight: 900; }}
    .t-text {{ color: #00e676; font-size: 45px; font-weight: 900; text-shadow: 0 0 15px #00e676; }}
    .p-badge {{ background: #00d2ff; color: #000; padding: 2px 10px; border-radius: 4px; font-size: 18px; margin-left: 10px; font-weight: 800; }}
    
    .banca-card {{ 
        background: rgba(0, 210, 255, 0.1); color: #00e676; padding: 20px; border-radius: 12px; 
        font-size: 28px; font-weight: 800; border: 1px solid #00d2ff; text-align: center;
    }}
    
    .signal-card {{ 
        background: rgba(5, 10, 25, 0.95); border-radius: 20px; padding: 40px; text-align: center; 
        border: 2px solid #00d2ff; box-shadow: 0 0 40px rgba(0,0,0,1);
    }}
    
    /* BOTÕES COM TEXTO PRETO */
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000 !important; font-weight: 900 !important; border: none !important;
        height: 50px !important; font-size: 16px !important; text-transform: uppercase;
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE BLOQUEIO (RESOLVE O VAZAMENTO DO DASHBOARD) ---
# Criamos um container vazio que só será preenchido se logado
placeholder = st.empty()

if not st.session_state.logado:
    with placeholder.container():
        st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)
        _, col_login, _ = st.columns([1, 1.2, 1])
        with col_login:
            st.markdown("<div style='background:rgba(0,0,0,0.5); padding:30px; border-radius:15px; border:1px solid #00d2ff;'>", unsafe_allow_html=True)
            u = st.text_input("USUÁRIO", placeholder="Seu login...")
            p = st.text_input("SENHA", type="password", placeholder="Sua senha...")
            if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
                if u == "romildo" and p == "12345":
                    st.session_state.logado = True
                    st.rerun()
                else:
                    st.error("Acesso Negado")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop() # Mata o processo aqui se não estiver logado

# --- 4. DASHBOARD COMPLETO (SÓ CARREGA SE LOGADO) ---
with placeholder.container():
    st.markdown('<div class="logo-box"><span class="u-text">ULTIMATE</span><span class="t-text">TRADER</span><span class="p-badge">PRO</span></div>', unsafe_allow_html=True)

    # Status Bar
    s1, s2 = st.columns([2, 1])
    with s1:
        st.markdown(f'<div class="banca-card">SALDO OPERACIONAL: R$ {st.session_state.banca:.2f}</div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="banca-card" style="border-color:#00e676; color:#fff;">WINS: {st.session_state.wins} | LOSS: {st.session_state.losses}</div>', unsafe_allow_html=True)

    # Inputs de Gestão e Martingale (O que você queria de volta)
    st.markdown("<br>", unsafe_allow_html=True)
    g1, g2, g3, g4 = st.columns(4)
    st.session_state.entrada = g1.number_input("VALOR ENTRADA:", value=float(st.session_state.entrada))
    st.session_state.payout = g2.number_input("PAYOUT %:", value=int(st.session_state.payout))
    ativo = g3.selectbox("ATIVO DISPONÍVEL:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USDT"])
    m_gale = g4.selectbox("SISTEMA MARTINGALE:", ["Nenhum", "Gale 1 (2.2x)", "Gale 2 (4.4x)"])

    # Engine de Sinal
    now = datetime.now()
    seed = int(now.timestamp() / 60)
    np.random.seed(seed)
    sinal, cor = "ANALISANDO...", "#4b5563"

    if np.random.random() > 0.6:
        if np.random.random() > 0.5: sinal, cor = "CALL 🟢", "#00e676"
        else: sinal, cor = "PUT 🔴", "#ff1744"

    timer = 60 - now.second
    multiplicador = 2.2 if "Gale 1" in m_gale else (4.4 if "Gale 2" in m_gale else 1.0)
    valor_sugerido = st.session_state.entrada * multiplicador

    # Card de Sinal Central
    st.markdown(f"""
    <div class="signal-card">
        <div style="color:#00d2ff; font-size:12px; letter-spacing:3px;">QUANTUM ENGINE ACTIVE | {ativo}</div>
        <h1 style="color:{cor}; font-size:90px; margin:10px 0; font-weight:900; text-shadow: 0 0 30px {cor};">{sinal}</h1>
        <div style="font-size:40px; color:#00d2ff; font-family:monospace; font-weight:bold;">00:{timer:02d}</div>
        <div style="margin-top:15px; font-size:16px; color:#888;">MODO: <b>{m_gale}</b> | SUGERIDO: <span style="color:#00e676;">R$ {valor_sugerido:.2f}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Botões de Controle
    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 1, 1])
    if b1.button("✅ REGISTRAR WIN", use_container_width=True):
        st.session_state.wins += 1
        st.session_state.banca += (st.session_state.entrada * (st.session_state.payout / 100))
        st.rerun()
    if b2.button("❌ REGISTRAR LOSS", use_container_width=True):
        st.session_state.losses += 1
        st.session_state.banca -= st.session_state.entrada
        st.rerun()
    if b3.button("LOGOUT / SAIR", use_container_width=True):
        st.session_state.logado = False
        st.rerun()

    time.sleep(1)
    st.rerun()
