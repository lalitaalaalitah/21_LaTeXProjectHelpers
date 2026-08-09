#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click>=8.0.0",
#     "rich>=13.0.0",
# ]
# ///
"""
latex_manuscript_macro_manager.py
==================================
Universal LaTeX Manuscript Macro, VS Code Snippet, & Keybinding Manager.

Author: lalitaalaalitah
Website: https://www.lalitaalaalitah.com
GitHub: https://github.com/lalitaalaalitah
Version: 1.0.0
License: MIT

This script manages manuscript and editor macro commands across all `02_macros_*.tex`
files in any LaTeX project. It auto-generates project-specific VS Code snippets
(with Devanagari comments and tabstops) and sets up project-scoped keybindings (`cmd+a cmd+a`).
Synchronizes both global VS Code User Settings (for Settings Sync) and project-level `.vscode/`
(for GitHub repository backups).
"""

__author__ = "lalitaalaalitah"
__website__ = "https://www.lalitaalaalitah.com"
__github__ = "https://github.com/lalitaalaalitah"
__version__ = "1.0.0"

import json
import os
import re
import sys
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

CONFIG_FILENAME = "manuscripts_config.json"
USER_HOME = Path.home()
GLOBAL_USER_DIRS = [
    USER_HOME / "Library" / "Application Support" / "Code" / "User",
    USER_HOME / "Library" / "Application Support" / "Antigravity IDE" / "User",
    USER_HOME / "Library" / "Application Support" / "Antigravity" / "User",
    USER_HOME / "Library" / "Application Support" / "Code - Insiders" / "User",
    USER_HOME / "Library" / "Application Support" / "VSCodium" / "User",
]

DEFAULT_MANUSCRIPTS = [
    {"command": "mssone", "comment": "मातृका १", "display_name": "mssone"},
    {"command": "msstwo", "comment": "मातृका २", "display_name": "msstwo"},
]

DEFAULT_EDITORS = [
    {"command": "CorrectionBylalitaalaalitah", "comment": "ललितालालितेन शोधितः पाठः", "display_name": "lalitaalaalitah"},
    {"command": "CorrectionBymds", "comment": "आचार्य्यैः शोधितः पाठः", "display_name": "mds"},
]

def print_banner():
    banner_text = (
        f"[bold bright_magenta]LaTeX Manuscript Macro & Snippet Manager[/bold bright_magenta] [cyan]v{__version__}[/cyan]\n"
        f"[bold yellow]Author:[/bold yellow] {__author__} | [bold green]Website:[/bold green] {__website__} | [bold blue]GitHub:[/bold blue] {__github__}"
    )
    console.print(Panel(banner_text, border_style="bright_blue", expand=False))

def get_project_dir(custom_path=None) -> Path:
    if custom_path:
        p = Path(custom_path).resolve()
    else:
        p = Path.cwd().resolve()
    return p

def load_config(project_dir: Path) -> dict:
    config_path = project_dir / CONFIG_FILENAME
    if not config_path.exists():
        project_name = project_dir.name
        # Clean prefix without underscores or special chars
        prefix = "पबम"
        snippet_name = f"pAThabhedaFor{project_name}"
        keybinding = "cmd+a cmd+a"
        config = {
            "project_name": project_name,
            "snippet_prefix": prefix,
            "snippet_name": snippet_name,
            "keybinding": keybinding,
            "manuscripts": DEFAULT_MANUSCRIPTS,
            "editors": DEFAULT_EDITORS,
        }
        save_config(project_dir, config)
        return config
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(project_dir: Path, config: dict):
    config_path = project_dir / CONFIG_FILENAME
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def find_macro_files(project_dir: Path) -> list[Path]:
    return [
        p for p in project_dir.glob("02_macros_*.tex")
        if not p.name.endswith(".bak")
    ]

