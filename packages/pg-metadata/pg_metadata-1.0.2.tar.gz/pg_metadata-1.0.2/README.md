# Description

PostgreSQL metadata (DDL) grabber and database schema diff

# Dependencies

* [Python 3](https://www.python.org/downloads/)
* [psycopg2](https://pypi.org/project/psycopg2/)

# Installation

```bash
pip install psycopg2-binary pg-metadata
```

# Grabbing

1 ) Create config file with connection params and other settings:

```json
{
    "connect": {
        "host": "localhost",
        "port": 5432,
        "database": "db",
        "username": "some_user",
        "password": "some_password"
    },
    "path": "/some/path/to/grabber/result/folder",
    "exclude_schemas": [
        "information_schema",
        "pg_catalog"
    ],
    "threads": 8
}
```

2 ) By default script opens config file `config_grab.json` from the same directory as `zzz_Grabber.py` file.

3 ) Alternatively you can specify path to config file as a first run parameter.

4 ) Run grabber:

```bash
# Run with default config (config_grab.json)
python "zzz_Grabber.py"
# Run with specified config file path
python "zzz_Grabber.py" "/some/path/to/config.json"
```

# Compare (diff) databases

1 ) Create config file with connection params and other settings:

```json
{
    "source": {
        "host": "localhost",
        "port": 5432,
        "database": "db_from",
        "username": "user",
        "password": "password"
    },
    "target": {
        "host": "localhost",
        "port": 5432,
        "database": "db_to",
        "username": "user",
        "password": "password"
    },
    "path": "/some/path/to/compare/result/folder",
    "exclude_schemas": [
        "information_schema",
        "pg_catalog"
    ]
}
```

2 ) By default script opens config file `config_diff.json` from the same directory as `zzz_Grabber.py` file.

3 ) Alternatively you can specify path to config file as a first run parameter.

4 ) Run diff:

```bash
# Run with default config (config_grab.json)
python "zzz_Diff.py"
# Run with specified config file path
python "zzz_Diff.py" "/some/path/to/config.json"
```

# Links

* [GitHub](https://github.com/ish1mura/pg_metadata)
* [PyPI](https://pypi.org/project/pg-metadata/)
