Release Guide

- Bump version:
  - Edit `setup.cfg:version` and commit.

- Push the release commit and wait for CI to pass:
  - `git push origin main`

- Configure Trusted Publishing (one-time):
  - Create the GitHub Actions environment `pypi` in `Reve/django-events-framework`.
  - In PyPI's `django-events-framework` project, open Publishing and add a GitHub publisher:
    - Owner: `Reve`
    - Repository: `django-events-framework`
    - Workflow: `publish.yml`
    - Environment: `pypi`

- Tag the verified release commit:
  - `git tag -a vX.Y.Z -m "Release X.Y.Z"`
  - `git push origin vX.Y.Z`

- What happens:
  - The publish workflow builds and validates the sdist and wheel.
  - A separate publishing job downloads those artifacts and authenticates to PyPI through GitHub OIDC in the `pypi` environment.

- Verify on PyPI:
  - `pip install django-events-framework==X.Y.Z`