ORDINALS = {
    "१": "प्रथमायाः",
    "२": "द्वितीयायाः",
    "३": "तृतीयायाः",
    "४": "चतुर्थायाः",
    "५": "पञ्चम्याः",
    "६": "षष्ठ्याः",
    "७": "सप्तम्याः",
    "८": "अष्टम्याः",
    "९": "नवम्याः",
    "१०": "दशम्याः",
    "प्रथमा": "प्रथमायाः",
    "द्वितीया": "द्वितीयायाः",
    "तृतीया": "तृतीयायाः",
    "चतुर्था": "चतुर्थायाः",
    "पञ्चमी": "पञ्चम्याः",
}

def word_to_shashthi(word: str) -> str:
    """Inflect a single Sanskrit word or ordinal to its 6th case (Shashthi Vibhakti)."""
    word = word.strip()
    if not word:
        return word
    if word in ORDINALS:
        return ORDINALS[word]
    
    if word.endswith("म्") or word.endswith("म\u094d"):
        return word[:-2] + "स्य"
    elif word.endswith("\u093e"):  # ā-mātrā
        return word + "याः"
    elif word.endswith("\u0940"):  # ī-mātrā
        return word[:-1] + "्याः"
    elif word.endswith("\u0903"):  # Visarga
        return word[:-1] + "स्य"
    elif word.endswith("\u094d"):  # General halanta
        return word[:-1] + "स्य"
    else:  # Vowel-implicit a-kārānta
        return word + "स्य"

def to_shashthi_vibhakti(text: str) -> str:
    """Converts a Sanskrit phrase/name from 1st case (Prathama) to 6th case (Shashthi Vibhakti)."""
    if not text:
        return text
    words = text.split()
    converted = [word_to_shashthi(w) for w in words]
    return " ".join(converted)

def generate_manuscripts_latex_block(manuscripts: list[dict]) -> str:
    lines = [
        "% [ReadingsFromManuscripts]",
        "% %"
    ]
    for item in manuscripts:
        cmd = item["command"]
        desc = item.get("comment") or item.get("display_name") or cmd
        shashthi_desc = item.get("shashthi_comment") or to_shashthi_vibhakti(desc)
        lines.extend([
            f"% Commands for the manuscript OR edition : {cmd}%",
            "% %",
            f"\\newcommand{{\\{cmd}}}[1]{{`{{#1}} - {desc}.'}}",
            f"\\newcommand*{{\\{cmd}LineEnd}}[1]{{\\footnoteD{{`{{#1}} {shashthi_desc} पङ्क्तिरत्र समाप्यते ।'}}}}",
            f"\\newcommand*{{\\{cmd}PageEnd}}[1]{{\\footnoteD{{`{{#1}} {shashthi_desc} पुटमत्र समाप्यते ।'}}}}",
            f"\\newcommand*{{\\{cmd}LineNPageEnd}}[2]{{\\footnoteD{{`{{#1}} {shashthi_desc} पङ्क्तिरत्र समाप्यते । {{#2}} पुटमत्र समाप्यते ।'}}}}",
            "% %"
        ])
    lines.append("% [/ReadingsFromManuscripts]")
    return "\n".join(lines)

def generate_editors_latex_block(editors: list[dict]) -> str:
    lines = [
        "% [ReadingSuggestedByEditors]",
        "% %"
    ]
    for item in editors:
        cmd = item["command"]
        desc = item.get("comment") or item.get("display_name") or cmd
        lines.append(f"\\newcommand{{\\{cmd}}}[1]{{{{#1}} - {desc} Correction.}}%")
    lines.extend([
        "% %",
        "\\newcommand{\\WrongNCorrect}[2]{{{#2}\\footnote{{{#1}} - इतिमुद्रितपाठः । {{#2}} - इति समीचीनः स्यात् पाठः ।}}",
        "% %",
        "% [/ReadingSuggestedByEditors]"
    ])
    return "\n".join(lines)

