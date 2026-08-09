# 21_LaTeXProjectHelpers

## Overview
A centralized repository for Python utilities and workflow scripts designed to automate, manage, and enhance LaTeX critical edition book projects.

## Included Helpers

### 1. `latex_manuscript_macro_manager.py`
Universal LaTeX Manuscript Macro, VS Code Snippet, & Keybinding Manager.

**Key Capabilities:**
- **TeX Macro Management:** Automatically updates `% [ReadingsFromManuscripts]` and `% [ReadingSuggestedByEditors]` blocks across all `02_macros_*.tex` files in any LaTeX project.
- **VS Code Snippet Generator:** Auto-generates project-specific `pAThabheda` snippets with Devanagari comments, `$TM_SELECTED_TEXT`, and sequential tabstops (`$1`, `$2`, ..., `$N`).
- **Dual-Destination Sync:** Updates both global VS Code User Settings (`~/Library/Application Support/Code/User/`) for Settings Sync and project repository `.vscode/` folders for GitHub backups.
- **Project-Scoped Keybindings:** Binds `cmd+a cmd+a` to trigger the project snippet when working inside the project directory.

### 2. `latex_vertical_comment_formatter.py`
Automates the formatting of LaTeX critical edition text files by inserting and enforcing exactly 3 commented lines (`%`) before and after structural markers (`%<*1>%`, `\pstart%`, `\pend%`, `\begin{...}`, `\end{...}`, `\section{...}`).

**Key Capabilities:**
- **Exact Spacing Enforcer:** Normalizes comments to maintain exact 3-commented-line (`%`) boundaries around TeX structural tags and commands.
- **Idempotent Formatting:** Running the script multiple times produces clean, identical results without accumulating duplicate comment lines.
- **Smart Batch Filtering:** Recursively processes content/body TeX files while automatically skipping non-content macro definitions (`02_macros_*.tex`) and root project driver files (`03_AllTexFiles.tex`).
- **Secondary Post-Formatter Execution:** Supports executing custom post-formatting commands (e.g. `latexindent -w {file}`) via `-p / --post-command`.
- **Companion VS Code Extension:** This Python CLI utility is tightly coupled with the official [VS Code & Antigravity IDE Extension](https://github.com/lalitaalaalitah/01_AddCommentedLines) (`latex-vertical-comment-formatter`), sharing the exact same core formatting and smart batch logic.


## Author & Contact
- **Author:** lalitaalaalitah
- **Website:** [https://www.lalitaalaalitah.com](https://www.lalitaalaalitah.com)
- **GitHub:** [https://github.com/lalitaalaalitah](https://github.com/lalitaalaalitah)
