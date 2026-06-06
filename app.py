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
    page_icon="💼",
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
  ctx.fillStyle='#1C1C1E';
  if(ctx.roundRect){ctx.roundRect(0,0,192,192,48);}else{ctx.rect(0,0,192,192);}
  ctx.fill();
  ctx.fillStyle='#fff'; ctx.font='bold 100px serif';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText('💼',96,100);
  var png=cv.toDataURL('image/png');
  var lnk=d.createElement('link');
  lnk.rel='apple-touch-icon'; lnk.sizes='192x192'; lnk.href=png;
  d.head.appendChild(lnk);
  var manifest={name:'Meu Dinheiro',short_name:'Dinheiro',
    display:'standalone',background_color:'#F8F7F5',theme_color:'#1C1C1E',
    icons:[{src:png,sizes:'192x192',type:'image/png'}]};
  var blob=new Blob([JSON.stringify(manifest)],{type:'application/json'});
  var ml=d.createElement('link'); ml.rel='manifest';
  ml.href=URL.createObjectURL(blob); d.head.appendChild(ml);
})();
</script>""", height=0)


# ─── CSS tema escuro confortável ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp { background:#1A1A1A !important; }
header[data-testid="stHeader"] { display:none !important; }
div[data-testid="stToolbar"] { display:none !important; }
#MainMenu { display:none !important; }
.block-container {
    padding-top:1.2rem !important;
    padding-left:1rem !important;
    padding-right:1rem !important;
    max-width:480px;
}
section[data-testid="stSidebar"] { display:none !important; }
button[data-testid="collapsedControl"] { display:none !important; }

/* Cards */
.card {
    background:#242424;
    border-radius:10px;
    padding:16px;
    margin-bottom:10px;
    border:1px solid #2E2E2E;
}
.card-sm {
    background:#242424;
    border-radius:8px;
    padding:13px 15px;
    margin-bottom:8px;
    border:1px solid #2E2E2E;
}

/* Versículo */
.versiculo {
    border-left:3px solid #4A4A4A;
    padding:14px 16px;
    margin-bottom:14px;
    background:#242424;
    border-radius:0 8px 8px 0;
    border-top:1px solid #2E2E2E;
    border-right:1px solid #2E2E2E;
    border-bottom:1px solid #2E2E2E;
}
.versiculo-texto {
    font-size:13px;
    line-height:1.6;
    font-style:italic;
    color:#A0A0A0;
    margin:0 0 6px 0;
}
.versiculo-ref {
    font-size:10px;
    font-weight:700;
    letter-spacing:1.2px;
    text-transform:uppercase;
    color:#888;
}

/* Valores */
.valor-grande { font-size:20px; font-weight:700; color:#E8E8E8; line-height:1; }
.valor-label  { font-size:9px; color:#888; text-transform:uppercase;
    letter-spacing:1px; margin-bottom:3px; }
.valor-verde    { color:#4ADE80; }
.valor-vermelho { color:#F87171; }
.valor-cinza    { color:#888; }

/* Tags */
.tag-pago { background:#14532D; color:#4ADE80; border:1px solid #166534;
    border-radius:4px; padding:2px 8px; font-size:10px; font-weight:700; }
.tag-pend { background:#450A0A; color:#F87171; border:1px solid #7F1D1D;
    border-radius:4px; padding:2px 8px; font-size:10px; font-weight:700; }

/* Barra de progresso */
.prog-bg   { background:#2E2E2E; border-radius:4px; height:4px; overflow:hidden; }
.prog-fill { background:#5A5A5A; height:100%; border-radius:4px; }

/* Linha de item */
.item-row {
    display:flex; justify-content:space-between; align-items:flex-start;
    padding:12px 0; border-bottom:1px solid #2A2A2A;
}
.item-row:last-child { border-bottom:none; }
.item-desc { font-weight:600; color:#E8E8E8; font-size:14px; }
.item-sub  { font-size:11px; color:#888; margin-top:2px; }
.item-val  { font-weight:700; font-size:15px; color:#E8E8E8; white-space:nowrap; }

/* Seção título */
.sec { font-size:10px; font-weight:700; color:#888;
    text-transform:uppercase; letter-spacing:1.5px; margin:16px 0 8px; }

/* Botões */
.stButton>button {
    border-radius:8px !important;
    font-weight:600 !important;
    border:1px solid #333 !important;
    min-height:42px !important;
    font-size:14px !important;
    width:100% !important;
    background:#242424 !important;
    color:#C8C8C8 !important;
}
.stButton>button[kind="primary"] {
    background:#333 !important;
    color:#E8E8E8 !important;
    border:1px solid #444 !important;
}
button[data-testid="baseButton-secondary"] {
    min-height:34px !important;
    font-size:14px !important;
    background:#242424 !important;
    color:#888 !important;
    border-radius:8px !important;
    border:1px solid #333 !important;
    padding:4px !important;
}

/* Abas */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:#242424;
    border-radius:8px;
    padding:3px;
    gap:2px;
    border:1px solid #2E2E2E;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius:6px;
    font-size:12px;
    font-weight:500;
    color:#666;
    padding:7px 4px !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background:#333 !important;
    color:#E8E8E8 !important;
    font-weight:700 !important;
    box-shadow:0 1px 3px rgba(0,0,0,0.40) !important;
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    font-size:16px !important;
    min-height:44px !important;
    border-radius:8px !important;
    color:#E8E8E8 !important;
    background:#2A2A2A !important;
    border:1px solid #3A3A3A !important;
}
.stTextInput input::placeholder, .stNumberInput input::placeholder { color:#555 !important; }
.stSelectbox > div > div {
    border-radius:8px !important;
    font-size:14px !important;
    color:#E8E8E8 !important;
    background:#2A2A2A !important;
    border:1px solid #3A3A3A !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label,
.stDateInput label, .stCheckbox label { color:#888 !important; font-size:13px !important; }
div[data-baseweb="popover"] * { color:#E8E8E8 !important; background:#2A2A2A !important; }
div[data-baseweb="menu"] [role="option"]:hover { background:#333 !important; }
/* Checkbox */
.stCheckbox label span { color:#C0C0C0 !important; }

/* Divider */
hr { border:none; border-top:1px solid #2E2E2E; margin:12px 0; }

/* Selectbox arrow / dropdown text */
.stSelectbox svg { fill:#888 !important; }
p, span, div { color:#E8E8E8; }
/* Força texto claro em todo conteúdo */
.stMarkdown, .stMarkdown p, .stMarkdown span { color:#E8E8E8 !important; }
[data-testid="stMarkdownContainer"] p { color:#E8E8E8 !important; }
[data-testid="stMarkdownContainer"] b, [data-testid="stMarkdownContainer"] strong { color:#FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# ─── Versículos ───────────────────────────────────────────────────────────────
VERSICULO = [
    ("Provérbios 21:20", "Na casa do sábio há precioso tesouro e azeite, mas o homem tolo os desperdiça."),
    ("Provérbios 13:11", "A riqueza obtida às pressas diminui, mas quem a ajunta pouco a pouco a aumenta."),
    ("Lucas 14:28", "Pois qual de vós, desejando edificar uma torre, não se assenta primeiro e calcula a despesa?"),
    ("Provérbios 22:7", "O rico domina os pobres, e o devedor é servo do credor."),
    ("Provérbios 3:9-10", "Honra ao Senhor com os teus bens e com as primícias de toda a tua renda."),
    ("Filipenses 4:19", "O meu Deus, segundo as suas riquezas em glória, suprirá todas as vossas necessidades."),
    ("Mateus 6:33", "Buscai, pois, em primeiro lugar o reino de Deus e a sua justiça."),
    ("Eclesiastes 5:10", "Quem ama o dinheiro nunca se satisfaz com dinheiro."),
    ("Provérbios 6:6-8", "Vai ter com a formiga, ó preguiçoso, considera os seus caminhos e sê sábio."),
    ("I Timóteo 6:6", "A piedade com contentamento é grande ganho."),
    ("Provérbios 27:12", "O avisado vê o mal e esconde-se, mas os simples passam e sofrem a pena."),
    ("Deuteronômio 8:18", "Lembra-te do Senhor teu Deus, porque é ele que te dá força para adquirir riqueza."),
    ("Eclesiastes 11:2", "Reparte com sete, e ainda com oito, pois não sabes que mal poderá vir sobre a terra."),
    ("Provérbios 28:20", "O homem fiel terá muitas bênçãos, mas o que se apressa a ficar rico não ficará impune."),
    ("Mateus 6:21", "Porque onde estiver o seu tesouro, aí estará também o seu coração."),
    ("Provérbios 13:22", "O homem bom deixa herança para os filhos dos seus filhos."),
    ("Romanos 13:8", "A ninguém devais coisa alguma, exceto o amor mútuo."),
    ("Provérbios 11:24", "Há quem distribua, e ainda lhe aumenta a riqueza; e há quem retenha mais do que é justo."),
    ("I Coríntios 16:2", "No primeiro dia da semana, cada um de vós ponha de parte, segundo a sua prosperidade."),
    ("Provérbios 22:26-27", "Não sejas dos que batem as palmas, nem dos que são fiadores de dívidas."),
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

def prox_mes(key):
    y, m = int(key[:4]), int(key[5:])
    m += 1
    if m > 12: m, y = 1, y + 1
    return f"{y}-{m:02d}"

# ─── Dados iniciais ───────────────────────────────────────────────────────────
INITIAL_DATA = {
    "meses": {
        "2025-06": {
            "receitas": [],
            "meta_poupanca": 0.0,
            "lancamentos": [
                {"id":"m6l1","data":5,"descricao":"OAB SP","valor":361.23,"parcela":"2/3","categoria":"⚖️ Profissional","pago":False,"obs":""},
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
    "poupanca": {"objetivo": "", "meta_total": 0.0, "depositos": []},
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
        if sha:
            body["sha"] = sha
        payload = json.dumps(body).encode()
        req = urllib.request.Request(_GH_API,data=payload,headers=_gh_headers(),method="PUT")
        with urllib.request.urlopen(req,timeout=15) as resp:
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

# ─── Auto-geração de meses com parcelas cascateadas ──────────────────────────
def _parcela_nums(ps):
    """Retorna (atual, total) de uma string 'a/t' ou None."""
    if not ps or "/" not in ps:
        return None
    try:
        a, t = ps.strip().split("/", 1)
        return int("".join(c for c in a if c.isdigit())), int("".join(c for c in t if c.isdigit()))
    except:
        return None

def _criar_mes_novo(d, novo_key, ant_key):
    """Cria um mês a partir do anterior, avançando parcelas automaticamente."""
    ant = d["meses"][ant_key]
    parcelas_novas = []
    # Avança cada lancamento parcelado que ainda não terminou
    for l in ant.get("lancamentos", []):
        nums = _parcela_nums(l.get("parcela", ""))
        if nums is None:
            continue
        atual, total_p = nums
        if atual < total_p:
            parcelas_novas.append({
                "id": str(uuid.uuid4()),
                "data": l.get("data", 1),
                "descricao": l["descricao"],
                "valor": l["valor"],
                "parcela": f"{atual+1}/{total_p}",
                "categoria": l.get("categoria", "🎯 Outros"),
                "pago": False,
                "obs": l.get("obs", ""),
            })
    d["meses"][novo_key] = {
        "receitas": [],
        "meta_poupanca": ant.get("meta_poupanca", 0.0),
        "lancamentos": parcelas_novas,
        "fixas": [
            {"id": str(uuid.uuid4()), "descricao": t["descricao"],
             "valor": t["valor"], "categoria": t["categoria"], "pago": False}
            for t in d.get("template_fixas", [])
        ],
    }

def garantir_meses_ate_2026(d):
    """Garante que existam meses de dados até 2026-12, cascateando parcelas."""
    alvo = "2026-12"
    chaves_existentes = sorted(d["meses"].keys())
    if not chaves_existentes:
        return
    ultima = chaves_existentes[-1]
    cur = prox_mes(ultima)
    while cur <= alvo:
        ant = sorted(k for k in d["meses"].keys() if k < cur)[-1]
        _criar_mes_novo(d, cur, ant)
        cur = prox_mes(cur)

# ─── Inicializa sessão ────────────────────────────────────────────────────────
if "dados" not in st.session_state:
    st.session_state["dados"] = load_data()
    st.session_state.setdefault("gh_sha","")

d = st.session_state["dados"]

# Retrocompatibilidade
for _mk in list(d["meses"].keys()):
    d["meses"][_mk].setdefault("receitas", [])
    d["meses"][_mk].setdefault("meta_poupanca", 0.0)
d.setdefault("poupanca", {"objetivo": "", "meta_total": 0.0, "depositos": []})
d.setdefault("template_fixas", INITIAL_DATA["template_fixas"])

# Auto-gera meses faltantes até 2026-12
_precisa_salvar = False
_antes = set(d["meses"].keys())
garantir_meses_ate_2026(d)
if set(d["meses"].keys()) != _antes:
    _precisa_salvar = True
    save_data(d)

# ─── Cabeçalho ────────────────────────────────────────────────────────────────
meses_keys  = sorted(d["meses"].keys())
mes_labels  = [nome_mes(k) for k in meses_keys]
_hoje_key   = _date.today().strftime("%Y-%m")

# Padrão: mês mais recente com receitas registradas (evita cair em mês futuro auto-gerado vazio)
_default_key = _hoje_key
for _mk in sorted(d["meses"].keys(), reverse=True):
    if d["meses"][_mk].get("receitas"):
        _default_key = _mk
        break
_default_idx = meses_keys.index(_default_key) if _default_key in meses_keys else len(meses_keys) - 1

st.markdown(
    "<p style='margin:8px 0 10px;font-size:20px;font-weight:700;color:#E8E8E8;letter-spacing:-0.5px;'>"
    "Meu Dinheiro</p>",
    unsafe_allow_html=True,
)
mes_sel = st.selectbox("", mes_labels, index=_default_idx,
                        key=f"ms_{_date.today().strftime('%Y%m')}",
                        label_visibility="collapsed")
mes_key = meses_keys[mes_labels.index(mes_sel)]

# ─── Versículo ────────────────────────────────────────────────────────────────
ver = versiculo_do_dia()
st.markdown(f"""
<div class="versiculo">
  <p class="versiculo-texto">"{ver[1]}"</p>
  <div class="versiculo-ref">{ver[0]}</div>
