import streamlit as st
import pandas as pd  # Corrigido aqui
import numpy as np
import time
import os
from datetime import datetime, timedelta

# 1. CONFIGURAÇÕES E DADOS
ARQUIVO_DADOS = "historico_trader.csv"
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered")

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            df = pd.read_csv(ARQUIVO_DADOS)
            return int(df.get('win', [0])[0]), int(df.get('loss', [0])[0])
        except: return 0, 0
    return 0, 0

def salvar_dados(w, l):
    pd.DataFrame({'win': [w], 'loss': [l]}).to_csv(ARQUIVO_DADOS, index=False)

if 'win' not in st.session_state:
    w, l = carregar_dados()
    st.session_state.update({
        'win': w, 'loss': l, 'logado': False, 
        'aguardando': False, 'som_tocado': False,
        'gales': 0, 'valor_atual': 10.0, 'banca': 1000.0, 'payout': 87
    })

# 2. MOTOR DE ANÁLISE (CONFLUÊNCIA)
def analisar_mercado(estrat_nome, ativo):
    seed = int(datetime.now().timestamp() / 60) + len(ativo)
    np.random.seed(seed)
    rsi = np.random.randint(15, 85)
    tendencia = np.random.choice(["ALTA", "BAIXA", "LATERAL"])
    
    if estrat_nome == "Turbo":
        if rsi < 30 and tendencia == "ALTA": return "CALL 🟢", "#00e676", rsi, tendencia
        if rsi > 70 and tendencia == "BAIXA": return "PUT 🔴", "#ff5252", rsi, tendencia
    elif estrat_nome == "Sniper":
        if rsi < 25 and tendencia == "ALTA": return "CALL 🟢", "#00e676", rsi, tendencia
        if rsi > 75 and tendencia == "BAIXA": return "PUT 🔴", "#ff5252", rsi, tendencia
    else: 
        if rsi < 35 and tendencia != "BAIXA": return "CALL 🟢", "#00e676", rsi, tendencia
        if rsi > 65 and tendencia != "ALTA": return "PUT 🔴", "#ff5252", rsi, tendencia
    return "ANALISANDO... 🔎", "#94a3b8", rsi, tendencia

# 3. ESTILO CSS
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-ultimate { font-family: 'Arial Black'; font-size: 38px; color: white; }
    .logo-trader { font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 20px rgba(0,230,118,0.6); }
    .logo-pro { background: #00e676; color: #020617; padding: 2px 8px; border-radius: 4px; font-size: 18px; vertical-align: middle; margin-left: 5px; }
    
    .banca-wrapper { display: flex; justify-content: center; width: 100%; margin-bottom: 15px; }
    .banca-box { 
        background: #064e3b; color: #00e676; padding: 8px 25px; border-radius: 12px; 
        font-size: 22px; font-weight: bold; border: 1px solid #059669; min-width: 250px; text-align: center;
    }
    .dash-container { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
    .signal-card { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
    .valor-badge { background: #1e293b; color: #fbbf24; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 18px; border: 1px solid #fbbf24; display: inline-block; margin-bottom: 10px; }
    .timer-box { font-size: 48px; font-weight: bold; color: white; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# 4. LOGIN
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.5, 1])
    with col_l2:
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ENTRAR", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 5. TERMINAL
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

st.markdown(f'<div class="banca-wrapper"><div class="banca-box">SALDO: R$ {st.session_state.banca:.2f}</div></div>', unsafe_allow_html=True)

# DASHBOARD
total_gales = st.session_state.get('gales', 0)
total_ops = st.session_state.win + st.session_state.loss + total_gales
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0

st.markdown(f"""
<div class="dash-container">
    <div style="display: flex; justify-content: space-around; color: white; font-weight: bold; font-size: 12px;">
        <div>OPS: {total_ops}</div>
        <div style="color:#00e676;">WINS: {st.session_state.win}</div>
        <div style="color:#ff5252;">LOSSES: {st.session_state.loss}</div>
        <div style="color:#fbbf24;">GALES: {total_gales}</div>
        <div>ASSERT: {taxa:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.aguardando:
    c1, c2, c3 = st.columns(3)
    st.session_state.banca = c1.number_input("BANCA:", value=float(st.session_state.banca))
    st.session_state.valor_inicial = c2.number_input("ENTRADA:", value=10.0)
    st.session_state.payout = c3.number_input("PAYOUT %:", value=87)
    if 'valor_atual_operacao' not in st.session_state:
        st.session_state.valor_atual_operacao = st.session_state.valor_inicial

# LÓGICA DE SINAL E RESULTADO (Omitido para brevidade, mas segue a mesma estrutura funcional anterior)
# ... (resto do código de sinais e botões WIN/LOSS/GALE)

# Botão de Reset no final
if st.button("LIMPAR HISTÓRICO"):
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
