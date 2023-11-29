import subprocess
import sys
import argparse


def is_git_repository():
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True, check=True)
        return result.stdout.strip() == 'true'
    except subprocess.CalledProcessError:
        return False


def run_git_config(args):
    result = subprocess.run(['git', 'config'] + args,
                            capture_output=True, text=True)
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
    original_source = {}
    override_source = {}
    original_values = {}

    # Load system configuration
    for key, value in system_config.items():
        effective_config[key] = value
        original_source[key] = 'system'
        original_values[key] = [('system', value)]

    # Update with global configuration and track overrides and original values
    for key, value in global_config.items():
        if key in effective_config and effective_config[key] != value:
            override_source[key] = 'global'
            original_values.setdefault(key, []).append(('global', value))
        effective_config[key] = value
        if key not in original_source:
            original_source[key] = 'global'

    # Update with local configuration and track overrides and original values
    for key, value in local_config.items():
        if key in effective_config and effective_config[key] != value:
            override_source[key] = 'local'
            original_values.setdefault(key, []).append(('local', value))
        effective_config[key] = value
        if key not in original_source:
            original_source[key] = 'local'

    return effective_config, original_source, override_source, original_values



def main():
    parser = argparse.ArgumentParser(
        description='Display Git configurations with override option')
    parser.add_argument('--override', action='store_true',
                        help='Run script even if not in a Git repository')
    args = parser.parse_args()

    if not args.override and not is_git_repository():
        print("Not inside a Git repository. Use --override to run anyway.")
        sys.exit(1)

    # Colors dictionary
    COLORS = {
        'system': '38;5;228',  # Soft Yellow
        'global': '38;5;111',  # Pale Blue or '38;5;250' for Light Gray
        'local': '38;5;120',   # Light Green
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
    effective_config, original_source, override_source, original_values = determine_effective_config(
        system_config, global_config, local_config)

    # Print effective configuration with color coding and color key
    print('\033[35mEffective Configuration:\033[0m', end='  ')  # Magenta

    # Print color key
    for label, color_code in COLORS.items():
        print(f'\033[{color_code}m\u25A0 {label}\033[0m', end='  ')
    print('\n')

    for key, value in sorted(effective_config.items()):
        source = override_source.get(key, original_source[key])
        color_code = COLORS[source]
        print(f'\033[{color_code}m    {key} = {value}\033[0m')

        # Print overridden values with keys and indentation
        if key in original_values and len(original_values[key]) > 1:
            indent_level = 2
            for source, old_value in reversed(original_values[key][:-1]):
                indent = ' ' * indent_level
                color_code = COLORS[source]
                print(
                    f'{indent}\033[{color_code}m    ^ {key} = {old_value}\033[0m')
                indent_level += 4  # Increase indent for each level

    print('\033[0m')  # Reset to default color after printing the configuration


# Execute main function
if __name__ == '__main__':
    main()
