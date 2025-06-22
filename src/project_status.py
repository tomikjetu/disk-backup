import os
from colorama import Fore, Style
from settings import BACKUP_VOLUME, PROJECTS, SKIP_GIT_REMOTE
PROJECT_STATUS = {
    'BACKED': {
        'color': Fore.GREEN,
        'label': 'Backed up',
        'icon': 'B'
    },
    'UPDATED': {
        'color': Fore.RED,
        'label': 'Changed',
        'icon': 'N'
    },
    'NOT_TRACKED': {
        'color': Fore.YELLOW,
        'label': 'New project',
        'icon': 'N'
    },
    'GIT_SKIPPED': {
        'color': Fore.LIGHTBLACK_EX,
        'label': 'Git remote',
        'icon': 'G'
    }
}

def isRemote(path):
    # Implement logic to check if the path is a remote git repository
    return False

def isUpToDate(subdir_path):
    # Implement logic to check file signature
    return True

def getStatus(subdir):
    subdir_path = os.path.join(project.get('path'), subdir)
    if os.path.exists(os.path.join(BACKUP_VOLUME, project.get('name'), subdir)):
        if isUpToDate(subdir_path):
            return 'BACKED'
        else:
            return 'UPDATED'
    else:
        if SKIP_GIT_REMOTE and isRemote(subdir_path):
            return 'GIT_SKIPPED'
        return 'NOT_TRACKED'

def printStatus(subdir):
    status = getStatus(subdir)
    color = PROJECT_STATUS[status]['color']
    icon = PROJECT_STATUS[status]['icon']
    print(f"    [{color}{icon}{Style.RESET_ALL}] {color}{subdir}{Style.RESET_ALL}")

print(f"[{PROJECT_STATUS['BACKED']['icon']}] {PROJECT_STATUS['BACKED']['color']}{PROJECT_STATUS['BACKED']['label']}{Style.RESET_ALL}", end=' ')
print(f"[{PROJECT_STATUS['UPDATED']['icon']}] {PROJECT_STATUS['UPDATED']['color']}{PROJECT_STATUS['UPDATED']['label']}{Style.RESET_ALL}", end=' ')
print(f"[{PROJECT_STATUS['NOT_TRACKED']['icon']}] {PROJECT_STATUS['NOT_TRACKED']['color']}{PROJECT_STATUS['NOT_TRACKED']['label']}{Style.RESET_ALL}", end=' ')
print(f"[{PROJECT_STATUS['GIT_SKIPPED']['icon']}] {PROJECT_STATUS['GIT_SKIPPED']['color']}{PROJECT_STATUS['GIT_SKIPPED']['label']}{Style.RESET_ALL}")
for project in PROJECTS:
    print(f"{Fore.CYAN}Project: {Style.BRIGHT}{project.get('name')}{Style.RESET_ALL}")
    if not os.path.isdir(project.get('path')):
        print(f"{Fore.RED}  [!] Directory does not exist: {project.get('path')}{Style.RESET_ALL}")
        continue
    subdirs = [d for d in os.listdir(project.get('path')) if os.path.isdir(os.path.join(project.get('path'), d))]
    for subdir in subdirs:
        if subdir.startswith('.'): # Skip hidden directories
            continue
        printStatus(subdir)

