# Notes

## poetry
- new
- env use path_to_python

[training video](https://youtu.be/G-OAVLBFxbw?t)

### how to use package in editable mode

add:

[tool.poetry.scripts]
alias = 'package_name.script_name:function_name'

e.g.
[tool.poetry.scripts]
eve = 'poetry_example_dg.cli:cli'

```bash
poetry run eve 
```

### vscode cant find poetry env

```bash
poetry config virtualenvs.in-project true
```

The virtualenv will be created inside the project path and vscode will recognize.

If you already have created your project, you need to re-create the virtualenv to make it appear in the correct place:
```bash
poetry env list  # shows the name of the current environment
poetry env remove <current environment>
poetry install  # will create a new environment using your updated configuration
```

### testing
```bash
poetry run pytest
```

### getting package ready for publishing

add to toml:

[tool.poetry]
name = "dbt-cloud-cli-python-remake"
version = "0.1.0"
description = ""
authors = ["David Griffiths <davidgg777@hotmail.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/wisemuffin/repo"
repository = "https://github.com/wisemuffin/repo"
keywords = ["wisemuffin"]

### upload package to pypi

poetry build - creates files in sdist (source format) and wheel (dist format)
poetry publish - pushes to pypi

:warning: *pypi prompting for password**: [see here!](https://youtu.be/G-OAVLBFxbw?t=1014)

or

poetry publish -r testpypi - make sure it looks good first

https://test.pypi.org/project/project_name/

non pypi:
poetry config repositories.my_repo https://foo.bar/simple/
poetry publish -r my_repo
