# Directory handeler.

Create and handle directory.

## Install
```shell
pip install --upgrade dir-handeler==0.0.1
```

## Usage
```python

# Import Dir class
from dir_handeler.dir import Dir

# tmp directory current directory.
tmp_dir = Dir(name="tmp", parent="")

# test directory inside tmp directory.
tmp_dir = Dir(name="test", parent=tmp_dir)
```