import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime

# =========================================================
# 1. CONFIGURAÇÃO - COLOQUE O LINK DA PLANILHA ABAIXO
# =========================================================
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

# Extração automática do ID da planilha
match = re.search(r"/d/([\w-]+)", LINK_PLANILHA)
SHEET_ID = match.group(1) if match else ""
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Ultimate Trader Pro", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00f2ff; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #ff00ff; }
    h1, h2, h3 { color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-align: center; }
    .btn-wpp { background-color: #25d366; color: white !important; padding: 12px; border-radius: 8px; 
                text-align: center; text-decoration: none; display: block; font-weight: bold; margin: 10px 0; }
    .stMetric { background: rgba(255, 0, 255, 0.05); border: 1px solid #ff00ff; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'stats' not in st.session_state:
    st.session_state.stats = {"Reversão": {"w": 0, "l": 0}, "Tendência": {"w": 0, "l": 0}, "Rompimento": {"w": 0, "l": 0}}

# --- FUNÇÃO DE ACESSO COM PLANO B ---
def verificar_acesso():
    try:
        # Tenta ler do Google Sheets
        df = pd.read_csv(SHEET_URL)
        df.columns = [str(c).strip().lower() for c in df.columns]
        df['expiracao'] = pd.to_datetime(df['expiracao'], errors='coerce').dt.date
        return df
    except Exception as e:
        # PLANO B: Se a planilha der erro, libera este login fixo para não travar o sistema
        return pd.DataFrame({
            'usuario': ['teste', 'admin'],
