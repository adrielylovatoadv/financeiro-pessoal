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

# ─── Login ────────────────────────────────────────────────────────────────────
_senha_ok = st.secrets.get("SENHA","adriely2025") if hasattr(st,"secrets") else "adriely2025"
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if not st.session_state["logado"]:
    st.markdown("""
<div style="max-width:340px;margin:60px auto 0;text-align:center;">
  <div style="font-size:52px;margin-bottom:8px;">🌿</div>
  <h2 style="color:#2D6A4F;font-weight:700;margin:0;">Meu Dinheiro</h2>
  <p style="color:#718096;margin:6px 0 28px;font-size:14px;">Controle pessoal com propósito</p>
</div>""", unsafe_allow_html=True)
    with st.form("login_p"):
        senha_i = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        if st.form_submit_button("Entrar →", use_container_width=True):
            if senha_i == _senha_ok:
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.markdown("""<p style="text-align:center;color:#a0aec0;font-size:12px;margin-top:40px;">
    "Porque onde estiver o seu tesouro, aí estará também o seu coração." — Mt 6:21</p>""",
    unsafe_allow_html=True)
    st.stop()

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp { background:#F7F3EE !important; }
.block-container { padding-top:1rem !important; max-width:640px; }

/* Cards */
.card {
    background:white; border-radius:16px;
    padding:20px; margin-bottom:14px;
    box-shadow:0 1px 6px rgba(0,0,0,0.07);
}
.card-sm {
    background:white; border-radius:12px;
    padding:14px 18px; margin-bottom:10px;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);
}

