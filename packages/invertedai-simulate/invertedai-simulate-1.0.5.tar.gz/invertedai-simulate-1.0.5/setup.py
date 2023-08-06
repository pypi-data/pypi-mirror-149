# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invertedai_simulate', 'invertedai_simulate.dataset']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.31',
 'Sphinx==4.5.0',
 'furo==2022.4.7',
 'gym>=0.17.2,<1.0.0',
 'halo==0.0.31',
 'iai_common==1.0.3',
 'imageio-ffmpeg>=0.4.7,<0.5.0',
 'inquirer>=2.9.2,<3.0.0',
 'matplotlib==3.5.1',
 'myst-parser==0.17.2',
 'packaging>=21.0,<22.0',
 'pygame>=2.0.0',
 'pyzmq==22.3.0',
 'scikit-image==0.19.2',
 'sphinx-copybutton==0.5.0',
 'sphinx-design==0.1.0',
 'sphinx-rtd-theme==1.0.0',
 'sphinxcontrib-applehelp==1.0.2',
 'sphinxcontrib-devhelp==1.0.2',
 'sphinxcontrib-htmlhelp==2.0.0',
 'sphinxcontrib-jsmath==1.0.1',
 'sphinxcontrib-qthelp==1.0.3',
 'sphinxcontrib-serializinghtml==1.1.5']

setup_kwargs = {
    'name': 'invertedai-simulate',
    'version': '1.0.5',
    'description': 'Client Interface for InvertedAI Simulate',
    'long_description': "[![Documentation Status](https://readthedocs.org/projects/invertedai-simulate/badge/?version=latest)](https://invertedai-simulate.readthedocs.io/en/latest/?badge=latest)\n\n#   Product Interface Client\n\n<!-- start elevator-pitch -->\n- **Safety Validation**\n- **Synthetic Data Generation** \n- **Training and Testing**\n- **Real-World Results From Simulation** \n<!-- end elevator-pitch -->\n\n\n\n<!-- start quickstart -->\n1. Install invertedai_simulate in your project environment.\n\n   ```shell\n   pip install invertedai_simulate\n   ```\n\n2. Alternatively, build the environment with the packages in the 'requirements.txt'.\n   ```shell\n   poetry install --no-dev\n   ```\n4. Run your simulation! 🎉\n- For driving run:\n  ```shell\n   python client_app_driving.py  --zmq_server_address 'x.x.x.x:5555'\n  ```\n- For data generation run:\n   ```shell\n   python client_app_trafficlight_data.py --zmq_server_address 'x.x.x.x:5555'\n   ```\n5. Sample codes are also provided as Jupyter-notebooks.\n\n- For driving:\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-driving.ipynb)\n\n- For data generation:\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-datageneration.ipynb)\n\n- For data generation as a pytorch dataloader:\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-dataloader.ipynb)\n<!-- end quickstart -->\n",
    'author': 'Inverted AI',
    'author_email': 'info@inverted.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
