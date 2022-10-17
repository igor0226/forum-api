import os.path
import pathlib
import yaml

with open('config.yaml') as f:
    app_config = yaml.load(f, Loader=yaml.FullLoader)
    app_config['logs_dir'] = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'log',
    )
