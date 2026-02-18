import streamlit as st
import pandas as pd
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES BÁSICAS E PERSISTÊNCIA
SEU_WHATSAPP = "5521998203486"
ARQUIVO_DADOS = "historico_trader.csv"

st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Função para carregar dados salvos
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        df = pd.read_csv(ARQUIVO_DADOS)
        return int(df['win'][0]), int(df['loss'][0])
    return 0, 0

# Função para salvar dados
def salvar_dados(w, l):
    df = pd.DataFrame({'win': [w], 'loss': [l]})
    df.to_csv(ARQUIVO_DADOS, index=False)

# Inicializa o estado com os dados do arquivo
w_salvo, l_salvo = carregar_dados()

if 'win' not in st.session_state: st.session_state.win = w_salvo
if 'loss' not in st.session_state: st.session_state.loss = l_salvo
if 'logado' not in st.session_state: st.session_state.logado = False
if 'aguardando' not in st.session_state: st.session_state.aguardando = False
if 'som_tocado' not in st.session_state: st.session_state.som_tocado = False

# 2. ESTILO CSS
st.markdown(f"""
<style>
    .block-container {{ padding-top: 3rem !important; }}
    .stApp {{ background: linear-gradient(135deg, #0f172a 0%, #020617 100%); background-attachment: fixed; }}
    .logo-text {{ font-family: 'Arial Black', sans-serif; font-size: 36px; text-align: center; margin-bottom: 25px; width: 100%; display: block; }}
    .logo-ultimate {{ color: #ffffff; }}
    .logo-trader {{ color: #00e676; text-shadow: 0 0 15px rgba(0,230,118,0.5); }}
    .logo-pro {{ font-size: 16px; background: #00e676; color: #020617; padding: 2px 6px; border-radius: 4px; margin-left: 5px; vertical-align: middle; }}
    .dash-container, .signal-card {{ background: rgba(30, 41, 59, 0.6) !important; backdrop-filter: blur(12px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); padding: 20px; text-align: center; margin-top: 5px; }}
    .timer-box {{ font-size: 50px; font-weight: bold; color: #ffffff; font-family: monospace; }}
</style>
""", unsafe_allow_html=True)

# 3. TELA DE LOGIN
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

# 4. TERMINAL LOGADO
st.markdown('<div class="logo-text"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# Placar (Lendo da Session State que foi alimentada pelo arquivo)
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

# 5. LÓGICA DE SINAIS E RESULTADOS
if st.session_state.aguardando:
    st.markdown("<div class='signal-card'><h3>RESULTADO DA OPERAÇÃO</h3>", unsafe_allow_html=True)
    c_w, c_l, c_g, c_p = st.columns(4)
    
    if c_w.button("✅ WIN", use_container_width=True):
        st.session_state.win += 1
        salvar_dados(st.session_state.win, st.session_state.loss) # SALVA NO ARQUIVO
        st.session_state.aguardando = False
        st.session_state.som_tocado = False
        st.rerun()
        
    if c_l.button("❌ LOSS", use_container_width=True):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss) # SALVA NO ARQUIVO
        st.session_state.aguardando = False
        st.session_state.som_tocado = False
        st.rerun()

    if c_g.button("🔄 GALE", use_container_width=True):
        st.session_state.som_tocado = False
        st.rerun()

    if c_p.button("⚪ PULAR", use_container_width=True):
        st.session_state.aguardando = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Interface normal de sinais...
    c1, c2, c3 = st.columns(3)
    tf = c1.selectbox("TEMPO:", ["M1", "M5"])
    estrat = c2.selectbox("ESTRATÉGIA:", ["Turbo (Rápida)", "Moderada", "Sniper (Robusta)"])
    at = c3.selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "BITCOIN (BTC)"])

    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    np.random.seed(int(prox.timestamp()))
    f = np.random.randint(0, 100)
    threshold = 85 if estrat == "Turbo (Rápida)" else 98 if estrat == "Sniper (Robusta)" else 92
    
    if f >= threshold: sinal, cor = "PUT (VENDA) 🔴", "#ff5252"
    elif f <= (100 - threshold): sinal, cor = "CALL (COMPRA) 🟢", "#00e676"
    else: sinal, cor = "ANALISANDO... 🔎", "#94a3b8"

    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        st.markdown(f'<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-3.mp3" type="audio/mp3"></audio>', unsafe_allow_html=True)
        st.session_state.som_tocado = True

    st.markdown(f"<div class='signal-card'><h2>{at}</h2><h1 style='color:{cor} !important;'>{sinal}</h1><div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div></div>", unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.aguardando = True
        st.rerun()

# 6. BOTÃO SAIR E RESET
col_f1, col_f2 = st.columns(2)
if col_f1.button("SAIR DO SISTEMA"):
    st.session_state.logado = False
    st.rerun()

if col_f2.button("LIMPAR HISTÓRICO"):
    salvar_dados(0, 0)
    st.session_state.win = 0
    st.session_state.loss = 0
    st.rerun()

time.sleep(1)
st.rerun()
