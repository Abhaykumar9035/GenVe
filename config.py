import yaml

# Path to your config.yaml file
CONFIG_FILE_PATH = 'config.yaml'

def load_config():
    with open(CONFIG_FILE_PATH, 'r', encoding="utf-8") as file:
        return yaml.safe_load(file)

# Load the configuration
config = load_config()

# Access the configuration values
llms = config['llms']
module_assignments = config['module_assignments']
manim_settings = config['manim_settings']