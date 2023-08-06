# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_testing_extras', 'coveo_testing_extras.temporary_resource']

package_data = \
{'': ['*']}

install_requires = \
['coveo-functools',
 'coveo-settings',
 'coveo-systools',
 'coveo-testing',
 'docker']

setup_kwargs = {
    'name': 'coveo-testing-extras',
    'version': '2.1',
    'description': 'Dependency-hungry testing helpers',
    'long_description': '# coveo-testing-extras\n\nContains extra testing tools without dependency restrictions.\n\n\n## temporary resource implementation: Docker Container\n\nThe docker container temporary resource can be used to prepare short-lived containers.\n\n- Supports building from a dockerfile\n- Supports pulling images\n- Can signal on AWS ECR logout\n- Dynamic port mapping retrieval\n- Saves log output before removing the container\n\n\n### Automatic AWS ECR login example\n\nHere\'s how you can enhance `TemporaryDockerContainerResource` with automatic ECR login:\n\n```python\nfrom base64 import b64decode\n\nimport boto3\nfrom coveo_testing_extras.temporary_resource.docker_container import (\n    TemporaryDockerContainerResource, \n    ECRLogoutException,\n    get_docker_client\n)\n\nclass WithECR(TemporaryDockerContainerResource):\n    def obtain_image(self) -> None:\n        try:\n            super().obtain_image()\n        except ECRLogoutException:\n            self._do_ecr_login()\n            super().obtain_image()\n\n    def _do_ecr_login(self) -> None:\n        """ Performs an ecr login through awscli. """\n        assert self.ecr_region\n        ecr = boto3.client(\'ecr\')\n        account_id, *_ = self.image_name.split(\'.\')\n        assert account_id.isdigit()\n        authorization_data = ecr.get_authorization_token(registryIds=[account_id])[\'authorizationData\'][0]\n        username, password = b64decode(authorization_data[\'authorizationToken\']).decode().split(\':\')\n        with get_docker_client() as client:\n            login = client.login(username=username, password=password, registry=authorization_data[\'proxyEndpoint\'])\n        assert login[\'Status\'] == \'Login Succeeded\'\n```\n\n\n',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/coveo-python-oss/tree/main/coveo-testing-extras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
