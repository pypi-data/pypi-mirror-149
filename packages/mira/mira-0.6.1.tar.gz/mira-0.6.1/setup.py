# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mira',
 'mira.core',
 'mira.core.protos',
 'mira.datasets',
 'mira.detectors',
 'mira.detectors.assets.serve',
 'mira.detectors.experimental',
 'mira.thirdparty',
 'mira.thirdparty.detr',
 'mira.thirdparty.detr.models',
 'mira.thirdparty.detr.util',
 'mira.thirdparty.effdet',
 'mira.thirdparty.effdet.config',
 'mira.thirdparty.effdet.object_detection']

package_data = \
{'': ['*'], 'mira.datasets': ['assets/*']}

install_requires = \
['albumentations>=1.1.0',
 'matplotlib',
 'numpy',
 'pandas',
 'protobuf',
 'tqdm',
 'validators']

extras_require = \
{'detectors': ['segmentation-models-pytorch>=0.2.0',
               'timm',
               'omegaconf',
               'torchvision']}

setup_kwargs = {
    'name': 'mira',
    'version': '0.6.1',
    'description': 'A package for simplifying object detection',
    'long_description': '# mira [![CircleCI](https://circleci.com/gh/faustomorales/mira.svg?style=shield)](https://circleci.com/gh/faustomorales/mira) [![Documentation Status](https://readthedocs.org/projects/mira-python/badge/?version=latest)](https://mira-python.readthedocs.io/en/latest/?badge=latest)\n\nmira provides tooling for simple object detection projects. The package spans three areas of focus.\n\n- **Core** object detection abstractions for images and annotations\n- Access to **datasets** from common formats (e.g., VOC, COCO) and image sets (e.g., VOC 2012)\n- A common API to for **well-known models** (e.g., EfficientDet and FasterRCNN)\n\nCheck out [the docs](https://mira-python.readthedocs.io/en/latest/).\n\n## Installation\n\n```shell\npip install mira\n```\n',
    'author': 'Fausto Morales',
    'author_email': 'faustomorales@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/faustomorales/mira',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.10,<3.10',
}


setup(**setup_kwargs)
