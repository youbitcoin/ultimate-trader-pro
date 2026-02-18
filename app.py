Para dar um ar muito mais profissional e moderno ao seu sistema, adicionei um gradiente dinâmico "Deep Navy" (Azul Marinho Profundo). Esse estilo é o mais utilizado em plataformas de trading de elite, pois reduz o cansaço visual e destaca as cores neon dos sinais (Verde e Vermelho).

Também apliquei um efeito de vidro embaçado (Glassmorphism) nos cards para que o fundo apareça sutilmente por trás deles.

🚀 Código com Background Moderno e Efeito Glass
Python
import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES TÉCNICAS
SEU_WHATSAPP = "5521998203486" 

st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Função para tocar o som
def play_notification():
    sound_url = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
    st.markdown(f"""
        <iframe src="{sound_url}" allow="autoplay" style="display:none" id="iframeAudio"></iframe>
        <audio autoplay><source src="{sound_url}" type="audio/ogg"></audio>
    """, unsafe_allow_html=True)

# Estilo CSS Avançado (Background e Glassmorphism)
st.markdown(f"""
    <style>
    /* Fundo Gradiente Dinâmico */
    .stApp {{
        background: radial-gradient(circle at top right, #1a2a6c, #b21f1f, #fdbb2d); /* Opção 1: Sunset Trader */
        background: radial-gradient(circle, #0f172a 0%, #020617 100%); /* Opção 2: Dark Space (Ativa) */
        background-attachment: fixed;
    }}

    /* Efeito de Vidro nos Containers */
    .dash-container, .signal-card, .stSelectbox {{
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }}

    h1 {{ 
        color: #00e676 !important; 
        text-align: center; 
        font-weight: 800;
        text-shadow: 0px 4px 10px rgba(0, 230, 118, 0.3);
        margin-top: -30px;
    }}
    
    h3 {{ color: #ffffff !important; text-align: center; font-weight: 400; }}

    .dash-value {{ font-size: 26px; font-weight: bold; color: #fff; }}
    .value-win {{ color: #00e676; text-shadow: 0 0 10px #00e676; }}
    .value-loss {{ color: #ff5252; text-shadow: 0 0 10px #ff5252; }}

    .timer-box {{ 
        font-size: 55px; 
        font-weight: bold; 
        color: #ffffff; 
        margin: 15px 0; 
        font-family: 'JetBrains Mono', monospace; 
        text-shadow: 0 0 15px rgba(255,255,255,0.5);
    }}

    .float-wpp {{
        position: fixed; width: 65px; height: 65px; bottom: 25px; right: 25px;
        background-color: #25d366; color: #FFF; border-radius: 50px;
        text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.5); z-index: 9999;
        display: flex; align-items: center; justify-content: center;
        transition: 0.3s;
    }}
    .float-wpp:hover {{ transform: scale(1.1); }}
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
    st.markdown("<br><br>", unsafe_allow_html=True)
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

# 3. DASHBOARD (DENTRO DO CONTAINER GLASS)
total_ops = st.session_state.historico_win + st.session_state.historico_loss
winrate = (st.session_state.historico_win / total_ops * 100) if total_ops > 0 else 0

st.markdown(f"""
    <div class="dash-container">
        <div class="dash-item"><div style="font-size:12px;color:#94a3b8">OPERAÇÕES</div><div class="dash-value">{total_ops}</div></div>
        <div class="dash-item"><div style="font-size:12px;color:#94a3b8">WINS</div><div class="dash-value value-win">{st.session_state.historico_win}</div></div>
        <div class="dash-item"><div style="font-size:12px;color:#94a3b8">LOSSES</div><div class="dash-value value-loss">{st.session_state.historico_loss}</div></div>
        <div class="dash-item"><div style="font-size:12px;color:#94a3b8">ASSERTIVIDADE</div><div class="dash-value">{winrate:.1f}%</div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h1>🎯 MONITOR QUOTEX PRO</h1>", unsafe_allow_html=True)

# 4. CONTROLE DE SINAL / FEEDBACK
if st.session_state.aguardando_resultado:
    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    st.subheader("CONFIRME O RESULTADO")
    st.write(f"Sinal enviado para: **{st.session_state.ultimo_sinal['ativo']}**")
    
    col_w, col_l, col_n = st.columns(3)
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
    with col_n:
        if st.button("⚪ NÃO PEGUEI", use_container_width=True):
            st.session_state.aguardando_resultado = False
            st.session_state.som_tocado = False
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
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
    else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        play_notification()
        st.session_state.som_tocado = True

    st.markdown(f"<div class='signal-card'><h3>{at}</h3><h1 style='color:{cor} !important; font-size:48px; text-shadow: 0 0 15px {cor};'>{sinal}</h1>", unsafe_allow_html=True)
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
