# -*- coding: utf-8 -*-
"""
Planner 2026/2027 — VARIANTE COLORIDA (versão de teste para impressão).
>>> NOVO: suporte fácil para FERIADOS DO RIO (municipais/estaduais) e
    RECESSOS/FÉRIAS ESCOLARES — edite as listas REGIONAL e SCHOOL abaixo.

Requisitos: reportlab   ->   pip install reportlab
Uso:
    python planner_color.py                       # A4 e A5, com
     Rio e escolar
    python planner_color.py --size A4
    python planner_color.py --no-rio              # sem feriados do Rio
    python planner_color.py --no-escolar          # sem recessos escolares
"""
import argparse
import calendar
import datetime
import math
from reportlab.lib.pagesizes import A4, A5
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# ---------------- paleta inspirada em Kandinsky ----------------
INK = colors.HexColor("#111111")
BLACK = colors.HexColor("#000000")
GREY = colors.HexColor("#6b6b6b")
LIGHT = colors.HexColor("#c9ced6")
FAINT = colors.HexColor("#e8ecf1")
PAPER = colors.HexColor("#f7f1e3")
WHITE = colors.white

K_YELLOW = colors.HexColor("#f2c300")
K_BLUE = colors.HexColor("#0057a3")
K_RED = colors.HexColor("#d7261e")
K_GREEN = colors.HexColor("#2e8b57")
K_ORANGE = colors.HexColor("#e67e22")
K_PURPLE = colors.HexColor("#6a3d9a")
K_TEAL = colors.HexColor("#1f7a8c")
DOTS = colors.HexColor("#8f98a6")

FINANCE_FILL = colors.HexColor("#eef5ff")
FINANCE_ROW_FILL = colors.HexColor("#f8fbff")
FINANCE_HEADER = colors.HexColor("#a7c7e7")
FINANCE_TOTAL = colors.HexColor("#d6e6f5")

Q_QV = K_BLUE
Q_PE = K_PURPLE
Q_PR = K_GREEN
Q_RE = K_ORANGE
ACC = K_BLUE
ACC2 = K_RED
FAC = K_YELLOW
REG = K_TEAL
SCHOOL_BG = colors.HexColor("#f6e27a")

PT_MONTHS = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

# ================= Weekday config / i18n =================
# Controla o primeiro dia da semana em TODOS os calendários/grades.
# Troque para calendar.MONDAY se quiser semana começando na segunda.
FIRST_WEEKDAY = calendar.SUNDAY

# Abreviações e nomes fixos pelo padrão do Python:
# calendar.weekday() => Monday=0 ... Sunday=6
WD_ABBR_MON0 = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"}
WD_FULL_MON0 = {
    0: "Segunda", 1: "Terça", 2: "Quarta", 3: "Quinta",
    4: "Sexta", 5: "Sábado", 6: "Domingo",
}

def wd_full_pt(year, month, day):
    """Nome do dia da semana em PT-BR para uma data (Mon=0..Sun=6)."""
    return WD_FULL_MON0[calendar.weekday(year, month, day)]


def weekday_headers(first_weekday=FIRST_WEEKDAY):
    """Lista de 7 abreviações ordenada pelo primeiro dia da semana configurado."""
    # calendar.SUNDAY == 6 e calendar.MONDAY == 0
    order = [(first_weekday + i) % 7 for i in range(7)]
    return [WD_ABBR_MON0[d] for d in order]


calendar.setfirstweekday(FIRST_WEEKDAY)

# ================= FERIADOS NACIONAIS (N) / FACULTATIVOS (F) =================
HOLIDAYS = {
    2026: [
        (1, 1, "Confraternização Universal", "N"),
        (2, 16, "Carnaval", "F"),
        (2, 17, "Carnaval", "N"),
        (2, 18, "Quarta-feira de Cinzas", "F"),
        (4, 3, "Sexta-feira Santa", "N"),
        (4, 21, "Tiradentes", "N"),
        (5, 1, "Dia do Trabalho", "N"),
        (6, 4, "Corpus Christi", "F"),
        (9, 7, "Independência do Brasil", "N"),
        (10, 12, "Nossa Senhora Aparecida", "N"),
        (11, 2, "Finados", "N"),
        (11, 15, "Proclamação da República", "N"),
        (11, 20, "Consciência Negra", "N"),
        (12, 25, "Natal", "N"),
    ],
    2027: [
        (1, 1, "Confraternização Universal", "N"),
        (2, 8, "Carnaval", "F"),
        (2, 9, "Carnaval", "N"),
        (2, 10, "Quarta-feira de Cinzas", "F"),
        (3, 26, "Sexta-feira Santa", "N"),
        (4, 21, "Tiradentes", "N"),
        (5, 1, "Dia do Trabalho", "N"),
        (5, 27, "Corpus Christi", "F"),
        (9, 7, "Independência do Brasil", "N"),
        (10, 12, "Nossa Senhora Aparecida", "N"),
        (11, 2, "Finados", "N"),
        (11, 15, "Proclamação da República", "N"),
        (11, 20, "Consciência Negra", "N"),
        (12, 25, "Natal", "N"),
    ],
}

# ================================================================
# CALENDÁRIO DA REDE MUNICIPAL — SME-RIO  (EDUCAÇÃO INFANTIL / CRECHE)
# ================================================================
# Base legal: Resolução SME nº 550, de 22/12/2025 (institui o Calendário
# Escolar 2026 da rede pública municipal do Rio — Educação Infantil, Ensino
# Fundamental e EJA). 200 dias letivos.
#
# ATENÇÃO — HONESTIDADE DE FONTE:
#   Os itens marcados [OK] têm data CONFIRMADA em fonte oficial/detalhada.
#   Os itens marcados [ANEXO] seguem a ESTRUTURA padrão da rede, mas a data
#   exata deve ser conferida no ANEXO ÚNICO da Res. SME 550/2025 (a tabela
#   completa não estava acessível). Edite livremente as listas abaixo.
#
# Formato:
#   SME_SINGLE[ano] = lista de (mês, dia, "rótulo", "tipo")
#   SME_RANGES[ano] = lista de (mês_i, dia_i, mês_f, dia_f, "rótulo", "tipo")
# Tipos: 'PLAN' planejamento/formação | 'LETIVO' marco letivo |
#        'RECESSO' recesso/não letivo  | 'REUNIAO' reunião de responsáveis |
#        'AVAL' censo/avaliação        | 'COMEMOR' data comemorativa

