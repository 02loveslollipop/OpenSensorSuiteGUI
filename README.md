# OpenSensorSuite
> A simple sensor monitoring utility for ESP32 microcontrollers, powered by Python and Redis.

## Introduction
OpenSensorSuite is a simple sensor monitoring utility for ESP32 microcontrollers using a RedisDB for the data persistence. It is designed to be a simple, lightweight, and easy to use solution for monitoring sensor data from ESP32 microcontrollers. This repository contains the source code for GUI to view and manage the data. The source code for the ESP32 microcontroller can be found [here](https://github.com/02loveslollipop/OpenSensorSuiteESP32). And the data convertion service source code can be found [here](https://github.com/02loveslollipop/OpenSensorSuiteDataConvertion)

## Installation

1. Clone the repository
```sh
git clone https://github.com/02loveslollipop/OpenSensorSuiteGUI.git
```

2. Install the dependencies
```sh
pip install -r requirements.txt
```

3. Copy the `example_config.yml` file to `config.yml`
```sh
cp example_config.yml config.yml
```

4. Edit the `config.yml` file to match your configuration
```yaml
redis:
  host: redis-server.yourdomain.example #Set to your redis server doamin or IP
  port: 6379 #Set to your redis server port
  password: wVdsBAqzCaWtaOC7DLVeuj2SuMuZc1dm #Set to your redis server password

gui:
  graph_update_ms: 1000 #Set to the graph update interval in milliseconds
  graph_history: 100 #Set to the number of data points to show in the graph
```

5. Run the GUI
```sh
python main.py
```
