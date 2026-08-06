# AGENTS.md (OpenCode)

This repository is not a single app/package: it is a grab-bag of small, mostly standalone "reusable components" across C/VBA/Python/JS. Do not assume there is a root `build/test/lint` command.

## High-Value Entry Points

- C + SQLite examples live in `01_C/` (includes `sqlite-amalgamation/` vendored sources).
- Word VBA macros (ABNT styles + TOC) live in `02_VBA/ABNT_Word_styles/`.
- Python scripts are under `03_Python/`.
- Planner PDF generator is `06_Design/planner/planner_color.py`.

## C (SQLite) Gotchas + Commands

- The C logger (`01_C/SQLite_C_logger.c`) writes to `logs.db` and creates table `activities(description TEXT, activity_timestamp ...)`.
- `03_Python/SQLite_Py_logger.py` is a separate example that uses `activities.db` and a different schema (`activity_name`), so it is not compatible with the C logger DB.

Build from source (uses the vendored amalgamation, no system sqlite needed):

```bash
# Shared library (for ctypes example)
gcc -fPIC -shared 01_C/SQLite_C_logger.c 01_C/sqlite-amalgamation/sqlite3.c -lpthread -ldl -lm -o db_logger.so

# CLI executable
gcc 01_C/SQLite_C_logger.c 01_C/sqlite-amalgamation/sqlite3.c -lpthread -ldl -lm -o db_logger

# Print DB rows from CLI
gcc 01_C/SQLite_C_print_db.c 01_C/sqlite-amalgamation/sqlite3.c -lpthread -ldl -lm -o db_print
./db_print logs.db
```

## Python (ctypes + Planner) Gotchas + Commands

- `03_Python/SQLite_Py_C_logger.py` assumes `db_logger.so` is present in the current working directory.
- That script calls `os.add_dll_directory(...)`, which is Windows-only; on Linux/macOS it will raise. If you're running it on non-Windows, remove/guard that call.

Planner regeneration (`06_Design/planner/`):

```bash
pip install reportlab
python 06_Design/planner/planner_color.py            # generates A4 + A5 PDFs
python 06_Design/planner/planner_color.py --size A4
python 06_Design/planner/planner_color.py --no-escolar
python 06_Design/planner/planner_color.py --no-rio
```

## VBA (Word) ABNT Styles + TOC Workflow

- The import macro is `02_VBA/00_importModules.bas` (`Sub ImportModules`) and expects a `00_module_list.txt` inside the selected folder.
- For ABNT Word styles, select folder `02_VBA/ABNT_Word_styles/` when prompted; modules are listed in `02_VBA/ABNT_Word_styles/00_module_list.txt`.
- Main entrypoint is `02_VBA/ABNT_Word_styles/a1_mainScript.bas` (`Sub styleABNT`).
- TOC: run `Tool_createUserForm.bas` (`Sub createUserForm`) to create the `selectTOCLevel` form.
- TOC: run `Tool_addTOC.bas` (`Sub addTOC`) to show the form; it calls `Tool_createTOC.bas` (`Sub createTOC(level)`).
