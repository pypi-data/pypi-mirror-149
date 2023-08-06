# xlsxq

xlsxq is a lightweight and flexible command-line .xlsx processor.

# Usage

This is a beta version and specifications are subject to change.

```bash
# Show help message and exit.
xlsxq -h

# List worksheets.
xlsxq sheet list --infile infile.xlsx --output json

# Show range values.
xlsxq range show --infile infile.xlsx --sheet 'Sheet1' --range 'A1:B3' --output json

# Show range values in tab-delimited format.
xlsxq range show --infile infile.xlsx --sheet 'Sheet1' --range 'A1:B3' --output tsv
```

# Requirements

* Python 3.9+

# Installation

```bash
pip install -U xlsxq
```

# TODO

* Write docs
