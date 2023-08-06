# flake8-pep604

flake8 plugin which forbids use of `typing.Union` (in favour of `|`), per [PEP
604](https://www.python.org/dev/peps/pep-0604/).

Note the `|` notation is a syntax error for Python \< 3.10. In this case you can
use the `annotations` feature (see [PEP 563](https://peps.python.org/pep-0563/)).

## flake8 Codes

| Code   | Description                                      |
|--------|--------------------------------------------------|
| UNT001 | Use `\|` in place of `typing.Union`. See PEP-604 |

## Motivation

Motivated by just wanting to make a codebase consistent in usage between
`typing.Union` and union types.

## Development

Get started by installing everything in a virtualenv

```
$ python -m .venv venv
$ pip install --requirement requirements-dev.txt
$ pre-commit install
```

Then testing:

```
$ pytest
```

And linting:

```
$ pre-commit run --all-files
```
