# Wait for a DB and load data on it (for docker-compose). Only for Consul for the moment

[![Tests on push](https://github.com/nledez/wait-and-load/actions/workflows/tests.yml/badge.svg)](https://github.com/nledez/wait-and-load/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/nledez/wait-and-load/badge.svg?branch=main&service=github)](https://coveralls.io/github/nledez/wait-and-load?branch=main)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/nledez/wait-and-load?label=docker%20image)](https://hub.docker.com/repository/docker/nledez/wait-and-load)

## Requirements

Install [Poetry](https://python-poetry.org/docs/#installation) (>=1.2.1)

## Install

```
poetry install --with tests --with dev
```

## Tests & dev

```
poetry shell
ptw --nobeep --ignore .venv --onpass "terminal-notifier -title '✅' -message 'OK' ; coverage html" --onfail "terminal-notifier -title '🚨' -message 'KO'" -- --cov=wait_and_load --cov=tests
# Or only:
poetry run pytest -vvvvv --cov=wait_and_load --cov=tests && poetry run coverage html
```

## Use in docker compose

Get inspiration in `docker-compose.yml` and launch:
```
docker compose up
```

## Docker build multiarch

```
docker buildx build --push --platform=linux/amd64,linux/arm64 -t nledez/$(poetry version | sed 's/ /:/') .
```