def scan_and_update_from_tex(project_dir: Path) -> dict:
    """Scans project 02_macros_*.tex files for custom manuscript/editor descriptions and updates config."""
    config = load_config(project_dir)
    macro_files = find_macro_files(project_dir)
    if not macro_files:
        return config

    updated = False
    mss_descriptions = {}
    editor_descriptions = {}

    for mf in macro_files:
        with open(mf, "r", encoding="utf-8") as f:
            content = f.read()

        # Match \newcommand{\cmd}[1]{`{#1} - <desc>.'}
        for match in re.finditer(r"\\newcommand\{\\([A-Za-z0-9]+)\}\[1\]\{`\{#1\}\s*-\s*([^'\.]+)\.'\}", content):
            cmd, desc = match.group(1), match.group(2).strip()
            if cmd and desc:
                mss_descriptions[cmd] = desc

        # Match \newcommand{\cmd}[1]{{#1} - <desc> Correction.}
        for match in re.finditer(r"\\newcommand\{\\([A-Za-z0-9]+)\}\[1\]\{.*?-\s*(.*?)\s*Correction\.\}", content):
            cmd, desc = match.group(1), match.group(2).strip()
            if cmd and desc:
                editor_descriptions[cmd] = desc

    for m in config.get("manuscripts", []):
        cmd = m["command"]
        if cmd in mss_descriptions and mss_descriptions[cmd] != cmd:
            if m.get("comment") != mss_descriptions[cmd] or m.get("display_name") != mss_descriptions[cmd]:
                m["comment"] = mss_descriptions[cmd]
                m["display_name"] = mss_descriptions[cmd]
                updated = True

    for e in config.get("editors", []):
        cmd = e["command"]
        if cmd in editor_descriptions and editor_descriptions[cmd] != cmd:
            if e.get("comment") != editor_descriptions[cmd] or e.get("display_name") != editor_descriptions[cmd]:
                e["comment"] = editor_descriptions[cmd]
                e["display_name"] = editor_descriptions[cmd]
                updated = True

    if updated:
        save_config(project_dir, config)
        console.print("[green]✓ Updated manuscripts_config.json with custom descriptions extracted from TeX files.[/green]")

    return config