SME_SINGLE = {
    2026: [
        (2, 9,  "Início do ano letivo", "LETIVO"),                 # [OK]
        (5, 27, "Censo Escolar (últ. quarta de maio)", "AVAL"),    # [OK] Art. 6º
        (3, 28, "Reunião de Responsáveis (sábado)", "REUNIAO"),    # [ANEXO] preferenc. sábados
        (6, 20, "Reunião de Responsáveis (sábado)", "REUNIAO"),    # [ANEXO]
        (9, 12, "Reunião de Responsáveis (sábado)", "REUNIAO"),    # [ANEXO]
        (11, 21,"Reunião de Responsáveis (sábado)", "REUNIAO"),    # [ANEXO]
        (12, 22,"Término do ano letivo", "LETIVO"),                # [ANEXO] confira Anexo
    ],
    2027: [
        (2, 8,  "Início do ano letivo", "LETIVO"),                 # [ANEXO]
        (5, 26, "Censo Escolar (últ. quarta de maio)", "AVAL"),    # [ANEXO]
        (12, 22,"Término do ano letivo", "LETIVO"),                # [ANEXO]
    ],
}

SME_RANGES = {
    2026: [
        (2, 2, 2, 6,   "Planejamento e Formação Pedagógica", "PLAN"),   # [OK] 02–06/02
        (2, 13, 2, 17, "Semana do Carnaval Carioca", "COMEMOR"),        # [OK] atividades culturais
        (7, 13, 7, 24, "Recesso escolar de julho", "RECESSO"),          # [ANEXO] confira Anexo
        (12, 23, 12, 31, "Recesso / férias de fim de ano", "RECESSO"),  # [ANEXO]
    ],
    2027: [
        (2, 1, 2, 5,   "Planejamento e Formação Pedagógica", "PLAN"),   # [ANEXO]
        (7, 12, 7, 23, "Recesso escolar de julho", "RECESSO"),          # [ANEXO]
        (12, 23, 12, 31, "Recesso / férias de fim de ano", "RECESSO"),  # [ANEXO]
    ],
}

# Cores por tipo de evento SME (usadas nos marcadores e na legenda)
SME_COLORS = {
    "PLAN":    K_TEAL,
    "LETIVO":  K_BLUE,
    "RECESSO": SCHOOL_BG,
    "REUNIAO": K_PURPLE,
    "AVAL":    K_ORANGE,
    "COMEMOR": K_GREEN,
}
SME_LABELS = {
    "PLAN": "Planejamento/Formação", "LETIVO": "Marco letivo (início/término)",
    "RECESSO": "Recesso / não letivo", "REUNIAO": "Reunião de Responsáveis",
    "AVAL": "Censo/Avaliação", "COMEMOR": "Data comemorativa/cultural",
}

# Ligar/desligar a camada SME-Rio (creche)
INCLUDE_SME = True


def sme_events_sorted(year):
    """Lista unificada de eventos SME (single + início de ranges) ordenada."""
    ev = []
    for (m, d, lbl, tp) in SME_SINGLE.get(year, []):
        ev.append((m, d, None, None, lbl, tp))
    for (m1, d1, m2, d2, lbl, tp) in SME_RANGES.get(year, []):
        ev.append((m1, d1, m2, d2, lbl, tp))
    ev.sort(key=lambda e: (e[0], e[1]))
    return ev


def sme_day_types(year):
    """dict {(mes,dia): tipo} para marcar no mini-calendário.
    Ranges de RECESSO/PLAN preenchem todos os dias; single events marcam o dia."""
    out = {}
    for (m1, d1, m2, d2, _lbl, tp) in SME_RANGES.get(year, []):
        cur = datetime.date(year, m1, d1)
        end = datetime.date(year, m2, d2)
        while cur <= end:
            out[(cur.month, cur.day)] = tp
            cur += datetime.timedelta(days=1)
    for (m, d, _lbl, tp) in SME_SINGLE.get(year, []):
        out[(m, d)] = tp     # single sobrepõe para destacar o marco
    return out


def holiday_map(year, include_rio=True):
    """dict {(mes,dia): tipo} apenas dos FERIADOS (nacional/facultativo)."""
    return {(mo, d): t for (mo, d, _n, t) in HOLIDAYS[year]}


# Compat com assinatura antiga de build(): mantém o parâmetro include_school.
def school_day_set(year):
    """Compat: dias de RECESSO da rede SME (fundo amarelo no calendário)."""
    days = set()
    for (m1, d1, m2, d2, _lbl, tp) in SME_RANGES.get(year, []):
        if tp != "RECESSO":
            continue
        cur = datetime.date(year, m1, d1)
        end = datetime.date(year, m2, d2)
        while cur <= end:
            days.add((cur.month, cur.day))
            cur += datetime.timedelta(days=1)
    return days


