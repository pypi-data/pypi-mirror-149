# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datalake_catalog', 'datalake_catalog.schemas']

package_data = \
{'': ['*'], 'datalake_catalog': ['config/*']}

install_requires = \
['Flask-JWT-Extended>=4.3.1,<5.0.0',
 'Flask>=2.0.2,<3.0.0',
 'PyMySQL>=1.0.2,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'jsonschema>=4.2.1,<5.0.0',
 'pony>=0.7.14,<0.8.0',
 'psycopg2-binary>=2.9.3,<3.0.0']

entry_points = \
{'console_scripts': ['catalog = datalake_catalog.main:cli']}

setup_kwargs = {
    'name': 'datalake-catalog',
    'version': '1.0.3',
    'description': 'Datalake Catalog',
    'long_description': '## Setup and start the API \n\nConfigure the parameters with a [python file](https://flask.palletsprojects.com/en/2.0.x/config/#configuring-from-python-files) \n\nFor example, `catalog.conf.py`\n\n```python\nSECRET_KEY = b"changemenow"\nDB_STRING = "sqlite://localhost/catalog.sqlite"\n```\n\nStart the catalog \n\n```shell\ndocker run -d \\\n    -p \'8080:8080\' \\\n    -v \'catalog.conf.py:/etc/datacatalog/catalog.conf.py\' \\\n    -e \'CATALOG_SETTINGS=/etc/datacatalog/catalog.conf.py\' \\\n    public.ecr.aws/equancy-tech/datalake-catalog\n```\n\n## Generate an API token\n\nThe `catalog create-api-key` generated tokens that can be used with restricted endpoint.\n\n- **admin** role can access all restricted endpoints\n- **author** role can only access the restricted endpoints in `/catalog`\n\n```shell\nUsage: catalog create-api-key [OPTIONS] NAME\n\nOptions:\n  -e, --expires INTEGER      number of days before token expires\n  -r, --role [author|admin]  the role associated with the name\n  --help                     Show this message and exit.\n```\n\n## Update the storages configuration\n\nStorage configures aliases to help resolve actual buckets (S3, Azure, local fs, etc.).\nIt consists of a bucket name and an optional prefix.\n\nFor example:\n\n```json\n{\n    "landing": {\n        "bucket": "my-raw-bucket",\n        "prefix": "landing"\n    },\n    "archive": {\n        "bucket": "my-raw-bucket",\n        "prefix": "archives"\n    },\n    "bronze": {\n        "bucket": "my-bucket-bronze"\n    },\n    "silver": {\n        "bucket": "my-bucket-silver"\n    },\n    "gold": {\n        "bucket": "my-bucket-gold",\n    }\n}\n```\n\n```shell\ncurl -XPUT http://localhost:8080/storage \\\n    -H "Content-Type: application/json" \\\n    -H "Authorization: Bearer ${CATALOG_ADMIN_TOKEN}" \\\n    --data "@${STORAGE_CONFIG_FILE}" \n```\n',
    'author': 'Didier SCHMITT',
    'author_email': 'dschmitt@equancy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/equancy/datalake-catalog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
