# HParm

HParm is a simple module build to load yaml files in both dot notation as well as dictionary access notation.

## Install hparm
```
pip install git+https://github.com/knoriy/hparm.git
```

## Examples

### Example yaml file and use case
```
paths:
  first_file: 'path/to/first_file.yaml'
  second_file: 'path/to/second_file.yaml'
variable:
  epochs:100
  batch: 16

```

```
from hparm import HParm

hp = hparm('dir/to/file.yaml')

# dictionary notation
hp['variable']['epochs]

# dot notation
hp.varaibles.epochs

```