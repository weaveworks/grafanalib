
GLaDOS team publish changes to SR Nexus repo. All version are named with `postX` prefix.

Please perform following commands to build and publish a new version:

```
# Check setyp.py and increase version (only postX part, do not touch native major, minor and patch components)
# make and activate venv


pip3 install tox flake8
make deps
make all


pip install wheel
rm -rf dist
python setup.py sdist bdist_wheel

twine upload -r srai dist/*
```
