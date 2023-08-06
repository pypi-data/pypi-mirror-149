: pip install --upgrade setuptools wheel
: pip install --upgrade twine
del /Q /S build
del /Q /S  dist

python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

: pip install --upgrade logcat_monitor