def sync_macro_file(filepath: Path, manuscripts_block: str, editors_block: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # Sync manuscript block
    mss_pattern = re.compile(
        r"%\s*\[ReadingsFromManuscripts\].*?%\s*\[/ReadingsFromManuscripts\]",
        re.DOTALL
    )
    if mss_pattern.search(content):
        content = mss_pattern.sub(lambda match: manuscripts_block, content)
        modified = True
    else:
        if "% [STARTCUSTOMENVIRONMENT]" in content:
            content = content.replace("% [STARTCUSTOMENVIRONMENT]", f"{manuscripts_block}\n\n% [STARTCUSTOMENVIRONMENT]")
            modified = True
        else:
            content += f"\n\n{manuscripts_block}\n"
            modified = True

    # Sync editor block
    editor_pattern = re.compile(
        r"%\s*\[ReadingSuggestedByEditors\].*?%\s*\[/ReadingSuggestedByEditors\]",
        re.DOTALL
    )
    if editor_pattern.search(content):
        content = editor_pattern.sub(lambda match: editors_block, content)
        modified = True
    else:
        if "% [STARTCUSTOMENVIRONMENT]" in content:
            content = content.replace("% [STARTCUSTOMENVIRONMENT]", f"{editors_block}\n\n% [STARTCUSTOMENVIRONMENT]")
            modified = True
        else:
            content += f"\n\n{editors_block}\n"
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return modified

def build_snippet_object(config: dict) -> dict:
    snippet_name = config.get("snippet_name", f"pAThabhedaFor{config['project_name']}")
    prefix = config.get("snippet_prefix", "पबम")
    manuscripts = config.get("manuscripts", [])
    editors = config.get("editors", [])

    all_sources = manuscripts + editors
    body_lines = [
        "\\\\edtext{$TM_SELECTED_TEXT}{%",
        "\\t%\\\\lemma{}%",
        "\\t\\\\Afootnote{%"
    ]

    tabstop_idx = 1
    for item in all_sources:
        cmd = item["command"]
        comment = item.get("comment", "")
        if tabstop_idx == 1:
            body_lines.append(f"\\t\\t\\\\\\\\{cmd}{{$TM_SELECTED_TEXT${tabstop_idx}}} ; % {comment}")
        else:
            body_lines.append(f"\\t\\t\\\\\\\\{cmd}{{${tabstop_idx}}} ; % {comment}")
        tabstop_idx += 1

    body_lines.append("\\t}%")
    body_lines.append("}")
    body_lines.append(f"${tabstop_idx}")

    return {
        snippet_name: {
            "prefix": prefix,
            "body": body_lines,
            "description": f"Insert complete pAThabheda footnote with all manuscript & editor readings for {config['project_name']}"
        }
    }

def update_keybindings_file_safe(filepath: Path, keybinding_entry: dict) -> bool:
    target_name = keybinding_entry.get("args", {}).get("name", "")
    new_entry_json = json.dumps(keybinding_entry, ensure_ascii=False, indent=4)
    indented_entry = "\n".join("    " + line for line in new_entry_json.splitlines())

    comment_header = (
        "    //\n"
        "    //\n"
        f"    // --- Keybinding for {target_name} ---\n"
    )
    full_block = comment_header + indented_entry

    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("[\n" + full_block + "\n]\n")
        return True

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if this snippet keybinding already exists
    if f'"name": "{target_name}"' in content:
        pattern = re.compile(
            r'(?:[ \t]*//[^\n]*\n)*[ \t]*\{\s*"key":[^}]*?"args":\s*\{\s*"name":\s*"' + re.escape(target_name) + r'"\s*\}[^}]*?\}',
            re.DOTALL
        )
        if pattern.search(content):
            content = pattern.sub(full_block.strip(), content)
        else:
            last_bracket = content.rfind("]")
            if last_bracket != -1:
                prefix = content[:last_bracket].rstrip()
                if not prefix.endswith("[") and not prefix.endswith(","):
                    prefix += ","
                content = prefix + "\n" + full_block + "\n" + content[last_bracket:]
    else:
        last_bracket = content.rfind("]")
        if last_bracket != -1:
            prefix = content[:last_bracket].rstrip()
            if not prefix.endswith("[") and not prefix.endswith(","):
                prefix += ","
            content = prefix + "\n" + full_block + "\n" + content[last_bracket:]
        else:
            content += "\n[\n" + full_block + "\n]\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def update_snippets_file_safe(filepath: Path, snippet_name: str, snippet_data: dict) -> bool:
    snippet_content_json = json.dumps(snippet_data, ensure_ascii=False, indent=4)
    wrapped_json = f'"{snippet_name}": {snippet_content_json}'
    indented_snippet = "\n".join("    " + line for line in wrapped_json.splitlines())

    comment_header = (
        "    //\n"
        "    //\n"
        "    //\n"
        f"    // --- Snippet for {snippet_name} ---\n"
    )
    full_block = comment_header + indented_snippet

    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("{\n" + full_block + "\n}\n")
        return True

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if f'"{snippet_name}":' in content:
        pattern = re.compile(
            r'(?:[ \t]*//[^\n]*\n)*[ \t]*"' + re.escape(snippet_name) + r'"\s*:\s*\{.*?\n    \}',
            re.DOTALL
        )
        if pattern.search(content):
            content = pattern.sub(full_block.strip(), content)
        else:
            last_brace = content.rfind("}")
            if last_brace != -1:
                prefix = content[:last_brace].rstrip()
                if not prefix.endswith("{") and not prefix.endswith(","):
                    prefix += ","
                content = prefix + "\n" + full_block + "\n" + content[last_brace:]
    else:
        last_brace = content.rfind("}")
        if last_brace != -1:
            prefix = content[:last_brace].rstrip()
            if not prefix.endswith("{") and not prefix.endswith(","):
                prefix += ","
            content = prefix + "\n" + full_block + "\n" + content[last_brace:]
        else:
            content += "\n{\n" + full_block + "\n}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def generate_snippets_and_keybindings(project_dir: Path, config: dict):
    project_name = config["project_name"]
    snippet_name = config.get("snippet_name", f"pAThabhedaFor{project_name}")
    keybinding_key = config.get("keybinding", "cmd+a cmd+a")

    snippet_obj = build_snippet_object(config)
    snippet_body = snippet_obj[snippet_name]

    keybinding_obj = {
        "key": keybinding_key,
        "command": "editor.action.insertSnippet",
        "args": {
            "name": snippet_name
        },
        "when": f"resourceDirname =~ /.*{project_name}.*/"
    }

    # 1. Project-level update (.vscode/)
    vscode_dir = project_dir / ".vscode"
    vscode_dir.mkdir(exist_ok=True)
    project_snippet_file = vscode_dir / f"{project_name}.code-snippets"
    project_keybinding_file = vscode_dir / "keybindings.json"

    update_snippets_file_safe(project_snippet_file, snippet_name, snippet_body)
    update_keybindings_file_safe(project_keybinding_file, keybinding_obj)
    console.print(f"[green]✓ Project VS Code Snippet updated:[/green] {project_snippet_file}")
    console.print(f"[green]✓ Project VS Code Keybindings updated:[/green] {project_keybinding_file}")

    # 2. Global IDE User Settings update (VS Code, Antigravity IDE, etc.)
    for user_dir in GLOBAL_USER_DIRS:
        if user_dir.exists():
            global_snippets_file = user_dir / "snippets" / "latex.code-snippets"
            global_keybindings_file = user_dir / "keybindings.json"
            update_snippets_file_safe(global_snippets_file, snippet_name, snippet_body)
            update_keybindings_file_safe(global_keybindings_file, keybinding_obj)
            console.print(f"[green]✓ Global IDE User Settings updated ({user_dir.parent.name}):[/green] {user_dir}")

def save_and_sync_all(p_dir: Path, config: dict):
    """Saves manuscripts_config.json AND immediately updates all 02_macros_*.tex files and IDE snippets/keybindings."""
    save_config(p_dir, config)
    macro_files = find_macro_files(p_dir)
    mss_block = generate_manuscripts_latex_block(config.get("manuscripts", []))
    editor_block = generate_editors_latex_block(config.get("editors", []))
    for mf in macro_files:
        if sync_macro_file(mf, mss_block, editor_block):
            console.print(f"[green]✓ Synced macros in:[/green] {mf.name}")
    generate_snippets_and_keybindings(p_dir, config)
    console.print(f"[bold bright_magenta]✨ Automatically synchronized 02_macros_*.tex files & IDE snippets for '{config['project_name']}'![/bold bright_magenta]")

DEVANAGARI_DIGITS_MAP = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}

