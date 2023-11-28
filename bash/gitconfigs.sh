#!/bin/bash

# Function to display configurations with color
show_config() {
    local level=$1
    local color=$2
    echo -e "${color}${level} Configuration:\e[0m"
    git config --$level -l | sort | sed 's/^/    /'
    echo ""
}

# Colors
CYAN="\e[36m"
GREEN="\e[32m"
YELLOW="\e[33m"
MAGENTA="\e[35m"
WHITE="\e[37m"

# Display configurations
show_config system $YELLOW
show_config global $GREEN
show_config local $CYAN

# Determine and display effective configuration
echo -e "${MAGENTA}Effective Configuration:\e[0m"
git config --list | sort | uniq | while read line; do
    key=$(echo $line | cut -d '=' -f 1)
    is_overridden=$(git config --local --get $key && git config --global --get $key && git config --system --get $key)
    if [ ! -z "$is_overridden" ]; then
        echo -e "    $line" | sed "s/^/$WHITE/"
    else
        echo -e "    $line"
    fi
done
