import os.path
import pathlib
import yaml

config_yaml = os.path.join(
    pathlib.Path(__file__).parent.resolve(),
    'config.yaml',
)

with open(config_yaml) as f:
    app_config = yaml.load(f, Loader=yaml.FullLoader)
    app_config['logs_dir'] = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'log',
    )
