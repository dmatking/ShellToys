import subprocess
import sys
import argparse
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama


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
    if result.returncode != 0 or result.stdout == "":
        return {} # Return empty dictionary if no output or error
    config = {}
    for line in result.stdout.strip().split('\n'):
        key, value = line.split('=', 1)
        config[key] = value
    return config


def print_config(config, title, color_code):
    if config is not None:
        print(f'{color_code}{title} Configuration:{Style.RESET_ALL}')
        for key, value in sorted(config.items()):
            print(f'    {key} = {value}')
    else:
        print(f'{color_code}{title} Configuration: Not Found{Style.RESET_ALL}')
    print()


# Define color mappings
COLORS = {
    'system': Fore.YELLOW,
    'global': Fore.BLUE,
    'local': Fore.GREEN,
}


def main():
    parser = argparse.ArgumentParser(
        description='Display Git configurations with override option')
    parser.add_argument('--override', action='store_true',
                        help='Run script even if not in a Git repository')
    args = parser.parse_args()

    if not args.override and not is_git_repository():
        print("Not inside a Git repository. Use --override to run anyway.")
        sys.exit(1)

    # Read configurations
    system = run_git_config(['--system', '-l'])
    my_global = run_git_config(['--global', '-l'])
    local = run_git_config(['--local', '-l'])

    # Print configurations with colors
    print_config(system, 'System', COLORS['system'])
    print_config(my_global, 'Global', COLORS['global'])
    print_config(local, 'Local', COLORS['local'])

    # # Create system_out by taking items from system that are not in my_global or local
    # system_out = {key: value for key, value in system.items() if (my_global is None or key not in my_global) and (local is None or key not in local)}

    # # Create my_global_out by taking items from my_global that are also in system
    # my_global_out = {key: value for key, value in (my_global or {}).items() if key in system}

    # # Create local_out by taking items from local that are not in system_out or my_global_out
    # local_out = {key: value for key, value in (local or {}).items() if key not in system_out and key not in my_global_out}

    # Create system_out by taking items from system that are not in my_global or local
    system_out = {key: value for key, value in system.items() if key not in my_global and key not in local}

    # Create my_global_out by taking items from my_global that are also in system
    my_global_out = {key: value for key, value in my_global.items() if key in system}

    # Create local_out by taking items from local that are not in system_out or my_global_out
    local_out = {key: value for key, value in local.items() if key not in system_out and key not in my_global_out}


    # Define the custom sort order
    sort_order = {
        'system': 0,
        'global': 1,
        'local': 2,
    }

    # Merge the dictionaries and include source names in values with colors
    merged_dict = {}

    for k, v in system_out.items():
        merged_dict[f'{k}'] = (v, 'system')

    for k, v in my_global_out.items():
        merged_dict[f'{k}'] = (v, 'global')

    for k, v in local_out.items():
        merged_dict[f'{k}'] = (v, 'local')

    # Add items from system
    if system is not None:
        for k, v in system.items():
            if k not in merged_dict:
                merged_dict[f'{k}'] = (v, 'system')

    # Add items from my_global
    if my_global is not None:
        for k, v in my_global.items():
            if k not in merged_dict:
                merged_dict[f'{k}'] = (v, 'global')

    # Add items from local
    if local is not None:
        for k, v in local.items():
            if k not in merged_dict:
                merged_dict[f'{k}'] = (v, 'local')

    # Sort the merged dictionary by keys
    sorted_merged_dict = {k: v for k, v in sorted(merged_dict.items())}

    # Print effective configuration with color coding
    print(f'{Fore.MAGENTA}Effective Configuration:{Style.RESET_ALL}', end='  ')
    
    # Print color key
    for label, color_code in COLORS.items():
        print(f'{color_code}\u25A0 {label}{Style.RESET_ALL}', end='  ')
    print('\n')

    # Print the resulting dictionaries with colors based on source names  
    for key, (value, source) in sorted_merged_dict.items():
        source_color = {
            'system': Fore.YELLOW,
            'global': Fore.BLUE,
            'local': Fore.GREEN,
        }.get(source, Fore.RESET)

        print(f'    {source_color}{key}: {value}{Style.RESET_ALL}')


# Execute main function
if __name__ == '__main__':
    main()
