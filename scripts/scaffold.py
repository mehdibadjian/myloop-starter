#!/usr/bin/env python3
"""myloop-lean Scaffolder: Reusable Framework Generator for Future Projects.

Exports or installs the myloop-lean architecture (.agents rules & skills,
sprint ledger CLI, model-agnostic dispatcher, AGENTS.md, and GEMINI.md) into
any target repository or globally into ~/.gemini/antigravity-cli/.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, Optional


STARTER_SPRINT_YAML = """# Sprint Status Ledger ({project_name})
# Tracks epic and story progression across the development lifecycle.

project: {project_name}
tracking_system: file-system
story_location: docs/stories

development_status:
  epic-1: in-progress
  1-1-initial-setup: ready-for-dev
  epic-1-retrospective: optional

execution_tiers:
  1-1-initial-setup: flash

action_items: []
"""

STARTER_README = """# {project_name}

A software project driven by Kent Beck TDD, multi-model agent personas, and a closed-loop SDLC.

## Autonomous Loop Quickstart

### 1. Pre-Flight Grill (Gate 0)
Resolve design trade-offs and clarify system requirements before coding:
```bash
/grill-me
```

### 2. Fetch Next Ready Story
```bash
python3 scripts/sprint.py next
```

### 3. Verify Implementation (Kent Beck TDD + Anti-Cheat)
```bash
python3 scripts/sprint.py verify --cmd "python3 -m pytest tests/" --anti-cheat
```

### 4. Sprint Status Board
```bash
python3 scripts/sprint.py status
```

