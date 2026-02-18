import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# =========================================================
# CONFIGURAÇÕES DO PROPRIETÁRIO (CONFERIDO)
# =========================================================
SHEET_ID = "1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts"
SEU_WHATSAPP = "5521998203486" 

# Link de exportação direta (O mais estável)
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ultimate Trader Pro", layout="wide", page_icon="📈")

# Estilo visual neon
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00f2ff; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff00ff; }
    .stMetric { background: rgba(255, 0, 255, 0.05); border: 1px solid #ff00ff; border-radius: 10px; padding: 15px; }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-align: center; }
    .btn-wpp { background-color: #25d366; color: white !important; padding: 12px; border-radius: 8px; 
                text-align: center; text-decoration: none; display: block; font-weight: bold; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'stats' not in st.session_state:
    st.session_state.stats = {"Reversão": {"w": 0, "l": 0}, "Tendência": {"w": 0, "l": 0}, "Rompimento": {"w": 0, "l": 0}}

# --- FUNÇÃO DE VERIFICAÇÃO DE ACESSO (VERSÃO DETETIVE) ---
def verificar_acesso():
    try:
        # Tenta ler a planilha
        df = pd.read_csv(SHEET_URL)
        
        # Limpa os nomes das colunas (tira espaços e põe minúsculo)
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Verifica se as colunas essenciais existem
        colunas_necessarias = ['usuario', 'senha', 'expiracao']
        if not all(col in df.columns for col in colunas_necessarias):
            st.sidebar.warning(f"⚠️ Colunas na planilha: {list(df.columns)}")
            st.sidebar.error("Erro: A planilha deve ter as colunas: usuario, senha, expiracao")
            return pd.DataFrame()

        # Converte data de forma segura
        df['expiracao'] = pd.to_datetime(df['expiracao'], errors='coerce').dt.date
        return df
    except Exception as e:
        st.sidebar.error(f"❌ Erro de conexão: {e}")
        st.sidebar.info("Dica: Verifique se a planilha está 'Publicada na Web' e com acesso público.")
        return pd.DataFrame()

# --- GERADOR DE SINAIS ---
def gerar_sinal(par):
    rsi = np.random.randint(10, 90)
    estrat = np.random.choice(list(st.session_state.stats.keys()))
    if rsi >= 78: return "PUT (VENDA) 🔴", estrat
    if rsi <= 22: return "CALL (COMPRA) 🟢", estrat
    return "AGUARDANDO...", estrat

# --- LÓGICA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown("<h1>⚡ ULTIMATE TRADER PRO</h1>", unsafe_allow_html=True)
    
    df_users = verificar_acesso()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Usuário / ID")
        p = st.text_input("Senha", type="password")
        if st.button("DESBLOQUEAR TERMINAL"):
            if not df_users.empty:
                # Busca o usuário ignorando maiúsculas/minúsculas
                user_match = df_users[df_users['usuario'].astype(str).str.lower() == str(u).lower()]
                
                if not user_match.empty:
                    senha_correta = str(user_match.iloc[0]['senha'])
                    if str(p) == senha_correta:
                        data_exp
