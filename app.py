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

# Extração do ID
match = re.search(r"/d/([\w-]+)", LINK_PLANILHA)
SHEET_ID = match.group(1) if match else ""
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="Ultimate Trader Pro", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00f2ff; }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-align: center; }
    .btn-wpp { background-color: #25d366; color: white !important; padding: 12px; border-radius: 8px; 
                text-align: center; text-decoration: none; display: block; font-weight: bold; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'stats' not in st.session_state:
    st.session_state.stats = {"Reversão": {"w": 0, "l": 0}, "Tendência": {"w": 0, "l": 0}, "Rompimento": {"w": 0, "l": 0}}

# --- FUNÇÃO DE ACESSO REVISADA ---
def verificar_acesso():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        df['expiracao'] = pd.to_datetime(df['expiracao'], errors='coerce').dt.date
        return df
    except:
        # PLANO B: Login de emergência se a planilha falhar
        return pd.DataFrame({
            'usuario': ['teste', 'admin'],
            'senha': ['12345', 'admin123'],
            'expiracao': [datetime(2026, 12, 31).date(), datetime(2026, 12, 31).date()]
        })

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown("<h1>⚡ ULTIMATE TRADER PRO</h1>", unsafe_allow_html=True)
    df_users = verificar_acesso()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ENTRAR NO TERMINAL"):
            user_match = df_users[df_users['usuario'].astype(str).str.lower() == str(u).lower()]
            if not user_match.empty and str(user_match.iloc[0]['senha']) == str(p):
                data_exp = user_match.iloc[0]['expiracao']
                if data_exp and datetime.now().date() <= data_exp:
                    st.session_state.autenticado, st.session_state.user, st.session_state.valido = True, u, data_exp
                    st.rerun()
                else: st.error("Assinatura vencida!")
            else: st.error("Dados incorretos!")
        st.markdown(f'<a href="https://wa.me/{SEU_WHATSAPP}" class="btn-wpp">COMPRAR ACESSO</a>', unsafe_allow_html=True)
    st.stop()

# --- ÁREA LOGADA ---
st.title("🎯 SINAIS EM TEMPO REAL")
st.sidebar.title("Ultimate Trader")
st.sidebar.write(f"👤 {st.session_state.user}")

if st.sidebar.button("SAIR"):
    st.session_state.autenticado = False
    st.rerun()

# Simulação de sinais
pares = ["EUR/USD", "GBP/USD", "BTC/USD"]
cols = st.columns(3)
for i, par in enumerate(pares):
    with cols[i]:
        st.subheader(par)
        if np.random.randint(0, 10) > 7:
            st.markdown("### 🟢 CALL")
        elif np.random.randint(0, 10) < 3:
            st.markdown("### 🔴 PUT")
        else:
            st.info("Aguardando...")

time.sleep(5)
st.rerun()
