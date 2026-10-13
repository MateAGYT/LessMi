# Contributing to LessMi

First off, thanks for taking the time to contribute!

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Coding Style](#coding-style)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [License / Notice](#license--notice)

## Code of Conduct

By participating, you are expected to uphold the project's
[Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Reporting Bugs

Before opening an issue, check that it has not already been reported. When
reporting a bug, include:

- A clear and descriptive title.
- Steps to reproduce the problem.
- Expected behavior vs. actual behavior.
- Your environment (Windows version, Python version, relevant libraries).
- Any error output or traceback.

### Suggesting Features

Open an issue describing the feature, why it would be useful, and how you
imagine it working. Keep it focused.

### Pull Requests

- Fork the repository and create a branch off `main`.
- Keep changes scoped: one feature or fix per PR.
- Update documentation if your change affects usage.

## Project Structure

```
.
├── builder.py               # GUI builder (customtkinter) that compiles the RAT
├── source_assembled.py      # The RAT itself (Discord bot, gets compiled)
├── requirements.txt         # Python dependencies
├── resources/               # Auxiliary scripts (grabbers, jumpscare asset, etc.)
└── custom_imports.txt       # Extra PyInstaller hidden imports, if any
```

- `source_assembled.py` is injected with the token by the builder and then
  compiled with PyInstaller.
- Persistence lives in `setup_persistence()` inside the RAT and is also
  applied by the builder on build.

## Development Setup

1. Install Python 3.10+ (tested on 3.13).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the RAT directly for testing:

   ```bash
   python source_assembled.py
   ```

4. Run the builder:

   ```bash
   python builder.py
   ```

> The persistence step writes to `HKLM`, so run the builder **as
> administrator** if you want the registry part to succeed.

## Coding Style

- **Indentation:** 4 spaces. No tabs. Never mix them.
- **Naming:** `snake_case` for functions and variables, `PascalCase` for
  classes.
- Keep functions small and single-purpose.
- Prefer `discord.py` async APIs; do not block the event loop with long
  `time.sleep` — use threads or `asyncio`.
- Guard OS-specific calls (`winreg`, `ctypes`, `win32*`) with `try/except`.
- Channel lookups should be scoped to the category, not the whole guild,
  so multiple instances do not collide.

## Commit Guidelines

Use short, imperative commit messages. Optionally follow a prefix style:

```
feat: add screen-mode command
fix: scope channel lookup to category
docs: update CONTRIBUTING
refactor: clean on_message logic
```

## Pull Request Process

1. Ensure the project runs without syntax errors:
   `python -m py_compile source_assembled.py builder.py`
2. Describe what your PR changes and why.
3. Link the related issue if there is one.
4. Be responsive to review feedback.

## License / Notice

This project is released for **educational purposes**. The creator is not
responsible for any illegal or malicious use of the software, nor for any
direct or indirect damage caused by it. Test it, enjoy it, and use it
responsibly.

> **NOTE: YOUR PULL REQUEST NEEDS NOT TO BE OBFUSCATED OR A CLOSE SOURCE.**
