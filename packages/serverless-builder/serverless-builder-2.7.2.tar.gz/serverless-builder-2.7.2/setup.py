# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serverless',
 'serverless.aws',
 'serverless.aws.alerts',
 'serverless.aws.features',
 'serverless.aws.functions',
 'serverless.aws.iam',
 'serverless.aws.resources',
 'serverless.integration',
 'serverless.service',
 'serverless.service.plugins']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'inflection>=0.5.1,<0.6.0', 'troposphere>=3.2,<3.3']

setup_kwargs = {
    'name': 'serverless-builder',
    'version': '2.7.2',
    'description': 'Python interface to easily generate `serverless.yml`.',
    'long_description': '<h2 align="center">serverless-builder</h2>\n<p align="center">\n<a href="https://pypi.org/project/serverless-builder/"><img alt="PyPI" src="https://img.shields.io/pypi/v/serverless-builder"></a>\n<a href="https://pypi.org/project/serverless-builder/"><img alt="Python" src="https://img.shields.io/pypi/pyversions/serverless-builder.svg"></a>\n<a href="https://github.com/epsylabs/serverless-builder/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/lucyna.svg"></a>\n</p>\n\nPython interface to easily generate [serverless.yml](https://www.serverless.com/) file.\n\nMassive thanks goes to [@dxd1](https://github.com/dxd1) for his original idea and implementation.\n\n## Why\n`serverless.yml` easily can become a massive file with hundreds of lines, even if you have only a couple of services.\n\nModifying even semi advanced project can be difficult. Adding plugins and configuration for it, making sure your endless resources are configured correctly, making sure that you follow best practices.\nIf you will multiple that by all microservices you have, it can be really painful.\n\n## How\n`serverless-builder` comes and tries to help you with those tasks.\n- plugin management (with autoconfiguration)\n- function factory (with some best practice hints (DLQ))\n- autoconfiguration of some provider specific features like AWS X-Ray\n- monitoring support (wip)\n- easy resource manipulation with troposphere lib https://github.com/cloudtools/troposphere (but if you want you can use old good dict)\n- easier IAM management with predefined permission sets\n- built-in support for any serverless attributes\n\n# Example\n\n```python\nfrom serverless.aws.functions.event_bridge import RetryPolicy\nfrom serverless.aws.functions.http import HTTPFunction\nfrom serverless import Service\nfrom serverless.provider import AWSProvider\nfrom serverless.aws.features import XRay\nfrom serverless.aws.iam.dynamodb import DynamoDBReader\nfrom serverless.plugins import ComposedVars, PythonRequirements, Prune\n\nfrom troposphere.dynamodb import Table, AttributeDefinition, KeySchema\n\nservice = Service(\n    "service-name",\n    "some dummy service",\n    AWSProvider()\n)\nservice.plugins.add(ComposedVars())\nservice.plugins.add(Prune())\nservice.plugins.add(PythonRequirements())\n\ntable = Table(\n    "TestTable",\n    BillingMode="PAY_PER_REQUEST",\n    AttributeDefinitions=[\n        AttributeDefinition(AttributeName="name", AttributeType="S")\n    ],\n    KeySchema=[KeySchema(AttributeName="name", KeyType="HASH")]\n)\n\nservice.enable(XRay())\nservice.provider.iam.apply(DynamoDBReader(table))\n\nservice.builder.function.generic("test", "description")\nservice.builder.function.http("test", "description", "/", HTTPFunction.POST)\n\n# Multiple events with different paths and/or methods can be set up for the same handler\n# This will add the same handler to all of these: POST /, POST /alias, PUT /, PUT /alias\nservice.builder.function.http("test", "description", ["/", "/alias"], ["POST", "PUT"], handler="shared.handler")\n\n# Context with pre-defined setup\nwith service.preset(\n    layers=[{"Ref": "PythonRequirementsLambdaLayer"}],\n    handler="test.handlers.custom_handler.handle"\n) as p:\n    p.http_get("test-list", "List all tests", "/")\n    p.http_get("test-get", "Get one test", "/{test_id}")\n\nevent_bridge_function = service.builder.function.event_bridge(\n    "event_bridge_function",\n    "sample event bridge function",\n    "epsy",\n    {"source": ["saas.external"]},\n)\n\nevent_bridge_function.use_delivery_dlq(RetryPolicy(5, 300))\nevent_bridge_function.use_async_dlq()\n\nservice.resources.add(table)\n\nservice.render()\n```\n',
    'author': 'Epsy',
    'author_email': 'engineering@epsyhealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/epsylabs/serverless-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
