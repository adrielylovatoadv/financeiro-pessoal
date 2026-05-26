"""
Meu Dinheiro – Controle Financeiro Pessoal
Adriely Lovato · 2025
"""

import streamlit as st
import json
import os
import base64
import uuid
import urllib.request
import urllib.error
from datetime import date as _date
from pathlib import Path
import streamlit.components.v1 as _comp

# ─── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meu Dinheiro",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── PWA ─────────────────────────────────────────────────────────────────────
_comp.html("""<script>
(function(){
  var d=window.parent.document;
  if(d.querySelector('link[rel="apple-touch-icon"]'))return;
  var cv=document.createElement('canvas'); cv.width=cv.height=192;
  var ctx=cv.getContext('2d');
  ctx.fillStyle='#2D6A4F';
  if(ctx.roundRect){ctx.roundRect(0,0,192,192,48);}else{ctx.rect(0,0,192,192);}
  ctx.fill();
  ctx.fillStyle='#fff'; ctx.font='bold 100px serif';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText('🌿',96,100);
  var png=cv.toDataURL('image/png');
  var lnk=d.createElement('link');
  lnk.rel='apple-touch-icon'; lnk.sizes='192x192'; lnk.href=png;
  d.head.appendChild(lnk);
  var manifest={name:'Meu Dinheiro',short_name:'Dinheiro',
    display:'standalone',background_color:'#F7F3EE',theme_color:'#2D6A4F',
    icons:[{src:png,sizes:'192x192',type:'image/png'}]};
  var blob=new Blob([JSON.stringify(manifest)],{type:'application/json'});
  var ml=d.createElement('link'); ml.rel='manifest';
  ml.href=URL.createObjectURL(blob); d.head.appendChild(ml);
})();
</script>""", height=0)


# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp { background:#F7F3EE !important; }
/* Esconde barra preta do Streamlit */
header[data-testid="stHeader"] { display:none !important; }
div[data-testid="stToolbar"] { display:none !important; }
#MainMenu { display:none !important; }
.block-container {
    padding-top:1.2rem !important;
    padding-left:1rem !important;
    padding-right:1rem !important;
    max-width:480px;
}
/* esconde sidebar no mobile */
section[data-testid="stSidebar"] { display:none !important; }
button[data-testid="collapsedControl"] { display:none !important; }

/* Cards */
.card {
    background:white; border-radius:16px;
    padding:18px; margin-bottom:12px;
    box-shadow:0 1px 6px rgba(0,0,0,0.07);
}
.card-sm {
    background:white; border-radius:12px;
    padding:14px 16px; margin-bottom:10px;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);
}

