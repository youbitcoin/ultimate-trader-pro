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

# Estilo visual Turbo M1
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00f2ff; }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-align: center; }
    .signal-card { 
        background: rgba(0, 242, 255, 0.05); 
        border: 2px solid #00f2ff; 
        border-radius: 15px; padding: 20px; text-align: center;
    }
    .timer-box { font-size: 24px; font-weight: bold; color: #ffff00; margin: 10px 0; }
    .entry-alert { background-color: #ff00ff; color: white; padding: 10px; border-radius: 5px; font-weight: bold; animation: blinker 1s linear infinite; }
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
    st.markdown("<h1>⚡ ULTIMATE TRADER PRO</h1>")
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

# --- TERMINAL M1 ---
now = datetime.now()
proximo_minuto = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
segundos_para_entrada = (proximo_minuto - now).total_seconds()

st.markdown(f"### Trader: {st.session_state.user} | 🕒 {now.strftime('%H:%M:%S')}")

ativo = st.selectbox("SELECIONE O PAR PARA M1:", ["ESCOLHA O ATIVO", "EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD"])

if ativo != "ESCOLHA O ATIVO":
    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    
    # Lógica de Sinal (Exemplo Baseado em Horário/RSI Simulado)
    np.random.seed(now.minute) # Mantém o sinal fixo durante o mesmo minuto
    direcao = np.random.choice(["CALL 🟢", "PUT 🔴", "AGUARDANDO 🔍"])
    
    st.subheader(f"📊 MONITORANDO: {ativo}")
    st.write(f"Tempo de Operação: **M1 (1 Minuto)**")
    
    if direcao != "AGUARDANDO 🔍":
        st.markdown(f"<h2>SINAL: {direcao}</h2>", unsafe_allow_html=True)
        st.write(f"Entrada para o minuto: **{proximo_minuto.strftime('%H:%M')}**")
        
        # CONTTAGEM REGRESSIVA
        st.markdown(f"<div class='timer-box'>Próxima Vela em: {int(segundos_para_entrada)}s</div>", unsafe_allow_html=True)
        
        # ALERTA DE 2 SEGUNDOS DE DELAY
        if 2 <= segundos_para_entrada <= 5:
            st.markdown("<div class='entry-alert'>🔥 PREPARE A ENTRADA!</div>", unsafe_allow_html=True)
        elif segundos_para_entrada < 2:
            st.markdown("<div class='entry-alert' style='background-color: #00ff00;'>🚀 ENTRE AGORA! (DELAY 2S)</div>", unsafe_allow_html=True)
        else:
            st.info("Aguarde o momento exato da operação...")
    else:
        st.warning("Aguardando melhor oportunidade no gráfico...")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Rodapé
if st.sidebar.button("SAIR"):
    st.session_state.autenticado = False
    st.rerun()

# Atualização rápida para o timer ser preciso
time.sleep(1)
st.rerun()
