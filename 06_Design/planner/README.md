# Planner 2026/2027 — VARIANTE COLORIDA (Versão de Teste)

Recriação **funcional e não oficial** inspirada na estrutura do *Planner da MyPlan* (usemyplan.com.br), com **capa leve**. Para **imprimir e avaliar o fluxo** antes de
comprar a versão física.

> ⚠️ Uso **pessoal de avaliação**. Não é produto oficial da MyPlan.

---

## 📦 Conteúdo
| Arquivo | Descrição | 
|---|---|
| `planner_colorido_2026_2027_A4.pdf` | 14 páginas, **A4** (210 × 297 mm). |
| `planner_colorido_2026_2027_A5.pdf` | 14 páginas, **A5** (148 × 210 mm). |
| `planner_color.py` | Código-fonte (Python + reportlab). |
| `README.md` | Este arquivo. |

---

## ✅ Calendrário com duas categorias de datas

A página 3 (**Feriados e calendário escolar**) foi organizada em **duas categorias**, e ambas aparecem também nos **calendários anuais (págs. 4 e 5)**:

### 1 · Feriados NACIONAIS
Lista `HOLIDAYS` no código. Marcador: 🔴 nacional · ⭕ ponto facultativo.

### 2 · Rede municipal SME-Rio — EDUCAÇÃO INFANTIL / CRECHE
**Todos os eventos** da rede (não só feriados): planejamento, início/término, reuniões de responsáveis, censo, recessos, atividades culturais.
Base legal: **Resolução SME nº 550, de 22/12/2025** (200 dias letivos).

Marcadores por tipo:
- 🟢 **Planejamento/Formação** (`PLAN`)
- 🔵 **Marco letivo** — início/término (`LETIVO`)
- 🟣 **Reunião de Responsáveis** (`REUNIAO`)
- 🟠 **Censo/Avaliação** (`AVAL`)
- 🟩 **Data comemorativa/cultural** (`COMEMOR`)
- 🟨 **Recesso / não letivo** — fundo amarelo (`RECESSO`)


👉 Confira/edite tudo nas listas **`SME_SINGLE`** e **`SME_RANGES`** no topo do
`planner_color.py`. É só trocar as datas pelas do Anexo e regerar.


#### ✏️ Como editar o calendário da creche

```python
# Eventos de UM dia:  (mês, dia, "rótulo", "tipo")
SME_SINGLE = {
    2026: [
        (2, 9,  "Início do ano letivo", "LETIVO"),
        (5, 27, "Censo Escolar", "AVAL"),
        (3, 28, "Reunião de Responsáveis (sábado)", "REUNIAO"),
        (12, 22,"Término do ano letivo", "LETIVO"),
        # ... adicione quantos quiser
    ],
    2027: [ ... ],
}

# Eventos de VÁRIOS dias: (mês_i, dia_i, mês_f, dia_f, "rótulo", "tipo")
SME_RANGES = {
    2026: [
        (2, 2, 2, 6,   "Planejamento e Formação Pedagógica", "PLAN"),
        (7, 13, 7, 24, "Recesso escolar de julho", "RECESSO"),
        (12, 23, 12, 31,"Recesso / férias de fim de ano", "RECESSO"),
    ],
    2027: [ ... ],
}
```
Tipos válidos: `PLAN`, `LETIVO`, `RECESSO`, `REUNIAO`, `AVAL`, `COMEMOR`.

**Ligar/desligar a camada SME:** constante `INCLUDE_SME = True/False`
(ou `python planner_color.py --no-escolar`).

---

## 📄 Índice das 14 páginas
1. Capa
2. Como usar
3. **Feriados nacionais + Calendário SME-Rio (creche)**
4. Anual **2026**
5. Anual **2027**
6. Roda da Vida
7. Metas e Projetos
8. Visão Mensal
9. Semana (planejamento)
10. Semana (horários) ·
11. Controle Financeiro
12. Reflexão Mensal
13. Pautada
14. Pontilhada.

---

## 🖨️ Impressão
- **A4:** 100% / "Tamanho real".
- **A5:** papel A5 a 100%, **ou** 2 páginas por folha A4 (2-up).

## 🛠️ Regerar
```bash
pip install reportlab
python planner_color.py            # A4 e A5
python planner_color.py --size A4
python planner_color.py --no-escolar   # sem a camada SME-Rio
```

---

## 📚 Fontes
- **Feriados nacionais 2026/2027** (incl. móveis: Sexta-feira Santa, Corpus Christi, Carnaval).
- **Calendário SME-Rio 2026 (Educação Infantil/creche):** Resolução SME nº 550/2025
  — Semana de Planejamento 02–06/02, início 09/02, Censo 27/05 (últ. quarta de maio),
  200 dias letivos. Datas [ANEXO] a confirmar no Anexo Único.