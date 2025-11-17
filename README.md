# pyjoules-csv-handler

Find where your pyJoules lives:
```bash
python -c "import pyJoules, inspect; print(inspect.getfile(pyJoules))"
```

Use with
```python
csv_handler = CSVHandler(log_file, base_path)
```
