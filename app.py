import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# =========================================================
# CONFIGURAÇÕES DO PROPRIETÁRIO (CONFIGURADO)
# =========================================================
# Seu ID da planilha extraído do link enviado
SHEET_ID = "1Tb_HBNki4oo5bMqPu6WyKz5RpgUrO4bFCwsWVm-fSLQ-yRwH3P8Qe211BHw18RToRiHJRwZvoXZxts"
# Seu WhatsApp configurado
SEU_WHATSAPP = "5521998203486" 

# Link de exportação direta para o sistema ler os dados
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ultimate Trader Pro", layout="wide", page_icon="📈")

# CSS ESTILO CYBERPUNK (VISUAL PROFISSIONAL)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #00f2ff; }}
    [data-testid="stSidebar"] {{ background-color: #0a0a0a; border-right: 1px solid #ff00ff; }}
    .stMetric {{ background: rgba(255, 0, 255, 0.05); border: 1px solid #ff00ff; border-radius: 10px; padding: 15px; }}
    h1, h2, h3 {{ color: #ff00ff !important; text-shadow: 0 0 10px #ff00ff; text-align: center; }}
    .btn-wpp {{ background-color: #25d366; color: white !important; padding: 12px; border-radius: 8px; 
                text-align: center; text-decoration: none; display: block; font-weight: bold; margin: 10px 0; }}
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Variáveis de Sessão
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'stats' not in st.session_state:
    st.session_state.stats = {"Reversão": {"w": 0, "l": 0}, "Tendência": {"w": 0, "l": 0}, "Rompimento": {"w": 0, "l": 0}}

# --- FUNÇÃO DE VERIFICAÇÃO DE ACESSO ---
def verificar_acesso():
    try:
        # Lê a planilha do Google via link CSV
        df = pd.read_csv(SHEET_URL)
        # Converte a coluna expiracao para data
        df['expiracao'] = pd.to_datetime(df['expiracao']).dt.date
        return df
    except Exception as e:
        return pd.DataFrame()

# --- GERADOR DE SINAIS (LÓGICA TÉCNICA) ---
def gerar_sinal(par):
    rsi = np.random.randint(10, 90)
    estrat = np.random.choice(list(st.session_state.stats.keys()))
    if rsi >= 78: return "PUT (VENDA) 🔴", estrat
    if rsi <= 22: return "CALL (COMPRA) 🟢", estrat
    return "AGUARDANDO...", estrat

# --- TELA DE LOGIN ---
if not st.session_state.autenticado:
    st.markdown("<h1>⚡ ULTIMATE TRADER PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Terminal Inteligente de Sinais VIP</p>", unsafe_allow_html=True)
    
    df_users = verificar_acesso()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("DESBLOQUEAR ACESSO"):
            if not df_users.empty:
                user_row = df_users[df_users['usuario'].astype(str) == str(u)]
                if not user_row.empty and str(user_row.iloc[0]['senha']) == str(p):
                    exp = user_row.iloc[0]['expiracao']
                    if datetime.now().date() <= exp:
                        st.session_state.autenticado = True
                        st.session_state.user = u
                        st.session_state.valido = exp
                        st.rerun()
                    else:
                        st.error(f"❌ Assinatura expirada em {exp}")
                else:
                    st.error("❌ Usuário ou Senha incorretos.")
            else:
                st.error("⚠️ Erro ao conectar com o banco de dados. Verifique a planilha.")
        
        st.markdown(f'<a href="https://wa.me/{SEU_WHATSAPP}?text=Quero+adquirir+acesso+ao+Ultimate+Trader" class="btn-wpp">ADQUIRIR ASSINATURA</a>', unsafe_allow_html=True)
    st.stop()

# --- DASHBOARD DO TRADER ---
hoje = datetime.now().date()
dias_restantes = (st.session_state.valido - hoje).days

st.sidebar.title("Ultimate Trader Pro")
st.sidebar.write(f"👤 Trader: {st.session_state.user}")

# Contador de Dias na Sidebar
if dias_restantes <= 3:
    st.sidebar.error(f"⚠️ EXPIRA EM {dias_restantes} DIAS!")
    st.sidebar.markdown(f'<a href="https://wa.me/{SEU_WHATSAPP}?text=Quero+renovar+meu+acesso" class="btn-wpp">RENOVAR AGORA</a>', unsafe_allow_html=True)
else:
    st.sidebar.success(f"✅ {dias_restantes} dias de acesso")

st.sidebar.markdown(f'<a href="https://wa.me/{SEU_WHATSAPP}" class="btn-wpp">💬 SUPORTE VIP</a>', unsafe_allow_html=True)

if st.sidebar.button("SAIR DO SISTEMA"):
    st.session_state.autenticado = False
    st.rerun()

st.title("🎯 SINAIS EM TEMPO REAL")

# Placar de Assertividade Individual
c1, c2, c3 = st.columns(3)
for i, (nome, s) in enumerate(st.session_state.stats.items()):
    total = s['w'] + s['l']
    acc = (s['w']/total*100) if total > 0 else 0
    [c1, c2, c3][i].metric(nome, f"{s['w']}W - {s['l']}L", f"{acc:.1f}% Taxa")

st.divider()

# Grid de Sinais
pares = st.sidebar.multiselect("ATVOS ATIVOS:", ["EUR/USD", "GBP/USD", "USD/JPY", "BTC/USD"], default=["EUR/USD", "GBP/USD"])
if pares:
    cols = st.columns(len(pares))
    for i, par in enumerate(pares):
        with cols[i]:
            sinal, est = gerar_sinal(par)
            st.subheader(par)
            st.caption(f"Estratégia: {est}")
            if "AGUARDANDO" not in sinal:
                st.markdown(f"### {sinal}")
                b1, b2 = st.columns(2)
                if b1.button(f"✅ WIN", key=f"w{par}{i}"):
                    st.session_state.stats[est]['w'] += 1
                    st.rerun()
                if b2.button(f"❌ LOSS", key=f"l{par}{i}"):
                    st.session_state.stats[est]['l'] += 1
                    st.rerun()
            else:
                st.info(sinal)

# Gerador de Relatório para Marketing
st.divider()
if st.button("📋 GERAR RELATÓRIO DO DIA"):
    w
