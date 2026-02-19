import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

# 1. SETUP E PERSISTÊNCIA
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
        'win': w, 'loss': l, 'logado': False, 'aguardando': False, 
        'som_tocado': False, 'gales': 0, 'banca': 1000.0, 
        'entrada_fixa': 10.0, 'valor_atual': 10.0, 'payout': 87
    })

# 2. ESTILO CSS (RESTAURAÇÃO TOTAL DAS IMAGENS)
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 30px; }
    .logo-ultimate { font-family: 'Arial Black'; font-size: 38px; color: white; }
    .logo-trader { font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 15px #00e676; }
    .logo-pro { background: #00d2ff; color: #020617; padding: 2px 8px; border-radius: 4px; font-size: 18px; vertical-align: middle; }
    
    .saldo-card { background: none; border: 2px solid #00d2ff; color: #00e676; padding: 15px; border-radius: 12px; font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .stats-bar { background: rgba(30, 41, 59, 0.5); border-radius: 10px; padding: 10px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); }
    .main-card { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 30px; text-align: center; border: 1px solid #00d2ff; }
    
    .timer-val { font-size: 65px; font-weight: bold; color: white; font-family: monospace; }
    .badge-entrada { background: #1e293b; color: #fbbf24; padding: 5px 20px; border-radius: 50px; font-weight: bold; border: 1px solid #fbbf24; display: inline-block; margin-bottom: 15px; }
    
    /* Botões Customizados */
    .stButton>button { border-radius: 8px !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN (image_0171bd.png)
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span> <span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<h3 style='text-align:center; color:#bf40bf; margin-bottom:20px;'>SYSTEM ACCESS</h3>", unsafe_allow_html=True)
        u = st.text_input("USUÁRIO", placeholder="romildo")
        p = st.text_input("SENHA", type="password", placeholder="12345")
        if st.button("DESBLOQUEAR TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# 4. DASHBOARD (image_017c4b.png / image_02bbfb.png)
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span> <span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# Saldo e Placar
st.markdown(f"<div class='saldo-card'>SALDO DISPONÍVEL: R$ {st.session_state.banca:.2f}</div>", unsafe_allow_html=True)
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0

st.markdown(f"""
<div class="stats-bar">
    <div style="display: flex; justify-content: space-around; font-weight: bold; font-size: 14px;">
        <span style="color:#00e676;">WINS: {st.session_state.win}</span>
        <span style="color:#ff5252;">LOSSES: {st.session_state.loss}</span>
        <span style="color:#fbbf24;">GALES: {st.session_state.gales}</span>
        <span style="color:white;">ASSERT: {taxa:.1f}%</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Área de Gestão
if not st.session_state.aguardando:
    c1, c2, c3 = st.columns(3)
    st.session_state.banca = c1.number_input("BANCA ATUAL:", value=float(st.session_state.banca))
    st.session_state.entrada_fixa = c2.number_input("ENTRADA R$:", value=float(st.session_state.entrada_fixa))
    st.session_state.payout = c3.number_input("PAYOUT %:", value=int(st.session_state.payout))

# --- ÁREA DE SINAL / RESULTADO ---
if st.session_state.aguardando:
    # MOSTRA OS BOTÕES DE RESULTADO (O QUE ESTAVA SUMINDO)
    st.markdown(f"""
    <div class='main-card'>
        <div class='badge-entrada'>EM OPERAÇÃO: R$ {st.session_state.valor_atual:.2f}</div>
        <h2 style='color:white; margin-bottom:25px;'>QUAL FOI O RESULTADO?</h2>
    """, unsafe_allow_html=True)
    
    b1, b2, b3, b4 = st.columns(4)
    lucro = st.session_state.valor_atual * (st.session_state.payout / 100)
    
    if b1.button("WIN ✅", use_container_width=True):
        st.session_state.win += 1
        st.session_state.banca += (st.session_state.valor_atual + lucro)
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa, 'som_tocado': False})
        st.rerun()
        
    if b2.button("LOSS ❌", use_container_width=True):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa, 'som_tocado': False})
        st.rerun()
        
    if b3.button("GALE 🔄", use_container_width=True):
        st.session_state.valor_atual *= 2
        st.session_state.gales += 1
        st.session_state.som_tocado = False
        st.rerun()
        
    if b4.button("PULAR ⏭️", use_container_width=True):
        st.session_state.banca += st.session_state.valor_atual
        st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # MOSTRA O CRONÔMETRO E SINAL
    s1, s2, s3 = st.columns(3)
    tf = s1.selectbox("TIME FRAME:", ["M1", "M5"])
    est = s2.selectbox("ESTRATÉGIA:", ["Sniper (RSI/MM/VOL)", "Turbo"])
    at = s3.selectbox("ATIVO DISPONÍVEL:", ["EUR/USD (OTC)", "GBP/JPY (OTC)"])

    now = datetime.now()
    sinal, cor = ("CALL 🟢", "#00e676") if now.second < 30 else ("ANALISANDO...", "#94a3b8")
    faltam = 60 - now.second

    st.markdown(f"""
    <div class='main-card'>
        <div class='badge-entrada'>ENTRADA: R$ {st.session_state.entrada_fixa:.2f}</div>
        <h1 style='color:{cor}; font-size:55px; margin:10px 0;'>{sinal}</h1>
        <div class='timer-val'>00:{faltam:02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.banca -= st.session_state.entrada_fixa
        st.session_state.valor_atual = st.session_state.entrada_fixa
        st.session_state.aguardando = True
        st.rerun()

    time.sleep(1)
    st.rerun()

# 5. RODAPÉ (ÚNICO)
st.markdown("<br>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
if f1.button("EXIT TERMINAL", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if f2.button("WIPE DATA (ZERAR)", use_container_width=True):
    salvar_dados(0, 0)
    st.session_state.update({'win':0, 'loss':0, 'gales':0})
    st.rerun()
