# Releasing Final2x

Final2x desktop and the `Final2x-core` Python package use the version in the root `package.json`. The Python project keeps a synchronized PEP 621 version so its source and wheel metadata remain explicit.

## One-time PyPI setup

Configure a PyPI Trusted Publisher for the existing `Final2x-core` project with:

- Owner: `EutropicAI`
- Repository: `Final2x`
- Workflow: `Release.yml`
- Environment: `pypi`

Create the matching `pypi` environment in the GitHub repository. The release workflow requests a short-lived OIDC credential, so the old `PYPI_API` repository secret is not copied into the monorepo.

## Prepare a release

From a clean `main` checkout:

```shell
pnpm version 4.1.0 --no-git-tag-version
pnpm run version:sync
pnpm run version:check
git add package.json core/pyproject.toml core/uv.lock
git commit -m "release: v4.1.0"
git tag -a v4.1.0 -m "v4.1.0"
git push origin main v4.1.0
```

Replace `4.1.0` with the intended version. A `v*` tag starts one workflow that verifies the shared version, builds the desktop artifacts, builds and publishes the Python package from the PyPI job, and creates the GitHub Release.

The workflow rejects a tag that does not exactly match `package.json`. Do not reuse a published tag or version.

## Validate the release workflow

The `Release` workflow can be run manually from the Actions tab. A manual run verifies the shared version and builds all desktop artifacts, but it does not run the test suites, publish to PyPI, or create a GitHub Release.

Tag-triggered publishing is repository-aware:

- Tags in `EutropicAI/Final2x` publish to PyPI and create the official GitHub Release.
- Tags in a fork skip PyPI and create a prerelease in that fork, so the complete GitHub Release path can be tested without granting the fork access to the official PyPI project.

Python unit tests, standalone Core bundle tests, wheel installation tests, and the supported PyTorch compatibility matrix run in `CI-test-core.yml`. Release jobs consume the same root `package.json` commands but do not repeat those tests. The official PyPI Trusted Publisher configuration remains the final authorization gate.

## Local checks

```shell
pnpm install --frozen-lockfile
pnpm run version:check
pnpm run core:sync
pnpm run core:check
pnpm run lint
pnpm run core:build
pnpm run typecheck
pnpm run test
```

Run `pnpm run core:bundle` before building a Windows or macOS desktop package locally. It builds the core in `core/dist/Final2x-core`; copy it with `cp -R core/dist/Final2x-core resources/` on macOS or `Copy-Item core\dist\Final2x-core resources\Final2x-core -Recurse` in Windows PowerShell before running the desktop build, matching the CI and release workflows.
