#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "rich",
#     "click",
# ]
# ///
"""
LaTeX Vertical Comment Formatter for Sanskrit Critical Editions
===============================================================

Author: lalitaalaalitah
Website: https://www.lalitaalaalitah.com
GitHub: https://github.com/lalitaalaalitah
Version: 1.0.0

Description:
  Automates the formatting of LaTeX critical edition text files by inserting,
  normalizing, and enforcing exactly three commented lines (%) before and after
  structural markers:
    - Tag markers: %<*1>%, %</1>%, %<*१>%, %</१>%, etc.
    - TeX block markers: \\pstart%, \\pend%
    - Environment boundaries: \\begin{...}, \\end{...}
    - Section & Shloka commands: \\section{...}, \\shlokaH{...}

  Preserves indentation and guarantees idempotency (running multiple times produces
  identical, clean output without accumulating duplicate comment lines).
"""

__author__ = "lalitaalaalitah"
__website__ = "https://www.lalitaalaalitah.com"
__github__ = "https://github.com/lalitaalaalitah"
__version__ = "1.0.0"

import os
import re
import sys
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.theme import Theme

# Catppuccin Mocha Theme setup
custom_theme = Theme({
    "banner.title": "bold cyan",
    "banner.border": "magenta",
    "menu.option": "bold yellow",
    "menu.text": "bright_white",
    "info": "blue",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
})

console = Console(theme=custom_theme)

# Devanagari digit mapping for dual-numeral support
DEVANAGARI_DIGITS_MAP = str.maketrans("०१२३४५६७८९", "0123456789")

def normalize_digits(input_str: str) -> str:
    """Converts Devanagari numerals to Roman ASCII digits."""
    if not input_str:
        return ""
    return input_str.translate(DEVANAGARI_DIGITS_MAP).strip()


# Regex patterns for structural targets
TAG_MARKER_PATTERN = re.compile(
    r"^\s*%(?:<[\*/][\d\u0966-\u096f]+>%|<[\*/][^>]+>%)", re.IGNORECASE
)
PSTART_PEND_PATTERN = re.compile(
    r"^\s*\\(pstart|pend)%?\s*$", re.IGNORECASE
)
ENV_BOUNDARY_PATTERN = re.compile(
    r"^\s*\\(begin|end)\{(?:vyAkhyA|Jnanankusham|TikaA|TikaB|Pathabhedah|Ardhashlokanukramanika|[A-Za-z0-9_]+)\}",
    re.IGNORECASE,
)
STRUCTURAL_CMD_PATTERN = re.compile(
    r"^\s*\\(section|subsection|subsubsection|shlokaH|granthaH)\b", re.IGNORECASE
)


def is_target_line(line: str) -> bool:
    """Checks if a line contains a target marker requiring surrounding commented lines."""
    stripped = line.strip()
    if not stripped:
        return False
    return (
        bool(TAG_MARKER_PATTERN.match(line))
        or bool(PSTART_PEND_PATTERN.match(line))
        or bool(ENV_BOUNDARY_PATTERN.match(line))
        or bool(STRUCTURAL_CMD_PATTERN.match(line))
    )


def is_pure_comment_line(line: str) -> bool:
    """Checks if a line contains ONLY '%' with optional leading whitespace."""
    return line.strip() == "%"


def format_latex_comments(content: str, comment_count: int = 3) -> str:
    """
    Formats content to ensure exactly `comment_count` commented lines (%)
    exist before and after every target marker/command.
    
    Idempotent: repeating formatting yields the exact same clean output.
    """
    lines = content.splitlines()
    if not lines:
        return ""

    result_lines = []
    i = 0
    num_lines = len(lines)

    while i < num_lines:
        line = lines[i]

        if is_target_line(line):
            # Extract indentation of target line
            indent = line[: len(line) - len(line.lstrip())]
            comment_line = f"{indent}%"

            # Remove existing pure comment lines directly before this target in result_lines
            while result_lines and is_pure_comment_line(result_lines[-1]):
                result_lines.pop()

            # Insert exactly comment_count comment lines before target
            for _ in range(comment_count):
                result_lines.append(comment_line)

            # Insert the target line itself
            result_lines.append(line)

            # Skip any pure comment lines directly following this target in input lines
            i += 1
            while i < num_lines and is_pure_comment_line(lines[i]):
                i += 1

            # Insert exactly comment_count comment lines after target
            for _ in range(comment_count):
                result_lines.append(comment_line)

            continue

        else:
            result_lines.append(line)
            i += 1

    # Final cleanup: normalize multiple consecutive blank lines, preserving content
    output = "\n".join(result_lines) + ("\n" if content.endswith("\n") else "")
    return output


def print_banner():
    """Prints standard Catppuccin Mocha terminal banner with author branding."""
    banner_text = f"""
[banner.title]LaTeX Vertical Comment Formatter v{__version__}[/banner.title]
[menu.text]Enforces 3-commented-line (%) vertical block structure around tags & TeX commands.[/menu.text]

[info]Author:[/info]   {__author__}
[info]Website:[/info]  {__website__}
[info]GitHub:[/info]   {__github__}
"""
    console.print(Panel(banner_text.strip(), border_style="banner.border", expand=False))


