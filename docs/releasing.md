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
git add package.json packages/core/pyproject.toml packages/core/uv.lock
git commit -m "release: v4.1.0"
git tag -a v4.1.0 -m "v4.1.0"
git push origin main v4.1.0
```

Replace `4.1.0` with the intended version. A `v*` tag starts one workflow that verifies the shared version, builds the Python distributions and desktop artifacts, publishes the Python package to PyPI, and creates the GitHub Release.

The workflow rejects a tag that does not exactly match `package.json`. Do not reuse a published tag or version.

## Validate the release workflow

The `Release` workflow can be run manually from the Actions tab. A manual run builds and validates the Python distributions and all desktop artifacts, but it does not publish to PyPI or create a GitHub Release.

Tag-triggered publishing is repository-aware:

- Tags in `EutropicAI/Final2x` publish to PyPI and create the official GitHub Release.
- Tags in a fork skip PyPI and create a prerelease in that fork, so the complete GitHub Release path can be tested without granting the fork access to the official PyPI project.

PyPI upload readiness is checked in every run with `twine check`. A successful fork validation confirms that the wheel and source distribution can be built and have valid package metadata; the official PyPI Trusted Publisher configuration remains the final authorization gate.

## Local checks

```shell
pnpm install --frozen-lockfile
pnpm run version:check
pnpm run core:sync
pnpm run core:generate
pnpm run core:lint
pnpm run core:test
pnpm run core:build
pnpm run lint
pnpm run typecheck
pnpm run test
```

Run `pnpm run core:bundle` before building a Windows or macOS desktop package locally. It builds the core from `packages/core` and stages it in the ignored `resources/Final2x-core` directory.
