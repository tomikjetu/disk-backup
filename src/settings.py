import os
import yaml
from colorama import Fore, Style

SETTINGS_FILE = 'src/settings.yml'
# Loadede from settings.yml
BACKUP_VOLUME = ''
PROJECTS = []
SKIP_GIT_REMOTE = True

if not os.path.isfile(SETTINGS_FILE):
    raise FileNotFoundError("Projects file '{SETTINGS_FILE}' not found.")

with open(SETTINGS_FILE) as stream:
    try:
        data = yaml.safe_load(stream)
        PROJECTS = data.get('projects', [])
        BACKUP_VOLUME = data.get('backup_volume', '')
        SKIP_GIT_REMOTE = data.get('skip_git_remote', True)
    except yaml.YAMLError as exc:
        print(exc)

print(f"{Fore.YELLOW}Using backup volume: {Style.BRIGHT}{Fore.LIGHTBLACK_EX}{BACKUP_VOLUME}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Found projects: {Style.BRIGHT}{Fore.LIGHTBLACK_EX}{len(PROJECTS)}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Skip git remote: {Style.BRIGHT}{Fore.LIGHTBLACK_EX}{SKIP_GIT_REMOTE}{Style.RESET_ALL}")