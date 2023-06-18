import os
import pathlib
import yaml

deploy_env = os.environ['DEPLOY']
config_file = 'app.dev.yaml'

if deploy_env == 'local-kuber':
    config_file = 'app.local-kuber.yaml'

app_config_yaml = os.path.join(
    pathlib.Path(__file__).parent.resolve(),
    'configs',
    config_file,
)

endpoints_yaml = os.path.join(
    pathlib.Path(__file__).parent.resolve(),
    'configs',
    'endpoints.yaml',
)

with open(app_config_yaml) as f:
    app_config = yaml.load(f, Loader=yaml.FullLoader)
    app_config['logs_dir'] = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        'log',
    )

with open(endpoints_yaml) as f:
    loaded_endpoints = yaml.load(f, Loader=yaml.FullLoader)
    app_config['endpoints'] = loaded_endpoints['endpoints']
