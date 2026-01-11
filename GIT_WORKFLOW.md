# Git Workflow Guide - AI Hardware Designer

## Repository
**GitHub URL:** https://github.com/KUKI-Boi/PCB-Designing.git

## Initial Setup (Already Done)
```bash
git init
git remote add origin https://github.com/KUKI-Boi/PCB-Designing.git
git add .
git commit -m "Initial commit: AI Hardware Designer backend pipeline"
git push -u origin master
```

## Making Changes

### 1. Check Current Status
```bash
git status
```

### 2. Stage Your Changes
```bash
# Stage specific files
git add backend/module_name.py

# Or stage all changes
git add .
```

### 3. Commit Changes
```bash
git commit -m "Brief description of changes"
```

**Good commit messages:**
- `feat: Add STM32 support to circuit designer`
- `fix: Correct relay flyback diode placement`
- `docs: Update README with API configuration`
- `refactor: Simplify component database lookup`

### 4. Push to GitHub
```bash
git push origin master
```

## Common Workflows

### Adding New Features
```bash
# Create feature branch (optional but recommended)
git checkout -b feature/new-sensor-support

# Make changes, stage, and commit
git add backend/circuit_designer.py
git commit -m "feat: Add DHT11 sensor support"

# Push branch
git push origin feature/new-sensor-support

# Merge to master (after review)
git checkout master
git merge feature/new-sensor-support
git push origin master
```

### Viewing History
```bash
# View commit history
git log --oneline

# View specific file history
git log --oneline backend/intent_parser.py

# View changes in last commit
git show
```

### Creating Meaningful Commits

**By Module:**
```bash
# When updating intent parser
git add backend/intent_parser.py
git commit -m "feat: Add support for STM32 in intent parsing"

# When adding components
git add backend/component_selector.py
git commit -m "feat: Add LoRa modules to component database"

# When fixing bugs
git add backend/kicad_generator.py
git commit -m "fix: Correct footprint rotation in PCB generator"
```

**By Feature:**
```bash
# New hardware support
git add backend/*.py
git commit -m "feat: Add complete STM32F4 hardware support with peripherals"

# Bug fixes
git add backend/manufacturing.py
git commit -m "fix: BOM export now correctly groups passive components"
```

## Version Tags

### Creating Releases
```bash
# Tag current version
git tag -a v0.1.0 -m "MVP Release: ESP32 and ATmega328 support"
git push origin v0.1.0

# Tag future versions
git tag -a v0.2.0 -m "Added STM32 support and web UI"
git push origin v0.2.0
```

### Viewing Tags
```bash
git tag
git show v0.1.0
```

## Accessing Previous Versions

### View Old Commits
```bash
# List all commits
git log --oneline

# Checkout specific commit (read-only)
git checkout <commit-hash>

# Return to latest
git checkout master
```

### Restore Previous Files
```bash
# Restore specific file from previous commit
git checkout <commit-hash> -- backend/circuit_designer.py

# Restore all files from tag
git checkout v0.1.0
```

### Compare Versions
```bash
# Compare current with previous commit
git diff HEAD~1

# Compare two specific commits
git diff <commit1> <commit2>

# Compare specific file
git diff HEAD~1 backend/intent_parser.py
```

## Best Practices

### 1. Commit Often
- Small, focused commits are better than large ones
- Each commit should represent one logical change

### 2. Write Good Messages
```bash
# Good
git commit -m "feat: Add DHT22 sensor with pull-up resistor"

# Bad
git commit -m "updates"
```

### 3. Keep .gitignore Updated
Already configured to ignore:
- `.env` (secrets)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)
- Generated files in `output/`

### 4. Branch for Major Features
```bash
git checkout -b feature/web-ui
# Work on feature
git checkout master
git merge feature/web-ui
```

## Quick Reference

```bash
# View changes
git status                  # See modified files
git diff                    # See what changed
git log --oneline          # View history

# Stage and commit
git add .                   # Stage all changes
git commit -m "message"    # Commit staged files

# Sync with GitHub
git pull origin master     # Get latest changes
git push origin master     # Upload your changes

# Undo changes
git checkout -- file.py    # Discard local changes
git reset HEAD file.py     # Unstage file
git revert <commit>        # Undo a commit (safe)

# Branching
git branch                 # List branches
git checkout -b new-branch # Create and switch
git merge branch-name      # Merge into current
```

## Typical Development Cycle

```bash
# 1. Start working
git pull origin master

# 2. Make changes to files
# (edit backend/circuit_designer.py)

# 3. Check what changed
git status
git diff

# 4. Stage and commit
git add backend/circuit_designer.py
git commit -m "feat: Add I2C sensor support"

# 5. Push to GitHub
git push origin master
```

## Current Repository State

**Initial Commit:**
- Complete backend pipeline (7 modules)
- Component database with 20+ real parts
- MVP test outputs (ESP32 irrigation controller)
- Documentation (README, walkthrough)
- Configuration files (.env.example, requirements.txt)

**Next Commits Will Include:**
- Frontend development
- Additional hardware support
- Enhanced features
- Bug fixes and improvements

---

**Remember:** Every push to GitHub creates a snapshot you can return to!
