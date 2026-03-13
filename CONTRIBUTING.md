# Contributing

## Setting up for development

- Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
- `uv sync`
- (Optional but recommended) Install the pre-commit hooks, which will
  format and lint your git staged files:

```
uv run pre-commit install
```

- To run tests:

```
uv run pytest
```

- To run syntax checks:

```
uv run tox -e lint
```
