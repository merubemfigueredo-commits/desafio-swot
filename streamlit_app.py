"""DESAFIO SWOT

Jogo educacional em Streamlit para praticar análise SWOT/TOWS.

Execute com:
    streamlit run game-swot.py
"""

from __future__ import annotations

import io
import json
import random
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


st.set_page_config(
    page_title="DESAFIO SWOT",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Banco de cases
# ---------------------------------------------------------------------------

CASES: list[dict[str, Any]] = [
    {
        "empresa": "Cafeteria Artesanal “Grão de Boquim”",
        "contexto": (
            "Pequena cafeteria com café premiado, mas com pouca presença digital. "
            "Um shopping novo vai abrir na cidade."
        ),
        "fatores": [
            ("Café premiado e clientes fiéis", "Força"),
            ("Equipe com alta rotatividade", "Fraqueza"),
            ("Crescimento do consumo de cafés especiais no Brasil", "Oportunidade"),
            ("Aumento do preço do grão de café no mercado", "Ameaça"),
            ("Ponto bem localizado no centro", "Força"),
            ("Sem sistema de delivery", "Fraqueza"),
            ("Parceria com escritórios locais", "Oportunidade"),
            ("Chegada de uma grande rede de cafeterias na cidade", "Ameaça"),
        ],
        "pergunta_final": "Qual a melhor estratégia para a cafeteria nos próximos 6 meses?",
        "opcoes_final": [
            "Investir pesado em uma filial antes de testar a demanda",
            "Criar clube de assinatura + delivery e fechar parceria com empresas",
            "Diminuir o preço do café para competir somente por preço",
            "Vender a cafeteria enquanto o shopping ainda não abriu",
        ],
        "correta_final": 1,
        "justificativa_final": (
            "A opção combina forças (produto premiado e localização) com "
            "oportunidades (assinatura, delivery e empresas), sem ignorar a "
            "ameaça de uma rede maior."
        ),
        "estrategias": {
            "FO": ["cafe", "premiad", "assinatur", "delivery", "especial"],
            "FA": ["client", "fiel", "qualidad", "diferenci", "rede"],
            "WO": ["delivery", "digital", "instagram", "empresa", "parceria"],
            "WA": ["rotativ", "trein", "custo", "fornecedor", "margem"],
        },
    },
    {
        "empresa": "Loja de Roupas “Estilo SE”",
        "contexto": (
            "Loja física com 10 anos, estoque grande, mas vendas caindo por "
            "causa da concorrência online."
        ),
        "fatores": [
            ("Marca conhecida na cidade", "Força"),
            ("Estoque parado de coleções antigas", "Fraqueza"),
            ("Marketplace e Instagram Shopping", "Oportunidade"),
            ("Fast fashion com preços muito baixos", "Ameaça"),
            ("Atendimento personalizado", "Força"),
            ("Sem e-commerce próprio", "Fraqueza"),
            ("Influenciadoras locais acessíveis", "Oportunidade"),
            ("Crise econômica reduzindo o consumo", "Ameaça"),
        ],
        "pergunta_final": "Qual estratégia de crescimento é mais viável?",
        "opcoes_final": [
            "Fechar a loja física imediatamente e ir só para o online",
            "Lançar e-commerce + queima de estoque com lives com influenciadoras",
            "Comprar ainda mais estoque novo para aumentar a variedade",
            "Manter tudo como está até o mercado melhorar",
        ],
        "correta_final": 1,
        "justificativa_final": (
            "A estratégia usa a marca e o atendimento personalizado para testar "
            "o digital, liberar capital do estoque parado e alcançar novos clientes."
        ),
        "estrategias": {
            "FO": ["marca", "client", "influenci", "instagram", "live"],
            "FA": ["atend", "personal", "qualidad", "diferenci", "preco"],
            "WO": ["ecommerce", "marketplace", "estoque", "live", "influenci"],
            "WA": ["estoque", "desconto", "queima", "custo", "caixa"],
        },
    },
    {
        "empresa": "Sítio “Sabores do Agreste”",
        "contexto": (
            "Produtor familiar de geleias e polpas artesanais. A marca é bem "
            "avaliada, mas a produção ainda depende de vendas presenciais."
        ),
        "fatores": [
            ("Receitas próprias e ingredientes locais", "Força"),
            ("Produção limitada e pouco padronizada", "Fraqueza"),
            ("Feiras gastronômicas e turismo rural em crescimento", "Oportunidade"),
            ("Secas mais frequentes afetando a oferta de frutas", "Ameaça"),
            ("História familiar que gera conexão com o público", "Força"),
            ("Embalagens sem informação nutricional completa", "Fraqueza"),
            ("Venda para pousadas e cestas corporativas", "Oportunidade"),
            ("Aumento dos custos de embalagem e transporte", "Ameaça"),
        ],
        "pergunta_final": "Qual decisão ajuda o negócio a crescer com segurança?",
        "opcoes_final": [
            "Aceitar todos os pedidos sem limite, mesmo sem padronizar a produção",
            "Padronizar receitas e rótulos, testar vendas para pousadas e criar um calendário de safras",
            "Parar de vender polpas e produzir apenas o item mais barato",
            "Investir primeiro em uma fábrica grande financiada",
        ],
        "correta_final": 1,
        "justificativa_final": (
            "A opção fortalece a operação antes de escalar, aproveita canais "
            "promissores e reduz o risco de falta de matéria-prima."
        ),
        "estrategias": {
            "FO": ["receita", "local", "turismo", "feira", "historia"],
            "FA": ["safra", "fruta", "qualidad", "origem", "local"],
            "WO": ["rotulo", "padron", "pousada", "cesta", "corporativ"],
            "WA": ["embal", "transport", "safra", "calendario", "custo"],
        },
    },
    {
        "empresa": "Oficina “Rota 101”",
        "contexto": (
            "Oficina mecânica de bairro com boa reputação e equipe experiente. "
            "Novas oficinas e serviços móveis começaram a disputar os mesmos clientes."
        ),
        "fatores": [
            ("Mecânicos experientes e bem avaliados", "Força"),
            ("Agendamento feito apenas por telefone", "Fraqueza"),
            ("Crescimento da frota de motos na região", "Oportunidade"),
            ("Oficinas móveis com atendimento em domicílio", "Ameaça"),
            ("Diagnóstico transparente e orçamento explicado", "Força"),
            ("Pouca divulgação nas redes sociais", "Fraqueza"),
            ("Parceria com entregadores e pequenas frotas", "Oportunidade"),
            ("Peças paralelas de baixa qualidade mais baratas", "Ameaça"),
        ],
        "pergunta_final": "Como a oficina deve defender sua posição e crescer?",
        "opcoes_final": [
            "Reduzir todos os preços, inclusive sacrificando a margem",
            "Criar agendamento digital, plano de manutenção para frotas e comunicar a qualidade do diagnóstico",
            "Comprar muitos equipamentos caros antes de validar a procura",
            "Ignorar motos e concentrar esforços apenas nos carros",
        ],
        "correta_final": 1,
        "justificativa_final": (
            "A decisão transforma a reputação técnica em diferenciação, reduz "
            "o atrito do agendamento e aproveita o crescimento das motos e das frotas."
        ),
        "estrategias": {
            "FO": ["mecan", "diagnost", "moto", "frota", "manuten"],
            "FA": ["qualidad", "transparent", "peca", "segur", "diferenci"],
            "WO": ["agend", "digital", "redes", "parceria", "entreg"],
            "WA": ["peca", "qualidad", "domicil", "custo", "reput"],
        },
    },
]

SWOT_OPTIONS = ["Força", "Fraqueza", "Oportunidade", "Ameaça"]
MAX_SCORE = 190  # 80 (fase 1) + 40 (fase 2) + 50 (fase 3) + 20 (grupo)
RANKING_FILE = Path("data/ranking_swot.json")


# ---------------------------------------------------------------------------
# Funções puras: fáceis de validar e reutilizar
# ---------------------------------------------------------------------------

def normalize_text(value: str) -> str:
    """Remove acentos e deixa o texto mais fácil de comparar."""
    normalized = unicodedata.normalize("NFKD", value.lower())
    return "".join(char for char in normalized if not unicodedata.combining(char))


def evaluate_strategy(text: str, expected_terms: list[str]) -> tuple[int, list[str]]:
    """Avalia uma estratégia com uma rubrica simples e transparente (0 a 10)."""
    clean_text = normalize_text(text.strip())
    if len(clean_text) < 20:
        return 0, []

    matched = [term for term in expected_terms if normalize_text(term) in clean_text]
    score = 2  # há uma proposta legível
    if len(clean_text) >= 45:
        score += 2  # explicação mais desenvolvida
    score += min(6, len(matched) * 2)  # conexão com os fatores do case
    return min(score, 10), matched


def sort_ranking(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ordena por pontuação decrescente e, em empate, pelo menor tempo."""
    return sorted(
        records,
        key=lambda item: (
            -int(item.get("Pontos", 0)),
            float(item.get("Tempo (s)", 999999)),
            str(item.get("Data", "")),
        ),
    )


def load_ranking(path: Path = RANKING_FILE) -> list[dict[str, Any]]:
    """Lê o ranking salvo em JSON, sem quebrar o jogo no primeiro acesso."""
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, ValueError, TypeError):
        return []


def pdf_bytes(records: list[dict[str, Any]]) -> bytes:
    """Gera um PDF pronto para imprimir ou compartilhar com a turma."""
    output = io.BytesIO()
    records_sorted = sort_ranking(records)
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "SwotTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=22, leading=27, textColor=colors.HexColor("#172554"),
        alignment=TA_CENTER, spaceAfter=8,
    )
    subtitle = ParagraphStyle(
        "SwotSubtitle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9, leading=12, textColor=colors.HexColor("#475569"),
        alignment=TA_CENTER, spaceAfter=18,
    )
    body = ParagraphStyle(
        "SwotBody", parent=styles["Normal"], fontName="Helvetica",
        fontSize=8, leading=10, textColor=colors.HexColor("#172554"),
    )
    header = ParagraphStyle(
        "SwotHeader", parent=body, fontName="Helvetica-Bold",
        textColor=colors.white, alignment=TA_CENTER,
    )
    document = SimpleDocTemplate(
        output, pagesize=landscape(A4), rightMargin=1.2 * cm,
        leftMargin=1.2 * cm, topMargin=1.1 * cm, bottomMargin=1.1 * cm,
    )
    story: list[Any] = [
        Paragraph("DESAFIO SWOT", title),
        Paragraph(
            f"Ranking da turma · {datetime.now().astimezone().strftime('%d/%m/%Y %H:%M')} · "
            "pontuação máxima: 190 pontos",
            subtitle,
        ),
    ]
    if records_sorted:
        top = records_sorted[0]
        story.append(
            Paragraph(
                f"<b>Recorde atual:</b> {top.get('Participante', '—')} · "
                f"{top.get('Pontos', 0)} pontos · {top.get('Case', '—')}",
                body,
            )
        )
        story.append(Spacer(1, 0.35 * cm))
    table_data = [[
        Paragraph("Posição", header), Paragraph("Participante", header),
        Paragraph("Grupo / modo", header), Paragraph("Case", header),
        Paragraph("Pontos", header), Paragraph("Tempo", header),
    ]]
    for position, record in enumerate(records_sorted, 1):
        table_data.append([
            str(position),
            Paragraph(str(record.get("Participante", "—")), body),
            Paragraph(
                f"{record.get('Grupo', 'Individual')} · {record.get('Modalidade', '')}",
                body,
            ),
            Paragraph(str(record.get("Case", "—")), body),
            str(record.get("Pontos", 0)),
            f"{float(record.get('Tempo (s)', 0)):.1f}s",
        ])
    if len(table_data) == 1:
        table_data.append(["—", "Nenhuma partida registrada", "—", "—", "—", "—"])
    table = Table(table_data, colWidths=[1.6 * cm, 5.1 * cm, 5.3 * cm, 8.2 * cm, 2.5 * cm, 2.8 * cm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (4, 0), (5, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([table, Spacer(1, 0.45 * cm), Paragraph(
        "Uso em sala: cada aluno pode registrar sua pontuação; grupos podem defender suas estratégias da Fase 2 e receber até 20 pontos de votação da turma.",
        body,
    )])
    document.build(story)
    return output.getvalue()


def save_ranking(records: list[dict[str, Any]], path: Path = RANKING_FILE) -> None:
    """Persiste o ranking no disco para que ele sobreviva a novos acessos."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def reset_game() -> None:
    """Começa uma nova partida preservando o participante configurado."""
    st.session_state.case_atual = random.choice(CASES)
    st.session_state.fase = 1
    st.session_state.inicio = time.time()
    st.session_state.respostas_fase1 = {}
    st.session_state.resultado_fase1 = None
    st.session_state.resultado_fase2 = None
    st.session_state.decisao_final = None
    st.session_state.final_result = None
    st.session_state.resultado_registrado = False


# ---------------------------------------------------------------------------
# Estado e estilo
# ---------------------------------------------------------------------------

for key, default in {
    "game_started": False,
    "participante": "",
    "modalidade": "Individual",
    "grupo": "",
    "fase": 0,
    "case_atual": random.choice(CASES),
    "inicio": time.time(),
    "respostas_fase1": {},
    "resultado_fase1": None,
    "resultado_fase2": None,
    "decisao_final": None,
    "final_result": None,
    "resultado_registrado": False,
    "ranking_records": load_ranking(),
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown(
    """
    <style>
    .main-title { color: #172554; margin-bottom: 0; }
    .subtitle { color: #475569; margin-top: 0; }
    .phase-card {
        border: 1px solid #dbeafe; border-radius: 14px; padding: 18px;
        background: linear-gradient(135deg, #eff6ff, #ffffff);
        min-height: 145px;
    }
    .phase-number { color: #2563eb; font-weight: 800; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Barra lateral: configuração, progresso e ranking resumido
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("🎯 DESAFIO SWOT")
    st.caption("Você é o consultor. Salve o próximo negócio.")
    st.divider()

    if not st.session_state.game_started:
        st.subheader("Configuração")
        participante = st.text_input(
            "Nome do aluno ou grupo",
            key="participante_input",
            placeholder="Ex.: Rubem Alves ou Grupo A",
        )
        modalidade = st.radio(
            "Modo de jogo",
            ["Individual", "Em grupo"],
            key="modalidade_input",
        )
        grupo = ""
        if modalidade == "Em grupo":
            grupo = st.text_input(
                "Nome do grupo",
                key="grupo_input",
                placeholder="Ex.: Equipe Inovação",
            )
        iniciar = st.button(
            "🚀 Começar desafio",
            type="primary",
            use_container_width=True,
            disabled=not participante.strip() or (modalidade == "Em grupo" and not grupo.strip()),
        )
        if iniciar:
            st.session_state.participante = participante.strip()
            st.session_state.modalidade = modalidade
            st.session_state.grupo = grupo.strip() if modalidade == "Em grupo" else ""
            st.session_state.game_started = True
            reset_game()
            st.rerun()
    else:
        st.metric("Pontuação", st.session_state.final_result["total"] if st.session_state.final_result else (
            (st.session_state.resultado_fase1 or {}).get("pontos", 0)
            + (st.session_state.resultado_fase2 or {}).get("pontos", 0)
        ))
        fase_label = "Finalizado" if st.session_state.fase == 4 else f"{st.session_state.fase}/3"
        st.metric("Fase", fase_label)
        if st.session_state.fase < 4:
            tempo_atual = max(0, time.time() - st.session_state.inicio)
            st.metric("Tempo", f"{tempo_atual:.0f}s")
        st.caption(
            f"👤 {st.session_state.participante}"
            + (f" · {st.session_state.grupo}" if st.session_state.grupo else "")
        )
        st.divider()
        if st.button("🔄 Novo case / reiniciar", use_container_width=True):
            reset_game()
            st.rerun()

    if st.session_state.ranking_records:
        st.divider()
        st.subheader("🏅 Top 5")
        for position, record in enumerate(sort_ranking(st.session_state.ranking_records)[:5], 1):
            st.write(
                f"**{position}. {record.get('Participante', '—')}** — "
                f"{record.get('Pontos', 0)} pts"
            )


# ---------------------------------------------------------------------------
# Tela principal
# ---------------------------------------------------------------------------

st.markdown('<h1 class="main-title">DESAFIO SWOT</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Analise. Cruze. Decida. Transforme fatores em estratégia.</p>',
    unsafe_allow_html=True,
)

if not st.session_state.game_started:
    st.info("Configure sua partida na barra lateral para começar.")
    st.markdown("### O que você vai praticar")
    columns = st.columns(3)
    cards = [
        ("FASE 1 · CLASSIFICAÇÃO", "Identifique forças, fraquezas, oportunidades e ameaças."),
        ("FASE 2 · CRUZAMENTO", "Transforme a matriz SWOT em estratégias FO, FA, WO e WA."),
        ("FASE 3 · DECISÃO", "Escolha o caminho mais viável e defenda sua consultoria."),
    ]
    for column, (title, description) in zip(columns, cards):
        with column:
            st.markdown(
                f'<div class="phase-card"><div class="phase-number">{title}</div>'
                f"<p>{description}</p></div>",
                unsafe_allow_html=True,
            )
    st.markdown("### Como a pontuação funciona")
    st.write(
        "São até **190 pontos**: 80 na classificação, 40 nos cruzamentos, "
        "50 na decisão final e 20 pontos extras para grupos cuja estratégia "
        "for escolhida pela turma."
    )
    st.stop()

case = st.session_state.case_atual
st.header(f"Case: {case['empresa']}")
st.info(f"**Contexto:** {case['contexto']}")

if st.session_state.fase == 1:
    st.subheader("FASE 1 · Classificação SWOT — 10 pontos por acerto")
    st.write("Leia cada fator e classifique-o. O feedback aparece depois do envio.")
    with st.form("form_fase_1"):
        respostas: dict[int, str] = {}
        for index, (fator, _gabarito) in enumerate(case["fatores"]):
            respostas[index] = st.selectbox(
                f"{index + 1}. {fator}",
                ["Selecione"] + SWOT_OPTIONS,
                key=f"classificacao_{index}",
            )
        enviar_fase1 = st.form_submit_button("Finalizar Fase 1 ➡️", type="primary")

    if enviar_fase1:
        faltantes = [index + 1 for index, answer in respostas.items() if answer == "Selecione"]
        if faltantes:
            st.warning(f"Classifique todos os fatores antes de enviar. Faltam: {faltantes}.")
        else:
            acertos = sum(
                answer == case["fatores"][index][1]
                for index, answer in respostas.items()
            )
            st.session_state.respostas_fase1 = respostas
            st.session_state.resultado_fase1 = {
                "acertos": acertos,
                "pontos": acertos * 10,
                "gabarito": [gabarito for _, gabarito in case["fatores"]],
            }
            st.session_state.fase = 2
            st.toast(f"Fase 1 concluída: {acertos * 10}/80 pontos.")
            st.rerun()

elif st.session_state.fase == 2:
    fase1 = st.session_state.resultado_fase1
    st.subheader("FASE 2 · Cruzamento estratégico — até 40 pontos")
    st.write(
        "Crie uma estratégia para cada quadrante da matriz TOWS. "
        "Seja específico: cite fatores do case, público, canal ou ação."
    )
    st.success(f"Fase 1: **{fase1['acertos']}/8 acertos** · {fase1['pontos']}/80 pontos")

    prompts = {
        "FO": "Força + Oportunidade",
        "FA": "Força + Ameaça",
        "WO": "Fraqueza + Oportunidade",
        "WA": "Fraqueza + Ameaça",
    }
    with st.form("form_fase_2"):
        estrategias: dict[str, str] = {}
        for code, label in prompts.items():
            estrategias[code] = st.text_area(
                f"Estratégia {code} ({label})",
                placeholder=f"Ex.: Como usar os fatores do case para {label.lower()}...",
                height=95,
                key=f"estrategia_{code}",
            )
        enviar_fase2 = st.form_submit_button("Enviar estratégias ➡️", type="primary")

    if enviar_fase2:
        avaliacao: dict[str, dict[str, Any]] = {}
        total_fase2 = 0
        for code, text in estrategias.items():
            score, matched = evaluate_strategy(text, case["estrategias"][code])
            avaliacao[code] = {"pontos": score, "termos": matched, "texto": text.strip()}
            total_fase2 += score
        st.session_state.resultado_fase2 = {"pontos": total_fase2, "avaliacao": avaliacao}
        st.session_state.fase = 3
        st.toast(f"Fase 2 concluída: {total_fase2}/40 pontos.")
        st.rerun()

elif st.session_state.fase == 3:
    fase1 = st.session_state.resultado_fase1
    fase2 = st.session_state.resultado_fase2
    st.subheader("FASE 3 · Decisão do consultor — 50 pontos")
    st.write(case["pergunta_final"])
    st.success(
        f"Parcial: **{fase1['pontos'] + fase2['pontos']} pontos** "
        f"(Fase 1: {fase1['pontos']} · Fase 2: {fase2['pontos']})"
    )

    with st.form("form_fase_3"):
        decisao = st.radio("Sua decisão:", case["opcoes_final"])
        bonus_grupo = False
        if st.session_state.modalidade == "Em grupo":
            bonus_grupo = st.checkbox(
                "✅ A turma votou nesta estratégia na defesa do grupo (+20 pontos)",
                help="Marque somente após a apresentação e a votação da turma.",
            )
        finalizar = st.form_submit_button("Tomar decisão final 🏆", type="primary")

    if finalizar:
        decision_index = case["opcoes_final"].index(decisao)
        acertou = decision_index == case["correta_final"]
        pontos_fase3 = 50 if acertou else 0
        bonus = 20 if bonus_grupo else 0
        tempo_total = round(max(0, time.time() - st.session_state.inicio), 1)
        total = fase1["pontos"] + fase2["pontos"] + pontos_fase3 + bonus
        final_result = {
            "acertou": acertou,
            "decisao": decisao,
            "pontos_fase3": pontos_fase3,
            "bonus": bonus,
            "tempo": tempo_total,
            "total": total,
        }
        st.session_state.final_result = final_result
        st.session_state.decisao_final = decisao
        st.session_state.fase = 4

        ranking_record = {
            "Participante": st.session_state.participante,
            "Grupo": st.session_state.grupo or "—",
            "Modalidade": st.session_state.modalidade,
            "Case": case["empresa"],
            "Pontos": total,
            "Tempo (s)": tempo_total,
            "Data": datetime.now().astimezone().strftime("%d/%m/%Y %H:%M"),
            "Fase 1": fase1["pontos"],
            "Fase 2": fase2["pontos"],
            "Fase 3": pontos_fase3,
            "Bônus grupo": bonus,
            "Classificação": f"{fase1['acertos']}/8",
            "Estratégias": " | ".join(
                f"{code}: {item['pontos']}/10"
                for code, item in fase2["avaliacao"].items()
            ),
            "Decisão": decisao,
        }
        updated_records = st.session_state.ranking_records + [ranking_record]
        try:
            save_ranking(updated_records)
            st.session_state.ranking_records = updated_records
            st.session_state.resultado_registrado = True
        except (OSError, RuntimeError) as error:
            st.session_state.resultado_registrado = False
            st.warning(f"A partida terminou, mas não foi possível salvar o ranking: {error}")
        st.rerun()

else:
    result = st.session_state.final_result
    fase1 = st.session_state.resultado_fase1
    fase2 = st.session_state.resultado_fase2
    if result["acertou"]:
        st.balloons()
        st.success(
            f"🎉 DECISÃO CORRETA! Sua consultoria pontuou **{result['total']}/{MAX_SCORE}**."
        )
    else:
        st.error(
            f"A decisão não foi a melhor para este cenário. "
            f"Pontuação: **{result['total']}/{MAX_SCORE}**."
        )
    metrics = st.columns(4)
    metrics[0].metric("Pontuação final", f"{result['total']}/{MAX_SCORE}")
    metrics[1].metric("Classificação", f"{fase1['acertos']}/8")
    metrics[2].metric("Estratégias TOWS", f"{fase2['pontos']}/40")
    metrics[3].metric("Tempo", f"{result['tempo']:.1f}s")

    st.subheader("Feedback da consultoria")
    st.write(f"**Por que a decisão ideal era essa:** {case['justificativa_final']}")
    if not result["acertou"]:
        st.info(f"**Resposta recomendada:** {case['opcoes_final'][case['correta_final']]}")

    st.write("**Fase 2 — leitura da rubrica:**")
    for code, item in fase2["avaliacao"].items():
        matched_text = ", ".join(item["termos"]) if item["termos"] else "nenhum fator identificado automaticamente"
        st.write(f"- **{code}: {item['pontos']}/10** · conexões encontradas: {matched_text}")

    if result["bonus"]:
        st.success("Bônus de votação em grupo aplicado: +20 pontos.")
    if st.session_state.resultado_registrado:
        st.success("✅ Resultado salvo no ranking.")
    else:
        st.warning("O resultado está disponível, mas não foi salvo no ranking.")

    try:
        pdf_data = pdf_bytes(st.session_state.ranking_records)
        st.download_button(
            "⬇️ Baixar ranking completo em PDF",
            data=pdf_data,
            file_name="ranking_desafio_swot.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    except RuntimeError as error:
        st.error(str(error))

    st.divider()
    st.write("Quer tentar outro case? Use **Novo case / reiniciar** na barra lateral.")
