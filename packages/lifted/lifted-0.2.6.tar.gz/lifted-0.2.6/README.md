# lifted - a minimal parser combinator library.

See tests for example usage.
## Getting set up
```
python3 -mvenv env
env/bin/pip install -r requirements-dev.txt
```

## Building distribution

```
env/bin/python setup.py sdist bdist_wheel
```

## Uploading distribution

```
env/bin/twine upload dist/*
```
