# Dev Setup

**Setup a virtual env (or use an existing one)**

```shell
cd ~/   # or someplace else
python3.9 -m venv venv39
```

> prefer using `python3.9-intel` on Apple Silicon

**Activate the virtual environment**

```shell
source ~/venv39/bin/activate
```

**Install `poetry` and `pre-commit`**

```shell
pip install poetry pre-commit
```

**Git clone**

```shell
git clone https://github.com/truefoundry/servicefoundry-cli
```

**Install pre-commit hooks**

```shell
cd servicefoundry-cli/
pre-commit install --install-hooks
```

> You can run the hook manually with `pre-commit run --all-files`



It is recommended to go through [Poetry Docs](https://python-poetry.org/docs/) to get a hang of development, testing and
packaging process

# Local Installation

```shell
poetry install
```

# Testing

```shell
poetry run pytest
```

# Build distributions

```shell
poetry build
```

# Usage :

- Login : `servicefoundry login`

- Init : `servicefoundry init`

- Run : `servicefoundry run`

# Process flow to use the commands

- servicefoundry (should hint to servicefoundry login)
- servicefoundry login (should hint to init, run from example folder)
- servicefoundry init (should hint to run)
- servicefoundry run (should hint to grafanaendpoint and servicefoundry get service <service_id>)

- servicefoundry list workspace
- servicefoundry list
