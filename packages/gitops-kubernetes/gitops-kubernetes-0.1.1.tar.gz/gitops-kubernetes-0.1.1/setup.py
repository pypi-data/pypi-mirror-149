# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitops_kubernetes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gitops-kubernetes',
    'version': '0.1.1',
    'description': 'Implementa GitOps com Kubernetes',
    'long_description': 'GitOps Kubernetes\n=================\n\nImplementa GitOps com Kubernetes.\n\nTrata-se de um utilitário simples para implementar GitOps de forma simples\nusando Kubernetes.\n',
    'author': 'E5R Development Team',
    'author_email': None,
    'maintainer': 'Erlimar Silva Campos',
    'maintainer_email': 'erlimar@gmail.com',
    'url': 'https://github.com/e5r/gitops-kubernetes',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
