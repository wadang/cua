# Getting Started

## Project Structure

The project is organized as a monorepo with these main packages:

- `libs/core/` - Base package with telemetry support
- `libs/computer/` - Computer-use interface (CUI) library
- `libs/agent/` - AI agent library with multi-provider support
- `libs/som/` - Set-of-Mark parser
- `libs/computer-server/` - Server component for VM
- `libs/lume/` - Lume CLI

These packages are part of a uv workspace which manages a shared virtual environment and dependencies.

## Local Development Setup

1. Install Lume CLI:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/trycua/cua/main/libs/lume/scripts/install.sh)"
    ```

2. Clone the repository:

    ```bash
    git clone https://github.com/trycua/cua.git
    cd cua
    ```

3. Create a `.env.local` file in the root directory with your API keys:

    ```bash
    # Required for Anthropic provider
    ANTHROPIC_API_KEY=your_anthropic_key_here

    # Required for OpenAI provider
    OPENAI_API_KEY=your_openai_key_here
    ```

4. Open the workspace in VSCode or Cursor:

    ```bash
    # For Cua Python development
    code .vscode/py.code-workspace

    # For Lume (Swift) development
    code .vscode/lume.code-workspace
    ```

Using the workspace file is strongly recommended as it:

- Sets up correct Python environments for each package
- Configures proper import paths
- Enables debugging configurations
- Maintains consistent settings across packages

## Lume Development

Refer to the [Lume README](./libs/lume/Development.md) for instructions on how to develop the Lume CLI.

## Python Development

### Setup

Install all of workspace dependencies with a single command:

```bash
uv sync
```

This installs all dependencies in the virtual environment `.venv`.

Each Cua package is installed in editable mode, which means changes to the source code are immediately reflected in the installed package.

The `.venv` environment is also configured as the default VS Code Python interpreter in `.vscode/settings.json`.

### Running Python Scripts

To run Python scripts in the workspace, use the `uv run` command:

```bash
uv run python examples/agent_examples.py
```

Or activate the virtual environment manually:

```bash
source .venv/bin/activate
python examples/agent_examples.py
```

## Running Examples

The Python workspace includes launch configurations for all packages:

- "Run Computer Examples" - Runs computer examples
- "Run Agent Examples" - Runs agent examples
- "SOM" configurations - Various settings for running SOM

To run examples from VSCode / Cursor:

1. Press F5 or use the Run/Debug view
2. Select the desired configuration

The workspace also includes compound launch configurations:

- "Run Computer Examples + Server" - Runs both the Computer Examples and Server simultaneously

## Code Formatting Standards

The Cua project follows strict code formatting standards to ensure consistency across all packages.

### Python Code Formatting

#### Tools

The project uses the following tools for code formatting and linting:

- **[Black](https://black.readthedocs.io/)**: Code formatter
- **[Ruff](https://beta.ruff.rs/docs/)**: Fast linter and formatter
- **[MyPy](https://mypy.readthedocs.io/)**: Static type checker

These tools are automatically installed when you set up the development environment using the `./scripts/build.sh` script.

#### Configuration

The formatting configuration is defined in the root `pyproject.toml` file:

```toml
[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
target-version = "py311"
select = ["E", "F", "B", "I"]
fix = true

[tool.ruff.format]
docstring-code-format = true

[tool.mypy]
strict = true
python_version = "3.11"
ignore_missing_imports = true
disallow_untyped_defs = true
check_untyped_defs = true
warn_return_any = true
show_error_codes = true
warn_unused_ignores = false
```

#### Key Formatting Rules

- **Line Length**: Maximum of 100 characters
- **Python Version**: Code should be compatible with Python 3.11+
- **Imports**: Automatically sorted (using Ruff's "I" rule)
- **Type Hints**: Required for all function definitions (strict mypy mode)

#### IDE Integration

The repository includes VSCode workspace configurations that enable automatic formatting. When you open the workspace files (as recommended in the setup instructions), the correct formatting settings are automatically applied.

Python-specific settings in the workspace files:

```json
"[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    }
}
```

Recommended VS Code extensions:

- Black Formatter (ms-python.black-formatter)
- Ruff (charliermarsh.ruff)
- Pylance (ms-python.vscode-pylance)

#### Manual Formatting

To manually format code:

```bash
# Format all Python files using Black
uv run black .

# Run Ruff linter with auto-fix
uv run ruff check --fix .

# Run type checking with MyPy
uv run mypy .
```

#### Pre-commit Validation

Before submitting a pull request, ensure your code passes all formatting checks:

```bash
# Run all checks
uv run black --check .
uv run ruff check .
uv run mypy .
```

### Swift Code (Lume)

For Swift code in the `libs/lume` directory:

- Follow the [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
- Use SwiftFormat for consistent formatting
- Code will be automatically formatted on save when using the lume workspace
