# readycheck
[![PyPI](https://img.shields.io/pypi/v/readycheck)](https://pypi.org/project/readycheck)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/readycheck)](https://pypi.org/project/readycheck)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/readycheck)](https://pypi.org/project/readycheck)
[![Read the Docs](https://img.shields.io/readthedocs/readycheck)](https://readycheck.readthedocs.io)
[![Travis CI](https://img.shields.io/travis/loic-simon/readycheck)](https://travis-ci.org/github/loic-simon/readycheck)

Python package providing utilities to check classes attributes when accessing it.


## Installation

Use the package manager [pip](https://pypi.org/project/pip) to install readycheck:
```bash
pip install readycheck
```

### Dependencies

* Python **≥ 3.5**


## Goal

The goal of this module is to allow to add custom checks when accessing class
attributes.

It is designed to build classes that store objects not available at import time
(e.g. later fetched from a distant service).  It avoid us the pain to check if
the connection has been established each time we need these objects: trying to
access them will automagically raise an exception if they are not ready.


## Usage

This package's main external API in the **`ReadyCheck`** class.

This class is **not meant** to be instantiated (see documentation for details),
but to be subclassed using a custom check function:

```py
from readycheck import ReadyCheck

class User(ReadyCheck, check_type=dict, check=lambda val: "name" in val):
    john = {"id": "<john_id>", "area": 2}
    jane = {"id": "<jane_id>", "area": 5}
```

Usage:

```
>>> User.john
Traceback (most recent call last):
  ...
readycheck.NotReadyError: 'john' is not ready yet!
>>> john_data = User.get_raw("john")
>>> User.john = some_lib.load_user(john_data)
>>> User.john
{'id': '<john id>', 'area': 2, 'name': 'John Doe', 'subscribed': False}
```

Read [the docs](https://readycheck.readthedocs.io) for more information.


## Contributing

Pull requests are welcome. Do not hesitate to get in touch with me (see below)
for any question or suggestion about this project!


## License

This work is shared under [the MIT license](LICENSE).

© 2022 Loïc Simon ([loic.simon@espci.org](mailto:loic.simon@espci.org))
