# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['secstache']
install_requires = \
['argparse>=1.4.0,<2.0.0', 'boto3>=1.21.37,<2.0.0', 'pystache>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['secstache = secstache:main']}

setup_kwargs = {
    'name': 'secstache',
    'version': '0.3.7',
    'description': 'Fill mustache template(s) with secrets from secret store(s).',
    'long_description': '# secstache\n\nFill [mustache](https://mustache.github.io/) template(s) with secrets from secret store(s).\n\n## Installation\n```\npip install secstache\n```\n\n## Usage\n```\n$ secstache -h\nusage: secstache [-h] [--asm key] [--strict] [file1.mustache ...]\n\nFill mustache template(s) with secrets from secret store(s).\n\npositional arguments:\n  file1.mustache  mustache files to process\n\noptional arguments:\n  -h, --help      show this help message and exit\n  --asm key       AWS Secret Manager key\n  --strict        fail if a tag key is not found\n\nEXAMPLE:\n\tCreate db.conf from db.conf.mustache using secrets in AWS Secret Manager under "prod/db"\n\n\t\tsecstache --asm prod/db db.conf.mustache\n```\n\n## Example\n\nSay, you have a secret stored in secrets manager under the name of `prod/db` with the SecretString set to:\n```\n{\n  "DB_USER": "foo_user",\n  "DB_PASS": "foo_pass"\n}\n```\nYou can create a mustache file like this:\n```\n$ cat db.conf.mustache\nDB_NAME = foo_db\nDB_USER = {{DB_USER}}\nDB_PASS = {{DB_PASS}}\n```\nand run `secstache` this way:\n```\n$ secstache --asm prod/db db.conf.mustache\nRendered db.conf.mustache to db.conf\n```\nThis creates the db.conf file that looks like this:\n```\n$ cat db.conf\nDB_NAME = foo_db\nDB_USER = foo_user\nDB_PASS = foo_pass\n```\n\n## Supported secret stores\n\n### AWS Secrets Manager\nLoad secrets from [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) via `--asm key` option. Note that your environment must be configured so as to support `boto3`. (I.e., you must be able to run `aws` successfully in your environment.)\n\n### Other secret stores\nPR\'s welcome! :grin:\n\n',
    'author': 'Shinichi Urano',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/9horses/secstache',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