def normalize_digits(input_str: str) -> str:
    """Converts Devanagari numerals (०-९) to Roman ASCII digits (0-9)."""
    if not input_str:
        return input_str
    for dev_digit, ascii_digit in DEVANAGARI_DIGITS_MAP.items():
        input_str = input_str.replace(dev_digit, ascii_digit)
    return input_str.strip()

def run_interactive_menu(project_dir=None):
    """Interactive CLI menu when no options/subcommands are provided."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)

    while True:
        console.print("\n[bold cyan]Main Menu - Choose an Action:[/bold cyan]")
        console.print("[1] 🔄 Full Auto-Sync: Update all 02_macros_*.tex files AND VS Code / Antigravity IDE snippets & keybindings")
        console.print("[2] 📋 View Current Commands: Display all active manuscripts, editions, and editor commands")
        console.print("[3] ➕ Add or Edit a Manuscript / Print Edition: Add a new manuscript (e.g. \\mssone) or edit its Devanagari description")
        console.print("[4] ✏️  Add or Edit an Editor Correction: Add an editor correction command (e.g. \\CorrectionByMDS)")
        console.print("[5] ❌ Remove a Command: Delete a manuscript or editor command from the project")
        console.print("[6] 🔍 Scan TeX Files: Read custom descriptions directly from existing 02_macros_*.tex files")
        console.print("[7] ⚙️  Change Snippet Prefix or Keybinding: Change trigger prefix (e.g. 'पबम') or shortcut (e.g. 'cmd+a cmd+a')")
        console.print("[0] 🚪 Exit Menu")

        choices = ["0", "1", "2", "3", "4", "5", "6", "7", "०", "१", "२", "३", "४", "५", "६", "७"]
        raw_choice = Prompt.ask("\nSelect an option", choices=choices, default="1")
        choice = normalize_digits(raw_choice)

        if choice == "0":
            console.print("[bold yellow]Goodbye![/bold yellow]")
            break
        elif choice == "1":
            config = scan_and_update_from_tex(p_dir)
            save_and_sync_all(p_dir, config)
        elif choice == "2":
            list_items_func(p_dir)
        elif choice == "3":
            cmd_input = Prompt.ask("Enter LaTeX command name (e.g. mssone, tArAEdition)")
            comment_input = Prompt.ask("Enter Devanagari description / comment (e.g. अड्यारमातृका प्रथमा)")
            shashthi_input = Prompt.ask("Enter 6th case Shashthi description (press Enter for auto-declension)", default="")
            cmd_clean = cmd_input.lstrip("\\").strip()
            manuscripts = config.setdefault("manuscripts", [])
            existing = False
            for m in manuscripts:
                if m["command"] == cmd_clean:
                    m["comment"] = comment_input
                    m["display_name"] = comment_input
                    if shashthi_input:
                        m["shashthi_comment"] = shashthi_input
                    existing = True
                    break
            if not existing:
                item_dict = {"command": cmd_clean, "comment": comment_input, "display_name": comment_input}
                if shashthi_input:
                    item_dict["shashthi_comment"] = shashthi_input
                manuscripts.append(item_dict)
            save_and_sync_all(p_dir, config)
            console.print(f"[bold green]✓ Saved manuscript command:[/bold green] \\{cmd_clean} ({comment_input})")
        elif choice == "4":
            cmd_input = Prompt.ask("Enter Editor command name (e.g. CorrectionByMDS)")
            comment_input = Prompt.ask("Enter Devanagari comment (e.g. आचार्य्यैः शोधितः पाठः)")
            cmd_clean = cmd_input.lstrip("\\").strip()
            editors = config.setdefault("editors", [])
            existing = False
            for e in editors:
                if e["command"] == cmd_clean:
                    e["comment"] = comment_input
                    e["display_name"] = comment_input
                    existing = True
                    break
            if not existing:
                editors.append({"command": cmd_clean, "comment": comment_input, "display_name": comment_input})
            save_and_sync_all(p_dir, config)
            console.print(f"[bold green]✓ Saved editor command:[/bold green] \\{cmd_clean} ({comment_input})")
        elif choice == "5":
            cmd_input = Prompt.ask("Enter command name to remove")
            cmd_clean = cmd_input.lstrip("\\").strip()
            config["manuscripts"] = [m for m in config.get("manuscripts", []) if m["command"] != cmd_clean]
            config["editors"] = [e for e in config.get("editors", []) if e["command"] != cmd_clean]
            save_and_sync_all(p_dir, config)
            console.print(f"[bold green]✓ Removed command:[/bold green] \\{cmd_clean}")
        elif choice == "6":
            config = scan_and_update_from_tex(p_dir)
            save_and_sync_all(p_dir, config)
        elif choice == "7":
            new_prefix = Prompt.ask("Enter snippet prefix", default=config.get("snippet_prefix", "पबम"))
            new_key = Prompt.ask("Enter shortcut keybinding", default=config.get("keybinding", "cmd+a cmd+a"))
            config["snippet_prefix"] = new_prefix
            config["keybinding"] = new_key
            save_and_sync_all(p_dir, config)
            console.print("[bold green]✓ Updated prefix and keybinding in config.[/bold green]")

def list_items_func(project_dir=None):
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)

    console.print(f"\n[bold yellow]Project:[/bold yellow] [bright_cyan]{config['project_name']}[/bright_cyan]")
    console.print(f"[bold yellow]Snippet Prefix:[/bold yellow] [bright_magenta]{config.get('snippet_prefix', 'पबम')}[/bright_magenta]")
    console.print(f"[bold yellow]Keybinding:[/bold yellow] [bright_green]{config.get('keybinding', 'cmd+a cmd+a')}[/bright_green]\n")

    table = Table(title="Manuscript & Reference Edition Commands", header_style="bold magenta")
    table.add_column("Type", style="cyan", width=12)
    table.add_column("Command Name", style="bold green", width=30)
    table.add_column("Devanagari Description / Comment", style="yellow")

    for m in config.get("manuscripts", []):
        table.add_row("Manuscript", f"\\{m['command']}", m.get("comment", ""))
    for e in config.get("editors", []):
        table.add_row("Editor", f"\\{e['command']}", e.get("comment", ""))

    console.print(table)

# CLI setup using Click
@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show script version and exit.")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
@click.pass_context
def cli(ctx, version, project_dir):
    """Universal LaTeX Manuscript Macro & Snippet Manager CLI."""
    if version:
        print_banner()
        click.echo(f"latex_manuscript_macro_manager version {__version__}")
        sys.exit(0)
    if ctx.invoked_subcommand is None:
        run_interactive_menu(project_dir)

@cli.command(name="init")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def init_cmd(project_dir):
    """Initialize manuscripts_config.json for a project."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)
    save_and_sync_all(p_dir, config)
    console.print(f"[bold green]Initialized config at:[/bold green] {p_dir / CONFIG_FILENAME}")

