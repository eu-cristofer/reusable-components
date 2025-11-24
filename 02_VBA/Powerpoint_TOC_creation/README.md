# GeradorDeSumario.bas

## Purpose
Generates a slide summary (table of contents) based on the sections defined in the active PowerPoint presentation.

## Usage

1. Open the presentation that already contains a slide titled `Sumário`.
2. Run the `GeraSumario` macro from the `GeradorDeSumario` module.
3. The macro will:
   - Identify each section in the presentation.
   - Clear placeholder 2 on the `Sumário` slide and populate it with the titles of every section starting from the second section.
   - Convert each title into a hyperlink pointing to the first slide of the corresponding section.
   - Iterate through every slide from the second section onward and prepend the current section title into the appropriate placeholder (usually the one immediately before `Text Placeholder 2` or any placeholder whose name contains `Text Placeholder`).

## Expectations for correct operation

- The presentation must use sections. The macro reads section names and slide indices via `ActivePresentation.SectionProperties`.
- A slide titled `Sumário` must exist and use placeholder 1 for its title; placeholder 2 is assumed to be the textbox where the list is written.
- The slide that holds `Sumário` should be included in the presentation’s section list so `GetSlideSumario` can locate it.
- Each slide within a section should contain either `Text Placeholder 2` or another placeholder whose name contains `Text Placeholder`; the macro updates the preceding placeholder (or any matching placeholder) with the section title.
- Hyperlinks rely on `Section.FirstSlide` indices and assume contiguous slides; if your sections share slides or the structure is non-standard, the links may not point to the desired slide.
- Run the macro in the PowerPoint presentation that contains macros (a `.pptm`) so it can execute without security warnings.

Use this README to confirm the environment and slide structure before running `GeradorDeSumario`.

