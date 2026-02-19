import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

# 1. CONFIGURAÇÃO INICIAL (Obrigatório ser a primeira linha)
st.set_page_config(page_title="Ultimate Trader Pro", layout="centered", initial_sidebar_state="collapsed")

# 2. SISTEMA DE ARQUIVOS E DADOS
ARQUIVO_DADOS = "historico_trader.csv"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            df = pd.read_csv(ARQUIVO_DADOS)
            return int(df.get('win', [0])[0]), int(df.get('loss', [0])[0])
        except: return 0, 0
    return 0, 0

def salvar_dados(w, l):
    pd.DataFrame({'win': [w], 'loss': [l]}).to_csv(ARQUIVO_DADOS, index=False)

# Inicialização de Variáveis (Session State)
if 'init' not in st.session_state:
    w, l = carregar_dados()
    st.session_state.update({
        'init': True,
        'logado': False,
        'win': w, 'loss': l, 'gales': 0,
        'banca': 1000.0,
        'entrada_fixa': 10.0,
        'valor_atual': 10.0,
        'payout': 87,
        'aguardando': False,
        'som_tocado': False
    })

# 3. ESTILO CSS (A MÁGICA DO VISUAL)
st.markdown("""
<style>
    /* Fundo Geral */
    .stApp { background-color: #020617; }
    
    /* Esconde menu padrão do Streamlit para limpar a tela */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* LOGO */
    .logo-box { text-align: center; margin-bottom: 20px; padding-top: 20px; }
    .logo-text { font-family: 'Arial Black', sans-serif; font-size: 40px; color: white; }
    .logo-highlight { color: #00e676; text-shadow: 0 0 20px #00e676; }
    .logo-badge { background: #00d2ff; color: black; font-size: 14px; padding: 2px 6px; border-radius: 4px; vertical-align: middle; margin-left: 5px; }

    /* CARD NEON (SALDO NO LOGIN) */
    .neon-card {
        background: transparent;
        border: 2px solid #00d2ff;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3), inset 0 0 10px rgba(0, 210, 255, 0.1);
        color: #00e676;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 30px;
        font-family: monospace;
    }

    /* BARRA DE STATUS (DASHBOARD) */
    .stats-bar {
        background: #1e293b;
        border-top: 3px solid #00e676;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-around;
        color: white;
        font-weight: bold;
        font-family: sans-serif;
    }

    /* CARTÃO PRINCIPAL (SINAL/RESULTADO) */
    .main-card {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        margin-top: 10px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    /* TEXTOS */
    .big-timer { font-size: 70px; font-weight: bold; color: white; font-family: monospace; line-height: 1; margin-top: 10px; }
    .signal-text { font-size: 50px; font-weight: 900; margin: 0; }
    .info-badge { background: #334155; color: #fbbf24; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 16px; border: 1px solid #fbbf24; }

    /* BOTÕES CUSTOMIZADOS */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        height: 50px;
        border: none;
        transition: all 0.3s;
    }
    /* Cores específicas de botões são gerenciadas pelo Streamlit theme, mas o CSS acima garante o formato */
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# TELA 1: LOGIN (Baseado na image_01e565.png)
# ==============================================================================
if not st.session_state.logado:
    # 1. Logo
    st.markdown("""
        <div class="logo-box">
            <span class="logo-text">ULTIMATE <span class="logo-highlight">TRADER</span></span>
            <span class="logo-badge">PRO</span>
        </div>
    """, unsafe_allow_html=True)

    # 2. Card de Saldo Neon (Largo)
    st.markdown(f'<div class="neon-card">SALDO OPERACIONAL: R$ {st.session_state.banca:.2f}</div>', unsafe_allow_html=True)

    # 3. Formulário de Login (Mais estreito e centralizado)
    # Usamos colunas vazias nas laterais para "apertar" o formulário no meio
    c_esq, c_meio, c_dir = st.columns([1, 2, 1])
    
    with c_meio:
        usuario = st.text_input("USUÁRIO", placeholder="Digite seu usuário")
        senha = st.text_input("SENHA", type="password", placeholder="••••••")
        
        st.write("") # Espaçamento
        
        if st.button("DESBLOQUEAR SISTEMA", type="primary"):
            if usuario == "romildo" and senha == "12345":
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("Credenciais Inválidas")
    
    st.stop() # Para a execução aqui se não estiver logado

# ==============================================================================
# TELA 2: DASHBOARD (Baseado na image_02bbfb.png)
# ==============================================================================

# 1. Logo Menor
st.markdown("""
    <div class="logo-box" style="margin-bottom: 10px; padding-top: 0;">
        <span class="logo-text" style="font-size: 28px;">ULTIMATE <span class="logo-highlight">TRADER</span></span>
        <span class="logo-badge">PRO</span>
    </div>
""", unsafe_allow_html=True)

# 2. Barra de Saldo (Estilo Sólido Verde)
st.markdown(f"""
    <div style="background-color: #064e3b; color: #00e676; padding: 15px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold; border: 1px solid #059669; margin-bottom: 10px;">
        SALDO: R$ {st.session_state.banca:.2f}
    </div>
""", unsafe_allow_html=True)

# 3. Stats Bar
taxa_acerto = (st.session_state.win / (st.session_state.win + st.session_state.loss) * 100) if (st.session_state.win + st.session_state.loss) > 0 else 0.0
st.markdown(f"""
    <div class="stats-bar">
        <span style="color:#4ade80">WINS: {st.session_state.win}</span>
        <span style="color:#f87171">LOSSES: {st.session_state.loss}</span>
        <span style="color:#fbbf24">GALES: {st.session_state.gales}</span>
        <span style="color:#e2e8f0">{taxa_acerto:.1f}%</span>
    </div>
""", unsafe_allow_html=True)

# 4. Inputs de Configuração (Desabilitados se estiver aguardando resultado)
if not st.session_state.aguardando:
    col_inp1, col_inp2, col_inp3 = st.columns(3)
    st.session_state.banca = col_inp1.number_input("BANCA", value=float(st.session_state.banca))
    st.session_state.entrada_fixa = col_inp2.number_input("ENTRADA", value=float(st.session_state.entrada_fixa))
    st.session_state.payout = col_inp3.number_input("PAYOUT %", value=int(st.session_state.payout))

# 5. ÁREA DINÂMICA (SINAL ou RESULTADO)
placeholder_area = st.empty()

with placeholder_area.container():
    if st.session_state.aguardando:
        # --- TELA DE RESULTADO (Botões Fixos) ---
        st.markdown(f"""
            <div class="main-card" style="border-color: #fbbf24;">
                <span class="info-badge">OPERAÇÃO EM ANDAMENTO</span>
                <h2 style="color: white; margin-top: 20px;">VALOR: R$ {st.session_state.valor_atual:.2f}</h2>
                <h3 style="color: #94a3b8; margin-bottom: 30px;">SELECIONE O RESULTADO:</h3>
        """, unsafe_allow_html=True)
        
        # Botões de Ação
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        lucro_possivel = st.session_state.valor_atual * (st.session_state.payout / 100)
        
        if col_res1.button("WIN ✅", use_container_width=True):
            st.session_state.win += 1
            st.session_state.banca += (st.session_state.valor_atual + lucro_possivel)
            salvar_dados(st.session_state.win, st.session_state.loss)
            st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa})
            st.rerun()
            
        if col_res2.button("LOSS ❌", use_container_width=True):
            st.session_state.loss += 1
            salvar_dados(st.session_state.win, st.session_state.loss)
            st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa})
            st.rerun()
            
        if col_res3.button("GALE 🔄", use_container_width=True):
            st.session_state.valor_atual *= 2
            st.session_state.gales += 1
            st.rerun()
            
        if col_res4.button("PULAR ⏭️", use_container_width=True):
            st.session_state.banca += st.session_state.valor_atual # Devolve o valor
            st.session_state.update({'aguardando': False, 'valor_atual': st.session_state.entrada_fixa})
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # --- TELA DE SINAL (Cronômetro) ---
        # Lógica de Tempo
        agora = datetime.now()
        segundo_atual = agora.second
        tempo_restante = 60 - segundo_atual
        
        # Lógica Simples de Sinal (Verde nos primeiros 30s)
        if segundo_atual < 30:
            sinal_txt = "CALL 🟢"
            cor_sinal = "#00e676"
        else:
            sinal_txt = "ANALISANDO..."
            cor_sinal = "#64748b" # Cinza

        # Tocar Som (apenas uma vez quando entra o sinal)
        if "CALL" in sinal_txt and not st.session_state.som_tocado:
            st.components.v1.html('<audio autoplay><source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"></audio>', height=0)
            st.session_state.som_tocado = True
        elif "ANALISANDO" in sinal_txt:
            st.session_state.som_tocado = False

        # Visualização
        st.markdown(f"""
            <div class="main-card">
                <span class="info-badge">PRÓXIMA ENTRADA: R$ {st.session_state.entrada_fixa:.2f}</span>
                <div style="margin-top: 20px;">
                    <h1 class="signal-text" style="color: {cor_sinal}">{sinal_txt}</h1>
                    <div class="big-timer">00:{tempo_restante:02d}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Gatilho Automático (Faltando 2 segundos)
        if "CALL" in sinal_txt and tempo_restante <= 2:
            st.session_state.banca -= st.session_state.entrada_fixa
            st.session_state.valor_atual = st.session_state.entrada_fixa
            st.session_state.aguardando = True
            st.rerun()

# 6. RODAPÉ (Botões de Saída)
st.write("")
col_sair1, col_sair2 = st.columns(2)
if col_sair1.button("SAIR DO SISTEMA"):
    st.session_state.logado = False
    st.rerun()
if col_sair2.button("ZERAR DADOS"):
    salvar_dados(0, 0)
    st.session_state.win = 0
    st.session_state.loss = 0
    st.session_state.gales = 0
    st.rerun()

# Loop de atualização (apenas se não estiver aguardando clique)
if not st.session_state.aguardando:
    time.sleep(1)
    st.rerun()
