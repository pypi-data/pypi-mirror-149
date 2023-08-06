# ITk DB v0.4.0rc1

[![PyPI version](https://badge.fury.io/py/itkdb.svg)](https://badge.fury.io/py/itkdb)
[![Downloads](https://pepy.tech/badge/itkdb)](https://pepy.tech/project/itkdb) [![Downloads](https://pepy.tech/badge/itkdb/month)](https://pepy.tech/project/itkdb) [![Downloads](https://pepy.tech/badge/itkdb/week)](https://pepy.tech/project/itkdb)

To install as a user

```
pip install itkdb
```

or if you wish to develop/contribute

```
git clone ...
pip install -e .[develop]
```

or

```
git clone ...
pip install -e .[complete]
```

## Using

Command line available via

```
itkdb --help
```

## Environment Variables

See [itkdb/settings/base.py](src/itkdb/settings/base.py) for all environment variables that can be set. All environment variables for this package are prefixed with `ITKDB_`. As of now, there are:

* `ITKDB_ACCESS_CODE1`: access code #1 for authentication
* `ITKDB_ACCESS_CODE2`: access code #2 for authentication
* `ITKDB_ACCESS_SCOPE`: scope for the access token authentication request
* `ITKDB_AUTH_URL`: authentication server
* `ITKDB_SITE_URL`: API server
* `ITKDB_CASSETTE_LIBRARY_DIR`: for tests, where to store recorded requests/responses

## Develop

### Bump Version

Run `bump2version x.y.z` to bump to the next version. We will always tag any version we bump, and this creates the relevant commits/tags for you. All you need to do is `git push --tags` and that should be it.

# Examples

```
import itkdb

client = itkdb.Client()
comps = client.get(
    'listComponents', json={'project': 'P', 'pageInfo': {'pageSize': 32}}
)

for i, comp in enumerate(comps):
    print(i, comp['code'])
```
