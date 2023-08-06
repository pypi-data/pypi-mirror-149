# stvh

A collection of useful tools.

## Package building and uploading

Build package, requiring [build](https://pypa-build.readthedocs.io/en/stable/):

```sh
python -m build
```

Upload package to PyPI, requiring [Twine](https://twine.readthedocs.io/en/stable/):

```py
twine upload dist/*
```
