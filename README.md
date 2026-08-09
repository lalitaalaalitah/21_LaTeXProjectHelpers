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

## Author & Contact
- **Author:** lalitaalaalitah
- **Website:** [https://www.lalitaalaalitah.com](https://www.lalitaalaalitah.com)
- **GitHub:** [https://github.com/lalitaalaalitah](https://github.com/lalitaalaalitah)
