# Repository Guidelines

## Project Structure & Module Organization
- `libs/python/{agent,computer,core,...}` house the primary Python packages; each exposes its own `src` module and `tests` directory.
- `libs/typescript/` contains the UI tooling, while `libs/lume/` and `libs/lumier/` target Swift and UI assets.
- Shared integration and regression suites live in `tests/`; docs and notebooks are under `docs/` and `notebooks/`.
- Utility scripts (build, cleanup, Docker workflows) sit in `scripts/`; prefer these wrappers over ad-hoc commands.

## Build, Test, and Development Commands
- `./scripts/build.sh` — bootstrap every Python package in editable mode with a shared virtualenv.
- `pdm install -G:all` — install runtime, dev, docs, and test dependencies; use `pdm install -d` when you only need dev tooling.
- `pdm run pytest` — execute the full Python test suite; scope with package paths (e.g., `pdm run pytest libs/python/agent/tests`) for quicker iterations.
- `./scripts/run-docker-dev.sh build|run` — build and enter the Docker-based dev container when you need an isolated environment.

## Coding Style & Naming Conventions
- Python code uses 4-space indentation, 100-character lines, and strict typing; run `pdm run black .`, `pdm run ruff check --fix .`, and `pdm run mypy .` before submitting.
- Keep module names snake_case and exported classes in PascalCase; constants stay UPPER_SNAKE.
- TypeScript packages follow the existing ESLint/Prettier defaults; mirror the folder-level patterns already present in `libs/typescript`.

## Testing Guidelines
- PyProject config wires `pytest` with `asyncio_mode=auto` and `test_*.py` discovery; mimic that naming for new tests.
- Aim to touch both the package-local `libs/python/*/tests` suite and any affected integration checks under `tests/`.
- For coverage-sensitive changes, run `pdm run pytest --cov=libs/python --cov-report=term-missing` and document notable gaps in the PR.

## Commit & Pull Request Guidelines
- Follow the repo’s imperative, sentence-case commit style (`Fix computer tabs`, `Make DockerProvider API port configurable`); keep subject lines under ~72 characters.
- Each PR should summarise scope, link relevant issues, list manual/automated test output (command + result), and attach screenshots or logs when UI or UX changes are visible.
- Avoid bundling unrelated work; small, reviewable PRs merge faster and simplify release notes.

## Security & Configuration Tips
- Secrets live in `.env.local`; never commit API keys. Reference variables in code via environment lookups only.
- When using the Docker dev flow, ensure `lume serve` is running locally on port 7777 before invoking `./scripts/run-docker-dev.sh run`.
