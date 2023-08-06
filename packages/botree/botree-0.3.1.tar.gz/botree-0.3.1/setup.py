# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botree']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.19.8,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'botree',
    'version': '0.3.1',
    'description': 'A friendly wrapper for boto3.',
    'long_description': '# Botree: a friendly wrapper for boto3\n\nBotree is a higher level API and text user intercace tool for AWS services.\n\n## 🧠 Features\n\n- ✔️ High level and easy to remember API for AWS services.\n- 🔨 TUI (text user interface) powered by [Textual](https://github.com/willmcgugan/textual).\n\n## 🧰 Supported AWS services\n\n- ✔️ S3\n- ✔️ Secrets\n- 🔨 CloudWatch\n- 🔨 EC2\n\n## 💻 Examples\n\nUntil I\'ve written the documentation, some dummie examples may be the best way to get used to the Botree API.\n\n### S3\n\nTo start a Botree session, use the following:\n\n```Python\nimport botree\nsession = botree.session("us-east-1", profile="dev")\n```\n\nCreate a bucket:\n\n```Python\nsession.s3.create_bucket("sample-bucket")\nsession.s3.list_buckets()\n```\n\nNote that all S3 operations will use Python\'s pathlib to handle directory paths, so let\'s import it:\n\n```python\nfrom pathlib import Path\n```\n\nDownload and upload:\n\n```Python\nsource_file = Path("sample_source_file.png")\ntarget_file = Path("sample_target_file.png")\nsession.s3.bucket("sample-bucket").upload(source_file, target_file)\n\n# downloads are more of the same\nsession.s3.bucket("sample-bucket").download(source_file, target_file)\n```\n\nCopy files:\n\n```python\nsource_file = Path("sample_source_file.png")\ntarget_file = Path("sample_target_file.png")\nsession.s3.bucket("sample-bucket").copy(source_file, target_file)\n\n# you can specify a source bucket to copy a file from\nsession.s3.bucket("sample-bucket").copy(source_file, target_file, source_bucket="other-bucket")\n```\n\nList files:\n\n```python\nsession.s3.bucket("sample-bucket").list_objects()\n```\n\nDelete files:\n\n```python\nsession.s3.bucket("sample-bucket").delete("sample_target_file")\n```\n\n## 🏗️ Development\n\nBotree relies on [Poetry](https://github.com/python-poetry/poetry).\n\nInstall the Python dependencies with:\n\n```bash\npoetry install\n```\n\n## ⚗️ Testing\n\n```bash\npoetry run pytest --cov=botree tests/\n```\n',
    'author': 'ericmiguel',
    'author_email': 'ericmiguel@id.uff.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ericmiguel/timeless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