</div>
""", unsafe_allow_html=True)

# ─── Dados do mês ─────────────────────────────────────────────────────────────
mes        = d["meses"][mes_key]
lanc       = mes.get("lancamentos", [])
fixas      = mes.get("fixas", [])
receitas_m = mes.get("receitas", [])
meta_poupc = mes.get("meta_poupanca", 0.0)

total_rec  = sum(r["valor"] for r in receitas_m)
total      = sum(i["valor"] for i in lanc)
pago       = sum(i["valor"] for i in lanc if i.get("pago"))
pend       = total - pago

# Saldo residual acumulado de meses anteriores (receitas recebidas − pagos)
def calcular_residual(d, mes_key):
    acum = 0.0
    for mk in sorted(d["meses"].keys()):
        if mk >= mes_key:
            break
        mv = d["meses"][mk]
        rec_mk  = sum(r["valor"] for r in mv.get("receitas", []) if r.get("recebido", True))
        pago_mk = sum(l["valor"] for l in mv.get("lancamentos", []) if l.get("pago"))
        acum += rec_mk - pago_mk
    return acum

residual    = calcular_residual(d, mes_key)
res_pos     = max(residual, 0)

# Disponível = (receita + residual positivo) − débitos totais  → saldo real do mês
disponivel  = (total_rec + res_pos) - total
# Caixa agora = receita + residual − o que já foi pago  → dinheiro no bolso enquanto paga
caixa_agora = total_rec + res_pos - pago

# ─── 4 cards de resumo ────────────────────────────────────────────────────────
_disp_cor = "#4ADE80" if disponivel >= 0 else "#F87171"
_disp_sinal = "+" if disponivel >= 0 else "-"
_disp_txt = (_disp_sinal if disponivel < 0 else "") + fmt(abs(disponivel))
_res_txt  = (f"<div style='font-size:9px;color:#888;margin-top:3px;'>+{fmt(res_pos)} anterior</div>"
             if res_pos > 0.01 else "")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"""<div class='card' style='text-align:center;padding:12px 8px;'>
  <div class='valor-label'>Receita</div>
  <div style='font-size:14px;font-weight:700;color:#4ADE80;'>{fmt(total_rec)}</div>
  {('<div style="font-size:9px;color:#888;margin-top:2px;">+' + fmt(res_pos) + ' anterior</div>') if res_pos > 0.01 else ''}
