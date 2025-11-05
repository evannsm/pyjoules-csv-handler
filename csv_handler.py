# MIT License
# Copyright (c) 2019, INRIA
# Copyright (c) 2019, University of Lille
# All rights reserved.

import os
from . import EnergyHandler

class CSVHandler(EnergyHandler):
    """
    Custom CSVHandler that stores PyJoules energy traces inside
    data_analysis/energy_files/ automatically.
    """

    def __init__(self, filename: str, base_dir: str):
        """
        :param filename: name of the file (without or with .csv)
        :param base_dir: optional base directory (defaults to current working directory)
        """
        super().__init__()

        base_path = os.path.join(base_dir, 'data_analysis/') # Append the 'data_analysis' folder to the path
        parts = base_path.split(os.sep) # Split the path into components
        parts = ["src" if part in ("build","install") else part for part in parts] # Replace 'build' with 'src' if it exists in the path
        base_path = os.sep.join(parts) # Reconstruct the new path


        # Construct destination folder and ensure it exists
        energy_dir = os.path.join(base_path, 'energy_files')
        os.makedirs(energy_dir, exist_ok=True)

        # Normalize filename and make it full path
        # if not filename.endswith('.csv') and not filename.endswith('.log'):
        #     filename += '.csv'

        self._filename = os.path.join(energy_dir, filename)

        print(f"[pyjoules][CSVHandler] Writing energy log to: {self._filename}")

    def _gen_header(self, first_sample):
        domain_names = first_sample.energy.keys()
        return 'timestamp;tag;duration;' + ';'.join(domain_names)

    def _gen_sample_line(self, sample, domain_names):
        line_start = f'{sample.timestamp};{sample.tag};{sample.duration};'
        energy_values = [str(sample.energy[domain]) for domain in domain_names]
        return line_start + ';'.join(energy_values)

    def _init_file(self, first_sample):
        """Open CSV file and create header if it doesn’t exist."""
        mode = 'a+' if os.path.exists(self._filename) else 'w+'
        csv_file = open(self._filename, mode)
        if mode == 'w+':
            csv_file.write(self._gen_header(first_sample) + '\n')
        return csv_file

    def save_data(self):
        """Append processed trace to the CSV file."""
        flat_trace = self._flaten_trace()
        first_sample = flat_trace[0]
        domain_names = first_sample.energy.keys()

        csv_file = self._init_file(first_sample)
        for sample in flat_trace:
            csv_file.write(self._gen_sample_line(sample, domain_names) + '\n')
        csv_file.close()
        self.traces = []
