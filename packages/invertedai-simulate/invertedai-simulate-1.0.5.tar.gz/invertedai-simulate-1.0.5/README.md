[![Documentation Status](https://readthedocs.org/projects/invertedai-simulate/badge/?version=latest)](https://invertedai-simulate.readthedocs.io/en/latest/?badge=latest)

#   Product Interface Client

<!-- start elevator-pitch -->
- **Safety Validation**
- **Synthetic Data Generation** 
- **Training and Testing**
- **Real-World Results From Simulation** 
<!-- end elevator-pitch -->



<!-- start quickstart -->
1. Install invertedai_simulate in your project environment.

   ```shell
   pip install invertedai_simulate
   ```

2. Alternatively, build the environment with the packages in the 'requirements.txt'.
   ```shell
   poetry install --no-dev
   ```
4. Run your simulation! 🎉
- For driving run:
  ```shell
   python client_app_driving.py  --zmq_server_address 'x.x.x.x:5555'
  ```
- For data generation run:
   ```shell
   python client_app_trafficlight_data.py --zmq_server_address 'x.x.x.x:5555'
   ```
5. Sample codes are also provided as Jupyter-notebooks.

- For driving:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-driving.ipynb)

- For data generation:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-datageneration.ipynb)

- For data generation as a pytorch dataloader:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inverted-ai/iai-client/blob/main/examples/demo-dataloader.ipynb)
<!-- end quickstart -->
