# Release Process

This document describes how to create and publish a new release of `noonapi`.

Releases are triggered by pushing a Git tag matching `v*` (e.g. `v0.1.0`).
Publishing to PyPI requires manual approval via the `pypi` environment.

---

## Overview

Release flow:

1. Finish development on a feature branch (normal PR workflow)
2. Create a `release/vX.Y.Z` branch based on the feature branch tip
3. Apply release-only changes (version bump, README tweaks if needed)
4. Open a PR from `release/vX.Y.Z` into `master` and merge it
5. Create and push the `vX.Y.Z` git tag from `master`
6. Approve the GitHub Actions deployment
7. Verify the package on PyPI

---

## 1. Finish development on a feature branch

Work on a feature branch, open a PR, and get it approved.

Do not change the release version inside the feature branch unless required.

Example branch name:
- `feature/auth-errors`
- `fix/session-docs`

---

## 2. Create a release branch from the feature branch

After the feature PR is ready (and you want to ship it), create a release branch from the feature branch tip:

```bash
git checkout feature/auth-errors
git pull origin feature/auth-errors
git checkout -b release/v0.1.1
git push origin release/v0.1.1
````

---

## 3. Bump version and apply release-only changes

Update the version in `pyproject.toml`:

```toml
version = "0.1.1"
```

Follow semantic versioning:

* Patch release (bugfix): `0.1.0` → `0.1.1`
* Minor release (new features, no breaking changes): `0.1.0` → `0.2.0`
* Breaking changes (pre-1.0): increment minor

Commit the release-only changes:

```bash
git add pyproject.toml README.md
git commit -m "Release v0.1.1"
git push origin release/v0.1.1
```

---

## 4. Open a PR from release branch into master

Open a PR:

* Base: `master`
* Compare: `release/v0.1.1`

Requirements before merge:

* CI must pass
* Code review completed

Merge the PR (prefer **Squash & Merge** unless there is a reason not to).

---

## 5. Tag master

After the release PR is merged, tag the commit on `master`:

```bash
git checkout master
git pull origin master
git tag v0.1.1
git push origin v0.1.1
```

This triggers the `Release` GitHub Actions workflow.

---

## 6. Approve the deployment

The workflow will pause and wait for approval because it uses the `pypi` environment.

Steps:

1. Go to GitHub → Actions
2. Open the running `Release` workflow
3. Click **Review deployments**
4. Approve the deployment

After approval, the workflow will build and publish to PyPI.

---

## 7. Verify the release

After the workflow completes:

1. Check the project on PyPI:
   [https://pypi.org/project/noonapi/](https://pypi.org/project/noonapi/)
2. Install the new version locally:

```bash
pip install noonapi==0.1.1
```

3. Verify import works:

```python
from noonapi import NoonSession
```

---

## Important Rules

* Never modify or overwrite an existing published version.
* Never publish directly from local machines.
* Never force-push tags.
* If a release has incorrect metadata, publish a new patch version.
* All releases must go through GitHub Actions and the manual approval gate.

---

## If a Release Fails

If the workflow fails before publishing:

* Fix the issue on a new commit (preferably via PR)
* Re-run the workflow if possible
* If needed, delete the tag and re-create it after fixing

If the version was already published:

* Do not attempt to overwrite it
* Publish a new patch version instead

---

## Local Dry Run (Optional)

Before tagging, you can verify packaging locally:

```bash
uv sync --group dev
uv run python -m build
```

---

## Summary Checklist

* [ ] Feature branch is ready to ship
* [ ] Release branch `release/vX.Y.Z` created from feature branch tip
* [ ] Version bumped in `pyproject.toml`
* [ ] Release PR opened and merged into `master`
* [ ] Tag `vX.Y.Z` created from `master` and pushed
* [ ] Deployment approved
* [ ] PyPI verified