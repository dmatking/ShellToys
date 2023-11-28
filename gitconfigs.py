import subprocess
import os

def run_git_config(args):
    result = subprocess.run(['git', 'config'] + args, capture_output=True, text=True)
    if result.returncode != 0:
        return {}
    config = {}
    for line in result.stdout.strip().split('\n'):
        key, value = line.split('=', 1)
        config[key] = value
    return config

def print_config(config, title, color_code):
    print(f'\033[{color_code}m{title} Configuration:\033[0m')
    for key, value in sorted(config.items()):
        print(f'    {key} = {value}')
    print()

def determine_effective_config(system_config, global_config, local_config):
    effective_config = {}
    for key_set in [system_config, global_config, local_config]:
        for key, value in key_set.items():
            effective_config[key] = value
    return effective_config

# Read configurations
system_config = run_git_config(['--system', '-l'])
global_config = run_git_config(['--global', '-l'])
local_config = run_git_config(['--local', '-l'])

# Print configurations with colors
print_config(system_config, 'System', '33')  # Yellow
print_config(global_config, 'Global', '32')  # Green
print_config(local_config, 'Local', '36')   # Cyan

# Determine effective configuration
effective_config = determine_effective_config(system_config, global_config, local_config)

# Print effective configuration with color coding
print('\033[35mEffective Configuration:\033[0m')  # Magenta
for key, value in sorted(effective_config.items()):
    source = 'White'
    if key in local_config:
        source = 'Cyan'
    elif key in global_config:
        source = 'Green'
    elif key in system_config:
        source = 'Yellow'
    color_code = {'White': '37', 'Cyan': '36', 'Green': '32', 'Yellow': '33'}[source]
    print(f'\033[{color_code}m    {key} = {value}\033[0m')