/* Versículo */
.versiculo {
    background:linear-gradient(135deg,#2D6A4F 0%,#40916C 100%);
    border-radius:16px; padding:20px; margin-bottom:12px; color:white;
}
.versiculo-texto {
    font-size:15px; line-height:1.65; font-style:italic;
    color:rgba(255,255,255,0.95); margin:0 0 10px 0;
}
.versiculo-ref {
    font-size:11px; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; color:rgba(255,255,255,0.65);
}

/* Valores */
.valor-grande { font-size:26px; font-weight:700; color:#1A202C; line-height:1; }
.valor-label  { font-size:10px; color:#A0AEC0; text-transform:uppercase;
    letter-spacing:1px; margin-bottom:4px; }
.valor-verde    { color:#276749; }
.valor-vermelho { color:#9B2C2C; }

/* Tags */
.tag-pago { background:#C6F6D5; color:#276749; border-radius:20px;
    padding:3px 10px; font-size:11px; font-weight:700; }
.tag-pend { background:#FED7D7; color:#9B2C2C; border-radius:20px;
    padding:3px 10px; font-size:11px; font-weight:700; }

/* Barra de progresso */
.prog-bg   { background:#EDF2F7; border-radius:8px; height:8px; overflow:hidden; }
.prog-fill { background:linear-gradient(90deg,#2D6A4F,#D4A853);
    height:100%; border-radius:8px; }

/* Linha de item */
.item-row {
    display:flex; justify-content:space-between; align-items:flex-start;
    padding:13px 0; border-bottom:1px solid #F0EDE8;
}
.item-row:last-child { border-bottom:none; }
.item-desc { font-weight:600; color:#2D3748; font-size:15px; }
.item-sub  { font-size:12px; color:#A0AEC0; margin-top:3px; }
.item-val  { font-weight:700; font-size:16px; color:#2D3748; white-space:nowrap; }

/* Seção título */
.sec { font-size:11px; font-weight:700; color:#A0AEC0;
    text-transform:uppercase; letter-spacing:1.5px; margin:18px 0 8px; }

/* Botões primários — grandes para toque */
.stButton>button {
    border-radius:12px !important; font-weight:600 !important;
    border:none !important;
    min-height:44px !important;
    font-size:15px !important;
    width:100% !important;
}
/* Botões secundários (ações de item) — compactos e discretos */
button[data-testid="baseButton-secondary"] {
    min-height:34px !important;
    font-size:16px !important;
    background:rgba(0,0,0,0.04) !important;
    color:#718096 !important;
    border-radius:10px !important;
    padding:4px !important;
}

/* Abas estilo pill */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:#E8E0D5; border-radius:14px; padding:4px; gap:2px;
    position:sticky; top:0; z-index:10;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius:11px; font-size:13px; font-weight:500;
    color:#8B6F47; padding:8px 4px !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background:white !important; color:#2D6A4F !important;
    font-weight:700 !important; box-shadow:0 1px 4px rgba(0,0,0,0.12) !important;
}

/* Inputs maiores no mobile */
.stTextInput input, .stNumberInput input {
    font-size:16px !important; /* evita zoom automático no iOS */
    min-height:46px !important;
    border-radius:12px !important;
}
.stSelectbox > div > div {
    border-radius:12px !important;
    font-size:15px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Conteúdo: versículos e dicas ────────────────────────────────────────────
VERSICULO = [
    ("Provérbios 21:20", "Na casa do sábio há precioso tesouro e azeite, mas o homem tolo os desperdiça."),
    ("Provérbios 13:11", "A riqueza obtida às pressas diminui, mas quem a ajunta pouco a pouco a aumenta."),
    ("Lucas 14:28", "Pois qual de vós, desejando edificar uma torre, não se assenta primeiro e calcula a despesa?"),
    ("Provérbios 22:7", "O rico domina os pobres, e o devedor é servo do credor."),
    ("Provérbios 3:9-10", "Honra ao Senhor com os teus bens e com as primícias de toda a tua renda, e os teus celeiros se encherão com abundância."),
    ("Filipenses 4:19", "O meu Deus, segundo as suas riquezas em glória, suprirá todas as vossas necessidades em Cristo Jesus."),
    ("Mateus 6:33", "Buscai, pois, em primeiro lugar o reino de Deus e a sua justiça, e todas essas coisas vos serão acrescentadas."),
    ("Eclesiastes 5:10", "Quem ama o dinheiro nunca se satisfaz com dinheiro; nem quem ama a abundância colhe renda dele."),
    ("Provérbios 6:6-8", "Vai ter com a formiga, ó preguiçoso, considera os seus caminhos e sê sábio. Ela, sem ter guia, nem inspetor, nem senhor, prepara no verão o seu pão."),
    ("I Timóteo 6:6", "A piedade com contentamento é grande ganho. Porque nada trouxemos para este mundo e é certo que nada podemos levar."),
    ("Provérbios 27:12", "O avisado vê o mal e esconde-se, mas os simples passam e sofrem a pena."),
    ("Deuteronômio 8:18", "Lembra-te do Senhor teu Deus, porque é ele que te dá força para adquirir riqueza."),
    ("Provérbios 22:26-27", "Não sejas dos que batem as palmas, nem dos que são fiadores de dívidas. Se não tens com que pagar, por que hão de tomar a tua cama debaixo de ti?"),
    ("Eclesiastes 11:2", "Reparte com sete, e ainda com oito, pois não sabes que mal poderá vir sobre a terra."),
    ("Provérbios 28:20", "O homem fiel terá muitas bênçãos, mas o que se apressa a ficar rico não ficará impune."),
    ("Mateus 6:21", "Porque onde estiver o seu tesouro, aí estará também o seu coração."),
    ("Provérbios 13:22", "O homem bom deixa herança para os filhos dos seus filhos."),
    ("I Coríntios 16:2", "No primeiro dia da semana, cada um de vós ponha de parte, segundo a sua prosperidade, para não se fazerem coletas quando eu for."),
    ("Romanos 13:8", "A ninguém devais coisa alguma, exceto o amor mutuo."),
    ("Provérbios 11:24", "Há quem distribua, e ainda lhe aumenta a riqueza; e há quem retenha mais do que é justo, mas empobrecerá."),
]

def versiculo_do_dia():
    idx = _date.today().timetuple().tm_yday % len(VERSICULO)
    return VERSICULO[idx]

# ─── Constantes ───────────────────────────────────────────────────────────────
CATEGORIAS = [
    "💳 Cartão","🏦 Banco/Financ.","🏠 Moradia","🚗 Carro",
    "💊 Saúde","💪 Academia/Esporte","⚖️ Profissional","📱 Serviços",
    "🛡️ Seguro","🛒 Compras","💄 Beleza","🎾 Lazer","🎯 Outros",
]

CATEGORIAS_RECEITA = [
    "⚖️ Honorários","💼 Salário","🏠 Aluguel recebido",
    "🤝 Acordo/Êxito","💰 Reembolso","🎁 Presente","📈 Investimento","🎯 Outros",
]

MESES_PT = {
    "01":"Janeiro","02":"Fevereiro","03":"Março","04":"Abril",
    "05":"Maio","06":"Junho","07":"Julho","08":"Agosto",
    "09":"Setembro","10":"Outubro","11":"Novembro","12":"Dezembro",
}

def nome_mes(key):
    y, m = key.split("-")
    return f"{MESES_PT[m]}/{y}"

def fmt(v):
    s = f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
    return f"R$ {s}"

# ─── Dados iniciais ───────────────────────────────────────────────────────────
INITIAL_DATA = {
    "meses": {
        "2025-03": {
            "receitas": [],
            "meta_poupanca": 0.0,
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
            "receitas": [],
            "meta_poupanca": 0.0,
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
            "receitas": [],
            "meta_poupanca": 0.0,
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
            "receitas": [],
            "meta_poupanca": 0.0,
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
    "poupanca": {
        "objetivo": "",
        "meta_total": 0.0,
        "depositos": [],
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

# ─── Storage ──────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).parent
DATA_FILE = BASE_DIR / "dados.json"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN","") if hasattr(st,"secrets") else ""
GITHUB_REPO  = "adrielylovatoadv/financeiro-pessoal"
GITHUB_FILE  = "dados.json"
_GH_API = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE}"

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
        content = base64.b64encode(
            json.dumps(data,ensure_ascii=False,indent=2).encode()).decode()
        body = {"message":"atualiza dados","content":content}
        if sha:  # SHA só vai no payload se o arquivo já existir
            body["sha"] = sha
        payload = json.dumps(body).encode()
        req = urllib.request.Request(_GH_API,data=payload,headers=_gh_headers(),method="PUT")
        with urllib.request.urlopen(req,timeout=15) as resp:
            # Atualiza SHA local para o próximo save
            resp_body = json.loads(resp.read())
            new_sha = resp_body.get("content",{}).get("sha","")
            if new_sha:
                st.session_state["gh_sha"] = new_sha
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

if "dados" not in st.session_state:
    st.session_state["dados"] = load_data()
    st.session_state.setdefault("gh_sha","")

d = st.session_state["dados"]

# Garante chaves de receita em todos os meses (retrocompatibilidade)
for _mk in d["meses"]:
    d["meses"][_mk].setdefault("receitas", [])
    d["meses"][_mk].setdefault("meta_poupanca", 0.0)
# Garante estrutura de poupança
d.setdefault("poupanca", {"objetivo": "", "meta_total": 0.0, "depositos": []})

# ─── Cabeçalho ────────────────────────────────────────────────────────────────
meses_keys = sorted(d["meses"].keys())
mes_labels = [nome_mes(k) for k in meses_keys]

st.markdown("<p style='margin:8px 0 2px;font-size:22px;font-weight:700;color:#2D6A4F;'>🌿 Meu Dinheiro</p>", unsafe_allow_html=True)
_hoje_key    = _date.today().strftime("%Y-%m")
_default_idx = meses_keys.index(_hoje_key) if _hoje_key in meses_keys else len(meses_keys) - 1
# key com mês/ano garante que volta ao mês atual a cada novo mês (e nova sessão)
mes_sel = st.selectbox("", mes_labels, index=_default_idx,
                        key=f"ms_{_date.today().strftime('%Y%m')}",
                        label_visibility="collapsed")
mes_key = meses_keys[mes_labels.index(mes_sel)]

# ─── Versículo do dia ─────────────────────────────────────────────────────────
ver = versiculo_do_dia()
st.markdown(f"""
<div class="versiculo">
  <p class="versiculo-texto">"{ver[1]}"</p>
  <div class="versiculo-ref">📖 {ver[0]}</div>
</div>
""", unsafe_allow_html=True)

# ─── Dados do mês ─────────────────────────────────────────────────────────────
mes         = d["meses"][mes_key]
lanc        = mes.get("lancamentos", [])
fixas       = mes.get("fixas", [])
todos       = lanc + fixas
receitas_m  = mes.get("receitas", [])
meta_poupc  = mes.get("meta_poupanca", 0.0)

total       = sum(i["valor"] for i in todos)
pago        = sum(i["valor"] for i in todos if i.get("pago"))
pend        = total - pago
total_rec   = sum(r["valor"] for r in receitas_m)
saldo_mes   = total_rec - total
_saldo_cor  = "#276749" if saldo_mes >= 0 else "#9B2C2C"
_saldo_disp = fmt(abs(saldo_mes)) if saldo_mes >= 0 else "- " + fmt(abs(saldo_mes))

# ─── Cards de resumo ──────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.markdown(f"""<div class='card' style='text-align:center;'>
  <div class='valor-label'>Receitas</div>
  <div class='valor-grande valor-verde'>{fmt(total_rec)}</div>
</div>""", unsafe_allow_html=True)
c2.markdown(f"""<div class='card' style='text-align:center;'>
  <div class='valor-label'>Débitos</div>
  <div class='valor-grande valor-vermelho'>{fmt(total)}</div>
</div>""", unsafe_allow_html=True)
c3.markdown(f"""<div class='card' style='text-align:center;'>
  <div class='valor-label'>A pagar</div>
  <div class='valor-grande valor-vermelho'>{fmt(pend)}</div>
</div>""", unsafe_allow_html=True)

# ─── Abas ─────────────────────────────────────────────────────────────────────
tab_g, tab_f, tab_rec, tab_poupa, tab_p, tab_r = st.tabs([
    "💸 Gastos", "🔁 Fixas", "💰 Receita", "🐷 Poupar", "📅 Parcelas", "📊 Resumo"
])

# ═══════════════════════════════════════════════════════════════
# GASTOS (lançamentos variáveis)
# ═══════════════════════════════════════════════════════════════
with tab_g:
    # Mês de referência + botão adicionar
    cref, cadd = st.columns([3, 2])
    cref.markdown(f"<div style='font-size:13px;color:#718096;padding-top:8px;'>📅 {nome_mes(mes_key)}</div>",
                  unsafe_allow_html=True)
    if cadd.button("➕ Novo gasto", key="add_lanc_top", use_container_width=True):
        st.session_state["show_add_lanc"] = not st.session_state.get("show_add_lanc", False)

    # Formulário de adição rápida
    if st.session_state.get("show_add_lanc"):
        with st.form("f_lanc_g", clear_on_submit=True):
            desc_q = st.text_input("Descrição *", placeholder="Ex: Farmácia, Mercado...")
            val_q  = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            cq1, cq2 = st.columns(2)
            dia_q  = cq1.number_input("Dia", min_value=1, max_value=31, value=_date.today().day)
            parc_q = cq2.text_input("Parcela", placeholder="Ex: 1/6")
            cat_q  = st.selectbox("Categoria", CATEGORIAS)
            obs_q  = st.text_input("Observação", placeholder="opcional")
            pago_q = st.checkbox("Já pago?")
            cs1, cs2 = st.columns(2)
            if cs1.form_submit_button("✓ Adicionar", use_container_width=True, type="primary"):
                if desc_q.strip() and val_q > 0:
                    mes["lancamentos"].append({
                        "id": str(uuid.uuid4()), "data": int(dia_q),
                        "descricao": desc_q.strip(), "valor": float(val_q),
                        "parcela": parc_q.strip(), "categoria": cat_q,
                        "pago": pago_q, "obs": obs_q.strip(),
                    })
                    st.session_state["show_add_lanc"] = False
                    save_data(d)
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
            if cs2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_lanc"] = False
                st.rerun()

    if not lanc:
        st.markdown("<div style='text-align:center;color:#a0aec0;padding:30px 0;'>Nenhum gasto. Toque em ➕ Novo gasto.</div>",
                    unsafe_allow_html=True)
    else:
        lanc_ord = sorted(lanc, key=lambda x: x.get("data", 0))
        for item in lanc_ord:
            iid     = item["id"]
            pago_i  = item.get("pago", False)
            parc    = item.get("parcela", "")
            obs     = item.get("obs", "")
            sub     = " · ".join(filter(None, [
                f"Dia {int(item['data'])}" if item.get("data") else "",
                parc, obs
            ]))
            borda   = "#68d391" if pago_i else "#fc8181"
            tag     = "<span class='tag-pago'>✓ pago</span>" if pago_i else "<span class='tag-pend'>pendente</span>"

            # ── Modo edição ──
            if st.session_state.get("editing_lanc") == iid:
                st.markdown("<div style='background:white;border-radius:14px;padding:16px;"
                            "margin-bottom:4px;box-shadow:0 1px 6px rgba(0,0,0,0.1);'>",
                            unsafe_allow_html=True)
                st.markdown(f"**✏️ Editando: {item['descricao']}**")
                with st.form(f"ef_lanc_{iid}"):
                    nd = st.text_input("Descrição", value=item["descricao"])
                    nv = st.number_input("Valor (R$)", value=float(item["valor"]), step=0.01, format="%.2f")
                    ec1, ec2 = st.columns(2)
                    ndia  = ec1.number_input("Dia", value=int(item.get("data", 1)), min_value=1, max_value=31)
                    nparc = ec2.text_input("Parcela", value=item.get("parcela", ""))
                    ncat  = st.selectbox("Categoria", CATEGORIAS,
                                         index=CATEGORIAS.index(item["categoria"]) if item.get("categoria") in CATEGORIAS else 0)
                    nobs  = st.text_input("Observação", value=item.get("obs", ""))
                    es1, es2 = st.columns(2)
                    if es1.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
                        item.update({"descricao": nd, "valor": float(nv), "data": int(ndia),
                                     "parcela": nparc, "categoria": ncat, "obs": nobs})
                        st.session_state.pop("editing_lanc", None)
                        save_data(d)
                        st.rerun()
                    if es2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_lanc", None)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Modo normal ──
            else:
                st.markdown(f"""
<div style='background:white;border-radius:14px;padding:14px 16px;
     border-left:4px solid {borda};box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:2px;'>
  <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
    <div style='flex:1;'>
      <div style='font-weight:700;font-size:16px;color:#2D3748;'>{item['descricao']}</div>
      <div style='font-size:12px;color:#a0aec0;margin-top:3px;'>{sub}</div>
    </div>
    <div style='text-align:right;margin-left:12px;flex-shrink:0;'>
      <div style='font-weight:700;font-size:18px;color:#2D3748;'>{fmt(item['valor'])}</div>
      {tag}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

                # Ações inline
                ba, bb, bc = st.columns([7, 1, 1])
                lbl_pay = "↩ Pago" if pago_i else "✓ Pagar"
                if ba.button(lbl_pay, key=f"pay_{iid}", use_container_width=True, type="primary"):
                    item["pago"] = not pago_i
                    save_data(d)
                    st.rerun()
                if bb.button("✏️", key=f"edit_{iid}", use_container_width=True):
                    st.session_state["editing_lanc"] = iid
                    st.rerun()
                if bc.button("✕", key=f"del_{iid}", use_container_width=True):
                    st.session_state[f"cdel_{iid}"] = True
                    st.rerun()

                # Confirmação exclusão
                if st.session_state.get(f"cdel_{iid}"):
                    st.warning(f"Excluir **{item['descricao']}**?")
                    dc1, dc2 = st.columns(2)
                    if dc1.button("Sim, excluir", key=f"ydel_{iid}", type="primary", use_container_width=True):
                        mes["lancamentos"] = [l for l in lanc if l["id"] != iid]
                        st.session_state.pop(f"cdel_{iid}", None)
                        save_data(d)
                        st.rerun()
                    if dc2.button("Cancelar", key=f"ndel_{iid}", use_container_width=True):
                        st.session_state.pop(f"cdel_{iid}", None)
                        st.rerun()

            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FIXAS
# ═══════════════════════════════════════════════════════════════
with tab_f:
    # Mês de referência + totais
    tf = sum(i["valor"] for i in fixas)
    pf = sum(i["valor"] for i in fixas if i.get("pago"))
    crf, cadf = st.columns([3, 2])
    crf.markdown(f"<div style='font-size:13px;color:#718096;padding-top:8px;'>📅 {nome_mes(mes_key)}</div>",
                 unsafe_allow_html=True)
    if cadf.button("➕ Nova fixa", key="add_fixa_top", use_container_width=True):
        st.session_state["show_add_fixa"] = not st.session_state.get("show_add_fixa", False)

    # Total compacto
    st.markdown(f"<div style='display:flex;gap:16px;margin:8px 0;'>"
                f"<span style='font-size:13px;color:#718096;'>Total: <b style='color:#2D3748;'>{fmt(tf)}</b></span>"
                f"<span style='font-size:13px;color:#38a169;'>Pago: <b>{fmt(pf)}</b></span>"
                f"<span style='font-size:13px;color:#e53e3e;'>Falta: <b>{fmt(tf-pf)}</b></span>"
                f"</div>", unsafe_allow_html=True)

    # Formulário de adição rápida
    if st.session_state.get("show_add_fixa"):
        with st.form("f_fixa_g", clear_on_submit=True):
            desc_fq = st.text_input("Descrição *", placeholder="Ex: Streaming, Plano...")
            val_fq  = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            cat_fq  = st.selectbox("Categoria", CATEGORIAS)
            pago_fq = st.checkbox("Já pago?")
            fs1, fs2 = st.columns(2)
            if fs1.form_submit_button("✓ Adicionar", use_container_width=True, type="primary"):
                if desc_fq.strip() and val_fq > 0:
                    mes["fixas"].append({
                        "id": str(uuid.uuid4()), "descricao": desc_fq.strip(),
                        "valor": float(val_fq), "categoria": cat_fq, "pago": pago_fq,
                    })
                    st.session_state["show_add_fixa"] = False
                    save_data(d)
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
            if fs2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_fixa"] = False
                st.rerun()

    if not fixas:
        st.markdown("<div style='text-align:center;color:#a0aec0;padding:30px 0;'>Nenhuma conta fixa.</div>",
                    unsafe_allow_html=True)
    else:
        fixas_ord = sorted(fixas, key=lambda x: (x.get("pago", False), x["descricao"]))
        for item in fixas_ord:
            fid    = item["id"]
            pago_f = item.get("pago", False)
            borda  = "#68d391" if pago_f else "#fc8181"
            tag    = "<span class='tag-pago'>✓ pago</span>" if pago_f else "<span class='tag-pend'>pendente</span>"

            # ── Modo edição ──
            if st.session_state.get("editing_fixa") == fid:
                st.markdown("<div style='background:white;border-radius:14px;padding:16px;"
                            "margin-bottom:4px;box-shadow:0 1px 6px rgba(0,0,0,0.1);'>",
                            unsafe_allow_html=True)
                st.markdown(f"**✏️ Editando: {item['descricao']}**")
                with st.form(f"ef_fixa_{fid}"):
                    fnd  = st.text_input("Descrição", value=item["descricao"])
                    fnv  = st.number_input("Valor (R$)", value=float(item["valor"]), step=0.01, format="%.2f")
                    fnc  = st.selectbox("Categoria", CATEGORIAS,
                                        index=CATEGORIAS.index(item["categoria"]) if item.get("categoria") in CATEGORIAS else 0)
                    fes1, fes2 = st.columns(2)
                    if fes1.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
                        item.update({"descricao": fnd, "valor": float(fnv), "categoria": fnc})
                        st.session_state.pop("editing_fixa", None)
                        save_data(d)
                        st.rerun()
                    if fes2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_fixa", None)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Modo normal ──
            else:
                st.markdown(f"""
<div style='background:white;border-radius:14px;padding:14px 16px;
     border-left:4px solid {borda};box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:2px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div>
      <div style='font-weight:700;font-size:16px;color:#2D3748;'>{item['descricao']}</div>
      <div style='font-size:12px;color:#a0aec0;margin-top:3px;'>{item.get('categoria','')}</div>
    </div>
    <div style='text-align:right;'>
      <div style='font-weight:700;font-size:18px;color:#2D3748;'>{fmt(item['valor'])}</div>
      {tag}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

                fa, fb, fc = st.columns([7, 1, 1])
                lbl_fp = "↩ Pago" if pago_f else "✓ Pagar"
                if fa.button(lbl_fp, key=f"fpay_{fid}", use_container_width=True, type="primary"):
                    item["pago"] = not pago_f
                    save_data(d)
                    st.rerun()
                if fb.button("✏️", key=f"fedit_{fid}", use_container_width=True):
                    st.session_state["editing_fixa"] = fid
                    st.rerun()
                if fc.button("✕", key=f"fdel_{fid}", use_container_width=True):
                    st.session_state[f"cfdel_{fid}"] = True
                    st.rerun()

                if st.session_state.get(f"cfdel_{fid}"):
                    st.warning(f"Excluir **{item['descricao']}**?")
                    fc1, fc2 = st.columns(2)
                    if fc1.button("Sim, excluir", key=f"yfdel_{fid}", type="primary", use_container_width=True):
                        mes["fixas"] = [f for f in fixas if f["id"] != fid]
                        st.session_state.pop(f"cfdel_{fid}", None)
                        save_data(d)
                        st.rerun()
                    if fc2.button("Cancelar", key=f"nfdel_{fid}", use_container_width=True):
                        st.session_state.pop(f"cfdel_{fid}", None)
                        st.rerun()

            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# RECEITA
# ═══════════════════════════════════════════════════════════════
with tab_rec:
    rec_list = mes.get("receitas", [])

    # Cabeçalho do mês + botão adicionar
    crec, cadrec = st.columns([3, 2])
    crec.markdown(f"<div style='font-size:13px;color:#718096;padding-top:8px;'>📅 {nome_mes(mes_key)}</div>",
                  unsafe_allow_html=True)
    if cadrec.button("➕ Nova receita", key="add_rec_top", use_container_width=True):
        st.session_state["show_add_rec"] = not st.session_state.get("show_add_rec", False)

    # Formulário de adição rápida
    if st.session_state.get("show_add_rec"):
        with st.form("f_rec_g", clear_on_submit=True):
            desc_rq = st.text_input("Descrição *", placeholder="Ex: Honorários, Salário...")
            val_rq  = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            dia_rq  = st.number_input("Dia", min_value=1, max_value=31, value=_date.today().day)
            cat_rq  = st.selectbox("Categoria", CATEGORIAS_RECEITA)
            obs_rq  = st.text_input("Observação", placeholder="opcional")
            rec_rq  = st.checkbox("Já recebido?", value=True)
            rs1, rs2 = st.columns(2)
            if rs1.form_submit_button("✓ Adicionar", use_container_width=True, type="primary"):
                if desc_rq.strip() and val_rq > 0:
                    mes["receitas"].append({
                        "id": str(uuid.uuid4()), "data": int(dia_rq),
                        "descricao": desc_rq.strip(), "valor": float(val_rq),
                        "categoria": cat_rq, "recebido": rec_rq, "obs": obs_rq.strip(),
                    })
                    st.session_state["show_add_rec"] = False
                    save_data(d)
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
            if rs2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_rec"] = False
                st.rerun()

    # ── Card: Saldo e Meta de Poupança ──────────────────────────
    st.markdown("<div class='sec'>Saldo & Meta de poupança</div>", unsafe_allow_html=True)
    if st.session_state.get("editing_meta"):
        with st.form("f_meta"):
            nova_meta = st.number_input("Meta mensal (R$)", value=float(meta_poupc),
                                        min_value=0.0, step=100.0, format="%.2f")
            mm1, mm2 = st.columns(2)
            if mm1.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
                mes["meta_poupanca"] = float(nova_meta)
                st.session_state.pop("editing_meta", None)
                save_data(d)
                st.rerun()
            if mm2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.pop("editing_meta", None)
                st.rerun()
    else:
        _meta_pct = min((saldo_mes / meta_poupc * 100) if meta_poupc > 0 else 0, 100)
        _meta_pct = max(_meta_pct, 0)
        _meta_label = fmt(meta_poupc) if meta_poupc > 0 else "Não definida"
        _saldo_icon = "✅" if saldo_mes >= 0 else "⚠️"
        st.markdown(f"""
<div class='card'>
  <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;'>
    <div>
      <div class='valor-label'>Saldo do mês</div>
      <div class='valor-grande' style='color:{_saldo_cor};'>{_saldo_disp} {_saldo_icon}</div>
    </div>
    <div style='text-align:right;'>
      <div class='valor-label'>Meta poupar</div>
      <div style='font-weight:700;font-size:18px;color:#D4A853;'>{_meta_label}</div>
    </div>
  </div>
  <div class='prog-bg'><div class='prog-fill' style='width:{_meta_pct:.0f}%;'></div></div>
  <div style='font-size:12px;color:#718096;margin-top:6px;text-align:right;'>{_meta_pct:.0f}% da meta atingido</div>
</div>""", unsafe_allow_html=True)
        if st.button("✏️ Definir meta de poupança", key="btn_meta", use_container_width=True):
            st.session_state["editing_meta"] = True
            st.rerun()

    # ── Lista de receitas ────────────────────────────────────────
    st.markdown("<div class='sec'>Receitas do mês</div>", unsafe_allow_html=True)
    if not rec_list:
        st.markdown("<div style='text-align:center;color:#a0aec0;padding:30px 0;'>Nenhuma receita. Toque em ➕ Nova receita.</div>",
                    unsafe_allow_html=True)
    else:
        # Totalizador compacto
        total_rec_l  = sum(r["valor"] for r in rec_list)
        recebido_l   = sum(r["valor"] for r in rec_list if r.get("recebido"))
        aguardando_l = total_rec_l - recebido_l
        st.markdown(
            f"<div style='display:flex;gap:16px;margin:8px 0;'>"
            f"<span style='font-size:13px;color:#718096;'>Total: <b style='color:#2D3748;'>{fmt(total_rec_l)}</b></span>"
            f"<span style='font-size:13px;color:#38a169;'>Recebido: <b>{fmt(recebido_l)}</b></span>"
            f"<span style='font-size:13px;color:#d97706;'>Aguardando: <b>{fmt(aguardando_l)}</b></span>"
            f"</div>", unsafe_allow_html=True)

        rec_ord = sorted(rec_list, key=lambda x: x.get("data", 0))
        for item in rec_ord:
            rid   = item["id"]
            rec_i = item.get("recebido", False)
            sub_r = " · ".join(filter(None, [
                f"Dia {int(item['data'])}" if item.get("data") else "",
                item.get("categoria", ""),
                item.get("obs", ""),
            ]))
            borda_r = "#68d391" if rec_i else "#f6ad55"
            tag_r   = ("<span class='tag-pago'>✓ recebido</span>" if rec_i
                       else "<span style='background:#FEFCBF;color:#B7791F;border-radius:20px;"
                            "padding:3px 10px;font-size:11px;font-weight:700;'>aguardando</span>")

            # ── Modo edição ──
            if st.session_state.get("editing_rec") == rid:
                st.markdown("<div style='background:white;border-radius:14px;padding:16px;"
                            "margin-bottom:4px;box-shadow:0 1px 6px rgba(0,0,0,0.1);'>",
                            unsafe_allow_html=True)
                st.markdown(f"**✏️ Editando: {item['descricao']}**")
                with st.form(f"ef_rec_{rid}"):
                    rnd  = st.text_input("Descrição", value=item["descricao"])
                    rnv  = st.number_input("Valor (R$)", value=float(item["valor"]), step=0.01, format="%.2f")
                    rndia = st.number_input("Dia", value=int(item.get("data", 1)), min_value=1, max_value=31)
                    rncat = st.selectbox("Categoria", CATEGORIAS_RECEITA,
                                         index=CATEGORIAS_RECEITA.index(item["categoria"])
                                         if item.get("categoria") in CATEGORIAS_RECEITA else 0)
                    rnobs = st.text_input("Observação", value=item.get("obs", ""))
                    res1, res2 = st.columns(2)
                    if res1.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
                        item.update({"descricao": rnd, "valor": float(rnv),
                                     "data": int(rndia), "categoria": rncat, "obs": rnobs})
                        st.session_state.pop("editing_rec", None)
                        save_data(d)
                        st.rerun()
                    if res2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_rec", None)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Modo normal ──
            else:
                st.markdown(f"""
<div style='background:white;border-radius:14px;padding:14px 16px;
     border-left:4px solid {borda_r};box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:2px;'>
  <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
    <div style='flex:1;'>
      <div style='font-weight:700;font-size:16px;color:#2D3748;'>{item['descricao']}</div>
      <div style='font-size:12px;color:#a0aec0;margin-top:3px;'>{sub_r}</div>
    </div>
    <div style='text-align:right;margin-left:12px;flex-shrink:0;'>
      <div style='font-weight:700;font-size:18px;color:#276749;'>{fmt(item['valor'])}</div>
      {tag_r}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

                ra, rb, rc_btn = st.columns([7, 1, 1])
                lbl_rec = "↩ Recebido" if rec_i else "✓ Receber"
                if ra.button(lbl_rec, key=f"rpay_{rid}", use_container_width=True, type="primary"):
                    item["recebido"] = not rec_i
                    save_data(d)
                    st.rerun()
                if rb.button("✏️", key=f"redit_{rid}", use_container_width=True):
                    st.session_state["editing_rec"] = rid
                    st.rerun()
                if rc_btn.button("✕", key=f"rdel_{rid}", use_container_width=True):
                    st.session_state[f"crdel_{rid}"] = True
                    st.rerun()

                if st.session_state.get(f"crdel_{rid}"):
                    st.warning(f"Excluir **{item['descricao']}**?")
                    rd1, rd2 = st.columns(2)
                    if rd1.button("Sim, excluir", key=f"yrdel_{rid}", type="primary", use_container_width=True):
                        mes["receitas"] = [r for r in rec_list if r["id"] != rid]
                        st.session_state.pop(f"crdel_{rid}", None)
                        save_data(d)
                        st.rerun()
                    if rd2.button("Cancelar", key=f"nrdel_{rid}", use_container_width=True):
                        st.session_state.pop(f"crdel_{rid}", None)
                        st.rerun()

            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PARCELAS
# ═══════════════════════════════════════════════════════════════
with tab_p:
    cp_hd, cp_add = st.columns([3, 2])
    cp_hd.markdown("<div class='sec' style='margin-top:8px;'>Parcelas ativas</div>",
                   unsafe_allow_html=True)
    if cp_add.button("➕ Nova parcela", key="add_parc_top", use_container_width=True):
        st.session_state["show_add_parc"] = not st.session_state.get("show_add_parc", False)

    if st.session_state.get("show_add_parc"):
        with st.form("f_parc_add", clear_on_submit=True):
            pa_desc = st.text_input("Descrição *", placeholder="Ex: Financiamento, Cartão...")
            pa_val  = st.number_input("Valor da parcela (R$) *", min_value=0.0, step=0.01, format="%.2f")
            pac1, pac2 = st.columns(2)
            pa_dia  = pac1.number_input("Dia vencimento", min_value=1, max_value=31, value=_date.today().day)
            pa_parc = pac2.text_input("Parcela (ex: 1/12)")
            pa_cat  = st.selectbox("Categoria", CATEGORIAS)
            pa_obs  = st.text_input("Observação", placeholder="opcional")
            pa_pago = st.checkbox("Já pago?")
            pas1, pas2 = st.columns(2)
            if pas1.form_submit_button("✓ Adicionar", use_container_width=True, type="primary"):
                if pa_desc.strip() and pa_val > 0:
                    mes["lancamentos"].append({
                        "id": str(uuid.uuid4()), "data": int(pa_dia),
                        "descricao": pa_desc.strip(), "valor": float(pa_val),
                        "parcela": pa_parc.strip(), "categoria": pa_cat,
                        "pago": pa_pago, "obs": pa_obs.strip(),
                    })
                    st.session_state["show_add_parc"] = False
                    save_data(d); st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
            if pas2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_parc"] = False; st.rerun()

    # Monta mapa com referência ao lancamento original para edição
    parcelas_map = {}
    for mk in sorted(d["meses"].keys()):
        for l in d["meses"][mk].get("lancamentos", []):
            ps = l.get("parcela", "")
            if not ps or "/" not in ps: continue
            try:
                a_s, t_s = ps.strip().split("/")
                atual   = int("".join(c for c in a_s if c.isdigit()))
                total_p = int("".join(c for c in t_s if c.isdigit()))
            except: continue
            key = l["descricao"]
            if key not in parcelas_map or atual > parcelas_map[key]["atual"]:
                parcelas_map[key] = {
                    "atual": atual, "total": total_p,
                    "valor": l["valor"], "cat": l.get("categoria", ""),
                    "obs": l.get("obs", ""), "mes_key": mk, "id": l["id"],
                }

    if not parcelas_map:
        st.markdown("<div class='card' style='text-align:center;color:#a0aec0;padding:24px;'>"
                    "Nenhuma parcela registrada.</div>", unsafe_allow_html=True)
    else:
        for desc, info in sorted(parcelas_map.items()):
            a, t   = info["atual"], info["total"]
            restam = t - a
            pct    = a / t * 100
            val_rest = restam * info["valor"]
            pid    = info["id"]

            # ── Modo edição ──
            if st.session_state.get("editing_parc") == pid:
                st.markdown("<div style='background:white;border-radius:14px;padding:16px;"
                            "margin-bottom:4px;box-shadow:0 1px 6px rgba(0,0,0,0.1);'>",
                            unsafe_allow_html=True)
                st.markdown(f"**✏️ Editando: {desc}**")
                with st.form(f"ef_parc_{pid}"):
                    pnd  = st.text_input("Descrição", value=desc)
                    pnv  = st.number_input("Valor/parcela (R$)", value=float(info["valor"]), step=0.01, format="%.2f")
                    pec1, pec2 = st.columns(2)
                    pna  = pec1.number_input("Parcela atual", value=int(a), min_value=1)
                    pnt  = pec2.number_input("Total de parcelas", value=int(t), min_value=1)
                    pncat = st.selectbox("Categoria", CATEGORIAS,
                                         index=CATEGORIAS.index(info["cat"]) if info["cat"] in CATEGORIAS else 0)
                    pnobs = st.text_input("Observação", value=info.get("obs", ""))
                    pes1, pes2 = st.columns(2)
                    if pes1.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
                        mk_edit = info["mes_key"]
                        for l in d["meses"][mk_edit].get("lancamentos", []):
                            if l["id"] == pid:
                                l.update({
                                    "descricao": pnd.strip(), "valor": float(pnv),
                                    "parcela": f"{pna}/{pnt}", "categoria": pncat, "obs": pnobs,
                                })
                                break
                        st.session_state.pop("editing_parc", None)
                        save_data(d); st.rerun()
                    if pes2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_parc", None); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Modo normal ──
            else:
                st.markdown(f"""
<div class='card-sm'>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
    <div>
      <div style='font-weight:700;color:#2D3748;font-size:14px;'>{desc}</div>
      <div style='font-size:11px;color:#a0aec0;'>{info['cat']}</div>
    </div>
    <div style='text-align:right;'>
      <div style='font-weight:700;color:#2D3748;'>{fmt(info['valor'])}/mês</div>
      <div style='font-size:11px;color:#e53e3e;'>Restam {restam}x = {fmt(val_rest)}</div>
    </div>
  </div>
  <div style='display:flex;align-items:center;gap:8px;'>
    <div class='prog-bg' style='flex:1;'>
      <div class='prog-fill' style='width:{pct:.0f}%;'></div>
    </div>
    <div style='font-size:11px;color:#718096;white-space:nowrap;'>{a}/{t}</div>
  </div>
</div>""", unsafe_allow_html=True)

                pa_a, pa_b = st.columns([1, 1])
                if pa_a.button("✏️ Editar", key=f"pedit_{pid}", use_container_width=True):
                    st.session_state["editing_parc"] = pid; st.rerun()
                if pa_b.button("✕ Excluir", key=f"pdel_{pid}", use_container_width=True):
                    st.session_state[f"cpdel_{pid}"] = True; st.rerun()

                if st.session_state.get(f"cpdel_{pid}"):
                    st.warning(f"Excluir **{desc}** ({nome_mes(info['mes_key'])})?")
                    pd1, pd2 = st.columns(2)
                    if pd1.button("Sim, excluir", key=f"ypdel_{pid}", type="primary", use_container_width=True):
                        mk_del = info["mes_key"]
                        d["meses"][mk_del]["lancamentos"] = [
                            l for l in d["meses"][mk_del].get("lancamentos", []) if l["id"] != pid
                        ]
                        st.session_state.pop(f"cpdel_{pid}", None)
                        save_data(d); st.rerun()
                    if pd2.button("Cancelar", key=f"npdel_{pid}", use_container_width=True):
                        st.session_state.pop(f"cpdel_{pid}", None); st.rerun()

            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# POUPANÇA
# ═══════════════════════════════════════════════════════════════
with tab_poupa:
    poupa = d.get("poupanca", {"objetivo": "", "meta_total": 0.0, "depositos": []})
    deps  = poupa.get("depositos", [])
    total_poupado = sum(dep["valor"] for dep in deps)
    meta_total    = poupa.get("meta_total", 0.0)
    objetivo      = poupa.get("objetivo", "")
    pct_meta      = min((total_poupado / meta_total * 100) if meta_total > 0 else 0, 100)
    pct_meta      = max(pct_meta, 0)

    # ── Card principal ───────────────────────────────────────────
    _mt_label = fmt(meta_total) if meta_total > 0 else "Não definida"
    _obj_label = objetivo if objetivo else "Sem objetivo definido"
    _pct_cor   = "#276749" if pct_meta >= 100 else "#2D6A4F"
    st.markdown(f"""
<div class='card'>
  <div style='font-size:11px;font-weight:700;color:#A0AEC0;text-transform:uppercase;
              letter-spacing:1px;margin-bottom:4px;'>🎯 Objetivo</div>
  <div style='font-weight:700;font-size:17px;color:#2D3748;margin-bottom:14px;'>{_obj_label}</div>
  <div style='display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:10px;'>
    <div>
      <div class='valor-label'>Total poupado</div>
      <div class='valor-grande valor-verde'>{fmt(total_poupado)}</div>
    </div>
    <div style='text-align:right;'>
      <div class='valor-label'>Meta</div>
      <div style='font-weight:700;font-size:18px;color:#D4A853;'>{_mt_label}</div>
    </div>
  </div>
  <div class='prog-bg'><div class='prog-fill' style='width:{pct_meta:.0f}%;'></div></div>
  <div style='font-size:12px;color:#718096;margin-top:6px;text-align:right;'>{pct_meta:.0f}% da meta</div>
</div>""", unsafe_allow_html=True)

    # Editar objetivo / meta
    if st.session_state.get("editing_poupa_cfg"):
        with st.form("f_poupa_cfg"):
            n_obj  = st.text_input("Objetivo (ex: viagem, reserva...)", value=objetivo)
            n_meta = st.number_input("Meta total (R$)", value=float(meta_total),
                                     min_value=0.0, step=500.0, format="%.2f")
            pc1, pc2 = st.columns(2)
            if pc1.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
                poupa["objetivo"]   = n_obj.strip()
                poupa["meta_total"] = float(n_meta)
                d["poupanca"] = poupa
                st.session_state.pop("editing_poupa_cfg", None)
                save_data(d); st.rerun()
            if pc2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.pop("editing_poupa_cfg", None); st.rerun()
    else:
        if st.button("✏️ Editar objetivo e meta", key="btn_poupa_cfg", use_container_width=True):
            st.session_state["editing_poupa_cfg"] = True; st.rerun()

    # ── Depósitos ────────────────────────────────────────────────
    st.markdown("<div class='sec'>Depósitos registrados</div>", unsafe_allow_html=True)
    cadep, _ = st.columns([2, 3])
    if cadep.button("➕ Novo depósito", key="add_dep_top", use_container_width=True):
        st.session_state["show_add_dep"] = not st.session_state.get("show_add_dep", False)

    if st.session_state.get("show_add_dep"):
        with st.form("f_dep_g", clear_on_submit=True):
            val_dq  = st.number_input("Valor (R$) *", min_value=0.01, step=50.0, format="%.2f")
            # Mês de referência: lista de meses disponíveis
            dep_meses = sorted(d["meses"].keys(), reverse=True)
            dep_meses_labels = [nome_mes(k) for k in dep_meses]
            sel_dep_mes = st.selectbox("Mês de referência", dep_meses_labels)
            dep_mes_key = dep_meses[dep_meses_labels.index(sel_dep_mes)]
            obs_dq  = st.text_input("Observação", placeholder="Ex: poupança do mês, bônus...")
            ds1, ds2 = st.columns(2)
            if ds1.form_submit_button("✓ Adicionar", use_container_width=True, type="primary"):
                if val_dq > 0:
                    poupa["depositos"].append({
                        "id": str(uuid.uuid4()), "mes": dep_mes_key,
                        "valor": float(val_dq), "obs": obs_dq.strip(),
                    })
                    d["poupanca"] = poupa
                    st.session_state["show_add_dep"] = False
                    save_data(d); st.rerun()
                else:
                    st.error("Informe um valor.")
            if ds2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_dep"] = False; st.rerun()

    if not deps:
        st.markdown("<div style='text-align:center;color:#a0aec0;padding:24px 0;'>Nenhum depósito ainda.<br>Registre quanto guardou cada mês.</div>",
                    unsafe_allow_html=True)
    else:
        deps_ord = sorted(deps, key=lambda x: x.get("mes",""), reverse=True)
        for dep in deps_ord:
            did    = dep["id"]
            obs_d  = dep.get("obs","")
            sub_d  = " · ".join(filter(None, [nome_mes(dep.get("mes","")), obs_d]))

            if st.session_state.get("editing_dep") == did:
                st.markdown("<div style='background:white;border-radius:14px;padding:16px;"
                            "margin-bottom:4px;box-shadow:0 1px 6px rgba(0,0,0,0.1);'>",
                            unsafe_allow_html=True)
                with st.form(f"ef_dep_{did}"):
                    dnv  = st.number_input("Valor (R$)", value=float(dep["valor"]), step=50.0, format="%.2f")
                    dep_meses2 = sorted(d["meses"].keys(), reverse=True)
                    dep_ml2    = [nome_mes(k) for k in dep_meses2]
                    cur_idx    = dep_meses2.index(dep.get("mes","")) if dep.get("mes") in dep_meses2 else 0
                    sel_dm2    = st.selectbox("Mês", dep_ml2, index=cur_idx)
                    dnm        = dep_meses2[dep_ml2.index(sel_dm2)]
                    dnobs      = st.text_input("Observação", value=dep.get("obs",""))
                    de1, de2   = st.columns(2)
                    if de1.form_submit_button("💾 Salvar", use_container_width=True, type="primary"):
                        dep.update({"valor": float(dnv), "mes": dnm, "obs": dnobs})
                        st.session_state.pop("editing_dep", None)
                        save_data(d); st.rerun()
                    if de2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_dep", None); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div style='background:white;border-radius:14px;padding:14px 16px;
     border-left:4px solid #68d391;box-shadow:0 1px 4px rgba(0,0,0,0.06);margin-bottom:2px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div style='flex:1;'>
      <div style='font-weight:700;font-size:16px;color:#2D3748;'>💰 Depósito</div>
      <div style='font-size:12px;color:#a0aec0;margin-top:3px;'>{sub_d}</div>
    </div>
    <div style='text-align:right;margin-left:12px;'>
      <div style='font-weight:700;font-size:18px;color:#276749;'>{fmt(dep['valor'])}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                da, db = st.columns([3, 1])
                if da.button("✏️ Editar", key=f"dedit_{did}", use_container_width=True):
                    st.session_state["editing_dep"] = did; st.rerun()
                if db.button("🗑️", key=f"ddel_{did}", use_container_width=True):
                    st.session_state[f"cddel_{did}"] = True; st.rerun()
                if st.session_state.get(f"cddel_{did}"):
                    st.warning("Excluir este depósito?")
                    dd1, dd2 = st.columns(2)
                    if dd1.button("Sim, excluir", key=f"yddel_{did}", type="primary", use_container_width=True):
                        poupa["depositos"] = [x for x in deps if x["id"] != did]
                        d["poupanca"] = poupa
                        st.session_state.pop(f"cddel_{did}", None)
                        save_data(d); st.rerun()
                    if dd2.button("Cancelar", key=f"nddel_{did}", use_container_width=True):
                        st.session_state.pop(f"cddel_{did}", None); st.rerun()
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    # ── Saldo disponível por mês (referência) ────────────────────
    st.markdown("<div class='sec'>Quanto sobrou por mês (referência)</div>", unsafe_allow_html=True)
    rows_s = ""
    for mk in sorted(d["meses"].keys(), reverse=True)[-6:]:
        mv   = d["meses"][mk]
        mr   = sum(x["valor"] for x in mv.get("receitas", []))
        mt   = sum(x["valor"] for x in mv.get("lancamentos", [])) + sum(x["valor"] for x in mv.get("fixas", []))
        msd  = mr - mt
        sc   = "#276749" if msd >= 0 else "#9B2C2C"
        ss   = fmt(abs(msd)) if msd >= 0 else "- " + fmt(abs(msd))
        bold = "font-weight:700;" if mk == mes_key else ""
        rows_s += f"""
<div class='item-row'>
  <div style='font-size:14px;{bold}'>{nome_mes(mk)}</div>
  <div style='font-weight:700;font-size:14px;color:{sc};'>{ss}</div>
</div>"""
    st.markdown(f"<div class='card'>{rows_s}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# RESUMO / CATEGORIAS
# ═══════════════════════════════════════════════════════════════
with tab_r:
    cat_totais = {}
    for item in todos:
        c = item.get("categoria","🎯 Outros")
        cat_totais[c] = cat_totais.get(c, 0) + item["valor"]
    cat_ord = sorted(cat_totais.items(), key=lambda x: x[1], reverse=True)

    st.markdown("<div class='sec'>Por categoria</div>", unsafe_allow_html=True)
    if total > 0:
        rows = ""
        for cat, val in cat_ord:
            if val <= 0: continue
            pct = val / total * 100
            rows += f"""
<div class='item-row'>
  <div style='flex:1;'>
    <div style='font-weight:600;font-size:14px;color:#2D3748;'>{cat}</div>
    <div style='margin-top:4px;'>
      <div class='prog-bg'><div class='prog-fill' style='width:{pct:.0f}%;'></div></div>
    </div>
  </div>
  <div style='text-align:right;margin-left:16px;'>
    <div style='font-weight:700;color:#2D3748;'>{fmt(val)}</div>
    <div style='font-size:11px;color:#a0aec0;'>{pct:.0f}%</div>
  </div>
</div>"""
        st.markdown(f"<div class='card'>{rows}</div>", unsafe_allow_html=True)

    # Comparativo
    if len(meses_keys) > 1:
        st.markdown("<div class='sec'>Histórico</div>", unsafe_allow_html=True)
        rows_h = ""
        for mk in sorted(meses_keys)[-5:]:
            ml  = d["meses"][mk].get("lancamentos", [])
            mf  = d["meses"][mk].get("fixas", [])
            mr  = d["meses"][mk].get("receitas", [])
            mt  = sum(x["valor"] for x in ml) + sum(x["valor"] for x in mf)
            mtr = sum(x["valor"] for x in mr)
            msd = mtr - mt
            bold = "font-weight:700;color:#2D6A4F;" if mk == mes_key else ""
            saldo_c = "#276749" if msd >= 0 else "#9B2C2C"
            saldo_s = fmt(abs(msd)) if msd >= 0 else "- " + fmt(abs(msd))
            rows_h += f"""
<div class='item-row'>
  <div style='font-size:14px;{bold}'>{nome_mes(mk)}</div>
  <div style='text-align:right;'>
    <div style='font-weight:700;font-size:14px;color:#9B2C2C;'>{fmt(mt)}</div>
    <div style='font-size:11px;color:{saldo_c};font-weight:600;'>saldo {saldo_s}</div>
  </div>
</div>"""
        st.markdown(f"<div class='card'>{rows_h}</div>", unsafe_allow_html=True)

    # Criar próximo mês
    uy, um = int(mes_key.split("-")[0]), int(mes_key.split("-")[1])
    nm, ny = (um % 12) + 1, uy + (1 if um == 12 else 0)
    prox_key  = f"{ny}-{nm:02d}"
    prox_nome = nome_mes(prox_key)
    if prox_key not in d["meses"]:
        st.markdown("<div class='sec'>Novo mês</div>", unsafe_allow_html=True)
        if st.button(f"📅 Criar {prox_nome} (copia fixas automaticamente)",
                     use_container_width=True):
            d["meses"][prox_key] = {
                "receitas": [],
                "meta_poupanca": mes.get("meta_poupanca", 0.0),
                "lancamentos": [],
                "fixas": [{"id": str(uuid.uuid4()), "descricao": t["descricao"],
                           "valor": t["valor"], "categoria": t["categoria"], "pago": False}
                          for t in d.get("template_fixas", [])],
            }
            save_data(d); st.rerun()

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:24px 0 8px;'>
  <p style='color:#CBD5E0;font-size:11px;margin:0;'>
    "Honra ao Senhor com os teus bens" · Pv 3:9
  </p>
</div>
""", unsafe_allow_html=True)