def process_file(file_path: Path, comment_count: int = 3, dry_run: bool = False) -> bool:
    """Processes a single LaTeX file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        formatted = format_latex_comments(content, comment_count=comment_count)

        if content == formatted:
            console.print(f"[info]No changes needed for:[/info] {file_path.name}")
            return False

        if dry_run:
            console.print(f"[warning][DRY RUN] Would update:[/warning] {file_path}")
        else:
            file_path.write_text(formatted, encoding="utf-8")
            console.print(f"[success]Successfully formatted:[/success] {file_path}")
        return True

    except Exception as e:
        console.print(f"[error]Failed to process {file_path}: {e}[/error]")
        return False


def run_interactive_menu():
    """Interactive CLI menu supporting both Roman and Devanagari choices."""
    while True:
        console.clear()
        print_banner()

        menu_md = """
[menu.option][1] 📄 Format a Single TeX File[/menu.option]
[menu.option][2] 📁 Format All TeX Files in a Directory[/menu.option]
[menu.option][3] 🔍 Dry-Run Preview on a TeX File[/menu.option]
[menu.option][0] 🚪 Exit[/menu.option]
"""
        console.print(Panel(menu_md.strip(), title="Main Menu - Select Option", border_style="cyan"))

        choice_raw = Prompt.ask("Select an option [0/1/2/3]", default="1")
        choice = normalize_digits(choice_raw)

        if choice == "0":
            console.print("[info]Exiting. Namaste![/info]")
            sys.exit(0)

        elif choice == "1":
            target_path_str = Prompt.ask("Enter path to TeX file").strip().strip("'\"")
            if target_path_str:
                path = Path(target_path_str).expanduser().resolve()
                if path.is_file():
                    process_file(path, comment_count=3, dry_run=False)
                else:
                    console.print(f"[error]File not found: {path}[/error]")
            Prompt.ask("\nPress Enter to return to menu...")

        elif choice == "2":
            dir_path_str = Prompt.ask("Enter directory path").strip().strip("'\"")
            if dir_path_str:
                dir_path = Path(dir_path_str).expanduser().resolve()
                if dir_path.is_dir():
                    tex_files = list(dir_path.rglob("*.tex"))
                    if not tex_files:
                        console.print(f"[warning]No .tex files found in {dir_path}[/warning]")
                    else:
                        console.print(f"[info]Found {len(tex_files)} .tex files. Formatting...[/info]")
                        modified_count = 0
                        for tf in tex_files:
                            if process_file(tf, comment_count=3, dry_run=False):
                                modified_count += 1
                        console.print(f"[success]Completed! Updated {modified_count}/{len(tex_files)} files.[/success]")
                else:
                    console.print(f"[error]Directory not found: {dir_path}[/error]")
            Prompt.ask("\nPress Enter to return to menu...")

        elif choice == "3":
            target_path_str = Prompt.ask("Enter path to TeX file for dry-run").strip().strip("'\"")
            if target_path_str:
                path = Path(target_path_str).expanduser().resolve()
                if path.is_file():
                    process_file(path, comment_count=3, dry_run=True)
                else:
                    console.print(f"[error]File not found: {path}[/error]")
            Prompt.ask("\nPress Enter to return to menu...")


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-f", "--file", "file_path", type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path), help="Path to a single TeX file.")
@click.option("-d", "--dir", "dir_path", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path), help="Directory to process all .tex files recursively.")
@click.option("-c", "--count", "comment_count", type=int, default=3, help="Number of commented lines (%) to insert before/after target tags (default: 3).")
@click.option("--dry-run", is_flag=True, help="Preview changes without modifying files.")
@click.option("-v", "--version", "show_version", is_flag=True, help="Show version and branding information.")
def main(file_path: Path, dir_path: Path, comment_count: int, dry_run: bool, show_version: bool):
    """Formats TeX files to enforce exact vertical commented line (%) spacing around tags and commands."""
    if show_version:
        print_banner()
        sys.exit(0)

    if not file_path and not dir_path:
        run_interactive_menu()
        return

    print_banner()

    if file_path:
        process_file(file_path, comment_count=comment_count, dry_run=dry_run)

    if dir_path:
        tex_files = list(dir_path.rglob("*.tex"))
        if not tex_files:
            console.print(f"[warning]No .tex files found in {dir_path}[/warning]")
        else:
            console.print(f"[info]Found {len(tex_files)} .tex files. Processing...[/info]")
            modified_count = 0
            for tf in tex_files:
                if process_file(tf, comment_count=comment_count, dry_run=dry_run):
                    modified_count += 1
            console.print(f"[success]Done! Formatted {modified_count}/{len(tex_files)} files.[/success]")


if __name__ == "__main__":
    main()
