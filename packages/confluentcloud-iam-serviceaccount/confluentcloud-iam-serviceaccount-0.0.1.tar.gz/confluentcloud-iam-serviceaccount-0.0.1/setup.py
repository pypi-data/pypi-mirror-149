# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['confluentcloud_iam_serviceaccount']

package_data = \
{'': ['*']}

install_requires = \
['cloudformation-cli-python-lib>=2.1.11,<3.0.0',
 'compose-x-common>=0.4.2,<0.5.0',
 'confluent-cloud-sdk>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'confluentcloud-iam-serviceaccount',
    'version': '0.0.1',
    'description': 'AWS CFN Resource to provision a Confluent Cloud Service account',
    'long_description': '# Confluent::IAMv2::ServiceAccount\n\nAllows to create a new Service Account into an organization in Confluent Cloud via API.\n\nSee the [docs](./docs/README.md) for properties\n\n\n## Requirements\n\nYou need\n\n* An account on Confluent Cloud Platform\n* Create a new API key for cloud resource, ie. as follows from CLI.\n\n```bash\nconfluent api-key create --resource cloud\n```\n\n## Example\n\n### Set up requirements\n\n```bash\n\n# Optionally create an API key via the CLI\nconfluent api-key create --resource cloud -o json\n\nexport API_KEY=THEAPIKEYRETURNED\nexport API_SECRET=THEAPISECRETRETURNED\n\naws cloudformation deploy --stack-name confluent-cloud-api-credentials --template confluent-secrets.template \\\n  --parameter-overrides ConfluentApiKey=${API_KEY} ConfluentSecretKey=${API_SECRET}\n\nexport SECRET_ARN=`aws cloudformation describe-stack-resources --stack-name confluent-cloud-api-credentials --logical-resource-id ConfluentSecret | jq -r .StackResources[0].PhysicalResourceId`\n\n```\n\n### Activate the 3rd party CloudFormation resource\n\n```bash\naws cloudformation deploy --stack cfn-resource--confluentcloud-iam-serviceaccount --template activate.template \\\n  --capabilities CAPABILITY_IAM\n```\n\n\n### Create a new Service account\n\n```bash\naws cloudformation deploy --stack-name my-first-service-account --template resource-test.template \\\n  --parameter-overrides ConfluentCloudApiSecrets=${SECRET_ARN}\n```\n',
    'author': 'John Preston',
    'author_email': 'john@ews-network.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
