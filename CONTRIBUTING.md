# Contributing to Luma AI

First off, thank you for considering contributing to Luma AI. This project exists because of people like you who believe that old hardware deserves a second life.

## How Can I Contribute?

### Reporting Bugs

- **Check existing issues** – search the [Issues](https://github.com/LumaGameEngine/Luma-AI/issues) tab to see if it's already reported.
- **Use a clear title** – describe the problem concisely.
- **Include details** – device model, Android version, RAM, steps to reproduce, and any relevant logs.
- **Add screenshots** if possible – they help a lot.

### Suggesting Enhancements

- Open an Issue with the label `enhancement`.
- Describe the feature and why it would be useful.
- If possible, outline a rough implementation approach.

### Submitting Code

1. **Fork the repository** – click the "Fork" button on GitHub.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/Luma-AI.git
   cd Luma-AI

    Create a branch:
    bash

    git checkout -b feature/your-feature-name

    Make your changes – write clean, well-commented code.

    Test your changes – ideally on real hardware.

    Commit with a clear message:
    bash

    git commit -m "Add feature: concise description"

    Push to your fork:
    bash

    git push origin feature/your-feature-name

    Open a Pull Request – against the main branch. Describe your changes and why they matter.

Code Standards
Python (backend and worker)

    Follow PEP 8.

    Use 4 spaces for indentation.

    Keep functions focused and small.

    Add docstrings for public functions and classes.

    No emojis in code, comments, or commit messages (they clutter logs).

JavaScript (frontend)

    Use 2 spaces for indentation.

    Use const and let – avoid var.

    Keep functions small and descriptive.

    Use template literals for string concatenation.

CSS

    Use the existing CSS variables (--bg-primary, --accent, etc.).

    Follow the BEM-like naming pattern used in the codebase.

    Keep selectors shallow and specific.

Testing

    Test on actual hardware – Luma AI is built for physical devices. Virtual environments are not a substitute.

    Test at least one worker – confirm registration, heartbeats, and inference work.

    Test the UI – ensure the device appears, model selection works, and chat responds.

    If you add a new feature, update the relevant documentation.

Documentation

    If you add a new endpoint, document it in docs/API.md.

    If you change the setup process, update docs/SETUP_GUIDE.md.

    If you add a new model or architecture, update docs/MODELS.md.

    Keep documentation clear, concise, and free of emojis.

Hardware Testing

Luma AI is designed for old Android devices. If you test on a device not listed in the README, please share your results in a Pull Request or Issue.

Known working devices:

    Tecno Spark Go 2020 (ARMv7, 2GB RAM)

    Galaxy A15 (ARM64, 4GB RAM) – partial testing

Minimum requirements:

    Android 8+

    2GB RAM (1.8GB usable)

    ARMv7 or ARM64

    Termux installed (from F-Droid)

Code of Conduct

    Be respectful and constructive.

    Assume good intentions.

    Help others learn.

    No harassment, discrimination, or toxicity.

Questions?

    Open a Discussion on GitHub.

    Ping @LumaGameEngine on GitHub.

    Check the docs/ folder – many answers are already there.

Thank You

Luma AI is a community project. Every contribution, whether code, documentation, or testing, makes it better. You're helping give old hardware a second life – and that matters.