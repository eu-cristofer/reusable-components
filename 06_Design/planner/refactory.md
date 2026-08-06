# Refactory plan — `06_Design/planner/planner_color.py`

## Goal
Refactor the current monolithic planner generator into **three truly independent booklet generators** that match the real printing flow:

1. **Yearly booklet**
   - printed once per year
   - first sheet front: yearly cover
   - first sheet back: yearly calendar + holidays/school calendar reference

2. **Monthly booklet**
   - printed once per month
   - first sheet front: monthly cover
   - first sheet back: monthly overview/reference page for the selected month

3. **Weekly booklet**
   - printed as needed
   - first sheet front: weekly cover
   - first sheet back: weekly reference/setup page

All outputs should remain **A4 pages**, intended to be printed as **A3 booklet / livreto / duplex**.

---

## Non-goals
- Do **not** generate imposed A3 spreads.
- Do **not** redesign the visual identity completely.
- Do **not** change the data sources for holidays/SME unless necessary.
- Do **not** remove the current visual style unless a page must be simplified for booklet fit.

---

## Current situation
The file currently has:
- a single large `build()` function that renders the full 15-page planner
- new CLI arguments already added:
  - `--mode yearly|monthly|weekly|all`
  - `--year`
  - `--month`
- wrapper functions:
  - `build_yearly_booklet(...)`
  - `build_monthly_booklet(...)`
  - `build_weekly_booklet(...)`

But those wrappers still call the same legacy `build()`.

---

# Sprint 1 — Stabilize baseline and create rendering architecture

## Objective
Prepare the file for a safe large refactor by extracting reusable rendering helpers and page-level functions.

## Tasks

### 1.1 Keep a backup path in mind
- Before major editing, inspect current file and keep diff visibility high.
- Use `read_file` immediately before edits.

### 1.2 Create a reusable drawing context abstraction
Extract the helper logic currently nested inside `build()` into reusable top-level structures.

#### Target
Create either:
- a `PlannerDrawer` class, or
- a set of top-level helper functions that receive `(c, W, H, s, M, ...)`

#### Minimum helpers to extract
- `fs`
- `text`
- `rtext`
- `box`
- `bar`
- `hline`
- `label`
- `lines`
- `dots`
- `page_header`
- `footer`
- `booklet_page_header`
- `mini_month`

### 1.3 Introduce page-number state management
The new architecture should not depend on hardcoded page numbers.

#### Requirement
Use a small counter mechanism, e.g.:
- `drawer.page_no += 1` before each page footer
- or a helper `start_page(...)` / `finish_page(...)`

### 1.4 Preserve current rendering during extraction
Before splitting booklets, make sure the extracted structure can still reproduce the current pages without visual breakage.

#### Done criteria
- Legacy full planner can still be generated after helper extraction.
- No NameError from moved nested functions.

---

# Sprint 2 — Extract reusable page renderer functions

## Objective
Turn each logical page into an independent function.

## Tasks

### 2.1 Cover pages
Create reusable cover functions:
- `draw_general_cover(...)` or specialized covers:
  - `draw_yearly_cover(...)`
  - `draw_monthly_cover(...)`
  - `draw_weekly_cover(...)`

### 2.2 Informational/reference pages
Extract the current pages into separate functions:
- `draw_holidays_school_page(...)`
- `draw_yearly_overview_page(...)`
- `draw_wheel_of_life_page(...)`
- `draw_goals_projects_page(...)`
- `draw_finance_page(...)`
- `draw_month_reflection_page(...)`
- `draw_lined_notes_page(...)`
- `draw_dotted_notes_page(...)`

### 2.3 Booklet spread pages
Extract spread pages into true reusable functions:
- `draw_monthly_spread_left(...)`
- `draw_monthly_spread_right(...)`
- `draw_weekly_spread_left(...)`
- `draw_weekly_spread_right(...)`

### 2.4 Add month-aware reference page
Create a new page function for the monthly booklet:
- `draw_month_reference_page(...)`

