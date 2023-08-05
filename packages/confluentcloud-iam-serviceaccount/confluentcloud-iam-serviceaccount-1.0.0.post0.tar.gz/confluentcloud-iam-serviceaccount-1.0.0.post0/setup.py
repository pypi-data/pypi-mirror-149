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

extras_require = \
{'resource': ['troposphere>=4.0.1,<5.0.0']}

setup_kwargs = {
    'name': 'confluentcloud-iam-serviceaccount',
    'version': '1.0.0.post0',
    'description': 'AWS CFN Resource to provision a Confluent Cloud Service account',
    'long_description': '# ConfluentCloud::IAM::ServiceAccount\n\nAllows to create a new Service Account into an organization in Confluent Cloud via API.\n\nSee the [docs](./docs/README.md) for properties\n\n\n## Install\n\n### Requirements\n\nYou need\n\n* An account on Confluent Cloud Platform\n* Have a Confluent Cloud API Key\n* AWS Account, and for the following installation steps, aws cli\n\n### Confluent API Key\n\n```bash\n\n# Optionally create an API key via the CLI\nconfluent api-key create --resource cloud -o json\n\nexport API_KEY=<API KEY RETURNED>\nexport API_SECRET=<API SECRET RETURNED>\n\n```\n\n### Create a secret in AWS Secrets Manager with the API key\n\n```bash\naws cloudformation deploy --stack-name confluent-cloud-api-credentials --template confluent-secrets.template \\\n  --parameter-overrides ConfluentApiKey=${API_KEY} ConfluentSecretKey=${API_SECRET}\n```\n\n### Save the secret ARN into a variable\n\n```bash\nexport SECRET_ARN=`aws cloudformation describe-stack-resources --stack-name confluent-cloud-api-credentials --logical-resource-id ConfluentSecret | jq -r .StackResources[0].PhysicalResourceId`\n```\n\n### Activate the 3rd party CloudFormation resource\n\n#### Option 1 - IAM and Resource together\n\nUsing the [activate.template](activate.template) we create IAM roles and enable the resource in the account, all at once.\n\n```bash\naws cloudformation deploy --stack cfn-resource--confluentcloud-iam-serviceaccount --template activate.template \\\n  --capabilities CAPABILITY_IAM\n```\n\nThis option offers the "extra security" to have a different IAM Execution role for that resource than others.\n\n\n#### Option 2 - IAM first, resource separate\n\n**Most recommended if you consider enabling multiple ConfluentCloud:: resources published**\n\nWe are going to use [cfn-resources-iam-roles.template](cfn-resources-iam-roles.template) template to create the _Execution_\nand _LoggingRole_ first, then use these in the [activate.template](activate.template) as parameters.\n\n```bash\naws cloudformation deploy --stack-name iam--cfn--confluentcloud-resources --template cfn-resources-iam-roles.template \\\n  --capabilities CAPABILITY_IAM\n```\n\nExport the IAM Roles to env vars\n\n```bash\nEXEC_ROLE_ARN=`aws cloudformation describe-stacks --stack-name iam--cfn--confluentcloud-resources | jq -r \'.Stacks[0].Outputs[] |  select(.OutputKey=="ExecutionRoleArn")\' | jq -r .OutputValue`\nLOGGING_ROLE_ARN=`aws cloudformation describe-stacks --stack-name iam--cfn--confluentcloud-resources | jq -r \'.Stacks[0].Outputs[] |  select(.OutputKey=="CloudWatchRoleArn")\' | jq -r .OutputValue`\n```\n\nNow, we activate the resource using these IAM Roles\n\n```bash\naws cloudformation deploy --stack cfn-resource--confluentcloud-iam-serviceaccount --template activate.template \\\n  --capabilities CAPABILITY_IAM \\\n  --parameter-overrides ExecutionRoleArn=${EXEC_ROLE_ARN} LoggingRoleArn=${LOGGING_ROLE_ARN}\n```\n\n### Create a new Service account\n\n```bash\naws cloudformation deploy --stack-name my-first-service-account --template resource-test.template \\\n  --parameter-overrides ConfluentCloudApiSecrets=${SECRET_ARN} ServiceAccountName=cfn-test-service-account\n```\n\n## Troubleshooting\n\nIf you are getting errors with the resource, you can see in the logs what issues occurred that lead to this issue.\nWith the template [activate.template](activate.template), you can see that there is a CloudWatch log group that\nwill be logging the code execution and so you can open an [issue](https://github.com/JohnPreston/aws-cfn-confluentcloud-iam-serviceaccount/issues) on GitHub\n\nIf at any point in the logging you\'d notice information that is not supposed to be there, please notify it immediately.\nWith that said, as the "vendor" of that resource, we will **never** have access to these logs or anything in your account.\n',
    'author': 'John Preston',
    'author_email': 'john@ews-network.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