/* Versículo */
.versiculo {
    background:linear-gradient(135deg,#2D6A4F 0%,#40916C 100%);
    border-radius:16px; padding:22px 24px; margin-bottom:14px;
    color:white;
}
.versiculo-texto {
    font-size:15px; line-height:1.65; font-style:italic;
    color:rgba(255,255,255,0.95); margin:0 0 10px 0;
}
.versiculo-ref {
    font-size:11px; font-weight:700; letter-spacing:1.5px;
    text-transform:uppercase; color:rgba(255,255,255,0.65);
}

/* Dica */
.dica {
    background:#FFFBF0; border:1px solid #F6D860;
    border-left:4px solid #D4A853;
    border-radius:12px; padding:14px 18px; margin-bottom:14px;
}
.dica-titulo { font-size:11px; font-weight:700; color:#B7791F;
    text-transform:uppercase; letter-spacing:1px; margin-bottom:4px; }
.dica-texto { font-size:13px; color:#744210; line-height:1.5; margin:0; }

/* Valores */
.valor-grande { font-size:32px; font-weight:700; color:#1A202C; line-height:1; }
.valor-label  { font-size:11px; color:#A0AEC0; text-transform:uppercase;
    letter-spacing:1px; margin-bottom:4px; }
.valor-verde  { color:#276749; }
.valor-vermelho { color:#9B2C2C; }
.valor-azul   { color:#2B6CB0; }

/* Tags */
.tag-pago    { background:#C6F6D5; color:#276749; border-radius:20px;
    padding:3px 10px; font-size:11px; font-weight:700; }
.tag-pend    { background:#FED7D7; color:#9B2C2C; border-radius:20px;
    padding:3px 10px; font-size:11px; font-weight:700; }
.tag-cat     { background:#EBF4FF; color:#2B6CB0; border-radius:20px;
    padding:3px 8px; font-size:11px; font-weight:600; }

/* Barra de progresso */
.prog-bg   { background:#EDF2F7; border-radius:8px; height:8px; overflow:hidden; }
.prog-fill { background:linear-gradient(90deg,#2D6A4F,#D4A853);
    height:100%; border-radius:8px; }

/* Linha de item */
.item-row {
    display:flex; justify-content:space-between; align-items:flex-start;
    padding:12px 0; border-bottom:1px solid #F0EDE8;
}
.item-row:last-child { border-bottom:none; }
.item-desc { font-weight:600; color:#2D3748; font-size:14px; }
.item-sub  { font-size:11px; color:#A0AEC0; margin-top:2px; }
.item-val  { font-weight:700; font-size:15px; color:#2D3748; white-space:nowrap; }

/* Seção título */
.sec { font-size:12px; font-weight:700; color:#A0AEC0;
    text-transform:uppercase; letter-spacing:1.5px; margin:20px 0 10px; }

/* Botões */
.stButton>button {
    border-radius:12px !important; font-weight:600 !important;
    border:none !important; padding:10px 20px !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:#ECDDC8; border-radius:12px; padding:4px; gap:2px;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius:10px; font-size:13px; font-weight:500; color:#744210;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background:white !important; color:#2D6A4F !important;
    font-weight:700 !important; box-shadow:0 1px 4px rgba(0,0,0,0.1) !important;
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

DICAS = [
    ("Regra dos 50/30/20", "Destine 50% para necessidades, 30% para desejos e 20% para poupança e dívidas. Automatize essa separação todo mês."),
    ("Pague-se primeiro", "Assim que receber, transfira o valor de poupança antes de pagar qualquer outra conta. Guarde o que sobrar."),
    ("Fundo de emergência", "Construa uma reserva de 3 a 6 meses de despesas. Ela evita que imprevistos virem dívidas."),
    ("Cuidado com parcelamentos", "Parcelas pequenas parecem inofensivas, mas somadas podem comprometer boa parte da renda. Revise os seus compromissos futuros."),
    ("Liste antes de comprar", "Antes de ir ao mercado ou abrir um app de compras, escreva o que precisa. Evita impulso."),
    ("Espere 48h", "Sentiu vontade de comprar algo não essencial? Espere 48 horas. Muitas compras por impulso não sobrevivem à reflexão."),
    ("Negocie com fornecedores", "Planos de telefone, internet, seguros — renegocie anualmente. Empresas têm ofertas especiais para quem pede."),
    ("Revise assinaturas", "Confira todos os débitos automáticos. Serviços esquecidos são dinheiro desperdiçado todo mês."),
    ("Cozinhe mais em casa", "Reduzir pedidos de delivery em 2x por semana pode economizar centenas de reais por mês."),
    ("Compare preços", "Antes de comprar qualquer item acima de R$ 100, compare em pelo menos 3 lugares. Minutos de pesquisa economizam muito."),
    ("Anote todo gasto", "Pequenos gastos invisíveis (cafés, lanches, aplicativos) somam mais do que parece. Registre tudo."),
    ("Defina uma meta visual", "Quer fazer uma viagem? Reformar um cômodo? Cole uma imagem que inspire. Objetivos concretos motivam mais."),
    ("Dívidas: bola de neve ou avalanche?", "Na bola de neve, quite a menor primeiro. Na avalanche, a de maior juros. Escolha uma estratégia e seja consistente."),
    ("Evite o mínimo do cartão", "Pagar o mínimo da fatura é o caminho mais caro. Se não consegue pagar o total, revise os gastos urgentemente."),
    ("Um ano depois...", "Antes de uma compra grande, pergunte-se: em um ano, vou me arrepender de ter comprado? Ou de não ter poupado esse dinheiro?"),
]

def conteudo_do_dia():
    hoje = _date.today()
    idx_v = hoje.timetuple().tm_yday % len(VERSICULO)
    idx_d = (hoje.timetuple().tm_yday + 7) % len(DICAS)
    return VERSICULO[idx_v], DICAS[idx_d]

# ─── Constantes ───────────────────────────────────────────────────────────────
CATEGORIAS = [
    "💳 Cartão","🏦 Banco/Financ.","🏠 Moradia","🚗 Carro",
    "💊 Saúde","💪 Academia/Esporte","⚖️ Profissional","📱 Serviços",
    "🛡️ Seguro","🛒 Compras","💄 Beleza","🎾 Lazer","🎯 Outros",
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
        payload = json.dumps({"message":"atualiza dados","content":content,"sha":sha}).encode()
        req = urllib.request.Request(_GH_API,data=payload,headers=_gh_headers(),method="PUT")
        urllib.request.urlopen(req,timeout=15)
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

# ─── Cabeçalho ────────────────────────────────────────────────────────────────
meses_keys  = sorted(d["meses"].keys())
mes_labels  = [nome_mes(k) for k in meses_keys]

col_t, col_s = st.columns([3, 2])
col_t.markdown("### 🌿 Meu Dinheiro")
mes_sel = col_s.selectbox("", mes_labels,
    index=len(mes_labels)-1, label_visibility="collapsed")
mes_key = meses_keys[mes_labels.index(mes_sel)]

# ─── Versículo + Dica do dia ──────────────────────────────────────────────────
ver, dic = conteudo_do_dia()
st.markdown(f"""
<div class="versiculo">
  <p class="versiculo-texto">"{ver[1]}"</p>
  <div class="versiculo-ref">📖 {ver[0]}</div>
</div>
<div class="dica">
  <div class="dica-titulo">💡 Dica · {dic[0]}</div>
  <p class="dica-texto">{dic[1]}</p>
</div>
""", unsafe_allow_html=True)

# ─── Dados do mês ─────────────────────────────────────────────────────────────
mes    = d["meses"][mes_key]
lanc   = mes.get("lancamentos", [])
fixas  = mes.get("fixas", [])
todos  = lanc + fixas

total  = sum(i["valor"] for i in todos)
pago   = sum(i["valor"] for i in todos if i.get("pago"))
pend   = total - pago

# ─── Cards de resumo ──────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.markdown(f"""<div class='card' style='text-align:center;'>
  <div class='valor-label'>Total</div>
  <div class='valor-grande'>{fmt(total)}</div>
</div>""", unsafe_allow_html=True)
c2.markdown(f"""<div class='card' style='text-align:center;'>
  <div class='valor-label'>Pago</div>
  <div class='valor-grande valor-verde'>{fmt(pago)}</div>
</div>""", unsafe_allow_html=True)
c3.markdown(f"""<div class='card' style='text-align:center;'>
  <div class='valor-label'>A pagar</div>
  <div class='valor-grande valor-vermelho'>{fmt(pend)}</div>
</div>""", unsafe_allow_html=True)

# ─── Abas ─────────────────────────────────────────────────────────────────────
tab_g, tab_f, tab_p, tab_add, tab_r = st.tabs([
    "💸 Gastos", "🔁 Fixas", "📅 Parcelas", "➕ Novo", "📊 Resumo"
])

# ═══════════════════════════════════════════════════════════════
# GASTOS (lançamentos variáveis)
# ═══════════════════════════════════════════════════════════════
with tab_g:
    if not lanc:
        st.markdown("<div class='card' style='text-align:center;color:#a0aec0;padding:30px;'>"
                    "Nenhum gasto registrado.<br>Use a aba <b>➕ Novo</b> para adicionar.</div>",
                    unsafe_allow_html=True)
    else:
        lanc_ord = sorted(lanc, key=lambda x: x.get("data", 0))
        pend_lanc = [l for l in lanc_ord if not l.get("pago")]
        pago_lanc = [l for l in lanc_ord if l.get("pago")]

        def _render_lanc(items, collapsed=False):
            rows_html = ""
            for item in items:
                parc = item.get("parcela","")
                obs  = item.get("obs","")
                sub  = " · ".join(filter(None, [
                    f"Dia {int(item['data'])}" if item.get('data') else "",
                    parc, obs
                ]))
                tag_class = "tag-pago" if item["pago"] else "tag-pend"
                tag_txt   = "✓ pago" if item["pago"] else "pendente"
                rows_html += f"""
<div class='item-row'>
  <div>
    <div class='item-desc'>{item['descricao']}</div>
    <div class='item-sub'>{sub}</div>
  </div>
  <div style='text-align:right;'>
    <div class='item-val'>{fmt(item['valor'])}</div>
    <span class='{tag_class}'>{tag_txt}</span>
  </div>
</div>"""
            return f"<div class='card'>{rows_html}</div>"

        if pend_lanc:
            st.markdown("<div class='sec'>● A pagar</div>", unsafe_allow_html=True)
            st.markdown(_render_lanc(pend_lanc), unsafe_allow_html=True)
            for item in pend_lanc:
                if st.button(f"✓ Marcar pago: {item['descricao']} ({fmt(item['valor'])})",
                             key=f"pg_{item['id']}", use_container_width=True):
                    item["pago"] = True
                    save_data(d)
                    st.rerun()

        if pago_lanc:
            with st.expander(f"✓ Pagos ({len(pago_lanc)})"):
                st.markdown(_render_lanc(pago_lanc), unsafe_allow_html=True)
                for item in pago_lanc:
                    if st.button(f"↩ Desfazer: {item['descricao']}",
                                 key=f"dpg_{item['id']}", use_container_width=True):
                        item["pago"] = False
                        save_data(d)
                        st.rerun()

        with st.expander("🗑️ Excluir gasto"):
            opcoes = {f"Dia {l.get('data','?')} – {l['descricao']} ({fmt(l['valor'])})": l["id"]
                      for l in lanc_ord}
            sel = st.selectbox("", list(opcoes.keys()), label_visibility="collapsed")
            if st.button("Excluir", key="del_l", type="primary"):
                mes["lancamentos"] = [l for l in lanc if l["id"] != opcoes[sel]]
                save_data(d)
                st.rerun()

# ═══════════════════════════════════════════════════════════════
# FIXAS
# ═══════════════════════════════════════════════════════════════
with tab_f:
    if not fixas:
        st.info("Nenhuma conta fixa neste mês.")
    else:
        fixas_ord = sorted(fixas, key=lambda x: x["descricao"])
        pend_f = [f for f in fixas_ord if not f.get("pago")]
        pago_f = [f for f in fixas_ord if f.get("pago")]

        def _render_fixas(items):
            rows = ""
            for item in items:
                tag_class = "tag-pago" if item["pago"] else "tag-pend"
                tag_txt   = "✓ pago" if item["pago"] else "pendente"
                rows += f"""
<div class='item-row'>
  <div>
    <div class='item-desc'>{item['descricao']}</div>
    <div class='item-sub'>{item.get('categoria','')}</div>
  </div>
  <div style='text-align:right;'>
    <div class='item-val'>{fmt(item['valor'])}</div>
    <span class='{tag_class}'>{tag_txt}</span>
  </div>
</div>"""
            return f"<div class='card'>{rows}</div>"

        tf = sum(i["valor"] for i in fixas)
        pf = sum(i["valor"] for i in fixas if i["pago"])
        st.markdown(f"<div class='card' style='text-align:center;'>"
                    f"<div class='valor-label'>Total fixas</div>"
                    f"<div class='valor-grande'>{fmt(tf)}</div>"
                    f"<div style='font-size:12px;color:#a0aec0;margin-top:4px;'>"
                    f"Pago: {fmt(pf)} · Pendente: {fmt(tf-pf)}</div></div>",
                    unsafe_allow_html=True)

        if pend_f:
            st.markdown("<div class='sec'>● A pagar</div>", unsafe_allow_html=True)
            st.markdown(_render_fixas(pend_f), unsafe_allow_html=True)
            for item in pend_f:
                if st.button(f"✓ {item['descricao']} ({fmt(item['valor'])})",
                             key=f"fpg_{item['id']}", use_container_width=True):
                    item["pago"] = True
                    save_data(d)
                    st.rerun()

        if pago_f:
            with st.expander(f"✓ Pagas ({len(pago_f)})"):
                st.markdown(_render_fixas(pago_f), unsafe_allow_html=True)
                for item in pago_f:
                    if st.button(f"↩ Desfazer: {item['descricao']}",
                                 key=f"fdpg_{item['id']}", use_container_width=True):
                        item["pago"] = False
                        save_data(d)
                        st.rerun()

# ═══════════════════════════════════════════════════════════════
# PARCELAS
# ═══════════════════════════════════════════════════════════════
with tab_p:
    st.markdown("<div class='sec'>Parcelas ativas (todos os meses)</div>", unsafe_allow_html=True)
    parcelas_map = {}
    for mk in sorted(d["meses"].keys()):
        for l in d["meses"][mk].get("lancamentos", []):
            ps = l.get("parcela","")
            if not ps or "/" not in ps: continue
            try:
                a_s, t_s = ps.strip().split("/")
                atual = int("".join(c for c in a_s if c.isdigit()))
                total_p = int("".join(c for c in t_s if c.isdigit()))
            except: continue
            key = l["descricao"]
            if key not in parcelas_map or atual > parcelas_map[key]["atual"]:
                parcelas_map[key] = {
                    "atual":atual,"total":total_p,
                    "valor":l["valor"],"cat":l.get("categoria",""),
                }

    if not parcelas_map:
        st.markdown("<div class='card' style='text-align:center;color:#a0aec0;padding:24px;'>"
                    "Nenhuma parcela registrada.</div>", unsafe_allow_html=True)
    else:
        for desc, info in sorted(parcelas_map.items()):
            a, t = info["atual"], info["total"]
            restam = t - a
            pct = a / t * 100
            val_rest = restam * info["valor"]
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
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# NOVO GASTO
# ═══════════════════════════════════════════════════════════════
with tab_add:
    tipo = st.radio("", ["💸 Gasto variável","🔁 Conta fixa"], horizontal=True,
                    label_visibility="collapsed")

    if tipo == "💸 Gasto variável":
        with st.form("f_lanc", clear_on_submit=True):
            desc_n = st.text_input("Descrição *", placeholder="Ex: Mercado, Farmácia...")
            val_n  = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            c_a, c_b = st.columns(2)
            dia_n  = c_a.number_input("Dia", min_value=1, max_value=31, value=_date.today().day)
            parc_n = c_b.text_input("Parcela", placeholder="Ex: 1/12")
            cat_n  = st.selectbox("Categoria", CATEGORIAS)
            obs_n  = st.text_input("Observação", placeholder="opcional")
            pago_n = st.checkbox("Já pago?", value=False)
            ok = st.form_submit_button("✓ Adicionar", use_container_width=True, type="primary")
            if ok:
                if desc_n.strip() and val_n > 0:
                    mes["lancamentos"].append({
                        "id":str(uuid.uuid4()),"data":int(dia_n),
                        "descricao":desc_n.strip(),"valor":float(val_n),
                        "parcela":parc_n.strip(),"categoria":cat_n,
                        "pago":pago_n,"obs":obs_n.strip(),
                    })
                    save_data(d)
                    st.success(f"✅ {desc_n} adicionado!")
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")
    else:
        with st.form("f_fixa", clear_on_submit=True):
            desc_f = st.text_input("Descrição *", placeholder="Ex: Seguro, Streaming...")
            val_f  = st.number_input("Valor (R$) *", min_value=0.0, step=0.01, format="%.2f")
            cat_f  = st.selectbox("Categoria", CATEGORIAS)
            pago_f = st.checkbox("Já pago?", value=False)
            ok_f = st.form_submit_button("✓ Adicionar", use_container_width=True, type="primary")
            if ok_f:
                if desc_f.strip() and val_f > 0:
                    mes["fixas"].append({
                        "id":str(uuid.uuid4()),"descricao":desc_f.strip(),
                        "valor":float(val_f),"categoria":cat_f,"pago":pago_f,
                    })
                    save_data(d)
                    st.success(f"✅ {desc_f} adicionado!")
                    st.rerun()
                else:
                    st.error("Preencha descrição e valor.")

    st.markdown("---")
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
                "lancamentos": [],
                "fixas": [{"id":str(uuid.uuid4()),"descricao":t["descricao"],
                           "valor":t["valor"],"categoria":t["categoria"],"pago":False}
                          for t in d.get("template_fixas", [])],
            }
            save_data(d)
            st.rerun()

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
            ml = d["meses"][mk].get("lancamentos",[])
            mf = d["meses"][mk].get("fixas",[])
            mt = sum(x["valor"] for x in ml) + sum(x["valor"] for x in mf)
            bold = "font-weight:700;color:#2D6A4F;" if mk == mes_key else ""
            rows_h += f"""
<div class='item-row'>
  <div style='font-size:14px;{bold}'>{nome_mes(mk)}</div>
  <div style='font-weight:700;font-size:15px;{bold}'>{fmt(mt)}</div>
</div>"""
        st.markdown(f"<div class='card'>{rows_h}</div>", unsafe_allow_html=True)

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;padding:24px 0 8px;'>
  <p style='color:#CBD5E0;font-size:11px;margin:0;'>
    "Honra ao Senhor com os teus bens" · Pv 3:9
  </p>
</div>
""", unsafe_allow_html=True)
