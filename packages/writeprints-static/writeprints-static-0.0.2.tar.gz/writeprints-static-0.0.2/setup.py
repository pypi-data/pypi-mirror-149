# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['writeprints_static']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.0.0,<2.0.0', 'scipy>=1.5.0,<2.0.0', 'spacy==3.0.8']

setup_kwargs = {
    'name': 'writeprints-static',
    'version': '0.0.2',
    'description': 'Extract lexical and syntactic features for authorship attribution research.',
    'long_description': '# writeprints-static\n\nExtract lexical and syntactic features for authorship attribution research.\n\nThe writeprints-static package aims to reproduce "Writeprints-Static" featureset described in Brennan et al. (2012).\nCheck [Docs](https://literary-materials.github.io/writeprints-static/) for details.\n\n\n## License\n\nThis package is licensed under the ISC License.\n\n## Versions\n\n- May 4, 2022, launch v.0.0.1. \n\n## References\n\n- Brennan, M., Afroz, S., & Greenstadt, R. (2012). Adversarial stylometry: Circumventing authorship recognition to\npreserve privacy and anonymity. *ACM Transactions on Information and System Security (TISSEC)*, 15(3), 1-22.\n\n',
    'author': 'writeprints-static Authors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/literary-materials/writeprints-static',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
