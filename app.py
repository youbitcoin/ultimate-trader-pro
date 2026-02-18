import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from datetime import datetime, timedelta

# =========================================================
# 1. CONFIGURAÇÕES E BANCO DE DADOS
# =========================================================
LINK_PLANILHA = "https://docs.google.com/spreadsheets/d/1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts/edit#gid=0"
SEU_WHATSAPP = "5521998203486" 

# Configuração da Página
st.set_page_config(page_title="Ultimate Trader Pro - Quotex", layout="centered")

# --- BLOQUEIO DE LOGIN (SESSION STATE) ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_nome' not in st.session_state:
    st.session_state.usuario_nome = ""

# --- ESTILO VISUAL QUOTEX DARK ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    h1, h2, h3 { color: #00e676 !important; text-align: center; }
    .signal-card { 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 10px; padding: 25px; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .payout-badge { background-color: rgba(0, 230, 118, 0.1); color: #00e676; padding: 5px 15px; border-radius: 4px; font-weight:
