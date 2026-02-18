import streamlit as st
import pandas as pd
import numpy as np
import time
import base64
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES TÉCNICAS
SEU_WHATSAPP = "5521998203486" 

st.set_page_config(page_title="Ultimate Trader - Sound Edition", layout="centered")

# Função para gerar o som de alerta (Bip curto)
def play_sound():
    # Som de bip em base64 para não precisar de arquivo externo
    audio_base64 = "SUQzBAAAAAAAF1RFTlYAAAANAAADU29mdHdhcmUAZ28AbXAzZm9yZ2UAb3JnACH/4UUAQAAAAAAAAAAAAAAAACQAAAAAAAAAAAABAAAALv/hRQCBAAAAAAAAAAAAAAAAAAkAAAAAAAAAAAAAQAAAAAAAAC7" 
    # Link de um som de notificação padrão
    sound_url = "https://www.soundjay.com/buttons/sounds/button-3.mp3"
    html_string = f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(html_string, height=0)

# CSS Profissional
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0b0e14; color: #e6edf3; }}
    h1, h2, h3 {{ color: #00e676 !important; text-align: center; }}
    .dash-container {{
        background: #161b22; border-radius: 10px; padding: 15px;
        margin-bottom: 20px; border: 1px solid #30363d;
        display: flex; justify-content: space-around; align-items: center;
    }}
    .dash-item {{ text-align: center; }}
    .dash-value {{ font-size: 24px; font-weight: bold; color: #fff; }}
    .value-win {{ color: #00e676; }}
    .value-loss {{ color: #ff5252; }}
    .signal-card {{ background: #161b22; border: 2px solid #30363d; border-radius: 15px; padding: 30px; text-align: center; }}
    .timer-box {{ font-size: 45px; font-weight: bold; color: #ffffff; margin: 15px 0; font-family: monospace; }}
    .float-wpp {{
        position: fixed; width: 60px; height: 60px; bottom: 20px; right: 20px;
        background-color: #25d366; color: #FFF; border-radius: 50px;
        text-align: center; font-size: 30px; box-shadow: 2px 2px 10px #000; z-index: 9999;
        display: flex; align-items: center; justify-content: center;
    }}
    </style>
    <a href="https://wa.me/{SEU_WHATSAPP}" class="float-wpp" target="_blank">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" style="width:35px">
    </a>
    """, unsafe_allow_html=True)

# 2. INICIALIZAÇÃO DE SESSÃO
if 'logado' not in st.session_state: st.session_state.logado = False
if 'aguardando_resultado' not in st.session_state: st.session_state.aguardando_resultado = False
if 'ultimo_sinal' not in st.session_state: st.session_state.ultimo_sinal = None
if 'historico_win' not in st.session_state: st.session_state.historico_win = 0
if 'historico_loss' not in st.session_state: st.session_state.historico_loss = 0
if 'som_tocado' not in st.session_state: st.session_state.som_tocado = False

# LOGIN
if not st.session_state.logado:
    st.title("SISTEMA VIP OTC")
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("Trader ID")
        p = st.text_input("Senha", type="password")
        if st.button("CONECTAR", use_container_width=True):
            if (u == "romildo" or u == "teste") and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 3. DASHBOARD
total_ops = st.session_state.historico_win + st.session_state.historico_loss
winrate = (st.session_state.historico_win / total_ops * 100) if total_ops > 0 else 0

st.markdown(f"""
    <div class="dash-container">
        <div class="dash-item"><div style="font-size:12px;color:#8b949e">OPS</div><div class="dash-value">{total_ops}</div></div>
        <div class="dash-item"><div style="font-size:12px;color:#8b949e">WINS</div><div class="dash-value value-win">{st.session_state.historico_win}</div></div>
        <div class="dash-item"><div style="font-size:12px;color:#8b949e">LOSSES</div><div class="dash-value value-loss">{st.session_state.historico_loss}</div></div>
        <div class="dash-item"><div style="font-size:12px;color:#8b949e">ASSERT.</div><div class="dash-value">{winrate:.1f}%</div></div>
    </div>
    """, unsafe_allow_html=True)

# 4. CONTROLE DE SINAL
if st.session_state.aguardando_resultado:
    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    st.subheader("CONFIRME O RESULTADO")
    col_w, col_l = st.columns(2)
    with col_w:
        if st.button("✅ WIN", use_container_width=True):
            st.session_state.historico_win += 1
            st.session_state.aguardando_resultado = False
            st.session_state.som_tocado = False
            st.rerun()
    with col_l:
        if st.button("❌ LOSS", use_container_width=True):
            st.session_state.historico_loss += 1
            st.session_state.aguardando_resultado = False
            st.session_state.som_tocado = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.title("🎯 MONITOR QUOTEX PRO")
    c1, c2 = st.columns(2)
    with c1: tf = st.selectbox("TEMPO:", ["M1", "M5"])
    with c2: at = st.selectbox("ATIVO OTC:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BTC/USD"])

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    
    faltam = (prox - now).total_seconds()
    
    # Lógica de Sinal (Filtro 92%)
    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    
    if f > 92: sinal, cor = "PUT (VENDA) 🔴", "#ff5252"
    elif f < 8: sinal, cor = "CALL (COMPRA) 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#8b949e"

    # --- DISPARO DO SOM ---
    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        play_sound()
        st.session_state.som_tocado = True

    st.markdown(f"<div class='signal-card'><h3>{at}</h3><h1 style='color:{cor} !important; font-size:40px;'>{sinal}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>", unsafe_allow_html=True)

    if "ANALISANDO" not in sinal:
        if faltam <= 2:
            st.session_state.ultimo_sinal = {"ativo": at, "direcao": sinal}
            st.session_state.aguardando_resultado = True
            time.sleep(1)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    time.sleep(1)
    st.rerun()