@cli.command(name="list")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def list_items(project_dir):
    """List all registered manuscripts, editions, and editor corrections."""
    list_items_func(project_dir)

@cli.command(name="add-mss")
@click.option("--cmd", "-c", default=None, help="LaTeX command name (e.g. tArAEdition).")
@click.option("--comment", "-m", default=None, help="Devanagari comment/description.")
@click.option("--shashthi-comment", "-s", default=None, help="Optional 6th case Shashthi description.")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def add_mss(cmd, comment, shashthi_comment, project_dir):
    """Add a manuscript or reference edition command."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)

    if not cmd:
        cmd = Prompt.ask("Enter LaTeX command name (e.g. mssone, tArAEdition)")
    if not comment:
        comment = Prompt.ask("Enter Devanagari description / comment (e.g. अड्यारमातृका प्रथमा)")

    cmd_clean = cmd.lstrip("\\").strip()
    manuscripts = config.setdefault("manuscripts", [])
    existing = False
    for m in manuscripts:
        if m["command"] == cmd_clean:
            m["comment"] = comment
            m["display_name"] = comment
            if shashthi_comment:
                m["shashthi_comment"] = shashthi_comment
            existing = True
            break
    if not existing:
        item_dict = {"command": cmd_clean, "comment": comment, "display_name": comment}
        if shashthi_comment:
            item_dict["shashthi_comment"] = shashthi_comment
        manuscripts.append(item_dict)

    save_and_sync_all(p_dir, config)
    console.print(f"[bold green]✓ Added/updated manuscript command:[/bold green] \\{cmd_clean} ({comment})")

@cli.command(name="add-editor")
@click.option("--cmd", "-c", default=None, help="LaTeX command name (e.g. CorrectionByMDS).")
@click.option("--comment", "-m", default=None, help="Devanagari comment/description.")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def add_editor(cmd, comment, project_dir):
    """Add an editor correction command."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)

    if not cmd:
        cmd = Prompt.ask("Enter Editor command name (e.g. CorrectionByMDS)")
    if not comment:
        comment = Prompt.ask("Enter Devanagari comment (e.g. आचार्य्यैः शोधितः पाठः)")

    cmd_clean = cmd.lstrip("\\").strip()
    editors = config.setdefault("editors", [])
    existing = False
    for e in editors:
        if e["command"] == cmd_clean:
            e["comment"] = comment
            e["display_name"] = comment
            existing = True
            break
    if not existing:
        editors.append({"command": cmd_clean, "comment": comment, "display_name": comment})

    save_and_sync_all(p_dir, config)
    console.print(f"[bold green]✓ Added/updated editor command:[/bold green] \\{cmd_clean} ({comment})")

