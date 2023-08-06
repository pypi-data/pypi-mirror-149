# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_pypi_proxy']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.2,<3.0.0', 'boto3>=1.22.6,<2.0.0', 'structlog>=21.5.0,<22.0.0']

entry_points = \
{'console_scripts': ['s3-pypi-proxy = s3_pypi_proxy:main']}

setup_kwargs = {
    'name': 's3-pypi-proxy',
    'version': '0.0.1',
    'description': 'Turn an S3 bucket into a PyPI repo',
    'long_description': '# S3 PyPI Proxy\n\nLocal PEP 503 compatible PyPI index proxy, backed by\nS3.\n\nPackages must be stored under the S3 bucket in the\nfollowing structure (`{package_name}/{filename}`):\n\n```\nsome-s3-bucket/\n  secret-package/\n    secret_package-0.0.1-py3-none-any.whl\n    ...\n  ...\n...\n```\n\n## Installation\n\n```bash\n$ pip install s3-pypi-proxy\n```\n\n## Usage\n\n1. Configure [AWS credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).\n\n2. Start the proxy, optionally referencing a credential profile:\n\n```bash\n$ s3-pypi-proxy --profile-name dev\n```\n\n3. Use the proxy to install packages:\n\n```bash\n$ pip install --extra-index-url=http://localhost:5000/some-s3-bucket/simple/ secret-package\n```\n',
    'author': 'Josh Bode',
    'author_email': 'joshbode@fastmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
