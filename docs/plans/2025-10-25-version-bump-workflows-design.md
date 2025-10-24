# Version Bump Workflows Design

**Date:** 2025-10-25
**Status:** Approved
**Author:** Design Session

## Overview

Replace Makefile-based bump2version commands with GitHub Actions workflow_dispatch workflows, providing clickable links in Development.md for easy version bumping.

## Requirements

1. Separate workflow for each of the 7 Python packages
2. Workflows automatically commit and push version bumps to main
3. Links in Development.md only (not in individual package READMEs)
4. Do NOT automatically trigger PyPI publish workflows
5. Include rollback instructions in Development.md

## Architecture

### Approach: Reusable Workflow Pattern

**Rationale:** Follows GitHub Actions best practices, maintains DRY principle, easy to update core logic.

**File Structure:**
```
.github/workflows/
├── bump-version-reusable.yml          # Core reusable workflow
├── bump-version-core.yml              # Caller for cua-core
├── bump-version-computer.yml          # Caller for cua-computer
├── bump-version-agent.yml             # Caller for cua-agent
├── bump-version-som.yml               # Caller for cua-som
├── bump-version-pylume.yml            # Caller for pylume
├── bump-version-computer-server.yml   # Caller for cua-computer-server
└── bump-version-mcp-server.yml        # Caller for cua-mcp-server
```

## Component Details

### Reusable Workflow

**File:** `.github/workflows/bump-version-reusable.yml`

**Inputs:**
- `package_name` (string): Display name (e.g., "cua-core")
- `package_directory` (string): Path relative to repo root (e.g., "libs/python/core")
- `bump_type` (string): patch/minor/major (passed from caller)

**Permissions:**
- `contents: write` - Required to push commits and tags

**Jobs:**
1. **checkout**: Fetch repository with full history (needed for tags)
2. **setup-python**: Install Python 3.11+
3. **install-bump2version**: Install via pip
4. **run-bump2version**:
   ```bash
   cd $package_directory
   bump2version $bump_type
   ```
5. **git-operations**:
   - Configure git user as github-actions bot
   - bump2version automatically commits changes and creates tag
   - Push commits and tags: `git push origin main --follow-tags`

**Authentication:** Uses `GITHUB_TOKEN` (automatically provided)

### Caller Workflows

**Pattern (all 7 workflows follow this):**

```yaml
name: Bump {package-name} Version

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
      package_name: '{package-name}'
      package_directory: 'libs/python/{package}'
      bump_type: ${{ inputs.bump_type }}
    secrets: inherit
```

**Package-Specific Values:**

| Workflow File | package_name | package_directory |
|--------------|--------------|-------------------|
| bump-version-core.yml | cua-core | libs/python/core |
| bump-version-computer.yml | cua-computer | libs/python/computer |
| bump-version-agent.yml | cua-agent | libs/python/agent |
| bump-version-som.yml | cua-som | libs/python/som |
| bump-version-pylume.yml | pylume | libs/python/pylume |
| bump-version-computer-server.yml | cua-computer-server | libs/python/computer-server |
| bump-version-mcp-server.yml | cua-mcp-server | libs/python/mcp-server |

## Development.md Changes

### Replace "Releasing Packages" Section

**New content includes:**

1. **Link table** with workflow_dispatch links for all packages:
   ```markdown
   ### cua-core
   - [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-core.yml) - Select patch/minor/major

   ### cua-computer
   - [Bump Version](https://github.com/trycua/cua/actions/workflows/bump-version-computer.yml) - Select patch/minor/major

   ... (continue for all 7 packages)
   ```

2. **Branch Protection Note:**
   ```markdown
   > **Note:** The main branch is currently not protected. If branch protection is enabled in the future,
   > the github-actions bot must be added to the bypass list for these workflows to commit directly.
   ```

3. **Rollback Instructions:**
   ```markdown
   ### Rolling Back a Version Bump

   If you need to revert a version bump:

   1. Find the version bump commit hash:
      ```bash
      git log --oneline | grep "Bump {package-name}"
      ```

   2. Revert the commit:
      ```bash
      git revert <commit-hash>
      ```

   3. Delete the tag locally and remotely:
      ```bash
      # Find the tag (usually v{version})
      git tag -l

      # Delete locally
      git tag -d v{version}

      # Delete remotely
      git push origin :refs/tags/v{version}
      ```

   4. Push the revert:
      ```bash
      git push origin main
      ```

   **Per-package examples:**
   - cua-core: Look for tags like `v0.1.x` in `libs/python/core`
   - cua-computer: Look for tags like `v0.1.x` in `libs/python/computer`
   - etc.
   ```

## Error Handling

### Potential Failures

1. **bump2version fails**:
   - Cause: Missing or invalid `.bumpversion.cfg`
   - Effect: Workflow fails immediately, no commit made
   - Resolution: Check .bumpversion.cfg syntax

2. **Push fails**:
   - Cause: Non-fast-forward (someone pushed between checkout and push)
   - Effect: Git push fails
   - Resolution: Re-run workflow (will fetch latest)

3. **Wrong directory**:
   - Cause: Incorrect `package_directory` in caller workflow
   - Effect: bump2version can't find .bumpversion.cfg
   - Resolution: Fix package_directory parameter

4. **Permissions**:
   - Cause: GITHUB_TOKEN lacks write access
   - Effect: Push fails
   - Resolution: Ensure `permissions: contents: write` in workflow

### Edge Cases

- **Double-trigger**: Second run fails (version already bumped, nothing to commit) - acceptable
- **Manual edits**: bump2version handles correctly (bumps from current version)
- **No rollback automation**: Manual rollback required (documented in Development.md)

## Migration from Makefile

### Deprecate but Keep

Keep the Makefile targets for local testing, but update Development.md to recommend GitHub Actions workflows as the primary method.

**Makefile note to add:**
```makefile
# NOTE: For releases, prefer using GitHub Actions workflows (see Development.md)
# These targets are kept for local testing only
```

## Future Considerations

1. **PyPI publish integration**: Could add workflow_dispatch input to optionally trigger publish after bump
2. **Changelog generation**: Could integrate changelog updates in version bump workflow
3. **PR-based flow**: If branch protection is added, switch to creating PRs instead of direct push
4. **Notification**: Could add Slack/Discord notifications on successful version bumps

## Success Criteria

- [ ] 7 caller workflow files created and working
- [ ] 1 reusable workflow file created and working
- [ ] Development.md updated with links to all workflows
- [ ] Development.md includes branch protection note
- [ ] Development.md includes rollback instructions for each package
- [ ] Manual test: Successfully bump a package version via workflow_dispatch
- [ ] Verify: Commit, tag, and push happen automatically
- [ ] Verify: Links in Development.md navigate to correct workflows
