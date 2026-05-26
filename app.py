"""
Controle Financeiro Pessoal – Adriely Lovato
"""

import streamlit as st
import json
import os
import base64
import uuid
import urllib.request
import urllib.error
from datetime import date as _date, datetime
from pathlib import Path
import streamlit.components.v1 as _components

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Financeiro Pessoal – Adriely",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── PWA icon ────────────────────────────────────────────────────────────────
_components.html("""<script>
(function(){
  var d = window.parent.document;
  if (d.querySelector('link[rel="apple-touch-icon"]')) return;
  var cv = document.createElement('canvas');
  cv.width = cv.height = 192;
  var ctx = cv.getContext('2d');
  ctx.fillStyle = '#7b1d2e';
  if (ctx.roundRect){ctx.roundRect(0,0,192,192,38);}else{ctx.rect(0,0,192,192);}
  ctx.fill();
  ctx.fillStyle = '#C4973A';
  ctx.font = 'bold 80px Georgia, serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('AL', 96, 104);
  var png = cv.toDataURL('image/png');
  var lnk = d.createElement('link');
  lnk.rel = 'apple-touch-icon'; lnk.sizes = '192x192'; lnk.href = png;
  d.head.appendChild(lnk);
  var manifest = {name:'Financeiro Pessoal',short_name:'Pessoal',
    display:'standalone',background_color:'#7b1d2e',theme_color:'#7b1d2e',
    icons:[{src:png,sizes:'192x192',type:'image/png'}]};
  var blob = new Blob([JSON.stringify(manifest)],{type:'application/json'});
  var ml = d.createElement('link'); ml.rel='manifest'; ml.href=URL.createObjectURL(blob);
  d.head.appendChild(ml);
})();
</script>""", height=0)

# ─── Login ────────────────────────────────────────────────────────────────────
_senha_ok = st.secrets.get("SENHA", "adriely2025") if hasattr(st, "secrets") else "adriely2025"
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if not st.session_state["logado"]:
    st.markdown("""<div style="max-width:360px;margin:80px auto;background:white;border-radius:14px;
        padding:36px;box-shadow:0 4px 24px rgba(0,0,0,0.12);text-align:center;">
        <h2 style="color:#7b1d2e;margin-bottom:6px;">💰 Financeiro Pessoal</h2>
        <p style="color:#718096;margin-bottom:24px;">Adriely Lovato</p>
    </div>""", unsafe_allow_html=True)
    with st.form("login_pessoal"):
        st.markdown("### 🔐 Acesso")
        _s = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar", use_container_width=True):
            if _s == _senha_ok:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.stop()

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}

