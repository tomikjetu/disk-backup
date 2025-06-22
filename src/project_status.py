import os
from colorama import Fore, Style
from settings import BACKUP_VOLUME, PROJECTS, SKIP_GIT_REMOTE
import subprocess

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

def isRemote(subdir_path):
    try:
        result = subprocess.run(
            ['git', 'remote', '-v'],
            cwd=subdir_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        if result.stdout.strip():
            return True
    except Exception:
        pass

    return False

UPTODATE_CACHE = {}

def isUpToDate(subdir_path, project_name):
    # Cache per project
    if project_name not in UPTODATE_CACHE:
        UPTODATE_CACHE[project_name] = {}
    if subdir_path in UPTODATE_CACHE[project_name]:
        return UPTODATE_CACHE[project_name][subdir_path]

    def sha_dir(path):
        signature = []
        for root, dirs, files in os.walk(path):
            for fname in sorted(files):
                fpath = os.path.join(root, fname)
                try:
                    stat = os.stat(fpath)
                    rel_path = os.path.relpath(fpath, path)
                    signature.append((rel_path, stat.st_size, stat.st_mtime))
                except Exception:
                    continue
        return hash(tuple(signature))

    backup_path = os.path.join(BACKUP_VOLUME, project_name, os.path.basename(subdir_path))
    if not os.path.exists(backup_path):
        UPTODATE_CACHE[project_name][subdir_path] = False
        return False
    src_sha = sha_dir(subdir_path)
    backup_sha = sha_dir(backup_path)
    result = src_sha == backup_sha
    UPTODATE_CACHE[project_name][subdir_path] = result
    return result

def getStatus(subdir, project):
    subdir_path = os.path.join(project.get('path'), subdir)
    project_name = project.get('name')
    if os.path.exists(os.path.join(BACKUP_VOLUME, project_name, subdir)):
        if isUpToDate(subdir_path, project_name):
            return 'BACKED'
        else:
            return 'UPDATED'
    else:
        if SKIP_GIT_REMOTE and isRemote(subdir_path):
            return 'GIT_SKIPPED'
        if project_name not in UPTODATE_CACHE:
            UPTODATE_CACHE[project_name] = {}
        UPTODATE_CACHE[project_name][subdir_path] = False
        return 'NOT_TRACKED'

def printStatus(subdir, project):
    print(f"Loading {subdir}...", end='\r')
    status = getStatus(subdir, project)
    color = PROJECT_STATUS[status]['color']
    icon = PROJECT_STATUS[status]['icon']
    print(f"    [{color}{icon}{Style.RESET_ALL}] {color}{subdir}{Style.RESET_ALL}     ")

print(f"[{PROJECT_STATUS['BACKED']['icon']}] {PROJECT_STATUS['BACKED']['color']}{PROJECT_STATUS['BACKED']['label']}{Style.RESET_ALL}", end=' ')
print(f"[{PROJECT_STATUS['UPDATED']['icon']}] {PROJECT_STATUS['UPDATED']['color']}{PROJECT_STATUS['UPDATED']['label']}{Style.RESET_ALL}", end=' ')
print(f"[{PROJECT_STATUS['NOT_TRACKED']['icon']}] {PROJECT_STATUS['NOT_TRACKED']['color']}{PROJECT_STATUS['NOT_TRACKED']['label']}{Style.RESET_ALL}", end=' ')
print(f"[{PROJECT_STATUS['GIT_SKIPPED']['icon']}] {PROJECT_STATUS['GIT_SKIPPED']['color']}{PROJECT_STATUS['GIT_SKIPPED']['label']}{Style.RESET_ALL}")
stats = {
    'BACKED': 0,
    'UPDATED': 0,
    'NOT_TRACKED': 0,
    'GIT_SKIPPED': 0
}
for project in PROJECTS:
    print(f"{Fore.CYAN}Project: {Style.BRIGHT}{project.get('name')}{Style.RESET_ALL}")
    if not os.path.isdir(project.get('path')):
        print(f"{Fore.RED}  [!] Directory does not exist: {project.get('path')}{Style.RESET_ALL}")
        continue
    subdirs = [d for d in os.listdir(project.get('path')) if os.path.isdir(os.path.join(project.get('path'), d))]
    for subdir in subdirs:
        if subdir.startswith('.'): # Skip hidden directories
            continue
        printStatus(subdir, project)
        status = getStatus(subdir, project)
        stats[status] += 1
print(f"{Fore.CYAN}Summary:")
up_to_date_count = stats['BACKED'] + stats['GIT_SKIPPED']
needs_backup_count = stats['UPDATED'] + stats['NOT_TRACKED']

print(f"{Fore.GREEN}    UP TO DATE{Style.RESET_ALL}  : {up_to_date_count} ({PROJECT_STATUS['BACKED']['label']}: {stats['BACKED']}, {PROJECT_STATUS['GIT_SKIPPED']['label']}: {stats['GIT_SKIPPED']})")
print(f"{Fore.RED}    NEEDS BACKUP{Style.RESET_ALL}: {needs_backup_count} ({PROJECT_STATUS['UPDATED']['label']}: {stats['UPDATED']}, {PROJECT_STATUS['NOT_TRACKED']['label']}: {stats['NOT_TRACKED']})")