# myloop-starter

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
