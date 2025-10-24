# Version Bump Workflows Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace Makefile-based bump2version commands with GitHub Actions workflow_dispatch workflows accessible via links in Development.md.

**Architecture:** Reusable workflow pattern with one core workflow containing bump2version logic, and 7 caller workflows (one per Python package) that invoke the reusable workflow with package-specific parameters.

**Tech Stack:** GitHub Actions, bump2version, git

---

## Task 1: Create Reusable Workflow

**Files:**

- Create: `.github/workflows/bump-version-reusable.yml`

**Step 1: Create the reusable workflow file**

Create `.github/workflows/bump-version-reusable.yml`:

```yaml
name: Bump Version (Reusable)

on:
  workflow_call:
    inputs:
      package_name:
        description: 'Package display name (e.g., cua-core)'
        required: true
        type: string
      package_directory:
        description: 'Package directory relative to repo root (e.g., libs/python/core)'
        required: true
        type: string
      bump_type:
        description: 'Version bump type (patch, minor, or major)'
        required: true
        type: string

permissions:
  contents: write

jobs:
  bump-version:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install bump2version
        run: pip install bump2version

      - name: Configure Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Run bump2version
        run: |
          cd ${{ inputs.package_directory }}
          bump2version ${{ inputs.bump_type }}

      - name: Push changes
        run: |
          git push origin main --follow-tags
```

**Step 2: Validate YAML syntax**

Run: `yamllint .github/workflows/bump-version-reusable.yml` (if available) or use online validator

Expected: No syntax errors

**Step 3: Verify structure**

Check that:

- File has correct `workflow_call` trigger
- All 3 inputs are defined (package_name, package_directory, bump_type)
- Permissions include `contents: write`
- Steps follow correct order: checkout → setup → install → git config → bump → push

**Step 4: Commit**

```bash
git add .github/workflows/bump-version-reusable.yml
git commit -m "feat: add reusable bump version workflow"
```

---

## Task 2: Create Caller Workflow for cua-core

**Files:**

- Create: `.github/workflows/bump-version-core.yml`

**Step 1: Create the caller workflow file**

Create `.github/workflows/bump-version-core.yml`:

```yaml
name: Bump cua-core Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    uses: ./.github/workflows/bump-version-reusable.yml
    with:
      package_name: 'cua-core'
      package_directory: 'libs/python/core'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Step 2: Validate YAML syntax**

Run: Check syntax with validator

Expected: No syntax errors

**Step 3: Verify structure**

Check that:

- File has `workflow_dispatch` trigger with bump_type input
- Input type is `choice` with options: patch, minor, major
- Job calls reusable workflow with correct path
- Package-specific values are correct: 'cua-core' and 'libs/python/core'
- `secrets: inherit` is present

**Step 4: Commit**

```bash
git add .github/workflows/bump-version-core.yml
git commit -m "feat: add bump version workflow for cua-core"
```

---

## Task 3: Create Caller Workflow for cua-computer

**Files:**

- Create: `.github/workflows/bump-version-computer.yml`

**Step 1: Create the caller workflow file**

Create `.github/workflows/bump-version-computer.yml`:

```yaml
name: Bump cua-computer Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    uses: ./.github/workflows/bump-version-reusable.yml
    with:
      package_name: 'cua-computer'
      package_directory: 'libs/python/computer'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Step 2: Validate and verify**

Check syntax and structure (same as Task 2)

**Step 3: Commit**

```bash
git add .github/workflows/bump-version-computer.yml
git commit -m "feat: add bump version workflow for cua-computer"
```

---

## Task 4: Create Caller Workflow for cua-agent

**Files:**

- Create: `.github/workflows/bump-version-agent.yml`

**Step 1: Create the caller workflow file**

Create `.github/workflows/bump-version-agent.yml`:

```yaml
name: Bump cua-agent Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    uses: ./.github/workflows/bump-version-reusable.yml
    with:
      package_name: 'cua-agent'
      package_directory: 'libs/python/agent'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Step 2: Validate and verify**

Check syntax and structure

**Step 3: Commit**

```bash
git add .github/workflows/bump-version-agent.yml
git commit -m "feat: add bump version workflow for cua-agent"
```

---

## Task 5: Create Caller Workflow for cua-som

**Files:**

- Create: `.github/workflows/bump-version-som.yml`

**Step 1: Create the caller workflow file**

Create `.github/workflows/bump-version-som.yml`:

```yaml
name: Bump cua-som Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    uses: ./.github/workflows/bump-version-reusable.yml
    with:
      package_name: 'cua-som'
      package_directory: 'libs/python/som'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Step 2: Validate and verify**

Check syntax and structure

**Step 3: Commit**

```bash
git add .github/workflows/bump-version-som.yml
git commit -m "feat: add bump version workflow for cua-som"
```

---

## Task 6: Create Caller Workflow for pylume

**Files:**

- Create: `.github/workflows/bump-version-pylume.yml`

**Step 1: Create the caller workflow file**

Create `.github/workflows/bump-version-pylume.yml`:

```yaml
name: Bump pylume Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    uses: ./.github/workflows/bump-version-reusable.yml
    with:
      package_name: 'pylume'
      package_directory: 'libs/python/pylume'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Step 2: Validate and verify**

Check syntax and structure

**Step 3: Commit**

```bash
git add .github/workflows/bump-version-pylume.yml
git commit -m "feat: add bump version workflow for pylume"
```

---

## Task 7: Create Caller Workflow for cua-computer-server

**Files:**

- Create: `.github/workflows/bump-version-computer-server.yml`

**Step 1: Create the caller workflow file**

Create `.github/workflows/bump-version-computer-server.yml`:

```yaml
name: Bump cua-computer-server Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    uses: ./.github/workflows/bump-version-reusable.yml
    with:
      package_name: 'cua-computer-server'
      package_directory: 'libs/python/computer-server'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Step 2: Validate and verify**