</div>""", unsafe_allow_html=True)
c2.markdown(f"""<div class='card' style='text-align:center;padding:12px 8px;'>
  <div class='valor-label'>Débitos</div>
  <div style='font-size:14px;font-weight:700;color:#F87171;'>{fmt(total)}</div>
</div>""", unsafe_allow_html=True)
c3.markdown(f"""<div class='card' style='text-align:center;padding:12px 8px;'>
  <div class='valor-label'>A pagar</div>
  <div style='font-size:14px;font-weight:700;color:#F87171;'>{fmt(pend)}</div>
</div>""", unsafe_allow_html=True)
c4.markdown(f"""<div class='card' style='text-align:center;padding:12px 8px;'>
  <div class='valor-label'>Disponível</div>
  <div style='font-size:14px;font-weight:700;color:{_disp_cor};'>{_disp_txt}</div>
</div>""", unsafe_allow_html=True)

# ─── Abas ─────────────────────────────────────────────────────────────────────
tab_g, tab_f, tab_rec, tab_poupa, tab_p, tab_r = st.tabs([
    "Gastos", "Fixas", "Receita", "Poupar", "Parcelas", "Resumo"
])

# ═══════════════════════════════════════════════════════════════
# GASTOS
# ═══════════════════════════════════════════════════════════════
with tab_g:
    cref, cadd = st.columns([3, 2])
    cref.markdown(f"<div style='font-size:12px;color:#666;padding-top:10px;'>{nome_mes(mes_key)}</div>",
                  unsafe_allow_html=True)
    if cadd.button("+ Novo gasto", key="add_lanc_top", use_container_width=True):
        st.session_state["show_add_lanc"] = not st.session_state.get("show_add_lanc", False)

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
            if cs1.form_submit_button("Adicionar", use_container_width=True, type="primary"):
                if desc_q.strip() and val_q > 0:
                    mes["lancamentos"].append({
                        "id": str(uuid.uuid4()), "data": int(dia_q),
                        "descricao": desc_q.strip(), "valor": float(val_q),
                        "parcela": parc_q.strip(), "categoria": cat_q,
                        "pago": pago_q, "obs": obs_q.strip(),
                    })
                    st.session_state["show_add_lanc"] = False
                    save_data(d); st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
            if cs2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_lanc"] = False; st.rerun()

    # Caixa dinâmico: receita + residual − o que já foi pago (atualiza conforme você dá ok)
    if total_rec > 0 or res_pos > 0:
        _cx_cor = "#4ADE80" if caixa_agora >= 0 else "#F87171"
        _cx_txt = fmt(caixa_agora) if caixa_agora >= 0 else "- " + fmt(abs(caixa_agora))
        _cx_sub = f"receita {fmt(total_rec)}" + (f" + {fmt(res_pos)} anterior" if res_pos > 0.01 else "") + f" − pagos {fmt(pago)}"
        st.markdown(f"""
<div style='background:#242424;border:1px solid #2E2E2E;border-radius:8px;
     padding:12px 16px;margin-bottom:10px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div style='font-size:12px;color:#888;'>Caixa disponível agora</div>
    <div style='font-size:16px;font-weight:700;color:{_cx_cor};'>{_cx_txt}</div>
  </div>
  <div style='font-size:10px;color:#666;margin-top:4px;'>{_cx_sub}</div>
