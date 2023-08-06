# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_template',
 'fastapi_template.template.hooks',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_ormar',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_ormar.dao',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_ormar.migrations',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_ormar.migrations.versions',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_ormar.models',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_piccolo',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_piccolo.dao',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_piccolo.migrations',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_piccolo.models',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_psycopg',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_psycopg.dao',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_psycopg.models',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_sa',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_sa.dao',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_sa.migrations',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_sa.migrations.versions',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_sa.models',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_tortoise',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_tortoise.dao',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_tortoise.models',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.services',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.services.rabbit',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.services.redis',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.tests',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.api',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.api.docs',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.api.dummy',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.api.echo',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.api.monitoring',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.api.rabbit',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.api.redis',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.gql',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.gql.dummy',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.gql.echo',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.gql.rabbit',
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.web.gql.redis',
 'fastapi_template.tests']

package_data = \
{'': ['*'],
 'fastapi_template': ['template/*',
                      'template/{{cookiecutter.project_name}}/*',
                      'template/{{cookiecutter.project_name}}/.github/workflows/*',
                      'template/{{cookiecutter.project_name}}/deploy/*',
                      'template/{{cookiecutter.project_name}}/deploy/kube/*'],
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}': ['static/docs/*'],
 'fastapi_template.template.{{cookiecutter.project_name}}.{{cookiecutter.project_name}}.db_tortoise': ['migrations/models/*']}

install_requires = \
['cookiecutter>=1.7.3,<2.0.0',
 'pre-commit>=2.14.0,<3.0.0',
 'prompt-toolkit>=3.0.19,<4.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['fastapi_template = fastapi_template.__main__:main']}

setup_kwargs = {
    'name': 'fastapi-template',
    'version': '3.3.4',
    'description': 'Feature-rich robust FastAPI template',
    'long_description': '![python version](https://img.shields.io/pypi/pyversions/fastapi_template?style=for-the-badge) ![Build status](https://img.shields.io/github/workflow/status/s3rius/FastAPI-template/Release%20python%20package?style=for-the-badge) [![version](https://img.shields.io/pypi/v/fastapi_template?style=for-the-badge)](https://pypi.org/project/fastapi-template/)\n[![](https://img.shields.io/pypi/dm/fastapi_template?style=for-the-badge)](https://pypi.org/project/fastapi-template/)\n<div align="center">\n<img src="https://raw.githubusercontent.com/s3rius/FastAPI-template/master/images/logo.png" width=700>\n<div><i>Flexible and Lightweight general-purpose template for FastAPI.</i></div>\n</div>\n\n## Usage\n\n⚠️ [Git](https://git-scm.com/downloads), [Python](https://www.python.org/) and [Poetry](https://python-poetry.org/) must be installed and accessible ⚠️\n\nPoetry version must be greater or equal than 1.1.8. Otherwise it won\'t be able to install SQLAlchemy.\n\n```bash\npython3 -m pip install fastapi_template\npython3 -m fastapi_template\n# or fastapi_template\n# Answer all the questions\n# 🍪 Enjoy your new project 🍪\ncd new_project\ndocker-compose -f deploy/docker-compose.yml --project-directory . build\ndocker-compose -f deploy/docker-compose.yml --project-directory . up --build\n```\n\nIf you want to install in from sources then try this:\n```shell\npython3 -m pip install poetry\npython3 -m pip install .\npython3 -m fastapi_template\n```\n\nAlso you can use it with docker.\n```bash\ndocker run --rm -it -v "$(pwd):/projects" s3rius/fastapi_template\n```\n\n<div align="center">\n  <img src="https://user-images.githubusercontent.com/18153319/137182689-ce714440-7576-46a0-8f96-862a8469a28c.gif"/>\n  <p>Templator in action</p>\n</div>\n\n\n## Features\n\nOne of the coolest features is that this project is extremely small and handy.\nYou can choose between different databases and even ORMs. \nCurrently SQLAlchemy1.4, TortoiseORM and Ormar are supported.\n\nTUI and CLI and excellent code documentation.\n\nGenerator features:\n- You can choose between GraphQL and REST api;\n- Different databases support;\n- Different ORMs support;\n- Optional migrations for each ORM except raw drivers;\n- redis support;\n- rabbitmq support;\n- different CI\\CD;\n- Kubernetes config generation;\n- Demo routers and models;\n- Pre-commit integrations;\n- Generated tests;\n- Tests for the generator itself.\n\nThis project can handle arguments passed through command line.\n\n```shell\n$ python -m fastapi_template --help\n\nusage: FastAPI template [-h] [--version] [--name PROJECT_NAME]\n                        [--description PROJECT_DESCRIPTION]\n                        [--api-type {rest,graphql}]\n                        [--db {none,sqlite,mysql,postgresql}]\n                        [--orm {ormar,sqlalchemy,tortoise,psycopg,piccolo}]\n                        [--ci {none,gitlab_ci,github}] [--redis] [--rabbit]\n                        [--migrations] [--kube] [--dummy] [--routers]\n                        [--swagger] [--force] [--quite]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version, -V         Prints current version\n  --name PROJECT_NAME   Name of your awesome project\n  --description PROJECT_DESCRIPTION\n                        Project description\n  --api-type {rest,graphql}\n                        API type\n  --db {none,sqlite,mysql,postgresql}\n                        Database\n  --orm {ormar,sqlalchemy,tortoise,psycopg,piccolo}\n                        ORM\n  --ci {none,gitlab_ci,github}\n                        Choose CI support\n  --redis               Add Redis support\n  --rabbit              Add RabbitMQ support\n  --migrations          Add migrations support\n  --kube                Add Kubernetes configs\n  --dummy, --dummy-model\n                        Add dummy model\n  --routers             Add example routers\n  --swagger             Enable self-hosted Swagger\n  --force               Owerrite directory if it exists\n  --quite               Do not ask for features during generation\n```\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/s3rius/FastAPI-template',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
