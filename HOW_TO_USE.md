# Comprehensive Guide: LaTeX Manuscript Macro & Snippet Manager

The **LaTeX Manuscript Macro & Snippet Manager** (`latex_manuscript_macro_manager.py`) is an interactive CLI tool designed to simplify managing manuscript commands, reference editions, editor corrections, VS Code / Antigravity IDE snippets, and keyboard shortcuts across your LaTeX projects.

---

## Quick Start (How to Launch)

Run the script from your project folder in the terminal:

```bash
./latex_manuscript_macro_manager.py
```

Running the script without extra arguments opens the **Interactive Main Menu**.

---

## Interactive Menu Options Explained

When you run `./latex_manuscript_macro_manager.py`, you will see this menu:

```
Main Menu - Choose an Action:
[1] 🔄 Full Auto-Sync: Update all 02_macros_*.tex files AND VS Code / Antigravity IDE snippets & keybindings
[2] 📋 View Current Commands: Display all active manuscripts, editions, and editor commands
[3] ➕ Add or Edit a Manuscript / Print Edition: Add a new manuscript (e.g. \mssone) or edit its Devanagari description
[4] ✏️  Add or Edit an Editor Correction: Add an editor correction command (e.g. \CorrectionByMDS)
[5] ❌ Remove a Command: Delete a manuscript or editor command from the project
[6] 🔍 Scan TeX Files: Read custom descriptions directly from existing 02_macros_*.tex files
[7] ⚙️  Change Snippet Prefix or Keybinding: Change trigger prefix (e.g. 'पबम') or shortcut (e.g. 'cmd+a cmd+a')
[0] 🚪 Exit Menu
```

---

### Option `[1]` — 🔄 Full Auto-Sync (Recommended Default)
* **What it does**: 
  1. Scans existing `02_macros_*.tex` files to pick up any custom Devanagari descriptions.
  2. Updates all 16 `02_macros_*.tex` files in your project with matching manuscript & editor definitions.
  3. Automatically updates VS Code and Antigravity IDE global settings (`latex.code-snippets` and `keybindings.json`) AND your project `.vscode/` settings so your shortcuts work everywhere.
* **When to use**: Any time you add a new manuscript, update descriptions, or want to make sure your macros, snippets, and shortcuts are 100% in sync.

---

### Option `[2]` — 📋 View Current Commands
* **What it does**: Displays a formatted table listing every manuscript, printed edition, and editor correction registered for this project, along with its Devanagari description, snippet prefix (`पबम`), and shortcut (`cmd+a cmd+a`).
* **When to use**: To check what manuscripts and commands are currently defined in your project.

---

### Option `[3]` — ➕ Add or Edit a Manuscript / Print Edition
* **What it does**: Prompts you for:
  1. **LaTeX Command Name** (e.g., `mssone`, `tArAEdition`, `chaukhmbatantravArttikam`).
  2. **1st Case Devanagari Description** (e.g., `अड्यारमातृका प्रथमा` or `तारासंस्करणम्`).
  3. **(Optional) 6th Case Shashthi Description**: Press Enter to let the built-in Sanskrit grammar engine automatically convert `अड्यारमातृका प्रथमा` to `अड्यारमातृकायाः प्रथमायाः` for your line-end and page-end macros (`\mssoneLineEnd`, `\mssonePageEnd`).
* **When to use**: When you get a new manuscript, consult a new reference edition, or want to rename/describe an existing manuscript.

---

### Option `[4]` — ✏️ Add or Edit an Editor Correction
* **What it does**: Prompts you for:
  1. **Editor Command Name** (e.g., `CorrectionBylalitaalaalitah`, `CorrectionByMDS`).
  2. **Devanagari Description** (e.g., `ललितालालितेन शोधितः पाठः` or `आचार्य्यैः शोधितः पाठः`).
* **When to use**: When adding a new editor's correction command or updating the editor name.

---

### Option `[5]` — ❌ Remove a Command
* **What it does**: Prompts you for a command name (e.g. `mssthree` or `alrce`) and removes it from `manuscripts_config.json`.
* **When to use**: If a manuscript or reference edition was added by mistake or is no longer used.

