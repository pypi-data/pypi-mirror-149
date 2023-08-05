# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectral_synthesizer',
 'spectral_synthesizer.Base_Models',
 'spectral_synthesizer.RV_generation',
 'spectral_synthesizer.Sampling_Times',
 'spectral_synthesizer.data_interfaces',
 'spectral_synthesizer.spectra_generation',
 'spectral_synthesizer.spectral_effects',
 'spectral_synthesizer.spectral_effects.stellar_activity',
 'spectral_synthesizer.spectral_effects.telluric_features',
 'spectral_synthesizer.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'sbart>=0.1.4,<0.2.0', 'tabletexifier>=0.1.9,<0.2.0']

setup_kwargs = {
    'name': 'spectral-synthesizer',
    'version': '0.1.0',
    'description': 'Generate synthetic spectra with injected RVs',
    'long_description': None,
    'author': 'Kamuish',
    'author_email': 'andremiguel952@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
