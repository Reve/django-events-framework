!#/bin/bash

python -m build --sdist --wheel --outdir dist/ .
twine check dist/*
twine upload --repository pypi dist/*