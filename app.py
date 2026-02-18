import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime

# =========================================================
# CONFIGURAÇÕES
# =========================================================
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

match = re.search(r"/d/([\w-]+)", LINK_PLANILHA)
SHEET_ID = match.group(1) if match else ""
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

# Estilo visual Cyberpunk
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00f2ff; }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-align: center; }
    .stSelectbox label { color: #00f2ff !important; font-weight: bold; }
    .signal-card { 
        background: rgba(255, 0, 255, 0.05); 
        border: 2px solid #ff00ff; 
        border-radius: 15px; 
        padding: 30px; 
        text-align: center;
        margin-top: 20px;
    }
    .btn-wpp { background-color: #25d366; color: white !important; padding: 12px; border-radius: 8px; 
                text-align: center; text-decoration: none; display: block; font-weight: bold; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state: st.session_state.autenticado = False

def verificar_acesso():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        df['expiracao'] = pd.to_datetime(df['expiracao'], errors='coerce').dt.date
        return df
    except:
        return pd.DataFrame({
            'usuario': ['teste', 'romildo'],
            'senha': ['12345', '12345'],
            'expiracao': [datetime(2026, 12, 31).date(), datetime(2026, 12, 31).date()]
        })

# --- LOGIN ---
if not st.session_state.autenticado:
    st.markdown("<h1>⚡ ULTIMATE TRADER PRO</h1>")
    df_users = verificar_acesso()
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ENTRAR NO TERMINAL"):
            user_match = df_users[df_users['usuario'].astype(str).str.lower() == str(u).lower()]
            if not user_match.empty and str(user_match.iloc[0]['senha']) == str(p):
                st.session_state.autenticado, st.session_state.user = True, u
                st.rerun()
            else: st.error("Dados incorretos!")
        st.markdown(f'<a href="https://wa.me/{SEU_WHATSAPP}" class="btn-wpp">SUPORTE / COMPRAR</a>', unsafe_allow_html=True)
    st.stop()

# --- TERMINAL DE ANÁLISE ÚNICA ---
st.markdown(f"### Bem-vindo, {st.session_state.user} 💎")

# Menu de Escolha do Ativo
ativo_selecionado = st.selectbox(
    "QUAL ATIVO DESEJA ANALISAR AGORA?",
    ["ESCOLHA UM ATIVO", "EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD", "ETH/USD"]
)

if ativo_selecionado != "ESCOLHA UM ATIVO":
    st.markdown(f"<div class='signal-card'>", unsafe_allow_html=True)
    st.markdown(f"<h2>📊 ANALISANDO: {ativo_selecionado}</h2>", unsafe_allow_html=True)
    
    # Simulação de análise técnica
    rsi = np.random.randint(10, 90)
    progresso = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progresso.progress(i + 1)

    if rsi > 70:
        st.markdown("<h1 style='color: #ff4b4b !important;'>🔴 SINAL: PUT (VENDA)</h1>", unsafe_allow_html=True)
        st.markdown("### ⏳ Expiração: 5 Minutos")
    elif rsi < 30:
        st.markdown("<h1 style='color: #00ff00 !important;'>🟢 SINAL: CALL (COMPRA)</h1>", unsafe_allow_html=True)
        st.markdown("### ⏳ Expiração: 5 Minutos")
    else:
        st.info("🔎 O mercado está lateralizado. Aguardando confirmação...")
    
    st.markdown(f"</div>", unsafe_allow_html=True)
    
    if st.button("🔄 REFRESH ANÁLISE"):
        st.rerun()
else:
    st.warning("Selecione um par de moedas acima para iniciar o monitoramento em tempo real.")

# Rodapé e Logout
st.sidebar.markdown("---")
if st.sidebar.button("SAIR DO SISTEMA"):
    st.session_state.autenticado = False
    st.rerun()

# Atualização automática suave
time.sleep(10)
st.rerun()
