# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_example_dg']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['eve = poetry_example_dg.cli:cli']}

setup_kwargs = {
    'name': 'poetry-example-dg',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Notes\n\n## poetry\n- new\n- env use path_to_python\n\n[training video](https://youtu.be/G-OAVLBFxbw?t)\n\n### how to use package in editable mode\n\nadd:\n\n[tool.poetry.scripts]\nalias = \'package_name.script_name:function_name\'\n\ne.g.\n[tool.poetry.scripts]\neve = \'poetry_example_dg.cli:cli\'\n\n```bash\npoetry run eve \n```\n\n### vscode cant find poetry env\n\n```bash\npoetry config virtualenvs.in-project true\n```\n\nThe virtualenv will be created inside the project path and vscode will recognize.\n\nIf you already have created your project, you need to re-create the virtualenv to make it appear in the correct place:\n```bash\npoetry env list  # shows the name of the current environment\npoetry env remove <current environment>\npoetry install  # will create a new environment using your updated configuration\n```\n\n### testing\n```bash\npoetry run pytest\n```\n\n### getting package ready for publishing\n\nadd to toml:\n\n[tool.poetry]\nname = "dbt-cloud-cli-python-remake"\nversion = "0.1.0"\ndescription = ""\nauthors = ["David Griffiths <davidgg777@hotmail.com>"]\nlicense = "MIT"\nreadme = "README.md"\nhomepage = "https://github.com/wisemuffin/repo"\nrepository = "https://github.com/wisemuffin/repo"\nkeywords = ["wisemuffin"]\n\n### upload package to pypi\n\npoetry build - creates files in sdist (source format) and wheel (dist format)\npoetry publish - pushes to pypi\n\n:warning: *pypi prompting for password**: [see here!](https://youtu.be/G-OAVLBFxbw?t=1014)\n\nor\n\npoetry publish -r testpypi - make sure it looks good first\n\nhttps://test.pypi.org/project/project_name/\n\nnon pypi:\npoetry config repositories.my_repo https://foo.bar/simple/\npoetry publish -r my_repo\n',
    'author': 'David Griffiths',
    'author_email': 'davidgg777@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wisemuffin/poetry-example-dg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