</div>""", unsafe_allow_html=True)

    if not lanc:
        st.markdown("<div style='text-align:center;color:#bbb;padding:30px 0;font-size:13px;'>Nenhum gasto registrado.</div>",
                    unsafe_allow_html=True)
    else:
        lanc_ord = sorted(lanc, key=lambda x: (x.get("pago", False), x.get("data", 0)))
        for item in lanc_ord:
            iid    = item["id"]
            pago_i = item.get("pago", False)
            parc   = item.get("parcela", "")
            obs    = item.get("obs", "")
            sub    = " · ".join(filter(None, [
                f"Dia {int(item['data'])}" if item.get("data") else "",
                parc, item.get("categoria",""), obs
            ]))
            borda  = "#BBF7D0" if pago_i else "#FECACA"
            tag    = "<span class='tag-pago'>pago</span>" if pago_i else "<span class='tag-pend'>pendente</span>"

            if st.session_state.get("editing_lanc") == iid:
                with st.form(f"ef_lanc_{iid}"):
                    st.markdown(f"**Editando: {item['descricao']}**")
                    nd = st.text_input("Descrição", value=item["descricao"])
                    nv = st.number_input("Valor (R$)", value=float(item["valor"]), step=0.01, format="%.2f")
                    ec1, ec2 = st.columns(2)
                    ndia  = ec1.number_input("Dia", value=int(item.get("data", 1)), min_value=1, max_value=31)
                    nparc = ec2.text_input("Parcela", value=item.get("parcela", ""))
                    ncat  = st.selectbox("Categoria", CATEGORIAS,
                                         index=CATEGORIAS.index(item["categoria"]) if item.get("categoria") in CATEGORIAS else 0)
                    nobs  = st.text_input("Observação", value=item.get("obs", ""))
                    es1, es2 = st.columns(2)
                    if es1.form_submit_button("Salvar", use_container_width=True, type="primary"):
                        item.update({"descricao": nd, "valor": float(nv), "data": int(ndia),
                                     "parcela": nparc, "categoria": ncat, "obs": nobs})
                        st.session_state.pop("editing_lanc", None)
                        save_data(d); st.rerun()
                    if es2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_lanc", None); st.rerun()
            else:
                st.markdown(f"""