@cli.command(name="remove")
@click.option("--cmd", "-c", default=None, help="LaTeX command name to remove.")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def remove_cmd(cmd, project_dir):
    """Remove a manuscript or editor command."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)

    if not cmd:
        cmd = Prompt.ask("Enter command name to remove")

    cmd_clean = cmd.lstrip("\\").strip()
    config["manuscripts"] = [m for m in config.get("manuscripts", []) if m["command"] != cmd_clean]
    config["editors"] = [e for e in config.get("editors", []) if e["command"] != cmd_clean]

    save_and_sync_all(p_dir, config)
    console.print(f"[bold green]✓ Removed command:[/bold green] \\{cmd_clean}")

@cli.command(name="sync-macros")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def sync_macros_cmd(project_dir):
    """Sync all 02_macros_*.tex files with config macro definitions."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)
    macro_files = find_macro_files(p_dir)

    if not macro_files:
        console.print("[yellow]No 02_macros_*.tex files found to update.[/yellow]")
        return

    mss_block = generate_manuscripts_latex_block(config.get("manuscripts", []))
    editor_block = generate_editors_latex_block(config.get("editors", []))

    count = 0
    for mf in macro_files:
        if sync_macro_file(mf, mss_block, editor_block):
            count += 1
            console.print(f"[green]✓ Synced macros in:[/green] {mf.name}")

    console.print(f"\n[bold bright_green]Successfully synchronized {count} macro file(s).[/bold bright_green]")

