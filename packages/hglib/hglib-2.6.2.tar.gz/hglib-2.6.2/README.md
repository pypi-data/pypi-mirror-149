# hglib

The hglib is fork of of [hglib](https://www.mercurial-scm.org/wiki/PythonHglib), which is library with a fast, convenient interface to Mercurial. It uses Mercurial's command server for communication with hg.

Only difference for now is just name of the package and updated tests.

## Basic usage

```python
import hglib

client = hglib.open(path)
log = client.log(revrange="tip")
print(log)
```

## Dependencies ##

* Python 2.7 or 3.5

## Licence ##

MIT

## Contact ##

Michal Siska <michal.515k4@gmail.com>
