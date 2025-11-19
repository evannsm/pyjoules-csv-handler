# pyjoules-csv-handler

Find where your pyJoules lives:
```bash
python -c "import pyJoules, inspect; print(inspect.getfile(pyJoules))"
```

Ensure pyRAPL has permissions
```bash
sudo chmod -R a+r /sys/class/powercap/intel-rapl
```



Use with
```python
csv_handler = CSVHandler(log_file, base_path)
```
