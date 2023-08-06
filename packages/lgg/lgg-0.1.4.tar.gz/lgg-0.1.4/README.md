# python-logger
A simple yet fancy logger for Python scripts


## Install
- Using pip:
```shell
pip install lgg
```

- Using Poetry:
```shell
poetry add lgg
```

## Usage
```python
logger = get_logger()

logger.info('This is an info message')

logger.debug('Debugging message')

logger.error('error message')

logger.warning('DeprecationWarning: this feature won\'t'
               ' be available in the next release v0.10.0')
```
![Result](.resources/overview.png)