.card {
    background:white; border-radius:12px; padding:18px 22px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08); margin-bottom:12px; text-align:center;
}
.card-val { font-size:26px; font-weight:700; margin:4px 0; }
.card-lbl { font-size:11px; color:#718096; text-transform:uppercase; letter-spacing:0.5px; }
.card-sub { font-size:12px; color:#a0aec0; margin-top:2px; }

.row-item {
    background:#f7fafc; border-radius:8px; padding:10px 14px;
    margin:4px 0; border-left:4px solid #e2e8f0;
}
.row-pago   { border-left-color:#38a169; }
.row-pend   { border-left-color:#e53e3e; }

.tag-pago    { display:inline-block; padding:2px 8px; border-radius:20px;
               font-size:10px; font-weight:700; background:#c6f6d5; color:#276749; }
.tag-pendente{ display:inline-block; padding:2px 8px; border-radius:20px;
               font-size:10px; font-weight:700; background:#fed7d7; color:#9b2c2c; }
.tag-parcela { display:inline-block; padding:2px 8px; border-radius:20px;
               font-size:10px; font-weight:600; background:#e9d8fd; color:#553c9a; }

.secao-titulo {
    font-size:13px; font-weight:700; color:#4a5568;
    text-transform:uppercase; letter-spacing:1px;
    border-bottom:2px solid #e2e8f0; padding-bottom:6px; margin:16px 0 10px 0;
}
.barra-bg { background:#e2e8f0; border-radius:4px; height:10px; overflow:hidden; }
.barra-fill { height:100%; border-radius:4px;
              background:linear-gradient(90deg,#7b1d2e,#C4973A); }

.stButton>button { border-radius:8px; font-weight:500; }
.stButton>button:hover { opacity:0.9; }
</style>
""", unsafe_allow_html=True)

# ─── Constantes ───────────────────────────────────────────────────────────────
CATEGORIAS = [
    "💳 Cartão", "🏦 Banco/Financ.", "🏠 Moradia",
    "🚗 Carro", "💊 Saúde", "💪 Academia/Esporte",
    "⚖️ Profissional", "📱 Serviços", "🛡️ Seguro",
    "🛒 Compras", "💄 Beleza", "🎾 Lazer", "🎯 Outros",
]

CAT_CORES = {
    "💳 Cartão":         "#9f7aea",
    "🏦 Banco/Financ.":  "#4299e1",
    "🏠 Moradia":        "#ed8936",
    "🚗 Carro":          "#48bb78",
    "💊 Saúde":          "#f56565",
    "💪 Academia/Esporte":"#38b2ac",
    "⚖️ Profissional":   "#667eea",
    "📱 Serviços":       "#ecc94b",
    "🛡️ Seguro":         "#a0aec0",
    "🛒 Compras":        "#fc8181",
    "💄 Beleza":         "#f687b3",
    "🎾 Lazer":          "#68d391",
    "🎯 Outros":         "#cbd5e0",
}

MESES_PT = {
    "01":"Janeiro","02":"Fevereiro","03":"Março","04":"Abril",
    "05":"Maio","06":"Junho","07":"Julho","08":"Agosto",
    "09":"Setembro","10":"Outubro","11":"Novembro","12":"Dezembro",
}

def nome_mes(key):
    y, m = key.split("-")
    return f"{MESES_PT[m]}/{y}"

def fmt(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ─── Dados iniciais ───────────────────────────────────────────────────────────
INITIAL_DATA = {
    "meses": {
        "2025-03": {
            "lancamentos": [
                {"id":"m3l1","data":5,"descricao":"Nubank","valor":426.97,"parcela":"3/5","categoria":"💳 Cartão","pago":True,"obs":""},
                {"id":"m3l2","data":5,"descricao":"Nubank","valor":979.84,"parcela":"1/3","categoria":"💳 Cartão","pago":True,"obs":""},
                {"id":"m3l3","data":5,"descricao":"Academia","valor":135.00,"parcela":"","categoria":"💪 Academia/Esporte","pago":True,"obs":""},
                {"id":"m3l4","data":9,"descricao":"Mercado Pago","valor":424.99,"parcela":"1/2","categoria":"🛒 Compras","pago":True,"obs":""},
                {"id":"m3l5","data":10,"descricao":"Aluguel e net Escritório","valor":382.75,"parcela":"","categoria":"🏠 Moradia","pago":True,"obs":""},
                {"id":"m3l6","data":11,"descricao":"Sicoob","valor":2630.69,"parcela":"","categoria":"🏦 Banco/Financ.","pago":True,"obs":""},
                {"id":"m3l7","data":23,"descricao":"Parcela Carro","valor":2553.45,"parcela":"6/48","categoria":"🚗 Carro","pago":True,"obs":""},
                {"id":"m3l8","data":28,"descricao":"Cabelo casamento","valor":120.00,"parcela":"","categoria":"💄 Beleza","pago":True,"obs":""},
                {"id":"m3l9","data":28,"descricao":"Maquiagem casamento","valor":150.00,"parcela":"","categoria":"💄 Beleza","pago":True,"obs":""},
                {"id":"m3l10","data":30,"descricao":"OAB MG","valor":79.20,"parcela":"3/12","categoria":"⚖️ Profissional","pago":True,"obs":""},
            ],
            "fixas": [
                {"id":"m3f1","descricao":"Seguro","valor":258.18,"categoria":"🛡️ Seguro","pago":True},
                {"id":"m3f2","descricao":"Apple","valor":19.90,"categoria":"📱 Serviços","pago":True},
                {"id":"m3f3","descricao":"Google","valor":9.99,"categoria":"📱 Serviços","pago":True},
                {"id":"m3f4","descricao":"Tarifa bancária","valor":20.00,"categoria":"🏦 Banco/Financ.","pago":True},
                {"id":"m3f5","descricao":"Vivo","valor":89.90,"categoria":"📱 Serviços","pago":True},
                {"id":"m3f6","descricao":"Remédio","valor":100.00,"categoria":"💊 Saúde","pago":True},
                {"id":"m3f7","descricao":"Jusbrasil","valor":58.90,"categoria":"⚖️ Profissional","pago":True},
            ],
        },
        "2025-04": {
            "lancamentos": [
                {"id":"m4l1","data":5,"descricao":"Nubank","valor":430.11,"parcela":"4/5","categoria":"💳 Cartão","pago":True,"obs":""},
                {"id":"m4l2","data":5,"descricao":"Nubank","valor":532.77,"parcela":"2/3","categoria":"💳 Cartão","pago":True,"obs":""},
                {"id":"m4l3","data":5,"descricao":"Academia","valor":135.00,"parcela":"","categoria":"💪 Academia/Esporte","pago":True,"obs":""},
                {"id":"m4l4","data":9,"descricao":"Mercado Pago","valor":424.99,"parcela":"2/2","categoria":"🛒 Compras","pago":True,"obs":""},
                {"id":"m4l5","data":10,"descricao":"Aluguel e net Escritório","valor":339.95,"parcela":"","categoria":"🏠 Moradia","pago":True,"obs":""},
                {"id":"m4l6","data":11,"descricao":"Sicoob","valor":3979.10,"parcela":"","categoria":"🏦 Banco/Financ.","pago":True,"obs":"370 Lucas"},
                {"id":"m4l7","data":23,"descricao":"Parcela Carro","valor":2573.20,"parcela":"7/48","categoria":"🚗 Carro","pago":True,"obs":""},
                {"id":"m4l8","data":30,"descricao":"OAB MG","valor":79.20,"parcela":"4/12","categoria":"⚖️ Profissional","pago":True,"obs":""},
            ],
            "fixas": [
                {"id":"m4f1","descricao":"Seguro","valor":258.18,"categoria":"🛡️ Seguro","pago":True},
                {"id":"m4f2","descricao":"Apple","valor":19.90,"categoria":"📱 Serviços","pago":True},
                {"id":"m4f3","descricao":"Google","valor":9.99,"categoria":"📱 Serviços","pago":True},
                {"id":"m4f4","descricao":"Tarifa bancária","valor":20.75,"categoria":"🏦 Banco/Financ.","pago":True},
                {"id":"m4f5","descricao":"Vivo","valor":62.00,"categoria":"📱 Serviços","pago":True},
                {"id":"m4f6","descricao":"Remédio","valor":100.00,"categoria":"💊 Saúde","pago":True},
                {"id":"m4f7","descricao":"Aula de tênis","valor":150.00,"categoria":"💪 Academia/Esporte","pago":True},
                {"id":"m4f8","descricao":"Jusbrasil","valor":58.90,"categoria":"⚖️ Profissional","pago":True},
            ],
        },
        "2025-05": {
            "lancamentos": [
                {"id":"m5l1","data":5,"descricao":"OAB SP","valor":361.23,"parcela":"1/3","categoria":"⚖️ Profissional","pago":True,"obs":""},
                {"id":"m5l2","data":5,"descricao":"Academia","valor":135.00,"parcela":"","categoria":"💪 Academia/Esporte","pago":True,"obs":""},
                {"id":"m5l3","data":9,"descricao":"Mercado Pago","valor":87.24,"parcela":"1/3","categoria":"🛒 Compras","pago":True,"obs":""},
                {"id":"m5l4","data":10,"descricao":"Aluguel e net Escritório","valor":300.00,"parcela":"","categoria":"🏠 Moradia","pago":True,"obs":""},
                {"id":"m5l5","data":11,"descricao":"Sicoob","valor":3995.55,"parcela":"","categoria":"🏦 Banco/Financ.","pago":True,"obs":""},
                {"id":"m5l6","data":23,"descricao":"Parcela Carro","valor":2573.20,"parcela":"8/48","categoria":"🚗 Carro","pago":True,"obs":""},
                {"id":"m5l7","data":30,"descricao":"OAB MG","valor":79.20,"parcela":"5/12","categoria":"⚖️ Profissional","pago":True,"obs":""},
            ],
            "fixas": [
                {"id":"m5f1","descricao":"Seguro","valor":258.18,"categoria":"🛡️ Seguro","pago":True},
                {"id":"m5f2","descricao":"Apple","valor":19.90,"categoria":"📱 Serviços","pago":True},
                {"id":"m5f3","descricao":"Google","valor":9.99,"categoria":"📱 Serviços","pago":True},
                {"id":"m5f4","descricao":"Tarifa bancária","valor":20.75,"categoria":"🏦 Banco/Financ.","pago":True},
                {"id":"m5f5","descricao":"Vivo","valor":89.90,"categoria":"📱 Serviços","pago":True},
                {"id":"m5f6","descricao":"Remédio","valor":100.00,"categoria":"💊 Saúde","pago":True},
                {"id":"m5f7","descricao":"Claude","valor":110.00,"categoria":"📱 Serviços","pago":True},
                {"id":"m5f8","descricao":"Aula de tênis","valor":200.00,"categoria":"💪 Academia/Esporte","pago":True},
                {"id":"m5f9","descricao":"Jusbrasil","valor":58.90,"categoria":"⚖️ Profissional","pago":True},
            ],
        },
        "2025-06": {
            "lancamentos": [
                {"id":"m6l1","data":5,"descricao":"OAB SP","valor":361.23,"parcela":"2/3","categoria":"⚖️ Profissional","pago":False,"obs":""},
                {"id":"m6l2","data":5,"descricao":"Academia","valor":135.00,"parcela":"","categoria":"💪 Academia/Esporte","pago":False,"obs":""},
                {"id":"m6l3","data":9,"descricao":"Mercado Pago","valor":87.24,"parcela":"2/3","categoria":"🛒 Compras","pago":False,"obs":""},
                {"id":"m6l4","data":10,"descricao":"Aluguel e net Escritório","valor":339.95,"parcela":"","categoria":"🏠 Moradia","pago":False,"obs":""},
                {"id":"m6l5","data":11,"descricao":"Sicoob","valor":0.00,"parcela":"","categoria":"🏦 Banco/Financ.","pago":False,"obs":"valor a confirmar"},
                {"id":"m6l6","data":15,"descricao":"C&A","valor":199.99,"parcela":"1/2","categoria":"🛒 Compras","pago":False,"obs":""},
                {"id":"m6l7","data":23,"descricao":"Parcela Carro","valor":2573.20,"parcela":"9/48","categoria":"🚗 Carro","pago":False,"obs":""},
                {"id":"m6l8","data":30,"descricao":"OAB MG","valor":79.20,"parcela":"6/12","categoria":"⚖️ Profissional","pago":False,"obs":""},
            ],
            "fixas": [
                {"id":"m6f1","descricao":"Seguro","valor":258.18,"categoria":"🛡️ Seguro","pago":False},
                {"id":"m6f2","descricao":"Apple","valor":19.90,"categoria":"📱 Serviços","pago":False},
                {"id":"m6f3","descricao":"Google","valor":9.99,"categoria":"📱 Serviços","pago":False},
                {"id":"m6f4","descricao":"Tarifa bancária","valor":20.75,"categoria":"🏦 Banco/Financ.","pago":False},
                {"id":"m6f5","descricao":"Vivo","valor":89.90,"categoria":"📱 Serviços","pago":False},
                {"id":"m6f6","descricao":"Remédio","valor":100.00,"categoria":"💊 Saúde","pago":False},
                {"id":"m6f7","descricao":"Claude","valor":110.00,"categoria":"📱 Serviços","pago":False},
                {"id":"m6f8","descricao":"Aula de tênis","valor":200.00,"categoria":"💪 Academia/Esporte","pago":False},
                {"id":"m6f9","descricao":"Jusbrasil","valor":58.90,"categoria":"⚖️ Profissional","pago":False},
            ],
        },
    },
    "template_fixas": [
        {"descricao":"Seguro","valor":258.18,"categoria":"🛡️ Seguro"},
        {"descricao":"Apple","valor":19.90,"categoria":"📱 Serviços"},
        {"descricao":"Google","valor":9.99,"categoria":"📱 Serviços"},
        {"descricao":"Tarifa bancária","valor":20.75,"categoria":"🏦 Banco/Financ."},
        {"descricao":"Vivo","valor":89.90,"categoria":"📱 Serviços"},
        {"descricao":"Remédio","valor":100.00,"categoria":"💊 Saúde"},
        {"descricao":"Claude","valor":110.00,"categoria":"📱 Serviços"},
        {"descricao":"Aula de tênis","valor":200.00,"categoria":"💪 Academia/Esporte"},
        {"descricao":"Jusbrasil","valor":58.90,"categoria":"⚖️ Profissional"},
    ],
}

# ─── Storage / GitHub sync ────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
DATA_FILE  = BASE_DIR / "dados.json"
GITHUB_TOKEN = (st.secrets.get("GITHUB_TOKEN","") if hasattr(st,"secrets") else "")
GITHUB_REPO  = "adrielylovatoadv/financeiro-pessoal"
GITHUB_FILE  = "dados.json"
_GH_API      = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"

def _gh_headers():
    return {"Authorization":f"token {GITHUB_TOKEN}",
            "Accept":"application/vnd.github.v3+json",
            "Content-Type":"application/json"}

def _gh_get():
    if not GITHUB_TOKEN: return None, ""
    try:
        req = urllib.request.Request(_GH_API, headers=_gh_headers())
        with urllib.request.urlopen(req, timeout=10) as r:
            body = json.loads(r.read())
            return json.loads(base64.b64decode(body["content"]).decode()), body.get("sha","")
    except: return None, ""

def _gh_put(data, sha):
    if not GITHUB_TOKEN: return
    try:
        content = base64.b64encode(json.dumps(data,ensure_ascii=False,indent=2).encode()).decode()
        payload = json.dumps({"message":"atualiza dados","content":content,"sha":sha}).encode()
        req = urllib.request.Request(_GH_API,data=payload,headers=_gh_headers(),method="PUT")
        urllib.request.urlopen(req, timeout=15)
    except: pass

def load_data():
    gh_data, sha = _gh_get()
    if gh_data:
        DATA_FILE.write_text(json.dumps(gh_data,ensure_ascii=False,indent=2))
        st.session_state["gh_sha"] = sha
        return gh_data
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return INITIAL_DATA

def save_data(data):
    DATA_FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    _gh_put(data, st.session_state.get("gh_sha",""))

# ─── Init ─────────────────────────────────────────────────────────────────────
if "dados" not in st.session_state:
    st.session_state["dados"] = load_data()
    st.session_state.setdefault("gh_sha","")

d = st.session_state["dados"]

# ─── Header ───────────────────────────────────────────────────────────────────
_lp = BASE_DIR / "logo.png"
if _lp.exists():
    with open(_lp,"rb") as _f:
        _lb64 = base64.b64encode(_f.read()).decode()
    st.markdown(f"""
<div style='display:flex;align-items:center;gap:16px;
    background:linear-gradient(135deg,#7b1d2e 0%,#9b2335 100%);
    border-radius:12px;padding:18px 24px;margin-bottom:20px;color:white;'>
  <img src='data:image/png;base64,{_lb64}' style='width:60px;border-radius:8px;
       box-shadow:0 2px 10px rgba(0,0,0,0.35);flex-shrink:0;'>
  <div>
    <div style='font-size:9px;letter-spacing:3px;color:#fbd38d;font-weight:600;'>ADRIELY LOVATO</div>
    <h1 style='margin:3px 0 2px;color:white;font-size:20px;'>💰 CONTROLE FINANCEIRO PESSOAL</h1>
    <p style='margin:0;color:#fbd38d;font-size:12px;'>Gestão de gastos mensais · 2025</p>
  </div>
</div>""", unsafe_allow_html=True)

# ─── Sidebar: seletor de mês ──────────────────────────────────────────────────
meses_keys = sorted(d["meses"].keys())
mes_labels  = [nome_mes(k) for k in meses_keys]

with st.sidebar:
    st.markdown("### 📅 Mês")
    idx_atual = len(meses_keys) - 1  # padrão = último mês
    idx_sel = st.selectbox("", mes_labels, index=idx_atual, label_visibility="collapsed")
    mes_key = meses_keys[mes_labels.index(idx_sel)]

    st.markdown("---")
    st.markdown("### ➕ Novo mês")
    # Calcula próximo mês
    uy, um = int(mes_key.split("-")[0]), int(mes_key.split("-")[1])
    nm, ny = (um % 12) + 1, uy + (1 if um == 12 else 0)
    prox_key = f"{ny}-{nm:02d}"
    prox_nome = nome_mes(prox_key)
    if prox_key not in d["meses"]:
        if st.button(f"Criar {prox_nome}", use_container_width=True):
            d["meses"][prox_key] = {
                "lancamentos": [],
                "fixas": [
                    {"id": str(uuid.uuid4()), "descricao": t["descricao"],
                     "valor": t["valor"], "categoria": t["categoria"], "pago": False}
                    for t in d.get("template_fixas", [])
                ],
            }
            save_data(d)
            st.rerun()
    else:
        st.caption(f"✅ {prox_nome} já existe")

# ─── Dados do mês selecionado ─────────────────────────────────────────────────
mes = d["meses"][mes_key]
lanc  = mes.get("lancamentos", [])
fixas = mes.get("fixas", [])

total_lanc  = sum(l["valor"] for l in lanc)
total_fixas = sum(f["valor"] for f in fixas)
total_geral = total_lanc + total_fixas
total_pago  = sum(l["valor"] for l in lanc if l["pago"]) + sum(f["valor"] for f in fixas if f["pago"])
total_pend  = total_geral - total_pago

# ─── Abas ─────────────────────────────────────────────────────────────────────
tab_res, tab_lanc, tab_fix, tab_parc, tab_add = st.tabs([
    "📊 Resumo", "📋 Lançamentos", "🔁 Contas Fixas", "📅 Parcelas", "➕ Novo Gasto"
])

# ════════════════════════════════════════════════════════════════════════════════
# ABA: RESUMO
# ════════════════════════════════════════════════════════════════════════════════
with tab_res:
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class='card'>
        <div class='card-lbl'>Total do mês</div>
        <div class='card-val' style='color:#7b1d2e;'>{fmt(total_geral)}</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class='card'>
        <div class='card-lbl'>Pago</div>
        <div class='card-val' style='color:#38a169;'>{fmt(total_pago)}</div>
    </div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class='card'>
        <div class='card-lbl'>A pagar</div>
        <div class='card-val' style='color:#e53e3e;'>{fmt(total_pend)}</div>
    </div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class='card'>
        <div class='card-lbl'>Fixas</div>
        <div class='card-val' style='color:#4299e1;'>{fmt(total_fixas)}</div>
        <div class='card-sub'>Variáveis: {fmt(total_lanc)}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Breakdown por categoria
    cat_totais = {}
    for item in lanc + fixas:
        cat = item.get("categoria","🎯 Outros")
        cat_totais[cat] = cat_totais.get(cat, 0) + item["valor"]
    cat_totais = dict(sorted(cat_totais.items(), key=lambda x: x[1], reverse=True))

    st.markdown("<div class='secao-titulo'>Gastos por categoria</div>", unsafe_allow_html=True)

    for cat, val in cat_totais.items():
        if val <= 0: continue
        pct = val / total_geral * 100 if total_geral > 0 else 0
        cor = CAT_CORES.get(cat, "#cbd5e0")
        c_l, c_v, c_b = st.columns([3, 1.5, 4])
        c_l.markdown(f"**{cat}**")
        c_v.markdown(f"<div style='text-align:right;font-weight:600;color:{cor};'>{fmt(val)}</div>", unsafe_allow_html=True)
        c_b.markdown(
            f"<div class='barra-bg'><div class='barra-fill' style='width:{pct:.0f}%;background:{cor};'></div></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Comparativo meses anteriores
    if len(meses_keys) > 1:
        st.markdown("<div class='secao-titulo'>Comparativo mensal</div>", unsafe_allow_html=True)
        cols_hist = st.columns(min(len(meses_keys), 4))
        for i, mk in enumerate(sorted(meses_keys)[-4:]):
            ml = d["meses"][mk].get("lancamentos",[])
            mf = d["meses"][mk].get("fixas",[])
            mt = sum(x["valor"] for x in ml) + sum(x["valor"] for x in mf)
            destaque = "7b1d2e" if mk == mes_key else "4a5568"
            cols_hist[i].markdown(f"""<div class='card'>
                <div class='card-lbl'>{nome_mes(mk)}</div>
                <div class='card-val' style='font-size:18px;color:#{destaque};'>{fmt(mt)}</div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# ABA: LANÇAMENTOS
# ════════════════════════════════════════════════════════════════════════════════
with tab_lanc:
    if not lanc:
        st.info("Nenhum lançamento neste mês. Use a aba ➕ Novo Gasto.")
    else:
        # Ordenar por dia
        lanc_ord = sorted(lanc, key=lambda x: (x.get("data",0), x.get("descricao","")))

        # Cabeçalho
        h1,h2,h3,h4,h5,h6 = st.columns([1,4,2,2,2,2])
        for h,t in zip([h1,h2,h3,h4,h5,h6],["Dia","Descrição","Valor","Parcela","Status","Ação"]):
            h.markdown(f"<div style='font-size:11px;font-weight:700;color:#718096;text-transform:uppercase;'>{t}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:4px 0 8px 0;border-color:#e2e8f0;'>", unsafe_allow_html=True)

        for item in lanc_ord:
            c1,c2,c3,c4,c5,c6 = st.columns([1,4,2,2,2,2])
            c1.markdown(f"**{int(item.get('data',0)) if item.get('data') else '—'}**")
            desc = item["descricao"]
            obs  = item.get("obs","")
            _obs_html = f'  <span style="color:#a0aec0;font-size:11px;">{obs}</span>' if obs else ''
            c2.markdown(f"**{desc}**{_obs_html}", unsafe_allow_html=True)
            c3.markdown(f"**{fmt(item['valor'])}**")
            parc = item.get("parcela","")
            c4.markdown(f"<span class='tag-parcela'>{parc}</span>" if parc else "—", unsafe_allow_html=True)
            pago = item.get("pago", False)
            c5.markdown(
                f"<span class='tag-pago'>✓ pago</span>" if pago else "<span class='tag-pendente'>● pendente</span>",
                unsafe_allow_html=True
            )
            btn_label = "✓ Pagar" if not pago else "↩ Desfazer"
            if c6.button(btn_label, key=f"lbtn_{item['id']}", use_container_width=True):
                item["pago"] = not pago
                save_data(d)
                st.rerun()

        st.markdown("---")
        st.markdown(f"**Total lançamentos:** {fmt(total_lanc)}")

        # Excluir lançamento
        with st.expander("🗑️ Excluir lançamento"):
            opcoes_del = {f"Dia {l.get('data','?')} – {l['descricao']} ({fmt(l['valor'])})": l["id"] for l in lanc_ord}
            sel_del = st.selectbox("Selecione", list(opcoes_del.keys()), key="del_lanc")
            if st.button("Excluir", key="btn_del_lanc", type="primary"):
                mes["lancamentos"] = [l for l in lanc if l["id"] != opcoes_del[sel_del]]
                save_data(d)
                st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# ABA: CONTAS FIXAS
# ════════════════════════════════════════════════════════════════════════════════
with tab_fix:
    if not fixas:
        st.info("Nenhuma conta fixa neste mês.")
    else:
        fixas_ord = sorted(fixas, key=lambda x: x.get("descricao",""))

        h1,h2,h3,h4,h5 = st.columns([4,2,2,2,2])
        for h,t in zip([h1,h2,h3,h4,h5],["Descrição","Valor","Categoria","Status","Ação"]):
            h.markdown(f"<div style='font-size:11px;font-weight:700;color:#718096;text-transform:uppercase;'>{t}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:4px 0 8px 0;border-color:#e2e8f0;'>", unsafe_allow_html=True)

        for item in fixas_ord:
            c1,c2,c3,c4,c5 = st.columns([4,2,2,2,2])
            c1.markdown(f"**{item['descricao']}**")
            c2.markdown(f"**{fmt(item['valor'])}**")
            c3.markdown(item.get("categoria",""))
            pago = item.get("pago",False)
            c4.markdown(
                f"<span class='tag-pago'>✓ pago</span>" if pago else "<span class='tag-pendente'>● pendente</span>",
                unsafe_allow_html=True
            )
            btn_label = "✓ Pagar" if not pago else "↩ Desfazer"
            if c5.button(btn_label, key=f"fbtn_{item['id']}", use_container_width=True):
                item["pago"] = not pago
                save_data(d)
                st.rerun()

        st.markdown("---")
        pago_f = sum(f["valor"] for f in fixas if f["pago"])
        pend_f = sum(f["valor"] for f in fixas if not f["pago"])
        cf1, cf2, cf3 = st.columns(3)
        cf1.metric("Total Fixas", fmt(total_fixas))
        cf2.metric("Pagas", fmt(pago_f))
        cf3.metric("Pendentes", fmt(pend_f))

    # ── Editar template de fixas ──────────────────────────────────────────────
    with st.expander("⚙️ Editar modelo de contas fixas (template para novos meses)"):
        st.caption("Essas são as contas que aparecem automaticamente ao criar um novo mês.")
        template = d.get("template_fixas", [])
        for i, t in enumerate(template):
            tc1, tc2, tc3, tc4 = st.columns([4, 2, 3, 1])
            nd = tc1.text_input("", t["descricao"], key=f"td_{i}", label_visibility="collapsed")
            nv = tc2.number_input("", value=float(t["valor"]), min_value=0.0, step=0.01, key=f"tv_{i}", label_visibility="collapsed", format="%.2f")
            nc = tc3.selectbox("", CATEGORIAS, index=CATEGORIAS.index(t["categoria"]) if t["categoria"] in CATEGORIAS else 0, key=f"tc_{i}", label_visibility="collapsed")
            if tc4.button("🗑️", key=f"tdel_{i}"):
                template.pop(i)
                d["template_fixas"] = template
                save_data(d)
                st.rerun()
            template[i] = {"descricao": nd, "valor": nv, "categoria": nc}
        if st.button("💾 Salvar template", key="save_template"):
            d["template_fixas"] = template
            save_data(d)
            st.success("Template salvo!")
        if st.button("➕ Adicionar ao template", key="add_template"):
            template.append({"descricao": "Nova conta", "valor": 0.0, "categoria": "🎯 Outros"})
            d["template_fixas"] = template
            save_data(d)
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# ABA: PARCELAS
# ════════════════════════════════════════════════════════════════════════════════
with tab_parc:
    st.markdown("<div class='secao-titulo'>Parcelas ativas – todos os meses</div>", unsafe_allow_html=True)

    # Coleta todos os itens parcelados de todos os meses
    parcelas_vistas = {}  # descricao -> {total, atual, valor_mensal, ultima_parc}
    for mk in sorted(d["meses"].keys()):
        for l in d["meses"][mk].get("lancamentos", []):
            parc_str = l.get("parcela", "")
            if not parc_str or "/" not in parc_str: continue
            try:
                atual_str, total_str = parc_str.strip().split("/")
                atual = int("".join(c for c in atual_str if c.isdigit()))
                total = int("".join(c for c in total_str if c.isdigit()))
            except: continue
            key = l["descricao"]
            if key not in parcelas_vistas or atual > parcelas_vistas[key]["atual"]:
                parcelas_vistas[key] = {
                    "atual": atual, "total": total,
                    "valor_mensal": l["valor"],
                    "categoria": l.get("categoria",""),
                    "ultimo_mes": mk,
                }

    if not parcelas_vistas:
        st.info("Nenhuma parcela registrada.")
    else:
        for desc, info in sorted(parcelas_vistas.items()):
            atual = info["atual"]
            total = info["total"]
            restam = total - atual
            pct = atual / total * 100
            valor_restante = restam * info["valor_mensal"]

            c_a, c_b = st.columns([4, 6])
            with c_a:
                st.markdown(f"**{desc}**")
                st.markdown(f"<span style='font-size:12px;color:#718096;'>{info['categoria']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span class='tag-parcela'>{atual}/{total} parcelas</span> "
                            f"<span style='font-size:12px;color:#4a5568;margin-left:8px;'>{fmt(info['valor_mensal'])}/mês</span>",
                            unsafe_allow_html=True)
                st.markdown(f"<span style='font-size:12px;color:#e53e3e;'>Restam {restam}x = {fmt(valor_restante)}</span>",
                            unsafe_allow_html=True)
            with c_b:
                st.markdown(
                    f"<div style='margin-top:12px;'><div class='barra-bg'>"
                    f"<div class='barra-fill' style='width:{pct:.0f}%;'></div></div>"
                    f"<div style='text-align:right;font-size:11px;color:#718096;margin-top:2px;'>{pct:.0f}% pago</div></div>",
                    unsafe_allow_html=True
                )
            st.markdown("<hr style='margin:8px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# ABA: NOVO GASTO
# ════════════════════════════════════════════════════════════════════════════════
with tab_add:
    tipo = st.radio("Tipo de gasto", ["📋 Lançamento (variável)", "🔁 Conta fixa"], horizontal=True)

    if tipo == "📋 Lançamento (variável)":
        with st.form("form_lanc", clear_on_submit=True):
            fc1, fc2 = st.columns(2)
            desc_n = fc1.text_input("Descrição *", placeholder="Ex: Nubank, Academia...")
            val_n  = fc2.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            fd1, fd2, fd3 = st.columns(3)
            dia_n  = fd1.number_input("Dia do mês", min_value=1, max_value=31, value=1)
            parc_n = fd2.text_input("Parcela", placeholder="Ex: 2/6")
            cat_n  = fd3.selectbox("Categoria", CATEGORIAS)
            obs_n  = st.text_input("Observação", placeholder="opcional")
            pago_n = st.checkbox("Já pago?")

            if st.form_submit_button("💾 Adicionar lançamento", use_container_width=True, type="primary"):
                if desc_n and val_n > 0:
                    mes["lancamentos"].append({
                        "id": str(uuid.uuid4()), "data": int(dia_n),
                        "descricao": desc_n.strip(), "valor": float(val_n),
                        "parcela": parc_n.strip(), "categoria": cat_n,
                        "pago": pago_n, "obs": obs_n.strip(),
                    })
                    save_data(d)
                    st.success(f"✅ {desc_n} adicionado!")
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
    else:
        with st.form("form_fixa", clear_on_submit=True):
            ff1, ff2, ff3 = st.columns(3)
            desc_f = ff1.text_input("Descrição *", placeholder="Ex: Seguro...")
            val_f  = ff2.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            cat_f  = ff3.selectbox("Categoria", CATEGORIAS)
            pago_f = st.checkbox("Já pago?")

            if st.form_submit_button("💾 Adicionar conta fixa", use_container_width=True, type="primary"):
                if desc_f and val_f > 0:
                    mes["fixas"].append({
                        "id": str(uuid.uuid4()), "descricao": desc_f.strip(),
                        "valor": float(val_f), "categoria": cat_f, "pago": pago_f,
                    })
                    save_data(d)
                    st.success(f"✅ {desc_f} adicionado!")
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")

    st.markdown("---")
    st.caption("💡 Para marcar gastos como pagos, use as abas **Lançamentos** ou **Contas Fixas**.")
