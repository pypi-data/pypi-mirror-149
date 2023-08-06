# easy_file_manager
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

Lets users conveniently choose multiple files.
## Installation
The program can be installed from PyPi or GitHub
```
# From PyPi
python -m pip install easy-file-manager

# From GitHub.com
python -m pip install git+https://github.com/lstuma/easy_file_manager
```
## Usage
### Python Module
```python
from easy_file_manager import EasyFileSelect()

# Instantiate EasyFileSelect object
file_manager = EasyFileSelect()

# Open file selection: Returns filepaths
filepaths = file_manager.file_selection()
```
