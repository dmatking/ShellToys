import subprocess
import sys
import argparse

def is_git_repository():
    try:
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True, check=True)
        return result.stdout.strip() == 'true'
    except subprocess.CalledProcessError:
        return False

def run_git_config(args):
    result = subprocess.run(['git', 'config'] + args, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    config = {}
    for line in result.stdout.strip().split('\n'):
        key, value = line.split('=', 1)
        config[key] = value
    return config

def print_config(config, title, color_code):
    if config is not None:
        print(f'\033[{color_code}m{title} Configuration:\033[0m')
        for key, value in sorted(config.items()):
            print(f'    {key} = {value}')
    else:
        print(f'\033[{color_code}m{title} Configuration: Not Found\033[0m')
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

def main():
    parser = argparse.ArgumentParser(description='Display Git configurations with override option')
    parser.add_argument('--override', action='store_true', help='Run script even if not in a Git repository')
    args = parser.parse_args()

    if not args.override and not is_git_repository():
        print("Not inside a Git repository. Use --override to run anyway.")
        sys.exit(1)

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

# Execute main function
if __name__ == '__main__':
    main()