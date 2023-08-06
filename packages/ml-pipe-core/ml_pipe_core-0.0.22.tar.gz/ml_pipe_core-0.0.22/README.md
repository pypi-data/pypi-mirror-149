# ML Pipeline

Machine learning pipeline.
# How to create and run an Agent?
To create an Agent you need to clone the ml-pipe-service repository and install ml-pipe-core.

```
git clone 

```
```
mkdir .venv
```
```
pipenv install .
```

Afterwards you create a class which inherits form SimpleService.
```python
class SillyAgent(SimpleService):
    def __init__(self, name, adapter):
        super().__init__(name, adapter)
        self.factor = 1.0

    def reconfig_event(self, msg):
        factor = msg.get('factor')
        if factor is None:
            _logger.error("reconfig message doesn't have 'factor' as a key.")
        else:
            _logger.debug(f"set new factor to: {factor}")
            self.factor = factor

    def proposal(self, params):
        _logger.debug(f"use factor: {self.factor}")
        hcors = self.machine_adapter.get_hcors(names=self.machine_adapter.get_hcor_device_names(), is_group_call=True)
        self.set_machine(SetMachineMessage({'hcor': {"names": self.machine_adapter.get_hcor_device_names(),  "values": [val * self.factor for val in hcors]}}))

if __name__ == '__main__':
    agent = SillyAgent('silly_agent',  PetraSimulationAdapter())
    agent.init_local()
```
Inside this class you need to overload 
```python
def proposal(self, params)
``` 
which will be called when the Agent is triggered. The Machine/Simulation can be set with
```python
def set_machine(self, data: SetMachineMessage)
```
This function is taking an SetMachineMessage as input parameter. SetMachineMessage holds a python dictionary with which you can set the Machine/Simulation. Currently only setting horizontal/vertical correctors, machine parameters and twiss parameters are supported. The structure of the dictionary have to look like this:
```python
{'hcor': {'name': str, 'values': List[float]},
 'vcor': {'name': str, 'values': List[float]},
 'machineparams': {'name': str, 'values': List[float]}, 
 'twiss': {'name': str, 'mat': List[List[float]]} # only for simulation
 }
```

Optionally you can overload 
```python
def reconfig_event(self, msg) 
```
which give you the possibility to reset internal parameters without restarting your Agent.

After creating an Agent you need configure the agent in a yaml file.

Here is an example of config.yaml file. 

Notes: You have to replace localhost with the real server name.
```yml
observer:
  # used to check if jbb is done
  url: localhost:5003
  event_db_pw: xxxxx
  # event_db_url:
  event_db_usr: xxxxx
register:
  # registers all services
  url: localhost:5004
simulation:
  # sql database which maps the machine parameter
  sim_db_pw: xxxxx
  sim_db_usr: xxxxx
  sim_db_url: localhost:3306
msg_bus:
  # message bus
  broker_urls: localhost:9094,localhost:9096
```

Afterwards, set the path to the config yaml file in the environment value PIPE_CONFIG_FILEPATH.

```bash
PIPE_CONFIG_FILEPATH = /path/to/ml-pipe-config.yaml
```

To run the Agent you you can activate the python env.
```
pipenv shell
```
Afterwards you can run the Agent
```
python agents/testing/silly_agent.py
```
To interact with the pipeline (e.g trigger, start, list, stop Agents) you can used KafkaPipeClient.
```python
from ml_pipe_core.client.kafka_client import KafkaPipeClient

pipe = KafkaPipeClient()
print(pipe.get_running_service_info())
p_id = pipe.run_service('SillyAgent')
pipe.get_observation(p_id) # wait for response
```

An GUI will be come soon.


# Developer: Core Services and ml_pipe_core Package
The ML-Pipeline is using docker to run the infrastructure and test it locally. 
For this you need docker and docker-compose >= 1.28.0.


## Build Docker images
To build all docker images run:
```bash
make build-all
``` 
This can take a while...

Notes: After changing code you just need to rebuild the service images, which is much faster.
```
make build-service-images
```

## Start Core Services
To Start the core services of the ml-pipeline you need to set the following environment values
```
PIPE_EXTERNAL_HOST_ADDR=localhost
PIPE_DB_PW=xxxx
PIPE_DB_USER=xxxx
PIPE_CONFIG_FILEPATH = /path/to/ml-pipe-config.yaml
PATH_TO_ML_PIPE_SERVICES_ROOT=/path/to/ml-pipe-services
```

PIPE_CONFIG_FILEPATH is the path to the yaml config file, which look like this:

```yml
observer:
  # used to check if jbb is done
  url: observer:5003
  event_db_pw: xxxx
  # event_db_url:
  event_db_usr: xxxx
register:
  # registers all services
  url: register:5004
simulation:
  # sql database which maps the machine parameter
  sim_db_pw: xxxx
  sim_db_usr: xxxx
  sim_db_url: simulation_database:3306
msg_bus:
  # message bus
  # external_host_addr: localhost
  broker_urls: kafka_1:9092,kafka_2:9096
```

In production replace PIPE_EXTERNAL_HOST_ADDR=localhost with the server url and set PATH_TO_ML_PIPE_SERVICES_ROOT to the location of the cloned ml-pipe-services repository.
The environment values PIPE_DB_PW and PIPE_DB_USER define the credentials for the databases used by the pipeline.

## Stop Core Services
You have to stop the docker container at the end.
``` bash
make down
```

## Tests locally
Note: Docker and docker-compose => 2.80 is required to run tests locally

Run all tests:
```
make tests ENV_FILE=.env
```
Run end to end tests:
```
make e2e-tests ENV_FILE=.env
```
Run integration tests:
```
make integration-tests ENV_FILE=.env
```
Run unit tests
```
make unit-tests ENV_FILE=.env
```
## Additional Stuff
### Maxwell
Log in via ssh to max-wgs.desy.de

Install python 3.8.8 
```
wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
sh Anaconda3-2021.05-Linux-x86_64.sh
export PATH=$HOME/anaconda3/bin:$PATH
```

### PyTine and K2I2K_os on Machine PETRA III
The machine observer and controller for PETRA III are using the PetraAdapter which is using the libs PyTine and K2I2K_os.
The Path to this libs have to be added to the PYTHONPATH. 

For PyTine have a look at https://confluence.desy.de/display/HLC/Developing+with+Python. 

K2I2K_os can be cloned via git from: 
```bash
git clone https://username@stash.desy.de/scm/pihp/petra3.optics.tools.git
```


### Jupyter notebook
To use KafkaPipeClient in a Jupyter notebook you need to add the virtual environment to Jupyter.

First activate the python virtual environment.

For Pipenv
``` bash
pipenv shell
```

Start the jupyter notebook:
```bash
pip install --user ipykernel
```

Note: You have to add the virtual enviroment to jupyter. First, activate the virutal environment. Then run:
```bash
python -m ipykernel install --user --name=<myenv> 
```
