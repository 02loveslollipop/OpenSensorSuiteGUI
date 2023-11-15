import yaml

class config:
    def __init__(self) -> None:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.host = config['redis']['host']
            self.port = config['redis']['port']
            self.password = config['redis']['password']
            self.graph_time = config['gui']['graph_update_ms']
            self.graph_history = config['gui']['graph_history']

            
            
            
            