## Multi-Model Dispatch
Dispatch tasks to DeepSeek, Qwen, Gemini, or local models:
```bash
python3 scripts/sprint.py dispatch <story_key> --persona developer --dry-run
```
"""


def clean_repository(repo_dir: Path, project_name: str = "My Project") -> Dict[str, Any]:
    """Resets a freshly cloned template repository for a new application."""
    repo_dir = Path(repo_dir).resolve()

    # 1. Reset sprint-status.yaml
    ledger_path = repo_dir / "sprint-status.yaml"
    ledger_path.write_text(STARTER_SPRINT_YAML.format(project_name=project_name), encoding="utf-8")

    # 2. Reset README.md
    readme_path = repo_dir / "README.md"
    readme_path.write_text(STARTER_README.format(project_name=project_name), encoding="utf-8")

    # 3. Clean docs/ while preserving folder hierarchy with .gitkeep
    docs_dir = repo_dir / "docs"
    if docs_dir.exists():
        for item in docs_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    for sub in ["stories", "prd", "architecture", "retrospectives"]:
        sub_dir = docs_dir / sub
        sub_dir.mkdir(parents=True, exist_ok=True)
        gitkeep = sub_dir / ".gitkeep"
        gitkeep.touch()

    return {
        "success": True,
        "repo_dir": str(repo_dir),
        "project_name": project_name,
    }


def scaffold_project(
    source_root: Path,
    target_dir: Path,
    project_name: str = "My Project",
    global_antigravity: bool = False,
) -> Dict[str, Any]:
    """Copies myloop-lean assets into target directory or global Antigravity config."""
    target_dir = Path(target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    copied = []

    # 1. Copy .agents/ (rules and skills)
    src_agents = source_root / ".agents"
    if src_agents.exists():
        dst_agents = target_dir / ".agents"
        shutil.copytree(src_agents, dst_agents, dirs_exist_ok=True)
        copied.append(str(dst_agents))

    # 2. Copy scripts/ (sprint.py, dispatch.py, and scaffold.py)
    dst_scripts = target_dir / "scripts"
    dst_scripts.mkdir(parents=True, exist_ok=True)
    for script_name in ["sprint.py", "dispatch.py", "scaffold.py"]:
        src_script = source_root / "scripts" / script_name
        if src_script.exists():
            shutil.copy2(src_script, dst_scripts / script_name)
            copied.append(str(dst_scripts / script_name))

    # 3. Copy root agent markdown standards (AGENTS.md, GEMINI.md)
    for root_file in ["AGENTS.md", "GEMINI.md"]:
        src_file = source_root / root_file
        if src_file.exists():
            shutil.copy2(src_file, target_dir / root_file)
            copied.append(str(target_dir / root_file))

    # 4. Generate clean starter README.md and sprint-status.yaml if they don't exist
    target_readme = target_dir / "README.md"
    if not target_readme.exists():
        target_readme.write_text(
            STARTER_README.format(project_name=project_name),
            encoding="utf-8",
        )
        copied.append(str(target_readme))

    target_ledger = target_dir / "sprint-status.yaml"
    if not target_ledger.exists():
        target_ledger.write_text(
            STARTER_SPRINT_YAML.format(project_name=project_name),
            encoding="utf-8",
        )
        copied.append(str(target_ledger))

    # 5. Create starter docs directories with .gitkeep
    for doc_sub in ["stories", "prd", "architecture", "retrospectives"]:
        sub_dir = target_dir / "docs" / doc_sub
        sub_dir.mkdir(parents=True, exist_ok=True)
        (sub_dir / ".gitkeep").touch()

    # 6. Optional Global Antigravity Installation
    if global_antigravity:
        home = Path.home()
        global_cli = home / ".gemini" / "antigravity-cli"
        if global_cli.exists():
            # Copy skills
            global_skills = global_cli / "skills"
            global_skills.mkdir(parents=True, exist_ok=True)
            if (source_root / ".agents" / "skills").exists():
                shutil.copytree(
                    source_root / ".agents" / "skills",
                    global_skills,
                    dirs_exist_ok=True,
                )
                copied.append(str(global_skills))

            # Copy rules
            global_rules = global_cli / "rules"
            global_rules.mkdir(parents=True, exist_ok=True)
            if (source_root / ".agents" / "rules").exists():
                shutil.copytree(
                    source_root / ".agents" / "rules",
                    global_rules,
                    dirs_exist_ok=True,
                )
                copied.append(str(global_rules))

    return {
        "success": True,
        "target_dir": str(target_dir),
        "copied_artifacts": copied,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold myloop-lean into a new or existing repository",
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Target directory to initialize (default: current directory)",
    )
    parser.add_argument(
        "--project",
        default="My New Project",
        help="Name of the project to initialize in sprint ledger",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean a cloned template repo (wipes old docs/stories, resets README.md & sprint-status.yaml)",
    )
    parser.add_argument(
        "--global-antigravity",
        action="store_true",
        help="Also install skills and rules into ~/.gemini/antigravity-cli/",
    )

    args = parser.parse_args()
    source_root = Path(__file__).resolve().parent.parent
    target_path = Path(args.target_dir)

    if args.clean:
        print(f"Cleaning template repository at '{target_path.resolve()}' for '{args.project}'...")
        res = clean_repository(target_path, project_name=args.project)
        print("Template repository cleaned successfully:")
        print(f"  + Reset sprint-status.yaml for '{res['project_name']}'")
        print("  + Generated clean starter README.md")
        print("  + Wiped old docs/stories/retrospectives while preserving folder structure")
        sys.exit(0)

    print(f"Scaffolding myloop-lean into '{target_path.resolve()}'...")
    res = scaffold_project(
        source_root=source_root,
        target_dir=target_path,
        project_name=args.project,
        global_antigravity=args.global_antigravity,
    )

    print(f"Successfully scaffolded {len(res['copied_artifacts'])} assets into '{res['target_dir']}':")
    for f in res["copied_artifacts"]:
        print(f"  + {f}")
    print("\nNext steps:")
    print("  1. Edit sprint-status.yaml to define your first stories.")
    print("  2. Run 'python3 scripts/sprint.py next' to fetch the first story.")
    print("  3. Happy autonomous pair programming!")


if __name__ == "__main__":
    main()