---

### Option `[6]` — 🔍 Scan TeX Files
* **What it does**: Reads all `02_macros_*.tex` files in your project directory and extracts custom manuscript descriptions directly from lines like `\newcommand{\mssone}[1]{'{#1} - अड्यारमातृका प्रथमा.'}`.
* **When to use**: If you manually edited a `02_macros_*.tex` file and want the manager to pick up your manual edits automatically.

---

### Option `[7]` — ⚙️ Change Snippet Prefix or Keybinding
* **What it does**: Prompts you to change:
  - **Snippet Trigger Prefix** (default: `पबम`). Type `पबम` in VS Code/Antigravity IDE to insert the entire footnote block.
  - **Keybinding Shortcut** (default: `cmd+a cmd+a`). Highlight text and press `Cmd+A Cmd+A` to wrap selected text in the footnote snippet automatically.
* **When to use**: If you want a different shortcut or snippet prefix for this project.

---

### Option `[0]` — 🚪 Exit Menu
* **What it does**: Closes the interactive menu.

---

## Direct CLI Commands (For Power Users)

If you prefer running direct terminal commands without opening the menu, you can use these shortcuts:

| Command | Action |
| :--- | :--- |
| `./latex_manuscript_macro_manager.py sync-all` | Runs full auto-sync (Option 1) directly |
| `./latex_manuscript_macro_manager.py list` | Displays current commands table (Option 2) |
| `./latex_manuscript_macro_manager.py add-mss -c mssone -m "अड्यारमातृका प्रथमा"` | Adds/updates manuscript command |
| `./latex_manuscript_macro_manager.py add-editor -c CorrectionByMDS -m "आचार्य्यैः शोधितः पाठः"` | Adds/updates editor correction command |
| `./latex_manuscript_macro_manager.py remove -c mssthree` | Removes a command |
| `./latex_manuscript_macro_manager.py scan-macros` | Scans TeX files for descriptions |

---

## How Sanskrit Vibhakti (Declensions) Work Automatically

In Sanskrit:
- **1st Case (*Prathamā*)**: `अड्यारमातृका प्रथमा` is used for the main reading macro `\newcommand{\mssone}[1]{'{#1} - अड्यारमातृका प्रथमा.'}` and snippet comment `% अड्यारमातृका प्रथमा`.
- **6th Case (*Ṣaṣṭhī*)**: `अड्यारमातृकायाः प्रथमायाः` (*of the 1st Adyar manuscript*) is automatically derived and used for line-end and page-end macros:
  - `\newcommand*{\mssoneLineEnd}[1]{\footnoteD{'{#1} अड्यारमातृकायाः प्रथमायाः पङ्क्तिरत्र समाप्यते ।'}}`
  - `\newcommand*{\mssonePageEnd}[1]{\footnoteD{'{#1} अड्यारमातृकायाः प्रथमायाः पुटमत्र समाप्यते ।'}}`

You do **not** need to type the 6th case manually—the manager's built-in Sanskrit grammar engine converts it for you automatically!

---

## 2. `latex_vertical_comment_formatter.py` Guide

### Overview
This helper enforces standard 3-commented-line (`%`) vertical structure around structural markers (e.g. `%<*1>%`, `\pstart%`, `\pend%`, `\begin{vyAkhyA}`, `\section{...}`).

### Interactive Menu Mode
Simply launch the script without arguments:
```bash
./latex_vertical_comment_formatter.py
```
- **Option 1 (`1` or `१`)**: Select a single `.tex` file to format.
- **Option 2 (`2` or `२`)**: Format all `.tex` files in a directory recursively.
- **Option 3 (`3` or `३`)**: Dry-run preview without making changes.
- **Option 0 (`0` or `०`)**: Exit menu.

### Command-Line Arguments
```bash
# Format a single file
./latex_vertical_comment_formatter.py --file path/to/shlokaH_1.tex

# Format all .tex files in a directory recursively
./latex_vertical_comment_formatter.py --dir path/to/cleaned_tex/

# Preview changes without modifying files
./latex_vertical_comment_formatter.py --file path/to/shlokaH_1.tex --dry-run
```

