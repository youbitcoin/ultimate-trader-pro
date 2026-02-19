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

# Inicialização segura do estado
if 'logado' not in st.session_state:
    st.session_state.logado = False

if 'win' not in st.session_state:
    w, l = carregar_dados()
    st.session_state.update({
        'win': w, 'loss': l, 'aguardando': False, 
        'som_tocado': False, 'gales': 0, 'banca': 1000.0, 
        'entrada_fixa': 10.0, 'valor_atual': 10.0, 'payout': 87
    })

# 2. ESTILO CSS (DESIGN EXATO DA SUA IMAGEM image_01e565.png)
st.markdown("""
<style>
    .stApp { background: #020617; }
    .logo-container { text-align: center; margin-bottom: 20px; }
    .logo-ultimate { font-family: 'Arial Black'; font-size: 38px; color: white; }
    .logo-trader { font-family: 'Arial Black'; font-size: 38px; color: #00e676; text-shadow: 0 0 15px #00e676; }
    .logo-pro { background: #00d2ff; color: #020617; padding: 2px 8px; border-radius: 4px; font-size: 18px; vertical-align: middle; }
    
    .saldo-neon { 
        border: 2px solid #00d2ff; color: #00e676; padding: 20px; border-radius: 12px; 
        font-size: 26px; font-weight: bold; text-align: center; margin-bottom: 25px;
        box-shadow: inset 0 0 10px #00d2ff, 0 0 15px rgba(0,210,255,0.3);
    }
    
    .main-card { background: rgba(30, 41, 59, 0.7); border-radius: 20px; padding: 30px; text-align: center; border: 1px solid #00d2ff; }
    .timer-text { font-size: 65px; font-weight: bold; color: white; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# 3. TELA DE LOGIN (FIXA E SEM LOOP)
if not st.session_state.logado:
    st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span> <span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)
    
    # Caixa de Saldo que aparece no login (conforme image_01e565.png)
    st.markdown(f"<div class='saldo-neon'>SALDO OPERACIONAL: R$ {st.session_state.banca:.2f}</div>", unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 2, 1])
    with col:
        u = st.text_input("USUÁRIO", value="romildo")
        p = st.text_input("SENHA", type="password")
        
        # Botão com nome exato da imagem
        if st.button("DESBLOQUEAR SISTEMA", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.success("Acesso concedido!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Senha incorreta!")
    st.stop()

# 4. DASHBOARD (SÓ CARREGA APÓS LOGIN)
st.markdown('<div class="logo-container"><span class="logo-ultimate">ULTIMATE</span> <span class="logo-trader">TRADER</span> <span class="logo-pro">PRO</span></div>', unsafe_allow_html=True)

# Placar e Status
taxa = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0
st.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.5); border-radius: 10px; padding: 10px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-around; font-weight: bold;">
    <span style="color:#00e676;">W: {st.session_state.win}</span>
    <span style="color:#ff5252;">L: {st.session_state.loss}</span>
    <span style="color:#fbbf24;">G: {st.session_state.gales}</span>
    <span style="color:white;">{taxa:.1f}%</span>
</div>
""", unsafe_allow_html=True)

# Área Operacional
if st.session_state.aguardando:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.write(f"### OPERAÇÃO ATUAL: R$ {st.session_state.valor_atual:.2f}")
    
    c1, c2, c3 = st.columns(3)
    if c1.button("WIN ✅", use_container_width=True):
        st.session_state.win += 1
        st.session_state.banca += (st.session_state.valor_atual * (1 + st.session_state.payout/100))
        st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa})
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.rerun()
        
    if c2.button("LOSS ❌", use_container_width=True):
        st.session_state.loss += 1
        st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa})
        salvar_dados(st.session_state.win, st.session_state.loss)
        st.rerun()

    if c3.button("GALE 🔄", use_container_width=True):
        st.session_state.valor_atual *= 2
        st.session_state.gales += 1
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Cronômetro de Sinal
    now = datetime.now()
    faltam = 60 - now.second
    sinal = "CALL 🟢" if now.second < 30 else "ANALISANDO..."
    
    st.markdown(f"""
    <div class='main-card'>
        <h1 style='color:{"#00e676" if "CALL" in sinal else "#94a3b8"}; font-size:55px;'>{sinal}</h1>
        <div class='timer-text'>00:{faltam:02d}</div>
    </div>
    """, unsafe_allow_html=True)

    if "CALL" in sinal and faltam <= 2:
        st.session_state.banca -= st.session_state.entrada_fixa
        st.session_state.aguardando = True
        st.rerun()

    time.sleep(1)
    st.rerun()

# 5. BOTÕES DE RODAPÉ (LIMPANDO image_02479c.png)
st.markdown("<br>", unsafe_allow_html=True)
f1, f2 = st.columns(2)
if f1.button("LOGOUT / SAIR", use_container_width=True):
    st.session_state.logado = False
    st.rerun()
if f2.button("ZERAR HISTÓRICO", use_container_width=True):
    st.session_state.update({'win':0, 'loss':0, 'gales':0})
    salvar_dados(0,0)
    st.rerun()