def build(page_size, out_name, include_rio=True, include_school=True):
    W, H = page_size
    s = W / (210 * mm)
    M = 13 * mm * s
    c = canvas.Canvas(out_name, pagesize=page_size)

    def fs(x):
        return x * s

    # ---------- helpers ----------
    def text(x, y, ss, size=10, font="Helvetica", color=INK, align="l"):
        c.setFont(font, size); c.setFillColor(color)
        {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[align](x, y, ss)

    def rtext(x, y, ang, ss, size=10, font="Helvetica-Bold", color=INK, align="c"):
        c.saveState(); c.translate(x, y); c.rotate(ang)
        c.setFont(font, size); c.setFillColor(color)
        {"l": c.drawString, "c": c.drawCentredString, "r": c.drawRightString}[align](0, 0, ss)
        c.restoreState()

    def box(x, y, w, h, r=2.0 * mm, stroke=LIGHT, fill=None, lw=1.0):
        c.setLineWidth(lw); c.setStrokeColor(stroke)
        if fill:
            c.setFillColor(fill)
        c.roundRect(x, y, w, h, r * s, stroke=1 if stroke else 0, fill=1 if fill else 0)

    def bar(x, y, w, h, color, txt, tcolor=WHITE, size=9, align="c"):
        c.setFillColor(color); c.rect(x, y, w, h, stroke=0, fill=1)
        tx = x + w / 2 if align == "c" else x + 3 * mm * s
        if txt:
            text(tx, y + h / 2 - fs(size) * 0.35, txt, size=fs(size),
                 font="Helvetica-Bold", color=tcolor, align=align)

    def hline(x1, y, x2, color=FAINT, lw=0.8):
        c.setStrokeColor(color); c.setLineWidth(lw); c.line(x1, y, x2, y)

    def label(x, y, ss, size=8.5, color=ACC):
        text(x, y, ss.upper(), size=fs(size), font="Helvetica-Bold", color=color)

    def lines(x, y_top, w, n, gap, color=FAINT):
        for i in range(n):
            hline(x, y_top - i * gap, x + w, color=color)

    def dots(x0, y0, w, h, step):
        c.setFillColor(DOTS)
        for j in range(int(h // step) + 1):
            for i in range(int(w // step) + 1):
                c.circle(x0 + i * step, y0 + j * step, 0.5 * s, stroke=0, fill=1)

    def page_header(title, subtitle=None, color=ACC):
        c.setFillColor(color); c.rect(0, H - 4 * mm * s, W, 4 * mm * s, stroke=0, fill=1)
        text(M, H - M + 3 * mm * s, "PLANNER 2026/2027", size=fs(7.5),
             font="Helvetica-Bold", color=GREY)
        text(W - M, H - M + 3 * mm * s, "variante colorida", size=fs(7.5),
             color=GREY, align="r")
        if title:
            text(M, H - M - 6 * mm * s, title, size=fs(15), font="Helvetica-Bold", color=color)
        if subtitle:
            text(M, H - M - 12 * mm * s, subtitle, size=fs(9), color=GREY)
        return H - M - 20 * mm * s

    def footer(pg, color=ACC):
        hline(M, M - 3 * mm * s, W - M, color=LIGHT)
        c.setFillColor(color); c.circle(M + 1.2 * mm * s, M - 6 * mm * s + 1 * mm * s, 1.2 * mm * s, stroke=0, fill=1)
        text(M + 4 * mm * s, M - 7 * mm * s, "MyPlan • recriação funcional para avaliação pessoal",
             size=fs(7), color=GREY)
        text(W - M, M - 7 * mm * s, f"{pg}", size=fs(8), color=GREY, align="r")

    def mini_month(x, y, w, h, year, month, hol, school_days, sme_types=None):
        sme_types = sme_types or {}
        text(x + w / 2, y + h - 4 * mm * s, PT_MONTHS[month - 1], size=fs(8.5),
             font="Helvetica-Bold", color=ACC, align="c")
        top = y + h - 8.5 * mm * s
        cw = w / 7.0

        headers = weekday_headers(FIRST_WEEKDAY)
        sunday_col = (calendar.SUNDAY - FIRST_WEEKDAY) % 7
        for i, d in enumerate(headers):
            col = ACC2 if i == sunday_col else GREY
            text(x + cw * i + cw / 2, top, d[0], size=fs(5.6), color=col, align="c")
        weeks = calendar.monthcalendar(year, month)
        rh = (top - 3 * mm * s - y) / len(weeks)
        rad = min(cw, rh) * 0.42
        for r, week in enumerate(weeks):
            yy = top - 3 * mm * s - r * rh
            for i, day in enumerate(week):
                if day == 0:
                    continue
                cxp = x + cw * i + cw / 2
                cyp = yy - rh / 2
                # fundo de recesso SME (atrás de tudo)
                if (month, day) in school_days:
                    c.setFillColor(SCHOOL_BG)
                    c.roundRect(cxp - cw * 0.44, cyp - rh * 0.42, cw * 0.88, rh * 0.84,
                                0.6 * mm * s, stroke=0, fill=1)
                t = hol.get((month, day))
                col = INK
                if t == "N":
                    c.setFillColor(ACC2); c.circle(cxp, cyp + 0.9 * mm * s, rad, stroke=0, fill=1)
                    col = WHITE
                elif t == "F":
                    c.setStrokeColor(FAC); c.setLineWidth(0.9)
                    c.circle(cxp, cyp + 0.9 * mm * s, rad, stroke=1, fill=0)
                    col = colors.HexColor("#9a6b00")
                elif i == sunday_col:
                    col = ACC2
                text(cxp, cyp, str(day), size=fs(6), color=col,
                     font="Helvetica-Bold" if t else "Helvetica", align="c")
                # marcador de evento SME pontual (ponto no canto sup. dir.)
                st = sme_types.get((month, day))
                if st and st != "RECESSO" and t is None:
                    c.setFillColor(SME_COLORS.get(st, REG))
                    c.circle(cxp + cw * 0.30, cyp + rh * 0.30, 0.7 * mm * s, stroke=0, fill=1)

    # ========================================================
    # 1. CAPA (leve)
    # ========================================================
    c.setFillColor(Q_QV); c.rect(0, H - 10 * mm * s, W, 10 * mm * s, stroke=0, fill=1)
    c.setFillColor(Q_PE); c.rect(0, H - 12 * mm * s, W, 2 * mm * s, stroke=0, fill=1)
    c.setFillColor(Q_PR); c.rect(0, 10 * mm * s, W, 2 * mm * s, stroke=0, fill=1)
    c.setFillColor(Q_RE); c.rect(0, 0, W, 10 * mm * s, stroke=0, fill=1)
    text(W / 2, H * 0.66, "PLANNER", size=fs(46), font="Helvetica-Bold", color=Q_QV, align="c")
    text(W / 2, H * 0.60, "SEMANAL", size=fs(24), font="Helvetica", color=GREY, align="c")
    text(W / 2, H * 0.47, "2026", size=fs(70), font="Helvetica-Bold", color=Q_PE, align="c")
    text(W / 2, H * 0.415, "· 2 0 2 7 ·", size=fs(16), font="Helvetica-Bold", color=Q_PR, align="c")
    for i, col in enumerate([Q_QV, Q_PE, Q_PR, Q_RE]):
        c.setFillColor(col)
        c.circle(W / 2 - 12 * mm * s + i * 8 * mm * s, H * 0.37, 1.8 * mm * s, stroke=0, fill=1)
    text(W / 2, H * 0.30, "Organize sua semana • foque no que importa", size=fs(11), color=GREY, align="c")
    box(W / 2 - 55 * mm * s, H * 0.16, 110 * mm * s, 20 * mm * s, stroke=Q_QV, lw=1.2)
    text(W / 2, H * 0.16 + 13 * mm * s, "ESTE PLANNER PERTENCE A", size=fs(8.5),
         font="Helvetica-Bold", color=Q_QV, align="c")
    hline(W / 2 - 45 * mm * s, H * 0.16 + 5 * mm * s, W / 2 + 45 * mm * s, color=LIGHT, lw=0.8)
    text(W / 2, H * 0.055, "Versão de teste para avaliação de fluxo — imprima em A4/A5",
         size=fs(8), color=WHITE, align="c")
    c.showPage()

    # ========================================================
    # 2. COMO USAR
    # ========================================================
    y = page_header("Como usar este planner", "Um guia rápido de 1 minuto")
    steps = [
        ("1. Comece pelo topo", "Preencha a Roda da Vida e as Metas & Projetos uma vez.", Q_QV),
        ("2. Confira os feriados", "Nacionais, do Rio e recessos escolares — planeje pontes.", Q_PE),
        ("3. Abra cada mês", "Na Visão Mensal, registre os 3 focos e datas importantes.", Q_PR),
        ("4. Planeje a semana", "Defina até 3 prioridades, distribua tarefas e marque hábitos.", Q_RE),
        ("5. Feche o mês", "Preencha o Controle Financeiro e a Reflexão Mensal.", Q_QV),
    ]
    gap = (y - (M + 40 * mm * s)) / len(steps)
    for tt, dd, col in steps:
        c.setFillColor(col); c.circle(M + 1.5 * mm * s, y - 1 * mm * s, 1.6 * mm * s, stroke=0, fill=1)
        label(M + 6 * mm * s, y, tt, size=10, color=col)
        text(M + 6 * mm * s, y - 6 * mm * s, dd, size=fs(9), color=colors.HexColor("#444444"))
        y -= gap
    box(M, M + 2 * mm * s, W - 2 * M, 26 * mm * s, fill=FAINT, stroke=Q_QV, lw=1)
    label(M + 6 * mm * s, M + 21 * mm * s, "Dica de teste de fluxo", color=Q_QV)
    text(M + 6 * mm * s, M + 14 * mm * s, "Imprima 1 cópia de cada página e viva uma semana real com ela.",
         size=fs(9), color=colors.HexColor("#444444"))
    text(M + 6 * mm * s, M + 8 * mm * s, "Anote nas margens o que faltou ou sobrou — assim você compra a versão certa.",
         size=fs(9), color=colors.HexColor("#444444"))
    footer(2)
    c.showPage()

    # ========================================================
    # 3. DUAS CATEGORIAS: Feriados Nacionais | Calendário SME-Rio (creche)
    # ========================================================
    y = page_header("Feriados e calendário escolar",
                    "Categoria 1: Feriados nacionais  •  Categoria 2: Rede municipal SME-Rio (creche)",
                    color=ACC2)
    colw = (W - 2 * M - 8 * mm * s) / 2
    xL = M
    xR = M + colw + 8 * mm * s

    # ---------- COLUNA ESQUERDA: FERIADOS NACIONAIS (2026 e 2027) ----------
    bar(xL, y - 8 * mm * s, colw, 8 * mm * s, ACC2, "1 · FERIADOS NACIONAIS")
    yy = y - 8 * mm * s - 8 * mm * s
    for yr in [2026, 2027]:
        text(xL, yy, str(yr), size=fs(9), font="Helvetica-Bold", color=ACC)
        yy -= 5.5 * mm * s
        for (m, d, name, t) in sorted(HOLIDAYS[yr], key=lambda it: (it[0], it[1])):
            wd = wd_full_pt(yr, m, d)
            if t == "N":
                c.setFillColor(ACC2); c.circle(xL + 2 * mm * s, yy + 1 * mm * s, 1.4 * mm * s, stroke=0, fill=1)
            else:
                c.setStrokeColor(FAC); c.setLineWidth(1)
                c.circle(xL + 2 * mm * s, yy + 1 * mm * s, 1.4 * mm * s, stroke=1, fill=0)
            text(xL + 6 * mm * s, yy, f"{d:02d}/{m:02d}", size=fs(7.6), font="Helvetica-Bold", color=INK)
            text(xL + 17 * mm * s, yy, name, size=fs(7.6), color=colors.HexColor("#333333"))
            text(xL + colw - 1 * mm * s, yy, wd[:3], size=fs(7), color=GREY, align="r")
            hline(xL, yy - 2.2 * mm * s, xL + colw, color=FAINT)
            yy -= 5.6 * mm * s
        yy -= 2 * mm * s

    # ---------- COLUNA DIREITA: CALENDÁRIO SME-RIO (CRECHE) ----------
    bar(xR, y - 8 * mm * s, colw, 8 * mm * s, Q_PR, "2 · REDE MUNICIPAL SME-RIO · CRECHE")
    ry = y - 8 * mm * s - 8 * mm * s
    text(xR, ry, "Educação Infantil (creche) — Res. SME 550/2025", size=fs(6.8),
         color=GREY)
    ry -= 5.5 * mm * s
    for yr in [2026, 2027]:
        text(xR, ry, str(yr), size=fs(9), font="Helvetica-Bold", color=Q_PR)
        ry -= 5.5 * mm * s
        for (m1, d1, m2, d2, lbl, tp) in sme_events_sorted(yr):
            colr = SME_COLORS.get(tp, REG)
            if tp == "RECESSO":
                c.setFillColor(SCHOOL_BG)
                c.roundRect(xR + 0.7 * mm * s, ry - 0.3 * mm * s, 2.6 * mm * s, 2.6 * mm * s, 0.4 * mm * s, stroke=0, fill=1)
            else:
                c.setFillColor(colr); c.circle(xR + 2 * mm * s, ry + 1 * mm * s, 1.3 * mm * s, stroke=0, fill=1)
            if d2 is not None:
                dstr = f"{d1:02d}/{m1:02d}–{d2:02d}/{m2:02d}"
            else:
                dstr = f"{d1:02d}/{m1:02d}"
            text(xR + 6 * mm * s, ry, dstr, size=fs(7.2), font="Helvetica-Bold", color=INK)
            text(xR + 24 * mm * s, ry, lbl, size=fs(7.2), color=colors.HexColor("#333333"))
            hline(xR, ry - 2.1 * mm * s, xR + colw, color=FAINT)
            ry -= 5.5 * mm * s
        ry -= 2 * mm * s

    # ----- legenda (rodapé) -----
    ly = M + 9 * mm * s
    c.setFillColor(ACC2); c.circle(M + 2 * mm * s, ly + 1 * mm * s, 1.3 * mm * s, stroke=0, fill=1)
    text(M + 5.5 * mm * s, ly, "Feriado nacional", size=fs(7), color=INK)
    c.setStrokeColor(FAC); c.setLineWidth(1); c.circle(M + 42 * mm * s, ly + 1 * mm * s, 1.3 * mm * s, stroke=1, fill=0)
    text(M + 45.5 * mm * s, ly, "Ponto facultativo", size=fs(7), color=INK)
    # legenda SME por tipo — 3 colunas x 2 linhas, espaçamento fixo
    text(M, M + 6.4 * mm * s, "SME-Rio (creche):", size=fs(6.6), font="Helvetica-Bold", color=Q_PR)
    tps = ["PLAN", "LETIVO", "REUNIAO", "AVAL", "COMEMOR", "RECESSO"]
    colw_leg = (W - 2 * M) / 3
    for idx, tp in enumerate(tps):
        rr = idx // 3
        cc = idx % 3
        xleg = M + cc * colw_leg
        yleg = M + 2.8 * mm * s - rr * 3.4 * mm * s
        if tp == "RECESSO":
            c.setFillColor(SCHOOL_BG)
            c.roundRect(xleg, yleg - 0.3 * mm * s, 2.4 * mm * s, 2.4 * mm * s, 0.4 * mm * s, stroke=0, fill=1)
        else:
            c.setFillColor(SME_COLORS[tp]); c.circle(xleg + 1.2 * mm * s, yleg + 1 * mm * s, 1.2 * mm * s, stroke=0, fill=1)
        text(xleg + 4 * mm * s, yleg, SME_LABELS[tp], size=fs(6.3), color=INK)
    footer(3, color=ACC2)
    c.showPage()

    # ========================================================
    # 4 e 5. PLANEJAMENTO ANUAL (com feriados + Rio + escolar)
    # ========================================================
    for pg, yr in [(4, 2026), (5, 2027)]:
        sub = "Feriados nacionais"
        if include_school:
            sub += " + calendário SME-Rio (creche)"
        y = page_header(f"Planejamento anual {yr}", sub, color=ACC if yr == 2026 else Q_PE)
        hol = holiday_map(yr, include_rio)
        sdays = school_day_set(yr) if include_school else set()
        stypes = sme_day_types(yr) if include_school else {}
        cols, rows = 3, 4
        g = 5 * mm * s
        gw = (W - 2 * M - (cols - 1) * g) / cols
        gh = (y - M - (rows - 1) * g) / rows
        for m in range(12):
            r = m // cols; col = m % cols
            x = M + col * (gw + g)
            yy = y - gh - r * (gh + g)
            box(x, yy, gw, gh, stroke=LIGHT)
            mini_month(x, yy, gw, gh, yr, m + 1, hol, sdays, stypes)
        footer(pg, color=ACC if yr == 2026 else Q_PE)
        c.showPage()

    # ========================================================
    # 6. RODA DA VIDA
    # ========================================================
    page_header("Roda da vida", None, color=ACC)
    text(M, H - M - 12 * mm * s, "1. Preencha o nível de satisfação (0 no centro, 10 na borda) para cada área.",
         size=fs(8.5), color=colors.HexColor("#444444"))
    cx, cy = W / 2, H / 2 + 8 * mm * s
    R = min(W, H) * 0.285
    areas = [
        ("Saúde e disposição", Q_PE), ("Desenv. intelectual", Q_PE), ("Equilíbrio emocional", Q_PE),
        ("Realização e propósito", Q_PR), ("Recursos financeiros", Q_PR), ("Contribuição social", Q_PR),
        ("Família", Q_RE), ("Vida social", Q_RE), ("Relacion. amoroso", Q_RE),
        ("Hobbies e diversão", Q_QV), ("Plenitude e felicidade", Q_QV), ("Espiritualidade", Q_QV),
    ]
    c.setStrokeColor(LIGHT); c.setLineWidth(0.7)
    for k in range(1, 11):
        c.circle(cx, cy, R * k / 10, stroke=1, fill=0)
    for i, (name, col) in enumerate(areas):
        deg = 90 - i * 30
        center = math.radians(deg)
        bnd = math.radians(deg - 15)
        c.setStrokeColor(LIGHT); c.setLineWidth(0.7)
        c.line(cx, cy, cx + R * math.cos(bnd), cy + R * math.sin(bnd))
        for k in range(1, 11):
            rr = R * (k - 0.5) / 10
            text(cx + rr * math.cos(center), cy + rr * math.sin(center) - fs(6) * 0.35,
                 str(k), size=fs(6.6), color=col, align="c")
        r0 = R + 5 * mm * s
        if math.cos(center) >= 0:
            rot, al, xa = deg, "l", r0
        else:
            rot, al, xa = deg + 180, "r", -r0
        rtext(cx + r0 * math.cos(center), cy + r0 * math.sin(center), rot, name,
              size=fs(8.6), font="Helvetica-Bold", color=col, align=al)
    c.setFillColor(WHITE); c.circle(cx, cy, R * 0.05, stroke=0, fill=1)
    quad = [("Pessoal", 45, Q_PE), ("Profissional", -45, Q_PR),
            ("Relacionamentos", 225, Q_RE), ("Qualidade de vida", 135, Q_QV)]
    for name, deg, col in quad:
        a = math.radians(deg)
        rr = R + 32 * mm * s
        rot = deg if math.cos(a) >= 0 else deg + 180
        rtext(cx + rr * math.cos(a), cy + rr * math.sin(a), rot, name.upper(),
              size=fs(13), font="Helvetica-Bold", color=col, align="c")
    text(M, M + 10 * mm * s,
         "2. Ligue os pontos para enxergar o equilíbrio. Onde a nota é baixa, escreva 1 ação de melhoria:",
         size=fs(8.5), color=colors.HexColor("#444444"))
    lines(M, M + 5 * mm * s, W - 2 * M, 2, gap=6 * mm * s, color=LIGHT)
    footer(6)
    c.showPage()

    # ========================================================
    # 7. METAS E PROJETOS FUTUROS
    # ========================================================
    y = page_header("Metas e projetos futuros", "Relacionados a cada área da sua vida")
    g = 6 * mm * s
    bw = (W - 2 * M - g) / 2
    bh = (y - M - g) / 2
    quads = [("Qualidade de vida", Q_QV), ("Pessoal", Q_PE),
             ("Relacionamentos", Q_RE), ("Profissional", Q_PR)]
    for i, (name, col) in enumerate(quads):
        r = i // 2; cc = i % 2
        x = M + cc * (bw + g)
        yy = y - bh - r * (bh + g)
        box(x, yy, bw, bh, stroke=col, lw=1)
        bar(x, yy + bh - 8 * mm * s, bw, 8 * mm * s, col, name.upper())
        n = int((bh - 12 * mm * s) // (7 * mm * s))
        lines(x + 4 * mm * s, yy + bh - 14 * mm * s, bw - 8 * mm * s, n, gap=7 * mm * s, color=FAINT)
    footer(7)
    c.showPage()

    # ========================================================
    # 8. VISÃO MENSAL
    # ========================================================
    # Esta página é um TEMPLATE: imprime uma grade mensal vazia (preencher à mão).
    # A grade precisa respeitar FIRST_WEEKDAY (domingo/segunda).
    y = page_header("Visão mensal", "Mês: __________________________", color=Q_PR)

    cal_w = W - 2 * M
    cal_h = (y - M) * 0.66
    box(M, y - cal_h, cal_w, cal_h, stroke=LIGHT)

    cw = cal_w / 7.0
    hh = 8 * mm * s

    headers = weekday_headers(FIRST_WEEKDAY)
    sun_col = (calendar.SUNDAY - FIRST_WEEKDAY) % 7
    sat_col = (calendar.SATURDAY - FIRST_WEEKDAY) % 7

    for i, d in enumerate(headers):
        is_weekend = i in (sat_col, sun_col)
        c.setFillColor(colors.HexColor("#eaf3ee") if is_weekend else Q_PR)
        c.rect(M + i * cw, y - hh, cw, hh, stroke=0, fill=1)
        text(M + i * cw + cw / 2, y - hh + 2.5 * mm * s, d, size=fs(8),
             font="Helvetica-Bold", color=Q_PR if is_weekend else WHITE, align="c")

    # Corpo: 6 linhas (semanas) x 7 colunas
    rh = (cal_h - hh) / 6
    c.setStrokeColor(FAINT); c.setLineWidth(0.6)

    # linhas horizontais (entre as 6 semanas)
    for r in range(1, 6):
        c.line(M, y - hh - r * rh, M + cal_w, y - hh - r * rh)

    # linhas verticais (entre os 7 dias) — desenhar de cima (abaixo do header) até o fundo
    for i in range(1, 7):
        c.line(M + i * cw, y - hh, M + i * cw, y - cal_h)
    by = y - cal_h - 6 * mm * s
    bh2 = by - (M + 2 * mm * s)
    half = (cal_w - 6 * mm * s) / 2
    box(M, by - bh2, half, bh2, stroke=Q_PR, lw=1)
    bar(M, by - 8 * mm * s, half, 8 * mm * s, Q_PR, "3 FOCOS + METAS DO MÊS")
    for i in range(3):
        yy = by - 15 * mm * s - i * 7 * mm * s
        c.setStrokeColor(Q_PR); c.setLineWidth(1)
        c.rect(M + 5 * mm * s, yy - 1 * mm * s, 3.2 * mm * s, 3.2 * mm * s, stroke=1, fill=0)
        hline(M + 11 * mm * s, yy - 1 * mm * s, M + half - 5 * mm * s, color=LIGHT)
    nm = int((bh2 - 40 * mm * s) // (7 * mm * s))
    lines(M + 5 * mm * s, by - 40 * mm * s, half - 10 * mm * s, max(1, nm), gap=7 * mm * s, color=FAINT)
    box(M + half + 6 * mm * s, by - bh2, half, bh2, stroke=Q_PR, lw=1)
    bar(M + half + 6 * mm * s, by - 8 * mm * s, half, 8 * mm * s, Q_PR, "DATAS IMPORTANTES")
    nd = int((bh2 - 12 * mm * s) // (7.5 * mm * s))
    lines(M + half + 11 * mm * s, by - 14 * mm * s, half - 10 * mm * s, max(1, nd), gap=7.5 * mm * s, color=FAINT)
    footer(8, color=Q_PR)
    c.showPage()

    # ========================================================
    # 9. SEMANAL A
    # ========================================================
    y = page_header("Semana de ____ / ____  a  ____ / ____", "Foque no que faz diferença", color=Q_RE)
    bottom = M + 2 * mm * s
    colw = (W - 2 * M - 6 * mm * s) / 2
    total_h = y - bottom
    pri_h = total_h * 0.26
    box(M, y - pri_h, colw, pri_h, stroke=Q_RE, lw=1)
    bar(M, y - 8 * mm * s, colw, 8 * mm * s, Q_RE, "TOP 3 PRIORIDADES DA SEMANA")
    pg = (pri_h - 12 * mm * s) / 3
    for i in range(3):
        yy = y - 14 * mm * s - i * pg
        c.setStrokeColor(Q_RE); c.setLineWidth(1)
        c.rect(M + 5 * mm * s, yy - 2 * mm * s, 3.4 * mm * s, 3.4 * mm * s, stroke=1, fill=0)
        hline(M + 11 * mm * s, yy - 2 * mm * s, M + colw - 5 * mm * s, color=LIGHT)
    t_top = y - pri_h - 6 * mm * s
    t_h = t_top - bottom
    box(M, bottom, colw, t_h, stroke=Q_RE, lw=1)
    bar(M, t_top - 8 * mm * s, colw, 8 * mm * s, Q_RE, "LISTA DE TAREFAS")
    nt = max(1, int((t_h - 12 * mm * s) // (7.2 * mm * s)))
    for i in range(nt):
        yy = t_top - 14 * mm * s - i * 7.2 * mm * s
        c.setStrokeColor(GREY); c.setLineWidth(0.8)
        c.rect(M + 5 * mm * s, yy - 2 * mm * s, 3 * mm * s, 3 * mm * s, stroke=1, fill=0)
        hline(M + 11 * mm * s, yy - 2 * mm * s, M + colw - 5 * mm * s, color=FAINT)
    rx = M + colw + 6 * mm * s
    hab_h = total_h * 0.60
    box(rx, y - hab_h, colw, hab_h, stroke=Q_RE, lw=1)
    bar(rx, y - 8 * mm * s, colw, 8 * mm * s, Q_RE, "CONTROLE DE ATIVIDADES / HÁBITOS")
    gx = rx + 5 * mm * s; gy = y - 13 * mm * s
    labcol = 30 * mm * s
    dcw = (colw - 10 * mm * s - labcol) / 7
    headers = weekday_headers(FIRST_WEEKDAY)
    for i, d in enumerate(headers):
        text(gx + labcol + dcw * i + dcw / 2, gy, d[0], size=fs(6.5), color=GREY, align="c")
    nh = 8
    hg = (hab_h - 18 * mm * s) / nh
    for r in range(nh):
        ry = gy - 7 * mm * s - r * hg
        hline(gx, ry + hg * 0.62, rx + colw - 5 * mm * s, color=FAINT)
        text(gx, ry, "____________", size=fs(8), color=GREY)
        for i in range(7):
            c.setStrokeColor(Q_RE); c.setLineWidth(0.7)
            c.circle(gx + labcol + dcw * i + dcw / 2, ry + 1 * mm * s, 2.2 * s, stroke=1, fill=0)
    n_top = y - hab_h - 6 * mm * s
    n_h = n_top - bottom
    box(rx, bottom, colw, n_h, stroke=Q_RE, lw=1)
    bar(rx, n_top - 8 * mm * s, colw, 8 * mm * s, Q_RE, "NOTAS & IDEIAS")
    nn = max(1, int((n_h - 12 * mm * s) // (7.2 * mm * s)))
    lines(rx + 5 * mm * s, n_top - 14 * mm * s, colw - 10 * mm * s, nn, gap=7.2 * mm * s, color=FAINT)
    footer(9, color=Q_RE)
    c.showPage()

    # ========================================================
    # 10. SEMANAL B (grade de horários)
    # ========================================================
    y = page_header("Grade de horários da semana", "Encaixe compromissos e blocos de foco", color=Q_RE)
    grid_h = y - M - 2 * mm * s
    tcol = 15 * mm * s
    dayw = (W - 2 * M - tcol) / 7
    hh = 8 * mm * s
    c.setFillColor(Q_RE); c.rect(M, y - hh, W - 2 * M, hh, stroke=0, fill=1)
    headers = weekday_headers(FIRST_WEEKDAY)
    for i, d in enumerate(headers):
        text(M + tcol + dayw * i + dayw / 2, y - hh + 2.5 * mm * s, d, size=fs(8),
             font="Helvetica-Bold", color=WHITE, align="c")
    hours = list(range(6, 23))
    bt = y - hh
    rh = (grid_h - hh) / len(hours)
    c.setStrokeColor(FAINT); c.setLineWidth(0.6)
    for r, hr in enumerate(hours):
        yy = bt - r * rh
        c.line(M, yy, W - M, yy)
        text(M + 2.5 * mm * s, yy - rh / 2 - 1, f"{hr:02d}h", size=fs(7), color=GREY)
    c.line(M, bt - len(hours) * rh, W - M, bt - len(hours) * rh)
    c.setStrokeColor(LIGHT); c.setLineWidth(0.8)
    for i in range(8):
        xx = M + tcol + i * dayw
        c.line(xx, y - hh, xx, bt - len(hours) * rh)
    c.line(M, y - hh, M, bt - len(hours) * rh)
    footer(10, color=Q_RE)
    c.showPage()

    # ========================================================
    # 11. CONTROLE FINANCEIRO
    # ========================================================
    page_header("", None, color=Q_PR)
    top = H - M - 2 * mm * s
    bar(M, top - 8 * mm * s, W - 2 * M, 8 * mm * s, FINANCE_HEADER,
        "CONTROLE FINANCEIRO — MÊS: ____________", tcolor=INK)
    cur = top - 8 * mm * s

    def money_grid(x, w, cols_spec, nrows, rowh, header_color, header_txt):
        bh_ = 6.5 * mm * s
        bar(x, cur - bh_, w, bh_, header_color, header_txt)
        ch = 5 * mm * s
        c.setFillColor(FINANCE_FILL); c.rect(x, cur - bh_ - ch, w, ch, stroke=0, fill=1)
        xx = x
        for cname, cw_ in cols_spec:
            text(xx + 2 * mm * s, cur - bh_ - ch + 1.4 * mm * s, cname,
                 size=fs(6.5), font="Helvetica-Bold", color=GREY)
            xx += cw_
        gy0 = cur - bh_ - ch
        for r in range(nrows):
            if r % 2 == 0:
                c.setFillColor(FINANCE_ROW_FILL)
                c.rect(x, gy0 - (r + 1) * rowh, w, rowh, stroke=0, fill=1)
        c.setStrokeColor(FAINT); c.setLineWidth(0.7)
        for r in range(nrows + 1):
            c.line(x, gy0 - r * rowh, x + w, gy0 - r * rowh)
        xx = x; c.setStrokeColor(LIGHT); c.setLineWidth(0.8)
        for cname, cw_ in cols_spec[:-1]:
            xx += cw_
            c.line(xx, gy0 - nrows * rowh, xx, gy0)
        box(x, gy0 - nrows * rowh, w, bh_ + ch + nrows * rowh, r=1.2 * mm, stroke=LIGHT, lw=1.1)
        return gy0 - nrows * rowh

    gcol = 6 * mm * s
    cw2 = (W - 2 * M - gcol) / 2
    rowh = 6.2 * mm * s
    nrows_top = 11
    ent_cols = [("DATA", cw2 * 0.22), ("DESCRIÇÃO", cw2 * 0.55), ("VALOR", cw2 * 0.23)]
    b1 = money_grid(M, cw2, ent_cols, nrows_top, rowh, Q_PR, "ENTRADAS")
    money_grid(M + cw2 + gcol, cw2, ent_cols, nrows_top, rowh, Q_PE, "PARCELAMENTOS / RECORRENTES")
    for xb in [M, M + cw2 + gcol]:
        ty = b1 - 6 * mm * s
        bar(xb, ty, cw2, 6 * mm * s, FINANCE_TOTAL, "")
        text(xb + cw2 * 0.55, ty + 1.7 * mm * s, "TOTAL", size=fs(7),
             font="Helvetica-Bold", color=INK, align="r")
        box(xb + cw2 * 0.80, ty + 1 * mm * s, cw2 * 0.18, 4 * mm * s, r=0.6 * mm, stroke=INK, lw=0.8)
    cur = b1 - 6 * mm * s - 5 * mm * s
    sai_cols = [("DATA", (W - 2 * M) * 0.13), ("DESCRIÇÃO", (W - 2 * M) * 0.72), ("VALOR", (W - 2 * M) * 0.15)]
    saldo_h = 16 * mm * s
    avail = cur - (M + saldo_h + 4 * mm * s) - (6.5 + 5) * mm * s - 6 * mm * s
    nrows_sai = max(6, int(avail // rowh))
    bS = money_grid(M, W - 2 * M, sai_cols, nrows_sai, rowh, Q_RE, "SAÍDAS")
    tyS = bS - 6 * mm * s
    bar(M, tyS, W - 2 * M, 6 * mm * s, FINANCE_TOTAL, "")
    text(M + (W - 2 * M) * 0.85, tyS + 1.7 * mm * s, "TOTAL", size=fs(7),
         font="Helvetica-Bold", color=INK, align="r")
    box(M + (W - 2 * M) * 0.86, tyS + 1 * mm * s, (W - 2 * M) * 0.13, 4 * mm * s, r=0.6 * mm, stroke=INK, lw=0.8)
    sy = M + 2 * mm * s
    fields = [("ENTRADAS", Q_PR, "−"), ("PARC./RECOR.", Q_PE, "−"),
              ("SAÍDAS", Q_RE, "="), ("SALDO FINAL", FINANCE_HEADER, "")]
    fw = (W - 2 * M - 3 * 8 * mm * s) / 4
    fx = M
    for name, col, op in fields:
        label(fx, sy + 10 * mm * s, name, size=7, color=col)
        box(fx, sy, fw, 8 * mm * s, r=1 * mm, stroke=col, lw=1.1)
        if op:
            text(fx + fw + 4 * mm * s, sy + 2.4 * mm * s, op, size=fs(13),
                 font="Helvetica-Bold", color=GREY, align="c")
        fx += fw + 8 * mm * s
    footer(11, color=Q_PR)
    c.showPage()

    # ========================================================
    # 12. REFLEXÃO MENSAL
    # ========================================================
    y = page_header("Reflexão mensal", "Feche o mês com clareza", color=Q_PE)
    qs = ["O que funcionou bem este mês?", "O que travou ou consumiu energia à toa?",
          "Qual hábito quero manter no próximo mês?", "Qual foi minha maior conquista?",
          "O que vou ajustar no próximo ciclo?"]
    block = (y - M - 16 * mm * s) / len(qs)
    yy = y
    for q in qs:
        label(M, yy, q, size=9.5, color=Q_PE)
        nl = max(1, int((block - 8 * mm * s) // (7 * mm * s)))
        lines(M, yy - 8 * mm * s, W - 2 * M, nl, gap=7 * mm * s, color=FAINT)
        yy -= block
    label(M, yy, "Nota do mês (0 a 10)", color=Q_PE)
    step = (W - 2 * M - 16 * mm * s) / 10
    for i in range(11):
        c.setStrokeColor(Q_PE); c.setLineWidth(0.9)
        c.circle(M + 8 * mm * s + i * step, yy - 9 * mm * s, 4 * s, stroke=1, fill=0)
        text(M + 8 * mm * s + i * step, yy - 10.3 * mm * s, str(i), size=fs(7), color=GREY, align="c")
    footer(12, color=Q_PE)
    c.showPage()

    # ========================================================
    # 13. PÁGINA PAUTADA
    # ========================================================
    y = page_header("Anotações", "Página pautada", color=Q_QV)
    nl = int((y - M) // (8 * mm * s))
    lines(M, y, W - 2 * M, nl, gap=8 * mm * s, color=LIGHT)
    footer(13)
    c.showPage()

    # ========================================================
    # 14. PÁGINA PONTILHADA
    # ========================================================
    y = page_header("Anotações", "Página pontilhada", color=Q_QV)
    dots(M, M, W - 2 * M, y - M, step=6 * mm * s)
    footer(14)
    c.showPage()

    c.save()
    print(f"PDF gerado: {out_name} (14 páginas).")


SIZES = {"A4": A4, "A5": A5}


def main():
    ap = argparse.ArgumentParser(description="Planner colorido 2026/2027 (A4/A5).")
    ap.add_argument("--size", choices=["A4", "A5", "both"], default="both")
    ap.add_argument("--rio", dest="rio", action="store_true", help="incluir feriados do Rio (padrão)")
    ap.add_argument("--no-rio", dest="rio", action="store_false", help="não incluir feriados do Rio")
    ap.add_argument("--escolar", dest="escolar", action="store_true", help="incluir recessos escolares (padrão)")
    ap.add_argument("--no-escolar", dest="escolar", action="store_false", help="não incluir recessos escolares")
    ap.set_defaults(rio=INCLUDE_RIO, escolar=INCLUDE_SCHOOL)
    args = ap.parse_args()
    for sz in (["A4", "A5"] if args.size == "both" else [args.size]):
        build(SIZES[sz], f"planner_colorido_2026_2027_{sz}.pdf",
              include_rio=args.rio, include_school=args.escolar)


# Ligue/desligue por padrão aqui (ou use --no-rio / --no-escolar):
INCLUDE_RIO = True
INCLUDE_SCHOOL = True

if __name__ == "__main__":
    main()
