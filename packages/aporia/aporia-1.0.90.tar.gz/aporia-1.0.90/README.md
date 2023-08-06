# Aporia SDK

## Testing

To run the tests, first install the library locally:
```
pip install ".[all]" --upgrade
```

Then run the tests using `pytest`:
```
pytest -v
```

If you don't have Spark installed, skip the pyspark tests:
```
pytest -v --ignore=tests/pyspark
```
