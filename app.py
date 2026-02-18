import streamlit as st
import pandas as pd
import numpy as np
import time
import base64
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES BÁSICAS
SEU_WHATSAPP = "5521998203486"
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Função para carregar som local ou URL e transformar em HTML funcional
def play_sound():
    sound_url = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
    sound_html = f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# 2. ESTILO CSS
st.markdown(f"""
<style>
    .block-container {{ padding-top: 3rem !important; }}
    .stApp {{ background: linear-gradient(135deg, #0f172a 0%, #020617 100%); background-attachment: fixed; }}
    
    .logo-text {{
        font-family: 'Arial Black', sans-serif; font-size: 36px;
        text-align: center; margin-bottom: 25px; width: 100%; display: block;
    }}
    .logo-ultimate {{ color: #ffffff; }}
    .logo-trader {{ color: #00e676; text-shadow: 0 0 15px rgba(0,230,118,0.5); }}
    .logo-pro {{ 
        font-size: 16px; background: #00e676; color: #020617; 
        padding: 2px 6px; border-radius: 4px; margin-left: 5px; vertical-align: middle;
    }}

    .dash-container, .signal-card {{
        background: rgba(30, 41, 59, 0.6) !important;
        backdrop-filter: blur(12px); border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; text-align: center; margin-top: 5px;
    }}

    .timer-box {{ font-size: 50px; font-weight: bold; color: #ffffff; font-family: monospace; }}
</style>
""", unsafe_allow_html=True)

# 3. ESTADOS DA SESSÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'aguardando' not in st.session_state: st.session_state.aguardando = False
if 'win' not in st.session_state: st.session_state.win = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'som_tocado' not in st.session_state: st.session_state.som_tocado = False

# 4. TELA DE LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-text"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        u = st.text_input("Usuário / ID")
        p = st.text_input("Senha", type="password")
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if (u == "romildo" or u == "teste") and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. TERMINAL LOGADO
st.markdown('<div class="logo-text"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# Dashboard
total = st.session_state.win + st.session_state.loss
taxa = (st.session_state.win / total * 100) if total > 0 else 0
st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around;">
        <div><div style="font-size:11px;color:#94a3b8">OPS</div><div style="font-size:22px; font-weight:bold; color:white;">{total}</div></div>
        <div><div style="font-size:11px;color:#94a3b8">WINS</div><div style="font-size:22px; font-weight:bold; color:#00e676;">{st.session_state.win}</div></div>
        <div><div style="font-size:11px;color:#94a3b8">LOSSES</div><div style="font-size:22px; font-weight:bold; color:#ff5252;">{st.session_state.loss}</div></div>
        <div><div style="font-size:11px;color:#94a3b8">ASSERT.</div><div style="font-size:22px; font-weight:bold; color:white;">{taxa:.1f}%</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. LÓGICA DE SINAIS
if st.session_state.aguardando:
    st.markdown("<div class='signal-card'><h3>RESULTADO DA OPERAÇÃO</h3>", unsafe_allow_html=True)
    c_w, c_l, c_g, c_p = st.columns(4)
    
    if c_w.button("✅ WIN", use_container_width=True):
        st.session_state.win += 1
        st.session_state.aguardando = False
        st.session_state.som_tocado = False
        st.rerun()
    if c_l.button("❌ LOSS", use_container_width=True):
        st.session_state.loss += 1
        st.session_state.aguardando = False
        st.session_state.som_tocado = False
        st.rerun()
    if c_g.button("🔄 GALE", use_container_width=True):
        st.session_state.som_tocado = False
        st.toast("⚠️ Gale detetado! Aguardando novo sinal...", icon="🔥")
        time.sleep(1)
        st.rerun()
    if c_p.button("⚪ PULAR", use_container_width=True):
        st.session_state.aguardando = False
        st.session_state.som_tocado = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    col_menu1, col_menu2, col_menu3 = st.columns([1, 1, 1])
    tf = col_menu1.selectbox("TEMPO:", ["M1", "M5"])
    estrat = col_menu2.selectbox("ESTRATÉGIA:", ["Turbo (Rápida)", "Moderada", "Sniper (Robusta)"])
    at = col_menu3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BITCOIN (BTC)"])

    if estrat == "Turbo (Rápida)": threshold = 85
    elif estrat == "Sniper (Robusta)": threshold = 98
    else: threshold = 92

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    
    if f >= threshold: sinal, cor = "PUT (VENDA) 🔴", "#ff5252"
    elif f <= (100 - threshold): sinal, cor = "CALL (COMPRA) 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

    # --- LÓGICA DE SOM CORRIGIDA ---
    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        play_sound()
        st.session_state.som_tocado = True
    # -------------------------------

    st.markdown(f"""
    <div class='signal-card'>
        <h2 style="color:#fff !important; font-size:18px; margin-bottom:0;">{at} | {estrat}</h2>
        <h1 style='color:{cor} !important; font-size:38px; margin:5px 0;'>{sinal}</h1>
        <div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.aguardando = True
        time.sleep(1)
        st.rerun()

# 7. BOTÃO SAIR
st.markdown("<br>", unsafe_allow_html=True)
if st.button("SAIR DO SISTEMA", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

time.sleep(1)
st.rerun()