<div style='background:#242424;border-radius:8px;padding:12px 14px;
     border-left:3px solid {borda};border:1px solid #2E2E2E;border-left:3px solid {borda};
     margin-bottom:4px;'>
  <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
    <div style='flex:1;'>
      <div style='font-weight:600;font-size:14px;color:#E8E8E8;'>{item['descricao']}</div>
      <div style='font-size:11px;color:#666;margin-top:2px;'>{sub}</div>
    </div>
    <div style='text-align:right;margin-left:12px;flex-shrink:0;'>
      <div style='font-weight:700;font-size:15px;color:#E8E8E8;'>{fmt(item['valor'])}</div>
      <div style='margin-top:2px;'>{tag}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

                ba, bb, bc = st.columns([7, 1, 1])
                lbl_pay = "↩ Desfazer" if pago_i else "✓ Pagar"
                if ba.button(lbl_pay, key=f"pay_{iid}", use_container_width=True, type="primary"):
                    item["pago"] = not pago_i
                    save_data(d); st.rerun()
                if bb.button("✏", key=f"edit_{iid}", use_container_width=True):
                    st.session_state["editing_lanc"] = iid; st.rerun()
                if bc.button("✕", key=f"del_{iid}", use_container_width=True):
                    st.session_state[f"cdel_{iid}"] = True; st.rerun()

                if st.session_state.get(f"cdel_{iid}"):
                    st.warning(f"Excluir **{item['descricao']}**?")
                    dc1, dc2 = st.columns(2)
                    if dc1.button("Excluir", key=f"ydel_{iid}", type="primary", use_container_width=True):
                        mes["lancamentos"] = [l for l in lanc if l["id"] != iid]
                        st.session_state.pop(f"cdel_{iid}", None)
                        save_data(d); st.rerun()
                    if dc2.button("Cancelar", key=f"ndel_{iid}", use_container_width=True):
                        st.session_state.pop(f"cdel_{iid}", None); st.rerun()

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FIXAS — referência de custos fixos na fatura Sicoob (sem pago/pendente)
# ═══════════════════════════════════════════════════════════════
with tab_f:
    tf = sum(i["valor"] for i in fixas)
    crf, cadf = st.columns([3, 2])
    crf.markdown(f"<div style='font-size:12px;color:#888;padding-top:10px;'>{nome_mes(mes_key)}</div>",
                 unsafe_allow_html=True)
    if cadf.button("+ Nova fixa", key="add_fixa_top", use_container_width=True):
        st.session_state["show_add_fixa"] = not st.session_state.get("show_add_fixa", False)

    st.markdown(
        f"<div style='font-size:12px;color:#888;margin:8px 0 10px;'>"
        f"Total na fatura: <b style='color:#E8E8E8;font-size:15px;'>{fmt(tf)}</b></div>",
        unsafe_allow_html=True)

    if st.session_state.get("show_add_fixa"):
        with st.form("f_fixa_g", clear_on_submit=True):
            desc_fq = st.text_input("Descrição *", placeholder="Ex: Streaming, Plano...")
            val_fq  = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            cat_fq  = st.selectbox("Categoria", CATEGORIAS)
            fs1, fs2 = st.columns(2)
            if fs1.form_submit_button("Adicionar", use_container_width=True, type="primary"):
                if desc_fq.strip() and val_fq > 0:
                    mes["fixas"].append({
                        "id": str(uuid.uuid4()), "descricao": desc_fq.strip(),
                        "valor": float(val_fq), "categoria": cat_fq,
                    })
                    st.session_state["show_add_fixa"] = False
                    save_data(d); st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
            if fs2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_fixa"] = False; st.rerun()

    if not fixas:
        st.markdown("<div style='text-align:center;color:#666;padding:30px 0;font-size:13px;'>Nenhuma conta fixa.</div>",
                    unsafe_allow_html=True)
    else:
        fixas_ord = sorted(fixas, key=lambda x: x["descricao"])
        for item in fixas_ord:
            fid = item["id"]

            if st.session_state.get("editing_fixa") == fid:
                with st.form(f"ef_fixa_{fid}"):
                    st.markdown(f"**Editando: {item['descricao']}**")
                    fnd = st.text_input("Descrição", value=item["descricao"])
                    fnv = st.number_input("Valor (R$)", value=float(item["valor"]), step=0.01, format="%.2f")
                    fnc = st.selectbox("Categoria", CATEGORIAS,
                                       index=CATEGORIAS.index(item["categoria"]) if item.get("categoria") in CATEGORIAS else 0)
                    fes1, fes2 = st.columns(2)
                    if fes1.form_submit_button("Salvar", use_container_width=True, type="primary"):
                        item.update({"descricao": fnd, "valor": float(fnv), "categoria": fnc})
                        st.session_state.pop("editing_fixa", None)
                        save_data(d); st.rerun()
                    if fes2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_fixa", None); st.rerun()
            else:
                st.markdown(f"""
<div style='background:#242424;border-radius:8px;padding:12px 14px;
     border:1px solid #2E2E2E;margin-bottom:4px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div>
      <div style='font-weight:600;font-size:14px;color:#E8E8E8;'>{item['descricao']}</div>
      <div style='font-size:11px;color:#888;margin-top:2px;'>{item.get('categoria','')}</div>
    </div>
    <div style='font-weight:700;font-size:15px;color:#E8E8E8;'>{fmt(item['valor'])}</div>
  </div>
</div>""", unsafe_allow_html=True)

                fb, fc = st.columns([1, 1])
                if fb.button("✏ Editar", key=f"fedit_{fid}", use_container_width=True):
                    st.session_state["editing_fixa"] = fid; st.rerun()
                if fc.button("✕ Excluir", key=f"fdel_{fid}", use_container_width=True):
                    st.session_state[f"cfdel_{fid}"] = True; st.rerun()

                if st.session_state.get(f"cfdel_{fid}"):
                    st.warning(f"Excluir **{item['descricao']}**?")
                    fc1, fc2 = st.columns(2)
                    if fc1.button("Excluir", key=f"yfdel_{fid}", type="primary", use_container_width=True):
                        mes["fixas"] = [f for f in fixas if f["id"] != fid]
                        st.session_state.pop(f"cfdel_{fid}", None)
                        save_data(d); st.rerun()
                    if fc2.button("Cancelar", key=f"nfdel_{fid}", use_container_width=True):
                        st.session_state.pop(f"cfdel_{fid}", None); st.rerun()

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# RECEITA
# ═══════════════════════════════════════════════════════════════
with tab_rec:
    rec_list = mes.get("receitas", [])
    crec, cadrec = st.columns([3, 2])
    crec.markdown(f"<div style='font-size:12px;color:#666;padding-top:10px;'>{nome_mes(mes_key)}</div>",
                  unsafe_allow_html=True)
    if cadrec.button("+ Nova receita", key="add_rec_top", use_container_width=True):
        st.session_state["show_add_rec"] = not st.session_state.get("show_add_rec", False)

    if st.session_state.get("show_add_rec"):
        with st.form("f_rec_g", clear_on_submit=True):
            desc_rq = st.text_input("Descrição *", placeholder="Ex: Honorários, Salário...")
            val_rq  = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            dia_rq  = st.number_input("Dia", min_value=1, max_value=31, value=_date.today().day)
            cat_rq  = st.selectbox("Categoria", CATEGORIAS_RECEITA)
            obs_rq  = st.text_input("Observação", placeholder="opcional")
            rec_rq  = st.checkbox("Já recebido?", value=True)
            rs1, rs2 = st.columns(2)
            if rs1.form_submit_button("Adicionar", use_container_width=True, type="primary"):
                if desc_rq.strip() and val_rq > 0:
                    mes["receitas"].append({
                        "id": str(uuid.uuid4()), "data": int(dia_rq),
                        "descricao": desc_rq.strip(), "valor": float(val_rq),
                        "categoria": cat_rq, "recebido": rec_rq, "obs": obs_rq.strip(),
                    })
                    st.session_state["show_add_rec"] = False
                    save_data(d); st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
            if rs2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state["show_add_rec"] = False; st.rerun()

    # Card: saldo do mês
    _saldo_mes = total_rec - total
    _saldo_cor = "#16A34A" if _saldo_mes >= 0 else "#DC2626"
    _saldo_icon = "+" if _saldo_mes >= 0 else ""
    _meta_pct = min((_saldo_mes / meta_poupc * 100) if meta_poupc > 0 else 0, 100)
    _meta_pct = max(_meta_pct, 0)
    _meta_label = fmt(meta_poupc) if meta_poupc > 0 else "—"

    st.markdown("<div class='sec'>Saldo do mês</div>", unsafe_allow_html=True)
    if st.session_state.get("editing_meta"):
        with st.form("f_meta"):
            nova_meta = st.number_input("Meta mensal de poupança (R$)", value=float(meta_poupc),
                                        min_value=0.0, step=100.0, format="%.2f")
            mm1, mm2 = st.columns(2)
            if mm1.form_submit_button("Salvar", use_container_width=True, type="primary"):
                mes["meta_poupanca"] = float(nova_meta)
                st.session_state.pop("editing_meta", None)
                save_data(d); st.rerun()
            if mm2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.pop("editing_meta", None); st.rerun()
    else:
        st.markdown(f"""
<div class='card'>
  <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;'>
    <div>
      <div class='valor-label'>Receita do mês</div>
      <div style='font-size:18px;font-weight:700;color:#4ADE80;'>{fmt(total_rec)}</div>
      {'<div style="font-size:11px;color:#888;margin-top:2px;">+ ' + fmt(residual) + ' residual anterior</div>' if residual > 0.01 else ''}
    </div>
    <div style='text-align:right;'>
      <div class='valor-label'>Saldo projetado</div>
      <div style='font-size:18px;font-weight:700;color:{_saldo_cor};'>{_saldo_icon}{fmt(abs(_saldo_mes))}</div>
    </div>
  </div>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
    <div>
      <div class='valor-label'>Disponível agora</div>
      <div style='font-size:15px;font-weight:700;color:{_disp_cor};'>{_disp_txt}</div>
    </div>
    <div style='text-align:right;'>
      <div class='valor-label'>Meta poupar</div>
      <div style='font-size:15px;font-weight:700;color:#888;'>{_meta_label}</div>
    </div>
  </div>
  <div class='prog-bg'><div class='prog-fill' style='width:{_meta_pct:.0f}%;'></div></div>
  <div style='font-size:11px;color:#666;margin-top:5px;text-align:right;'>{_meta_pct:.0f}% da meta de poupança</div>
</div>""", unsafe_allow_html=True)
        if st.button("Definir meta de poupança", key="btn_meta", use_container_width=True):
            st.session_state["editing_meta"] = True; st.rerun()

    # Lista receitas
    st.markdown("<div class='sec'>Receitas do mês</div>", unsafe_allow_html=True)
    if not rec_list:
        st.markdown("<div style='text-align:center;color:#bbb;padding:24px 0;font-size:13px;'>Nenhuma receita registrada.</div>",
                    unsafe_allow_html=True)
    else:
        total_rec_l  = sum(r["valor"] for r in rec_list)
        recebido_l   = sum(r["valor"] for r in rec_list if r.get("recebido"))
        aguardando_l = total_rec_l - recebido_l
        st.markdown(
            f"<div style='display:flex;gap:16px;margin:8px 0 10px;'>"
            f"<span style='font-size:12px;color:#666;'>Total: <b style='color:#E8E8E8;'>{fmt(total_rec_l)}</b></span>"
            f"<span style='font-size:12px;color:#4ADE80;'>Recebido: <b>{fmt(recebido_l)}</b></span>"
            f"<span style='font-size:12px;color:#FBBF24;'>Aguardando: <b>{fmt(aguardando_l)}</b></span>"
            f"</div>", unsafe_allow_html=True)

        rec_ord = sorted(rec_list, key=lambda x: x.get("data", 0))
        for item in rec_ord:
            rid   = item["id"]
            rec_i = item.get("recebido", False)
            sub_r = " · ".join(filter(None, [
                f"Dia {int(item['data'])}" if item.get("data") else "",
                item.get("categoria", ""), item.get("obs", ""),
            ]))
            borda_r = "#BBF7D0" if rec_i else "#FDE68A"
            tag_r   = ("<span class='tag-pago'>recebido</span>" if rec_i
                       else "<span style='background:#FFFBEB;color:#FBBF24;border:1px solid #FDE68A;"
                            "border-radius:4px;padding:2px 8px;font-size:10px;font-weight:700;'>aguardando</span>")

            if st.session_state.get("editing_rec") == rid:
                with st.form(f"ef_rec_{rid}"):
                    st.markdown(f"**Editando: {item['descricao']}**")
                    rnd   = st.text_input("Descrição", value=item["descricao"])
                    rnv   = st.number_input("Valor (R$)", value=float(item["valor"]), step=0.01, format="%.2f")
                    rndia = st.number_input("Dia", value=int(item.get("data", 1)), min_value=1, max_value=31)
                    rncat = st.selectbox("Categoria", CATEGORIAS_RECEITA,
                                         index=CATEGORIAS_RECEITA.index(item["categoria"])
                                         if item.get("categoria") in CATEGORIAS_RECEITA else 0)
                    rnobs = st.text_input("Observação", value=item.get("obs", ""))
                    res1, res2 = st.columns(2)
                    if res1.form_submit_button("Salvar", use_container_width=True, type="primary"):
                        item.update({"descricao": rnd, "valor": float(rnv),
                                     "data": int(rndia), "categoria": rncat, "obs": rnobs})
                        st.session_state.pop("editing_rec", None)
                        save_data(d); st.rerun()
                    if res2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_rec", None); st.rerun()
            else:
                st.markdown(f"""
<div style='background:#242424;border-radius:8px;padding:12px 14px;
     border-left:3px solid {borda_r};border:1px solid #2E2E2E;border-left:3px solid {borda_r};
     margin-bottom:4px;'>
  <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
    <div style='flex:1;'>
      <div style='font-weight:600;font-size:14px;color:#E8E8E8;'>{item['descricao']}</div>
      <div style='font-size:11px;color:#666;margin-top:2px;'>{sub_r}</div>
    </div>
    <div style='text-align:right;margin-left:12px;flex-shrink:0;'>
      <div style='font-weight:700;font-size:15px;color:#4ADE80;'>{fmt(item['valor'])}</div>
      <div style='margin-top:2px;'>{tag_r}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

                ra, rb, rc_btn = st.columns([7, 1, 1])
                lbl_rec = "↩ Desfazer" if rec_i else "✓ Receber"
                if ra.button(lbl_rec, key=f"rpay_{rid}", use_container_width=True, type="primary"):
                    item["recebido"] = not rec_i
                    save_data(d); st.rerun()
                if rb.button("✏", key=f"redit_{rid}", use_container_width=True):
                    st.session_state["editing_rec"] = rid; st.rerun()
                if rc_btn.button("✕", key=f"rdel_{rid}", use_container_width=True):
                    st.session_state[f"crdel_{rid}"] = True; st.rerun()

                if st.session_state.get(f"crdel_{rid}"):
                    st.warning(f"Excluir **{item['descricao']}**?")
                    rd1, rd2 = st.columns(2)
                    if rd1.button("Excluir", key=f"yrdel_{rid}", type="primary", use_container_width=True):
                        mes["receitas"] = [r for r in rec_list if r["id"] != rid]
                        st.session_state.pop(f"crdel_{rid}", None)
                        save_data(d); st.rerun()
                    if rd2.button("Cancelar", key=f"nrdel_{rid}", use_container_width=True):
                        st.session_state.pop(f"crdel_{rid}", None); st.rerun()

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PARCELAS — visão consolidada de todas as parcelas ativas
# ═══════════════════════════════════════════════════════════════
with tab_p:
    cp_hd, cp_add = st.columns([3, 2])
    cp_hd.markdown("<div class='sec' style='margin-top:8px;'>Parcelas ativas</div>",
                   unsafe_allow_html=True)
    if cp_add.button("+ Nova parcela", key="add_parc_top", use_container_width=True):
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
            if pas1.form_submit_button("Adicionar", use_container_width=True, type="primary"):
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

    # Consolida parcelas: considera apenas meses até o mês selecionado
    # Isso evita mostrar parcelas futuras (auto-geradas) como se já tivessem avançado
    parcelas_map = {}
    for mk in sorted(d["meses"].keys()):
        if mk > mes_key:
            break  # não considera meses futuros ao selecionado
        for l in d["meses"][mk].get("lancamentos", []):
            nums = _parcela_nums(l.get("parcela", ""))
            if nums is None:
                continue
            atual, total_p = nums
            key = l["descricao"]
            if key not in parcelas_map or atual > parcelas_map[key]["atual"]:
                parcelas_map[key] = {
                    "atual": atual, "total": total_p,
                    "valor": l["valor"], "cat": l.get("categoria", ""),
                    "obs": l.get("obs", ""), "mes_key": mk, "id": l["id"],
                }

    if not parcelas_map:
        st.markdown("<div class='card' style='text-align:center;color:#bbb;padding:24px;font-size:13px;'>"
                    "Nenhuma parcela registrada.</div>", unsafe_allow_html=True)
    else:
        for desc, info in sorted(parcelas_map.items()):
            a, t   = info["atual"], info["total"]
            restam = t - a
            pct    = a / t * 100
            val_rest = restam * info["valor"]
            pid    = info["id"]

            if st.session_state.get("editing_parc") == pid:
                with st.form(f"ef_parc_{pid}"):
                    st.markdown(f"**Editando: {desc}**")
                    pnd  = st.text_input("Descrição", value=desc)
                    pnv  = st.number_input("Valor/parcela (R$)", value=float(info["valor"]), step=0.01, format="%.2f")
                    pec1, pec2 = st.columns(2)
                    pna  = pec1.number_input("Parcela atual", value=int(a), min_value=0)
                    pnt  = pec2.number_input("Total parcelas", value=int(t), min_value=1)
                    pncat = st.selectbox("Categoria", CATEGORIAS,
                                         index=CATEGORIAS.index(info["cat"]) if info["cat"] in CATEGORIAS else 0)
                    pnobs = st.text_input("Observação", value=info.get("obs", ""))
                    pes1, pes2 = st.columns(2)
                    if pes1.form_submit_button("Salvar", use_container_width=True, type="primary"):
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
            else:
                _falta_txt = f"Falta {fmt(val_rest)} ({restam}x)" if restam > 0 else "Quitada"
                _falta_cor = "#DC2626" if restam > 0 else "#16A34A"
                _prox_mes_label = ""
                if restam > 0 and info["mes_key"] < mes_key:
                    _prox_mes_label = f" · próxima em {nome_mes(prox_mes(info['mes_key']))}"

                st.markdown(f"""
<div style='background:#242424;border-radius:8px;padding:12px 14px;
     margin-bottom:4px;border:1px solid #2E2E2E;'>
  <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px;'>
    <div style='font-weight:600;color:#E8E8E8;font-size:14px;'>{desc}</div>
    <div style='font-size:11px;color:#666;'>{a}/{t} parcelas</div>
  </div>
  <div class='prog-bg' style='margin:8px 0 6px;'><div class='prog-fill' style='width:{pct:.0f}%;'></div></div>
  <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px;'>
    <div style='font-size:11px;color:#666;'>{info['cat']} · {fmt(info['valor'])}/mês{_prox_mes_label}</div>
    <div style='font-size:12px;font-weight:700;color:{_falta_cor};'>{_falta_txt}</div>
  </div>
</div>""", unsafe_allow_html=True)

                pa_a, pa_b = st.columns([1, 1])
                if pa_a.button("Editar", key=f"pedit_{pid}", use_container_width=True):
                    st.session_state["editing_parc"] = pid; st.rerun()
                if pa_b.button("Excluir", key=f"pdel_{pid}", use_container_width=True):
                    st.session_state[f"cpdel_{pid}"] = True; st.rerun()

                if st.session_state.get(f"cpdel_{pid}"):
                    st.warning(f"Excluir **{desc}** ({nome_mes(info['mes_key'])})?")
                    pd1, pd2 = st.columns(2)
                    if pd1.button("Excluir", key=f"ypdel_{pid}", type="primary", use_container_width=True):
                        mk_del = info["mes_key"]
                        d["meses"][mk_del]["lancamentos"] = [
                            l for l in d["meses"][mk_del].get("lancamentos", []) if l["id"] != pid
                        ]
                        st.session_state.pop(f"cpdel_{pid}", None)
                        save_data(d); st.rerun()
                    if pd2.button("Cancelar", key=f"npdel_{pid}", use_container_width=True):
                        st.session_state.pop(f"cpdel_{pid}", None); st.rerun()

            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# POUPANÇA
# ═══════════════════════════════════════════════════════════════
with tab_poupa:
    poupa         = d.get("poupanca", {"objetivo": "", "meta_total": 0.0, "depositos": []})
    deps          = poupa.get("depositos", [])
    total_poupado = sum(dep["valor"] for dep in deps)
    meta_total    = poupa.get("meta_total", 0.0)
    objetivo      = poupa.get("objetivo", "")
    pct_meta      = min((total_poupado / meta_total * 100) if meta_total > 0 else 0, 100)
    pct_meta      = max(pct_meta, 0)

    _mt_label  = fmt(meta_total) if meta_total > 0 else "—"
    _obj_label = objetivo if objetivo else "Sem objetivo definido"

    st.markdown(f"""
<div class='card'>
  <div style='font-size:10px;font-weight:700;color:#666;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;'>Objetivo</div>
  <div style='font-weight:700;font-size:15px;color:#E8E8E8;margin-bottom:12px;'>{_obj_label}</div>
  <div style='display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:10px;'>
    <div>
      <div class='valor-label'>Total poupado</div>
      <div style='font-size:18px;font-weight:700;color:#4ADE80;'>{fmt(total_poupado)}</div>
    </div>
    <div style='text-align:right;'>
      <div class='valor-label'>Meta</div>
      <div style='font-size:16px;font-weight:700;color:#888;'>{_mt_label}</div>
    </div>
  </div>
  <div class='prog-bg'><div class='prog-fill' style='width:{pct_meta:.0f}%;'></div></div>
  <div style='font-size:11px;color:#666;margin-top:5px;text-align:right;'>{pct_meta:.0f}% da meta</div>
</div>""", unsafe_allow_html=True)

    if st.session_state.get("editing_poupa_cfg"):
        with st.form("f_poupa_cfg"):
            n_obj  = st.text_input("Objetivo (ex: viagem, reserva...)", value=objetivo)
            n_meta = st.number_input("Meta total (R$)", value=float(meta_total),
                                     min_value=0.0, step=500.0, format="%.2f")
            pc1, pc2 = st.columns(2)
            if pc1.form_submit_button("Salvar", use_container_width=True, type="primary"):
                poupa["objetivo"]   = n_obj.strip()
                poupa["meta_total"] = float(n_meta)
                d["poupanca"] = poupa
                st.session_state.pop("editing_poupa_cfg", None)
                save_data(d); st.rerun()
            if pc2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.pop("editing_poupa_cfg", None); st.rerun()
    else:
        if st.button("Editar objetivo e meta", key="btn_poupa_cfg", use_container_width=True):
            st.session_state["editing_poupa_cfg"] = True; st.rerun()

    st.markdown("<div class='sec'>Depósitos</div>", unsafe_allow_html=True)
    cadep, _ = st.columns([2, 3])
    if cadep.button("+ Novo depósito", key="add_dep_top", use_container_width=True):
        st.session_state["show_add_dep"] = not st.session_state.get("show_add_dep", False)

    if st.session_state.get("show_add_dep"):
        with st.form("f_dep_g", clear_on_submit=True):
            val_dq  = st.number_input("Valor (R$) *", min_value=0.01, step=50.0, format="%.2f")
            dep_meses = sorted(d["meses"].keys(), reverse=True)
            dep_meses_labels = [nome_mes(k) for k in dep_meses]
            sel_dep_mes = st.selectbox("Mês de referência", dep_meses_labels)
            dep_mes_key = dep_meses[dep_meses_labels.index(sel_dep_mes)]
            obs_dq  = st.text_input("Observação", placeholder="Ex: poupança do mês...")
            ds1, ds2 = st.columns(2)
            if ds1.form_submit_button("Adicionar", use_container_width=True, type="primary"):
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
        st.markdown("<div style='text-align:center;color:#bbb;padding:24px 0;font-size:13px;'>Nenhum depósito ainda.</div>",
                    unsafe_allow_html=True)
    else:
        deps_ord = sorted(deps, key=lambda x: x.get("mes",""), reverse=True)
        for dep in deps_ord:
            did   = dep["id"]
            obs_d = dep.get("obs","")
            sub_d = " · ".join(filter(None, [nome_mes(dep.get("mes","")), obs_d]))

            if st.session_state.get("editing_dep") == did:
                with st.form(f"ef_dep_{did}"):
                    dnv  = st.number_input("Valor (R$)", value=float(dep["valor"]), step=50.0, format="%.2f")
                    dep_meses2 = sorted(d["meses"].keys(), reverse=True)
                    dep_ml2    = [nome_mes(k) for k in dep_meses2]
                    cur_idx    = dep_meses2.index(dep.get("mes","")) if dep.get("mes") in dep_meses2 else 0
                    sel_dm2    = st.selectbox("Mês", dep_ml2, index=cur_idx)
                    dnm        = dep_meses2[dep_ml2.index(sel_dm2)]
                    dnobs      = st.text_input("Observação", value=dep.get("obs",""))
                    de1, de2   = st.columns(2)
                    if de1.form_submit_button("Salvar", use_container_width=True, type="primary"):
                        dep.update({"valor": float(dnv), "mes": dnm, "obs": dnobs})
                        st.session_state.pop("editing_dep", None)
                        save_data(d); st.rerun()
                    if de2.form_submit_button("Cancelar", use_container_width=True):
                        st.session_state.pop("editing_dep", None); st.rerun()
            else:
                st.markdown(f"""
<div style='background:#242424;border-radius:8px;padding:12px 14px;
     border-left:3px solid #BBF7D0;border:1px solid #2E2E2E;border-left:3px solid #BBF7D0;
     margin-bottom:4px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div style='flex:1;'>
      <div style='font-weight:600;font-size:14px;color:#E8E8E8;'>Depósito</div>
      <div style='font-size:11px;color:#666;margin-top:2px;'>{sub_d}</div>
    </div>
    <div style='font-weight:700;font-size:15px;color:#4ADE80;margin-left:12px;'>{fmt(dep['valor'])}</div>
  </div>
</div>""", unsafe_allow_html=True)
                da, db = st.columns([3, 1])
                if da.button("Editar", key=f"dedit_{did}", use_container_width=True):
                    st.session_state["editing_dep"] = did; st.rerun()
                if db.button("✕", key=f"ddel_{did}", use_container_width=True):
                    st.session_state[f"cddel_{did}"] = True; st.rerun()
                if st.session_state.get(f"cddel_{did}"):
                    st.warning("Excluir este depósito?")
                    dd1, dd2 = st.columns(2)
                    if dd1.button("Excluir", key=f"yddel_{did}", type="primary", use_container_width=True):
                        poupa["depositos"] = [x for x in deps if x["id"] != did]
                        d["poupanca"] = poupa
                        st.session_state.pop(f"cddel_{did}", None)
                        save_data(d); st.rerun()
                    if dd2.button("Cancelar", key=f"nddel_{did}", use_container_width=True):
                        st.session_state.pop(f"cddel_{did}", None); st.rerun()
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    # Quanto sobrou por mês
    st.markdown("<div class='sec'>Sobra por mês (últimos 6)</div>", unsafe_allow_html=True)
    rows_s = ""
    meses_recentes = sorted(d["meses"].keys(), reverse=True)[:6]
    for mk in sorted(meses_recentes):
        mv  = d["meses"][mk]
        mr  = sum(x["valor"] for x in mv.get("receitas", []))
        mt  = sum(x["valor"] for x in mv.get("lancamentos", []))
        msd = mr - mt
        sc  = "#16A34A" if msd >= 0 else "#DC2626"
        ss  = (fmt(msd) if msd >= 0 else "- " + fmt(abs(msd)))
        bold = "font-weight:700;" if mk == mes_key else ""
        rows_s += f"""
<div class='item-row'>
  <div style='font-size:13px;{bold}'>{nome_mes(mk)}</div>
  <div style='font-weight:700;font-size:13px;color:{sc};'>{ss}</div>
</div>"""
    st.markdown(f"<div class='card'>{rows_s}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# RESUMO
# ═══════════════════════════════════════════════════════════════
with tab_r:
    # Por categoria
    cat_totais = {}
    for item in lanc:
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
    <div style='font-weight:500;font-size:13px;color:#E8E8E8;'>{cat}</div>
    <div style='margin-top:4px;'>
      <div class='prog-bg'><div class='prog-fill' style='width:{pct:.0f}%;'></div></div>
    </div>
  </div>
  <div style='text-align:right;margin-left:16px;'>
    <div style='font-weight:700;color:#E8E8E8;font-size:13px;'>{fmt(val)}</div>
    <div style='font-size:10px;color:#666;'>{pct:.0f}%</div>
  </div>
</div>"""
        st.markdown(f"<div class='card'>{rows}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center;color:#bbb;padding:16px;font-size:13px;'>Sem gastos registrados.</div>",
                    unsafe_allow_html=True)

    # Histórico
    if len(meses_keys) > 1:
        st.markdown("<div class='sec'>Histórico</div>", unsafe_allow_html=True)
        rows_h = ""
        for mk in sorted(meses_keys)[-6:]:
            ml  = d["meses"][mk].get("lancamentos", [])
            mr  = d["meses"][mk].get("receitas", [])
            mt  = sum(x["valor"] for x in ml)
            mtr = sum(x["valor"] for x in mr)
            msd = mtr - mt
            bold = "font-weight:700;color:#E8E8E8;" if mk == mes_key else "color:#888;"
            saldo_c = "#16A34A" if msd >= 0 else "#DC2626"
            saldo_s = (fmt(msd) if msd >= 0 else "- " + fmt(abs(msd)))
            rows_h += f"""
<div class='item-row'>
  <div style='font-size:13px;{bold}'>{nome_mes(mk)}</div>
  <div style='text-align:right;'>
    <div style='font-weight:700;font-size:13px;color:#F87171;'>{fmt(mt)}</div>
    <div style='font-size:11px;color:{saldo_c};font-weight:600;'>saldo {saldo_s}</div>
  </div>
</div>"""
        st.markdown(f"<div class='card'>{rows_h}</div>", unsafe_allow_html=True)

    # Template de fixas
    st.markdown("<div class='sec'>Template de fixas</div>", unsafe_allow_html=True)
    tf_list = d.get("template_fixas", [])
    if st.session_state.get("editing_template"):
        with st.form("f_template"):
            st.markdown("**Editar template (fixas copiadas todo mês)**")
            novas_tf = []
            for i, tf_item in enumerate(tf_list):
                tc1, tc2, tc3 = st.columns([3, 2, 3])
                td = tc1.text_input(f"Nome {i+1}", value=tf_item["descricao"], key=f"tfd_{i}")
                tv = tc2.number_input(f"R$ {i+1}", value=float(tf_item["valor"]), step=0.01, format="%.2f", key=f"tfv_{i}")
                tc_opts = CATEGORIAS
                tc_idx  = tc_opts.index(tf_item["categoria"]) if tf_item["categoria"] in tc_opts else 0
                tcc = tc3.selectbox(f"Cat {i+1}", tc_opts, index=tc_idx, key=f"tfc_{i}")
                if td.strip() and tv > 0:
                    novas_tf.append({"descricao": td.strip(), "valor": float(tv), "categoria": tcc})
            t1, t2 = st.columns(2)
            if t1.form_submit_button("Salvar template", use_container_width=True, type="primary"):
                d["template_fixas"] = novas_tf
                st.session_state.pop("editing_template", None)
                save_data(d); st.rerun()
            if t2.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.pop("editing_template", None); st.rerun()
    else:
        rows_tf = ""
        for tf_item in tf_list:
            rows_tf += f"""
<div class='item-row'>
  <div style='font-size:13px;color:#888;'>{tf_item['descricao']}</div>
  <div style='font-weight:600;font-size:13px;color:#E8E8E8;'>{fmt(tf_item['valor'])}</div>
</div>"""
        if rows_tf:
            st.markdown(f"<div class='card'>{rows_tf}</div>", unsafe_allow_html=True)
        if st.button("Editar template de fixas", key="btn_template", use_container_width=True):
            st.session_state["editing_template"] = True; st.rerun()

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:20px 0 6px;'>
  <p style='color:#444;font-size:10px;margin:0;letter-spacing:0.5px;'>
    "Honra ao Senhor com os teus bens" · Pv 3:9
  </p>
</div>
""", unsafe_allow_html=True)
