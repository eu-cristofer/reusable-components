# Planner 2026/2027 — VARIANTE COLORIDA (Versão de Teste)

---

## 📦 Conteúdo
| Arquivo | Descrição | 
|---|---|
| `planner_color.py` | Código-fonte principal (Python + reportlab). |
| `README.md` | Este arquivo. |
| `refactory.md` | Plano de refatoração em sprints para separar os booklets. |

> Os PDFs gerados dependem do modo de execução e do tamanho escolhido.

---

## ✅ Fluxo real de uso
O objetivo deste planner é funcionar em **três cadernos independentes**, cada um com um papel diferente no planejamento:

### 1 · Yearly booklet
Para imprimir **uma vez por ano**.

Uso esperado:
- visão do ano
- feriados e calendário escolar
- planejamento anual
- roda da vida
- metas e projetos

### 2 · Monthly booklet
Para imprimir **um novo exemplar a cada mês**.

Uso esperado:
- visão mensal
- focos e metas do mês
- datas importantes
- controle financeiro
- reflexão mensal

### 3 · Weekly booklet
Para imprimir **sempre que precisar**.

Uso esperado:
- prioridades da semana
- hábitos
- grade horária
- notas e ideias

---

## 🖨️ Impressão recomendada
Os arquivos devem ser gerados em **A4** e impressos em:

- **A3 frente e verso**
- modo **booklet / livreto**
- dobrado ao meio, formando páginas A4

### Regra importante de composição
Cada booklet deve respeitar este fluxo físico:

- **frente da primeira folha** = capa do booklet
- **verso da primeira folha** = página de referência principal daquele booklet

Ou seja:

- **Yearly:** no verso da primeira folha devem estar o **calendário anual + feriados/calendário escolar**
- **Monthly:** no verso da primeira folha deve estar a **referência do mês**
- **Weekly:** no verso da primeira folha deve estar a **referência/setup semanal**

---

## ✅ Calendário com duas categorias de datas
A camada de calendário foi organizada em **duas categorias**, usadas nas páginas de referência e nos calendários anuais:

### 1 · Feriados NACIONAIS
Lista `HOLIDAYS` no código.

Marcadores:
- 🔴 feriado nacional
- ⭕ ponto facultativo

### 2 · Rede municipal SME-Rio — EDUCAÇÃO INFANTIL / CRECHE
Todos os eventos da rede, não apenas feriados:
- planejamento
- início/término
- reuniões de responsáveis
- censo
- recessos
- atividades culturais

Base legal: **Resolução SME nº 550, de 22/12/2025** (200 dias letivos).

Marcadores por tipo:
- 🟢 **Planejamento/Formação** (`PLAN`)
- 🔵 **Marco letivo** — início/término (`LETIVO`)
- 🟣 **Reunião de Responsáveis** (`REUNIAO`)
- 🟠 **Censo/Avaliação** (`AVAL`)
- 🟩 **Data comemorativa/cultural** (`COMEMOR`)
- 🟨 **Recesso / não letivo** — fundo amarelo (`RECESSO`)

👉 Confira/edite tudo nas listas **`SME_SINGLE`** e **`SME_RANGES`** no topo do `planner_color.py`.

---

## ✏️ Como editar o calendário da creche

```python
# Eventos de UM dia: (mês, dia, "rótulo", "tipo")
SME_SINGLE = {
    2026: [
        (2, 9,  "Início do ano letivo", "LETIVO"),
        (5, 27, "Censo Escolar", "AVAL"),
        (3, 28, "Reunião de Responsáveis (sábado)", "REUNIAO"),
        (12, 22, "Término do ano letivo", "LETIVO"),
    ],
    2027: [
        # ...
    ],
}

# Eventos de VÁRIOS dias: (mês_i, dia_i, mês_f, dia_f, "rótulo", "tipo")
SME_RANGES = {
    2026: [
        (2, 2, 2, 6, "Planejamento e Formação Pedagógica", "PLAN"),
        (7, 13, 7, 24, "Recesso escolar de julho", "RECESSO"),
        (12, 23, 12, 31, "Recesso / férias de fim de ano", "RECESSO"),
    ],
    2027: [
        # ...
    ],
}
```

Tipos válidos:
- `PLAN`
- `LETIVO`
- `RECESSO`
- `REUNIAO`
- `AVAL`
- `COMEMOR`

### Ligar/desligar camadas
- `INCLUDE_RIO = True/False`
- `INCLUDE_SCHOOL = True/False`
- `INCLUDE_SME = True/False` (se mantido no código)

Via CLI:

```bash
python planner_color.py --no-rio
python planner_color.py --no-escolar
```

---

## 🧩 Modos de geração
O script já foi preparado para trabalhar por modo:

- `yearly`
- `monthly`
- `weekly`
- `all`

### Exemplos
```bash
python planner_color.py --mode yearly --year 2026 --size A4
python planner_color.py --mode monthly --year 2026 --month 3 --size A4
python planner_color.py --mode weekly --size A4
python planner_color.py --mode all --size A4
```

### Nomes de saída esperados
- `planner_yearly_2026_A4.pdf`
- `planner_monthly_2026_03_A4.pdf`
- `planner_weekly_A4.pdf`

> Observação: a separação completa dos booklets ainda depende da refatoração estrutural descrita em `refactory.md`.

---

## 🛠️ Regerar
```bash
pip install reportlab
python planner_color.py --mode yearly --year 2026 --size A4
python planner_color.py --mode monthly --year 2026 --month 3 --size A4
python planner_color.py --mode weekly --size A4
```

Se quiser gerar tudo:

```bash
python planner_color.py --mode all --size A4
```

---

## 📚 Fontes
- **Feriados nacionais 2026/2027** (incluindo móveis: Sexta-feira Santa, Corpus Christi e Carnaval).
- **Calendário SME-Rio 2026 (Educação Infantil / creche):** Resolução SME nº 550/2025
  — Semana de Planejamento 02–06/02, início 09/02, Censo 27/05 (última quarta de maio),
  200 dias letivos. Datas marcadas como `[ANEXO]` devem ser confirmadas no Anexo Único.

---

## 🚧 Estado atual do projeto
Hoje o projeto está em transição de um planner único para um fluxo baseado em **3 booklets independentes**.

### Já feito
- organização do CLI por modo (`yearly`, `monthly`, `weekly`, `all`)
- nomes de saída separados por fluxo
- plano formal de refatoração em `refactory.md`

### Em andamento
- extração dos renderizadores de página
- separação real dos PDFs em conteúdos independentes
- composição booklet-friendly com páginas múltiplas de 4
- garantia de que a página 2 seja o verso da primeira folha correta em cada booklet