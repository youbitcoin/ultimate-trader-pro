import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta

# --- SETUP E ESTILO ---
st.set_page_config(page_title="Ultimate Trader Pro | Global", layout="centered")

# Inicialização Blindada do Estado
if 'logado' not in st.session_state:
    st.session_state.update({
        'logado': False, 'banca': 1000.0, 'entrada': 10.0, 
        'payout': 87, 'wins': 0, 'losses': 0,
        'stop_gain': 200.0, 'stop_loss': 100.0
    })

# Wallpaper Pro (High-Tech Setup)
img_bg = "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=2064&auto=format&fit=crop"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 8, 20, 0.96), rgba(0, 8, 20, 0.96)), url("{img_bg}");
        background-size: cover;
    }}
    
    /* Branding */
    .brand {{ display: flex; align-items: center; justify-content: center; padding-bottom: 20px; }}
    .u-t {{ color: #FFFFFF; font-size: 32px; font-weight: 800; letter-spacing: -1px; }}
    .t-t {{ color: #00e676; font-size: 32px; font-weight: 800; text-shadow: 0 0 15px #00e676; margin-left: 5px; }}
    
    /* Dashboard Cards */
    .stat-card {{ 
        background: rgba(0, 210, 255, 0.05); border: 1px solid rgba(0, 210, 255, 0.2);
        padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;
    }}
    .stat-val {{ color: #00e676; font-size: 24px; font-weight: bold; font-family: monospace; }}

    /* Signal Engine */
    .signal-box {{ 
        background: rgba(10, 15, 30, 0.8); border-radius: 15px; padding: 30px; 
        text-align: center; border: 1px solid #00d2ff; box-shadow: 0 0 40px rgba(0,0,0,0.5);
    }}
    
    /* Buttons Fixos (Texto Preto - Alta Leitura) */
    .stButton>button {{
        background: linear-gradient(90deg, #00d2ff, #00e676) !important;
        color: #000000 !important; font-weight: 800 !important; border: none !important;
        height: 45px !important; border-radius: 8px !important; text-transform: uppercase;
    }}
    
    /* Inputs Discretos */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(0,0,0,0.6) !important; color: #00d2ff !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
    }}
    label {{ color: rgba(255,255,255,0.6) !important; font-size: 12px !important; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if not st.session_state.logado:
    st.markdown('<div class="brand"><span class="u-t">ULTIMATE</span><span class="t-t">TRADER</span></div>', unsafe_allow_html=True)
    _, col_log, _ = st.columns([1, 1.8, 1])
    with col_log:
        u = st.text_input("ACCESS ID")
        p = st.text_input("PASSWORD", type="password")
        if st.button("UNLOCK TERMINAL", use_container_width=True):
            if u == "romildo" and p == "12345":
                st.session_state.logado = True
                st.rerun()
    st.stop()

# --- TERMINAL OPERACIONAL ---
st.markdown('<div class="brand"><span class="u-t">ULTIMATE</span><span class="t-t">TRADER</span><span style="background:#00d2ff; color:#000; padding:2px 8px; border-radius:4px; font-size:12px; margin-left:10px; font-weight:900;">PRO</span></div>', unsafe_allow_html=True)

# 1. Painel de Informações Superiores
c_stat1, c_stat2 = st.columns(2)
with c_stat1:
    st.markdown(f'<div class="stat-card">BALANCE<br><span class="stat-val">R$ {st.session_state.banca:.2f}</span></div>', unsafe_allow_html=True)
with c_stat2:
    win_rate = (st.session_state.wins / (st.session_state.wins + st.session_state.losses) * 100) if (st.session_state.wins + st.session_state.losses) > 0 else 0
    st.markdown(f'<div class="stat-card">WIN RATE<br><span class="stat-val" style="color:#00d2ff;">{win_rate:.1f}%</span></div>', unsafe_allow_html=True)

# 2. Configurações de Risco e Parâmetros
with st.expander("⚙️ RISK MANAGEMENT & PARAMETERS", expanded=False):
    r1, r2, r3 = st.columns(3)
    st.session_state.banca = r1.number_input("BANCA TOTAL:", value=float(st.session_state.banca))
    st.session_state.stop_gain = r2.number_input("STOP GAIN (R$):", value=float(st.session_state.stop_gain))
    st.session_state.stop_loss = r3.number_input("STOP LOSS (R$):", value=float(st.session_state.stop_loss))
    
    g1, g2, g3 = st.columns(3)
    st.session_state.entrada = g1.number_input("VALOR ENTRADA:", value=float(st.session_state.entrada))
    st.session_state.payout = g2.number_input("PAYOUT %:", value=int(st.session_state.payout))
    asset = g3.selectbox("ASSET:", ["EUR/USD", "GBP/USD", "BTC/USDT"])

# 3. MOTOR DE SINAIS (LÓGICA DE CONFLUÊNCIA REAL)
st.markdown("<br>", unsafe_allow_html=True)
now = datetime.now()
seed = int(now.timestamp() / 60)
np.random.seed(seed)

# Simulador de Indicadores (Base para Confluência)
# Imagine que estes valores venham de uma API real no futuro
trend_power = np.random.randint(0, 100)
volatility = np.random.choice(["LOW", "MEDIUM", "HIGH"])
rsi_level = np.random.randint(10, 90)

sinal, cor, conf_tags = "WAITING...", "#4b5563", []

# Regra de Entrada Sniper (Exemplo: Tendência Forte + RSI + Volatilidade)
if trend_power > 75 and rsi_level < 30 and volatility != "LOW":
    sinal, cor = "CALL 🟢", "#00e676"
    conf_tags = ["TREND BULLISH", "RSI OVERSOLD", "VOL CONFIRMED"]
elif trend_power < 25 and rsi_level > 70 and volatility != "LOW":
    sinal, cor = "PUT 🔴", "#ff1744"
    conf_tags = ["TREND BEARISH", "RSI OVERBOUGHT", "VOL CONFIRMED"]

# 4. EXIBIÇÃO DO SINAL
prox = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
timer = int((prox - now).total_seconds())

st.markdown(f"""
<div class="signal-box">
    <div style="color:rgba(255,255,255,0.4); font-size:11px; letter-spacing:3px; margin-bottom:10px;">PROBABILITY ENGINE V3.2</div>
    <h1 style="color:{cor}; font-size:60px; margin:10px 0; font-weight:900; letter-spacing:-2px;">{sinal}</h1>
    <div style="font-size:35px; color:#00d2ff; font-family:monospace; font-weight:bold;">00:{timer:02d}</div>
    <div style="margin-top:15px;">
        {" ".join([f'<span style="color:#00e676; border:1px solid #00e676; padding:2px 10px; border-radius:4px; font-size:10px; margin:2px; display:inline-block; font-weight:bold;">{t}</span>' for t in conf_tags]) if conf_tags else '<span style="color:#4b5563; font-size:10px;">SCANNING CONFLUENCES...</span>'}
    </div>
</div>
""", unsafe_allow_html=True)

# 5. CONTROLES DE RESULTADO (Apenas uma vez, limpos)
st.markdown("<br>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([1.5, 1.5, 1])

if b1.button("✅ REGISTER WIN", use_container_width=True):
    st.session_state.wins += 1
    st.session_state.banca += (st.session_state.entrada * (st.session_state.payout / 100))
    st.rerun()

if b2.button("❌ REGISTER LOSS", use_container_width=True):
    st.session_state.losses += 1
    st.session_state.banca -= st.session_state.entrada
    st.rerun()

if b3.button("LOGOUT", use_container_width=True):
    st.session_state.logado = False
    st.rerun()

# Auto-refresh
time.sleep(1)
st.rerun()
