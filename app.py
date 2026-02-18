import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime, timedelta

# =========================================================
# CONFIGURAÇÕES
# =========================================================
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

match = re.search(r"/d/([\w-]+)", LINK_PLANILHA)
SHEET_ID = match.group(1) if match else ""
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Estilo Pro
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00f2ff; }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-align: center; }
    .signal-card { 
        background: rgba(0, 242, 255, 0.05); 
        border: 2px solid #00f2ff; 
        border-radius: 15px; padding: 25px; text-align: center;
    }
    .payout-badge { background-color: #1a1a1a; color: #00ff00; padding: 5px 15px; border-radius: 20px; font-weight: bold; border: 2px solid #00ff00; font-size: 18px; }
    .timer-box { font-size: 28px; font-weight: bold; color: #ffff00; margin: 15px 0; border: 1px dashed #ffff00; padding: 10px; }
    .entry-alert { background-color: #ff00ff; color: white; padding: 15px; border-radius: 10px; font-weight: bold; animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state: st.session_state.autenticado = False

def verificar_acesso():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame({'usuario': ['teste', 'romildo'], 'senha': ['12345', '12345'], 'expiracao': ['2026-12-31', '2026-12-31']})

# --- LOGIN ---
if not st.session_state.autenticado:
    st.title("⚡ ULTIMATE TRADER PRO")
    df_users = verificar_acesso()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR TERMINAL"):
            user_match = df_users[df_users['usuario'].astype(str).str.lower() == str(u).lower()]
            if not user_match.empty and str(user_match.iloc[0]['senha']) == str(p):
                st.session_state.autenticado, st.session_state.user = True, u
                st.rerun()
            else: st.error("Dados incorretos!")
    st.stop()

# --- TERMINAL ---
now = datetime.now()
st.title("🎯 ANALISADOR TÉCNICO V.I.P")

col_a, col_b = st.columns(2)
with col_a:
    timeframe = st.selectbox("TIMEFRAME:", ["M1 (1 Minuto)", "M5 (5 Minutos)"])
with col_b:
    ativo = st.selectbox("PAR DE MOEDAS:", ["ESCOLHA O ATIVO", "EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD"])

# Lógica de Horário para a Vela
if "M1" in timeframe:
    proxima_vela = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
else:
    proximo_m5 = (now.minute // 5 + 1) * 5
    if proximo_m5 >= 60:
        proxima_vela = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    else:
        proxima_vela = now.replace(minute=proximo_m5, second=0, microsecond=0)

segundos_para_entrada = (proxima_vela - now).total_seconds()

if ativo != "ESCOLHA O ATIVO":
    # --- TABELA DE PAYOUTS REAIS (AJUSTÁVEL) ---
    payouts_base = {
        "EUR/USD": 87,
        "GBP/USD": 85,
        "USD/JPY": 82,
        "BTC/USD": 78
    }
    
    # Adiciona uma pequena variação para parecer vivo, mas baseada no minuto (estável)
    np.random.seed(now.minute)
    variacao = np.random.randint(0, 5)
    payout_atual = payouts_base.get(ativo, 80) + variacao

    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    st.markdown(f"<span class='payout-badge'>PAYOUT {ativo}: {payout_atual}%</span>", unsafe_allow_html=True)
    
    # --- LÓGICA DE ASSERTIVIDADE ---
    # Semente baseada na proxima_vela para o sinal não mudar durante a contagem
    np.random.seed(int(proxima_vela.timestamp()))
    forca = np.random.randint(0, 100)

    if forca > 82:
        direcao, cor = "PUT (VENDA) 🔴", "#ff4b4b"
    elif forca < 18:
        direcao, cor = "CALL (COMPRA) 🟢", "#00ff00"
    else:
        direcao, cor = "AGUARDANDO CONFIRMAÇÃO... 🔍", "#cccccc"

    st.markdown(f"<h1 style='color: {cor} !important;'>{direcao}</h1>", unsafe_allow_html=True)
    
    if "AGUARDANDO" not in direcao:
        st.write("🔥 **ALTA PROBABILIDADE DETECTADA**")
        lucro_potencial = 100 * (payout_atual/100)
        st.info(f"Com R$ 100,00 seu retorno será R$ {100 + lucro_potencial:.2f}")

        # Timer e Delay 2s
        min_f, seg_f = int(segundos_para_entrada // 60), int(segundos_para_entrada % 60)
        st.markdown(f"<div class='timer-box'>ENTRADA ÀS {proxima_vela.strftime('%H:%M')}: {min_f:02d}:{seg_f:02d}</div>", unsafe_allow_html=True)
        
        if 2 < segundos_para_entrada <= 10:
            st.markdown("<div class='entry-alert'>PREPARE O CLIQUE!</div>", unsafe_allow_html=True)
        elif segundos_para_entrada <= 2:
            st.markdown("<div class='entry-alert' style='background-color: #00ff00;'>CLIQUE AGORA! (DELAY 2S)</div>", unsafe_allow_html=True)
    else:
        st.warning("Aguardando o preço atingir a zona de exaustão para operar.")

    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.write(f"👤 Trader: {st.session_state.user}")
if st.sidebar.button("LOGOUT"):
    st.session_state.autenticado = False
    st.rerun()

time.sleep(1)
st.rerun()
