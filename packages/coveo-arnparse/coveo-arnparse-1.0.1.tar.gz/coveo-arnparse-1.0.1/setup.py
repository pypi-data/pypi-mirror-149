# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_arnparse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coveo-arnparse',
    'version': '1.0.1',
    'description': 'Parse an arn in multiple components.',
    'long_description': '# coveo-arnparse\n\nSimple dataclass and parser around Amazon Resource Names (ARNs).\n\nRef: https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html\n\n## Usage\n\n### Parse from a string\n```python\n>>> from coveo_arnparse import arnparse\n>>> arn = arnparse("arn:aws:sns:us-east-1:123456789012:my_topic")\n>>> repr(arn)\nArn(partition=\'aws\', service=\'sns\', region=\'us-east-1\', account=\'123456789012\', resource=\'my_topic\')\n>>> str(arn)\n"arn:aws:sns:us-east-1:123456789012:my_topic"\n>>> arn.resource_type\n\'\'\n>>> arn.resource_id\n\'\'\n```\n\nWhen a `:` or a `/` is in the resource, you can also obtain either parts:\n\n```python\n>>> from coveo_arnparse import arnparse\n>>> arn = arnparse("arn:aws:ssm:us-east-1:123456789012:parameter/path/key")\n>>> arn.resource_type\n\'parameter\'\n>>> arn.resource_id\n\'path/key\'\n>>> arn.resource\n\'parameter/path/key\'\n```\n\n\n### Create an instance directly\n\n```python\n>>> from coveo_arnparse import Arn\n>>> Arn(service="s3", resource="my_bucket/path/file.jpg")\nArn(partition=\'aws\', service=\'s3\', region=\'\', account=\'\', resource=\'my_bucket/path/file.jpg\')\n```\n ',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/coveo-python-oss/tree/main/coveo-arnparse',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