#### It should include
- selected month name and year
- mini calendar for that month
- monthly holidays only
- SME events only for that month if enabled
- a small notes area or “focos do mês” reminder

### 2.5 Add weekly setup/reference page
Create a new page function for the weekly booklet:
- `draw_weekly_reference_page(...)`

#### It should include
- reusable weekly setup text or prompts
- small mini calendar(s), ideally current month and next month if date is known
- small habits / checklist / planning reminder
- notes area

If no explicit week date is provided, keep it generic but reusable.

### 2.6 Optional blank page helper
Create:
- `draw_blank_page(...)`

Useful for booklet page count padding.

#### Done criteria
- All major page content exists as separate callables.
- No page renderer depends on local nested functions from `build()`.

---

# Sprint 3 — Build the real booklet generators

## Objective
Replace wrapper behavior with true independent documents.

## Tasks

### 3.1 Real yearly booklet
Implement `build_yearly_booklet(page_size, out_name, year, include_rio=True, include_school=True)`

#### Required page order
Suggested minimum 8 pages for booklet friendliness:
1. Yearly cover
2. Holidays + school calendar reference page  ← back of first sheet
3. Annual overview for selected year
4. Wheel of life
5. Goals and projects
6. Lined notes
7. Dotted notes
8. Blank or extra notes page

#### Notes
- The annual overview should be for the selected `year` only, not both years.
- If you want to preserve a 2026/2027 cross-year feeling, keep that only where visually useful.

### 3.2 Real monthly booklet
Implement `build_monthly_booklet(page_size, out_name, year, month, include_rio=True, include_school=True)`

#### Required page order
Suggested 8 pages:
1. Monthly cover for selected month/year
2. Monthly reference page  ← back of first sheet
3. Monthly spread left
4. Monthly spread right
5. Finance page
6. Monthly reflection page
7. Lined notes
8. Dotted notes

#### Monthly-specific requirements
- cover must show selected month and year
- reference page must be specific to selected month
- finance/reflection should remain generic enough for reuse in that month

### 3.3 Real weekly booklet
Implement `build_weekly_booklet(page_size, out_name, include_rio=True, include_school=True)`

#### Required page order
Suggested minimum 4 pages, optionally 8:
Option A, minimal 4-page booklet:
1. Weekly cover
2. Weekly reference/setup page  ← back of first sheet
3. Weekly spread left
4. Weekly spread right

Option B, more complete 8-page booklet:
1. Weekly cover
2. Weekly reference/setup page
3. Weekly spread left
4. Weekly spread right
5. Lined notes
6. Dotted notes
7. Lined notes
8. Dotted notes

Choose one and keep it consistent.

### 3.4 Keep or replace legacy `build()`
One of these strategies:

#### Strategy A — recommended
Replace `build()` with a compatibility wrapper or remove it if no longer needed.

#### Strategy B
Keep `build()` only as `build_legacy_full_planner(...)` for backward compatibility.

If kept, rename it clearly so it no longer looks like the main path.

#### Done criteria
- `build_yearly_booklet()` no longer calls the legacy all-in-one build
- `build_monthly_booklet()` no longer calls the legacy all-in-one build
- `build_weekly_booklet()` no longer calls the legacy all-in-one build

---

# Sprint 4 — Booklet printing correctness and page count discipline

## Objective
Ensure each generated PDF is booklet-friendly.

## Tasks

### 4.1 Ensure page counts are multiples of 4
Implement a helper like:
- `pad_to_multiple_of_4(drawer, pages_drawn, filler=draw_blank_page)`

If a booklet ends with 5, 6, or 7 pages, pad with blank/notes pages until it reaches a multiple of 4.

### 4.2 Verify first-sheet-back requirement
For each booklet, confirm the second page is exactly:
- yearly: holidays/yearly reference
- monthly: month reference
- weekly: weekly setup/reference