Check syntax and structure

**Step 3: Commit**

```bash
git add .github/workflows/bump-version-computer-server.yml
git commit -m "feat: add bump version workflow for cua-computer-server"
```

---

## Task 8: Create Caller Workflow for cua-mcp-server

**Files:**

- Create: `.github/workflows/bump-version-mcp-server.yml`

**Step 1: Create the caller workflow file**

Create `.github/workflows/bump-version-mcp-server.yml`:

```yaml
name: Bump cua-mcp-server Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: 'Version bump type'
        required: true
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  bump:
    uses: ./.github/workflows/bump-version-reusable.yml
    with:
      package_name: 'cua-mcp-server'
      package_directory: 'libs/python/mcp-server'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Step 2: Validate and verify**

Check syntax and structure

**Step 3: Commit**

```bash
git add .github/workflows/bump-version-mcp-server.yml
git commit -m "feat: add bump version workflow for cua-mcp-server"
```

---

## Task 9: Update Development.md

**Files:**

- Modify: `Development.md` (replace "Releasing Packages" section)

**Step 1: Read the current Development.md**

Run: `cat Development.md | grep -A 50 "## Releasing Packages"`

Expected: See current content about Makefile and bump2version

**Step 2: Replace the "Releasing Packages" section**

Replace the entire "Releasing Packages" section (starting at line ~350) with:

````markdown
## Releasing Packages

Cua uses automated GitHub Actions workflows to bump package versions. Click the links below to trigger a version bump:

> **Note:** The main branch is currently not protected. If branch protection is enabled in the future, the github-actions bot must be added to the bypass list for these workflows to commit directly.

### Version Bump Workflows

| Package                 | Workflow Link                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------------ |
| **cua-core**            | [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-core.yml)            |
| **cua-computer**        | [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-computer.yml)        |
| **cua-agent**           | [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-agent.yml)           |
| **cua-som**             | [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-som.yml)             |
| **pylume**              | [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-pylume.yml)          |
| **cua-computer-server** | [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-computer-server.yml) |
| **cua-mcp-server**      | [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-mcp-server.yml)      |

**How to use:**

1. Click the workflow link for the package you want to bump
2. Click the "Run workflow" button in the GitHub UI
3. Select the bump type from the dropdown (patch/minor/major)
4. Click "Run workflow" to start the version bump
5. The workflow will automatically commit changes and push to main

### Rolling Back a Version Bump

If you need to revert a version bump, follow these steps:

**Step 1: Find the version bump commit**

```bash
# List recent commits
git log --oneline | grep "Bump"

# Example output:
# a1b2c3d Bump version: 0.1.8 → 0.1.9
```
````

**Step 2: Revert the commit**

```bash
# Revert the specific commit
git revert <commit-hash>

# Example:
# git revert a1b2c3d
```

**Step 3: Delete the git tag**

```bash
# List tags to find the version tag
git tag -l

# Delete the tag locally
git tag -d v0.1.9

# Delete the tag remotely
git push origin :refs/tags/v0.1.9
```

**Step 4: Push the revert**

```bash
git push origin main
```

**Per-package tag patterns:**

- All packages use tags like `v{version}` (e.g., `v0.1.9`, `v1.0.0`)
- Each package's .bumpversion.cfg defines the exact tag format

### Local Testing (Advanced)

The Makefile targets are kept for local testing only:

```bash
# Test version bump locally (dry run)
make dry-run-patch-core

# View current versions
make show-versions
```

**Note:** For production releases, always use the GitHub Actions workflows above instead of running Makefile commands directly.

````

**Step 3: Verify the changes**

Run: `grep -A 5 "## Releasing Packages" Development.md`

Expected: See new content with workflow links table

**Step 4: Commit**

```bash
git add Development.md
git commit -m "docs: update Development.md with version bump workflow links"
````

---

## Task 10: Add Note to Makefile (Optional)

**Files:**

- Modify: `Makefile`

**Step 1: Add deprecation note at the top of version bump section**

Find the version bump targets section in Makefile and add this comment at the top:

```makefile
# NOTE: For production releases, prefer using GitHub Actions workflows (see Development.md)
# These targets are kept for local testing and dry-runs only.
```

**Step 2: Commit**

```bash
git add Makefile
git commit -m "docs: add note to Makefile about preferring workflows"
```

---

## Verification Steps

After completing all tasks, verify the implementation:

**1. Check all workflow files exist:**

```bash
ls -la .github/workflows/bump-version*.yml
```

Expected: 8 files (1 reusable + 7 caller workflows)

**2. Verify Development.md has links:**

```bash
grep "bump-version-core.yml" Development.md
```

Expected: Link to workflow found

**3. Test one workflow manually:**

- Navigate to: https://github.com/trycua/cua/actions/workflows/bump-version-core.yml
- Click "Run workflow"
- Select "patch"
- Click "Run workflow"
- Verify it runs successfully and creates a commit + tag

**4. Final commit and push:**

```bash
git status
git push origin feature/version-bump-workflows
```

---

## Success Criteria

- ✅ 1 reusable workflow file created
- ✅ 7 caller workflow files created (one per package)
- ✅ Development.md updated with workflow links table
- ✅ Development.md includes branch protection note
- ✅ Development.md includes rollback instructions
- ✅ Makefile includes deprecation note
- ✅ All changes committed with clear commit messages
- ✅ Manual test of at least one workflow succeeds
