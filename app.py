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

# 2. MOTOR DE ANÁLISE (CONFLUÊNCIA)
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
    else: # Moderada
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
    .dash-container { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 15px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; }
    .signal-card { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1); }
    .banca-box { background: #064e3b; color: #00e676; padding: 10px; border-radius: 10px; font-size: 20px; font-weight: bold; margin-bottom: 10px; border: 1px solid #059669; text-align: center; }
    .valor-badge { background: #1e293b; color: #fbbf24; padding: 5px 15px; border-radius: 50px; font-weight: bold; font-size: 18px; border: 1px solid #fbbf24; display: inline-block; margin-bottom: 10px; }
    .timer-box { font-size: 48px; font-weight: bold; color: white; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# 4. LOGIN (COM TRAVA DE SEGURANÇA DEFINITIVA)
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    with st.container():
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.button("ACESSAR TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
    st.stop() # ESSA LINHA IMPEDE QUE O DASHBOARD APAREÇA ANTES DO LOGIN

# 5. TERMINAL (SÓ CARREGA APÓS LOGIN)
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span><span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# Painel de Controle de Banca
total_gales = st.session_state.get('gales', 0)
total_ops = st.session_state.win + st.session_state.loss + total_gales
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0

st.markdown(f"<div class='banca-box'>SALDO ATUAL: R$ {st.session_state.banca:.2f}</div>", unsafe_allow_html=True)

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

# Lógica de Operação em Curso
if not st.session_state.aguardando:
    c_g1, c_g2, c_g3 = st.columns(3)
    banca_init = c_g1.number_input("BANCA INICIAL:", value=float(st.session_state.banca), step=50.0)
    entrada_init = c_g2.number_input("ENTRADA (R$):", value=10.0, step=1.0)
    payout_init = c_g3.number_input("PAYOUT %:", value=87, step=1)
    
    st.session_state.banca = banca_init
    st.session_state.valor_inicial = entrada_init
    if 'valor_atual_operacao' not in st.session_state:
        st.session_state.valor_atual_operacao = entrada_init
    st.session_state.payout = payout_init

if st.session_state.aguardando:
    st.markdown(f"""
    <div class='signal-card'>
        <div class='valor-badge'>EM OPERAÇÃO: R$ {st.session_state.valor_atual_operacao:.2f}</div>
        <h3 style="color:white;">CONFIRMAR RESULTADO?</h3>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    lucro_possivel = st.session_state.valor_atual_operacao * (st.session_state.payout / 100)

    if c1.button("WIN ✅", use_container_width=True):
        st.session_state.win += 1
        st.session_state.banca += (st.session_state.valor_atual_operacao + lucro_possivel)
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.valor_atual_operacao = st.session_state.valor_inicial
        st.session_state.update({'aguardando': False, 'som_tocado': False})
        st.rerun()
        
    if c2.button("LOSS ❌", use_container_width=True):
        st.session_state.loss += 1
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.session_state.valor_atual_operacao = st.session_state.valor_inicial
        st.session_state.update({'aguardando': False, 'som_tocado': False})
        st.rerun()
        
    if c3.button("GALE 🔄", use_container_width=True):
        nova_entrada = st.session_state.valor_atual_operacao * 2
        if st.session_state.banca >= nova_entrada:
            st.session_state.banca -= nova_entrada
            st.session_state.valor_atual_operacao = nova_entrada
            st.session_state.gales += 1
            st.session_state.som_tocado = False
            st.toast(f"Gale aplicado! Debitado: R$ {nova_entrada}", icon="🔄")
        else:
            st.error("Saldo insuficiente para Gale!")
        st.rerun()
        
    if c4.button("PULAR ⏭️", use_container_width=True):
        st.session_state.banca += st.session_state.valor_atual_operacao # Estorna
        st.session_state.valor_atual_operacao = st.session_state.valor_inicial
        st.session_state.aguardando = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Seletores de Ativo e Estratégia
    cols = st.columns([1, 1, 1.5])
    tf = cols[0].selectbox("TEMPO:", ["M1", "M5"])
    est = cols[1].selectbox("ESTRATÉGIA:", ["Turbo", "Moderada", "Sniper"])
    at = cols[2].selectbox("ATIVO:", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BITCOIN (BTC)", "SOLANA (SOL)"])

    sinal, cor, rsi_v, tend_v = analisar_mercado(est, at)
    now = datetime.now()
    prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0) if tf == "M1" else \
           now.replace(minute=((now.minute // 5) + 1) * 5 % 60, second=0, microsecond=0)
    faltam = (prox - now).total_seconds()

    if "ANALISANDO" not in sinal and not st.session_state.som_tocado:
        st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3" type="audio/mp3"></audio>', height=0)
        st.session_state.som_tocado = True

    st.markdown(f"""
    <div class='signal-card'>
        <div class='valor-badge'>ENTRADA: R$ {st.session_state.valor_inicial:.2f}</div>
        <h2 style='color:white; margin:0;'>{at}</h2>
        <h1 style='color:{cor}; font-size:52px; margin:10px 0;'>{sinal}</h1>
        <div class='timer-box'>{int(faltam // 60):02d}:{int(faltam % 60):02d}</div>
        <div style='font-size:11px; color:#94a3b8; margin-top:10px;'>
            CONFLUÊNCIA: RSI {rsi_v} | TENDÊNCIA: {tend_v}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "ANALISANDO" not in sinal and faltam <= 2:
        if st.session_state.banca >= st.session_state.valor_inicial:
            st.session_state.banca -= st.session_state.valor_inicial
            st.session_state.aguardando = True
            st.rerun()
        else:
            st.warning("SALDO INSUFICIENTE PARA OPERAÇÃO!")

# 6. RODAPÉ
st.markdown("<br>", unsafe_allow_html=True)
b1, b2 = st.columns(2)
if b1.button("LOGOUT / SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if b2.button("ZERAR HISTÓRICO", use_container_width=True):
    salvar_dados(0, 0)
    st.session_state.update({'win': 0, 'loss': 0, 'gales': 0, 'banca': 1000.0})
    st.rerun()

time.sleep(1)
st.rerun()
