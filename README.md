# pyroll
**Dice notation parsing and rolling**

### Installation
`pip install pyroll`

### Usage
#### As a program
```shell script
usage: pyroll [-h] [-v, --verbose] DICE [DICE ...]

Dice notation parsing and rolling

positional arguments:
  DICE

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Include dice notation in output

```

#### As a library
```python
    import pyroll

    result = pyroll.roll('2d4+1d12-2')
```