@cli.command(name="generate-snippet")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def generate_snippet_cmd(project_dir):
    """Generate VS Code snippet and keybinding (dual sync)."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = load_config(p_dir)
    generate_snippets_and_keybindings(p_dir, config)

@cli.command(name="scan-macros")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def scan_macros_cmd(project_dir):
    """Scan 02_macros_*.tex files for custom descriptions, update config, and sync snippet comments."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = scan_and_update_from_tex(p_dir)
    macro_files = find_macro_files(p_dir)

    mss_block = generate_manuscripts_latex_block(config.get("manuscripts", []))
    editor_block = generate_editors_latex_block(config.get("editors", []))

    count = 0
    for mf in macro_files:
        if sync_macro_file(mf, mss_block, editor_block):
            count += 1
            console.print(f"[green]✓ Synced macros in:[/green] {mf.name}")

    generate_snippets_and_keybindings(p_dir, config)
    console.print(f"\n[bold bright_green]✓ Scanned and synchronized all macro files & snippet comments for '{config['project_name']}'![/bold bright_green]")

@cli.command(name="sync-all")
@click.option("--project-dir", "-p", default=None, help="Path to LaTeX project directory.")
def sync_all_cmd(project_dir):
    """Perform full sync (scan TeX -> config -> all 02_macros_*.tex files -> VS Code & Antigravity snippets/keybindings)."""
    print_banner()
    p_dir = get_project_dir(project_dir)
    config = scan_and_update_from_tex(p_dir)
    macro_files = find_macro_files(p_dir)

    mss_block = generate_manuscripts_latex_block(config.get("manuscripts", []))
    editor_block = generate_editors_latex_block(config.get("editors", []))

    count = 0
    for mf in macro_files:
        if sync_macro_file(mf, mss_block, editor_block):
            count += 1
            console.print(f"[green]✓ Synced macros in:[/green] {mf.name}")

    generate_snippets_and_keybindings(p_dir, config)
    console.print(f"\n[bold bright_magenta]✨ Full synchronization complete for project '{config['project_name']}'![/bold bright_magenta]")

if __name__ == "__main__":
    cli()
