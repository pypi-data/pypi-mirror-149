# simpleprofiler
Tool to profile your code in python

## Installation

`pip install simpleprofiler`

## Logging Level

Defaultly simpleprofiler use INFO as logging level

## Example

Code: 

```python
from simpleprofiler import get_profile

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
_logger = logging.getLogger(__name__)

@get_profile
def try_func(bool, arr):
    if bool:
        for item in arr:
            _logger.info(item)
    else:
        for item in arr:
            _logger.info(info)

try_func(True, ["try" * 10])
```

On Console:

```
try_func >  calls     ms
try_func >  ------------------------------------ /DIRECTORY_TO/example.py, 8

try_func > 1         0.0       @get_profile
try_func >                     def try_func(bool, arr):
try_func > 1         0.0           if bool:
try_func > 2         0.0               for item in arr:
try_func > 1         0.21                  _logger.info(item)
try_func >                         else:
try_func >                             for item in arr:
try_func >                                 _logger.info(item)

try_func > Total:
try_func > 1         0.21  
```