### 4.3 Preserve A4 output size
Do not switch to A3 pages in code.
The intended workflow remains:
- generate A4 PDF
- print as booklet on A3 duplex

### 4.4 Footer numbering
Make footer page numbers dynamic and correct for each booklet.
Do not hardcode legacy values like `footer(12)`.

#### Done criteria
- every booklet has page count divisible by 4
- page 2 of each booklet is the intended “back of first sheet” page
- footer numbering matches actual booklet length

---

# Sprint 5 — CLI finishing and behavior polish

## Objective
Ensure the command-line experience matches the new flow cleanly.

## Tasks

### 5.1 Validate monthly arguments
- `--month` must be required when `--mode monthly`
- when `--mode all`, if `--month` is omitted, generate all 12 monthly booklets
- when `--mode all` and `--month` is set, generate only that monthly booklet plus yearly/weekly

### 5.2 Output filenames
Use clear names:
- yearly: `planner_yearly_{year}_{size}.pdf`
- monthly: `planner_monthly_{year}_{month:02d}_{size}.pdf`
- weekly: `planner_weekly_{size}.pdf`

### 5.3 Optional future improvements
Only if easy and safe:
- add `--notes-pages` for weekly booklet expansion
- add `--legacy-full` to preserve old behavior if desired

### 5.4 Update top docstring
Rewrite top usage instructions so they reflect the new modes.

#### Done criteria
- CLI help is accurate
- output file naming is consistent
- top docstring no longer describes only the legacy build behavior

---

# Sprint 6 — QA and regression checks

## Objective
Make sure the refactor works and remains stable.

## Tasks

### 6.1 Smoke test command set
Run at least:

```powershell
python 06_Design/planner/planner_color.py --mode yearly --year 2026 --size A4
```

```powershell
python 06_Design/planner/planner_color.py --mode monthly --year 2026 --month 3 --size A4
```

```powershell
python 06_Design/planner/planner_color.py --mode weekly --size A4
```

### 6.2 Confirm PDFs are created
Check output files exist and names are correct.

### 6.3 Visual sanity checks
At minimum verify:
- no clipped titles
- no missing helper references
- no page-number mismatch
- no malformed booklet spread pages
- monthly reference page shows the selected month only
- yearly overview page shows the selected year only

### 6.4 Optional syntax check
If available:

```powershell
python -m py_compile 06_Design/planner/planner_color.py
```

---

# Implementation guidance

## Preferred refactor strategy
Do the refactor incrementally, not in one blind rewrite.

Recommended order:
1. extract helpers
2. extract page functions
3. switch one booklet builder at a time
4. verify after each step

## Edit discipline
- Always `read_file` just before `multi_edit`
- Use one `multi_edit` per large coherent section when possible
- Avoid shell-based file editing

## Naming guidance
Prefer explicit names over generic names. Example:
- good: `draw_month_reference_page`
- weak: `page2`

## Backward compatibility
If preserving the old full planner matters, rename old `build()` to something explicit like:
- `build_legacy_full_planner(...)`

Then optionally keep a compatibility path.

---

# Acceptance criteria summary
The refactor is complete when all of the following are true:

- `planner_color.py` can generate three truly independent PDFs
- `--mode yearly` generates a yearly booklet only
- `--mode monthly` generates a month-specific booklet only
- `--mode weekly` generates a weekly booklet only
- each booklet’s page 2 is the correct “back of first sheet” content
- each booklet has booklet-friendly page counts
- page renderers are extracted and reusable
- no hardcoded legacy footer numbering remains
- legacy all-in-one behavior is either removed or clearly renamed

---

# Nice-to-have follow-up sprint

## Sprint 7 — Optional date-aware weekly booklet
If desired later, add:
- `--week-start YYYY-MM-DD`

Then weekly booklet can show:
- actual week date range on cover/reference page
- small current-month mini calendar with that week highlighted
- optional relevant holidays for that week

This is optional and should not block the main refactor.
