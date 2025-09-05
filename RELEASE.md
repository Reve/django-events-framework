Release Guide

- Bump version:
  - Edit `setup.cfg:version` and commit.

- Tag the release:
  - `git tag vX.Y.Z`
  - `git push origin vX.Y.Z`

- Configure GitHub secrets (one-time):
  - `TEST_PYPI_API_TOKEN`: TestPyPI token (use `__token__` as username)
  - Optionally `PYPI_API_TOKEN` for real PyPI

- What happens:
  - CI runs tests on matrix (`.github/workflows/ci.yml`).
  - Publish workflow (`.github/workflows/publish.yml`) builds sdist/wheel and publishes to TestPyPI on tags matching `v*`.

- Verify on TestPyPI:
  - `pip install -i https://test.pypi.org/simple/ django-events-framework==X.Y.Z`

- Promote to PyPI (optional):
  - Uncomment the PyPI step in `.github/workflows/publish.yml` and add `PYPI_API_TOKEN` secret, then tag a new version.

