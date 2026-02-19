import streamlit as st
import pandas as pd
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

# 2. MOTOR DE ANÁLISE
def analisar_mercado(estrat_nome, ativo):
    seed = int(datetime.now().timestamp() / 60) + len(ativo)
    np.random.seed(seed)
    rsi = np.random.randint(15, 85)
    tendencia = np.random.choice(["ALTA", "BAIXA", "LATERAL"])
    volume = np.random.randint(40, 100)
    
    if estrat_nome == "Turbo":
        if rsi < 30 and tendencia == "ALTA": return "CALL 🟢", "#00e676", rsi, tendencia
        if rsi > 70 and tendencia == "BAIXA": return "PUT 🔴", "#ff5252", rsi, tendencia
    elif estrat_nome == "Sniper":
        if rsi < 25 and tendencia == "ALTA" and volume > 85: return "CALL 🟢", "#00e676", rsi, tendencia
        if rsi > 75 and tendencia == "BAIXA" and volume > 85: return "PUT 🔴", "#ff5252", rsi, tendencia
    else: 
        if rsi < 35 and tendencia != "BAIXA": return "CALL 🟢", "#00e676", rsi, tendencia
        if rsi > 65 and tendencia != "ALTA": return "PUT 🔴", "#ff5252", rsi, tendencia
    return "ANALISANDO...", "#94a3b8", rsi, tendencia

# 3. ESTILO CSS COMPACTO
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-compacta { font-family: 'Arial Black'; font-size: 24px; color: white; text-align: center; margin-bottom: 10px; }
    .logo-trader { color: #00e676; }
    
    /* Barra de Saldo Compacta */
    .banca-mini { 
        background: linear-gradient(90deg, #064e3b, #020617); 
        color: #00e676; padding: 5px 15px; border-radius: 8px; 
        font-size: 16px; font-weight: bold; border: 1px solid #059669;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 10px;
    }

    .dash-mini { 
        background: rgba(30, 41, 59, 0.4); border-radius: 10px; padding: 8px; 
        text-align: center; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 10px;
    }

    .signal-card { 
        background: rgba(30, 41, 59, 0.6); border-radius: 15px; padding: 15px; 
        text-align: center; border: 1px solid rgba(255,255,255,0.1); 
    }

    .timer-mini { font-size: 38px; font-weight: bold; color: white; font-family: monospace; line-height: 1; }
    
    /* Ajuste de inputs para ficarem menores */
    .stNumberInput, .stSelectbox { margin-bottom: -15px; }
</style>
""", unsafe_allow_html=True)

# 4. LOGIN COMPACTO
if not st.session_state.logado:
    st.markdown('<div class="logo-compacta">ULTIMATE <span class="logo-trader">TRADER</span> PRO</div>', unsafe_allow_html=True)
    with st.container():
        _, center, _ = st.columns([1, 2, 1])
        with center:
            c1, c2 = st.columns(2)
            u = c1.text_input("Usuário", label_visibility="collapsed", placeholder="Usuário")
            p = c2.text_input("Senha", type="password", label_visibility="collapsed", placeholder="Senha")
            if st.button("ENTRAR NO TERMINAL", use_container_width=True):
                if u == "romildo" and p == "12345":
                    st.session_state.logado = True
                    st.rerun()
    st.stop()

# 5. TERMINAL OTIMIZADO
st.markdown('<div class="logo-compacta">ULTIMATE <span class="logo-trader">TRADER</span> PRO</div>', unsafe_allow_html=True)

# Barra de Saldo e Placar (Tudo em uma linha ou blocos menores)
total_gales = st.session_state.get('gales', 0)
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0

st.markdown(f"""
<div class='banca-mini'>
    <span>SALDO: R$ {st.session_state.banca:.2f}</span>
    <span style='color:white; font-size:12px;'>W:{st.session_state.win} | L:{st.session_state.loss} | G:{total_gales} | {taxa:.1f}%</span>
</div>
""", unsafe_allow_html=True)

if not st.session_state.aguardando:
    c_g1, c_g2, c_g3 = st.columns(3)
    banca_init = c_g1.number_input("BANCA:", value=float(st.session_state.banca), step=50.0, format="%.2f")
    entrada_init = c_g2.number_input("ENTRADA:", value=10.0, step=1.0)
    payout_init = c_g3.number_input("PAYOUT %:", value=87, step=1)
    
    st.session_state.banca = banca_init
    st.session_state.valor_inicial = entrada_init
    if 'valor_atual_operacao' not in st.session_state:
        st.session_state.valor_atual_operacao = entrada_init
    st.session_state.payout = payout_init

# Card Principal
if st.session_state.aguardando:
    st.markdown("<div class='signal-card'>", unsafe_allow_html=True)
    st.markdown(f"<small style='color:#fbbf24;'>VALOR: R$ {st.session_state.valor_atual_operacao:.2f}</small>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    lucro = st.session_state.valor_atual_operacao * (st.session_state.payout / 100)
    
    if c1.button("WIN", use_container_width=True):
        st.session_state.win += 1
        st.session_state.banca += (st.session_state.valor_atual_operacao + lucro)
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
        st.rerun()
    if c2.button("LOSS", use_container_width=True):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial, 'som_tocado': False})
        st.rerun()
    if c3.button("GALE", use_container_width=True):
        st.session_state.valor_atual_operacao *= 2
        st.session_state.gales += 1
        st.session_state.som_tocado = False
        st.rerun()
    if c4.button("SKIP", use_container_width=True):
        st.session_state.banca += st.session_state.valor_atual_operacao
        st.session_state.update({'aguardando': False, 'valor_atual_operacao': st.session_state.valor_inicial})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    cols = st.columns([1, 1, 1])
    tf = cols[0].selectbox("T:", ["M1", "M5"], label_visibility="collapsed")
    est = cols[1].selectbox("E:", ["Turbo", "Moderada", "Sniper"], label_visibility="collapsed")
    at = cols[2].selectbox("A:", ["EUR/USD (OTC)", "BITCOIN (BTC)"], label_visibility="collapsed")

    sinal, cor, rsi_v, tend_v = analisar_mercado(est, at)
    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"></audio>', height=0)
        st.session_state.som_tocado = True

    st.markdown(f"""
    <div class='signal-card'>
        <h2 style='color:white; margin:0; font-size:18px;'>{at}</h2>
        <h1 style='color:{cor}; font-size:42px; margin:5px 0;'>{sinal}</h1>
        <div class='timer-mini'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>
        <div style='font-size:10px; color:#94a3b8; margin-top:5px;'>RSI: {rsi_v} | {tend_v}</div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        st.session_state.banca -= st.session_state.valor_inicial
        st.session_state.aguardando = True
        st.rerun()

# Rodapé minimalista
st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
r1, r2 = st.columns(2)
if r1.button("SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if r2.button("RESET", use_container_width=True):
    st.session_state.update({'win':0, 'loss':0, 'gales':0})
    st.rerun()

time.sleep(1)
st.rerun()
