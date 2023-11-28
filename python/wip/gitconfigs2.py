import subprocess

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
    source_of_override = {}
    for key, value in system_config.items():
        effective_config[key] = value
        source_of_override[key] = 'system'

    for key, value in global_config.items():
        if key not in effective_config or effective_config[key] != value:
            source_of_override[key] = 'global'
        effective_config[key] = value

    for key, value in local_config.items():
        if key not in effective_config or effective_config[key] != value:
            source_of_override[key] = 'local'
        effective_config[key] = value

    return effective_config, source_of_override

# Colors
COLORS = {
    'system': '33',  # Yellow
    'global': '32',  # Green
    'local': '36',   # Cyan
    'default': '37'  # White
}

# Read configurations
system_config = run_git_config(['--system', '-l'])
global_config = run_git_config(['--global', '-l'])
local_config = run_git_config(['--local', '-l'])

# Print configurations with colors
print_config(system_config, 'System', COLORS['system'])
print_config(global_config, 'Global', COLORS['global'])
print_config(local_config, 'Local', COLORS['local'])

# Determine effective configuration
effective_config, source_of_override = determine_effective_config(system_config, global_config, local_config)

# Print effective configuration with color coding
print('\033[35mEffective Configuration:\033[0m')  # Magenta
for key, value in sorted(effective_config.items()):
    source = source_of_override.get(key, 'default')
    color_code = COLORS.get(source, COLORS['default'])
    print(f'\033[{color_code}m    {key} = {value}\033[0m')
