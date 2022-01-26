import yaml

with open('config.yaml') as f:
    app_config = yaml.load(f, Loader=yaml.FullLoader)
