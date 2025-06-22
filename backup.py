import os
import yaml

SETTINGS_FILE = 'settings.yml'
# Loadede from settings.yml
BACKUP_VOLUME = ''
PROJECTS = []

if not os.path.isfile(SETTINGS_FILE):
    raise FileNotFoundError("Projects file 'projects.yml' not found.")

with open(SETTINGS_FILE) as stream:
    try:
        data = yaml.safe_load(stream)
        PROJECTS = data.get('projects', [])
        BACKUP_VOLUME = data.get('backup_volume', '')
    except yaml.YAMLError as exc:
        print(exc)

print(f'Using backup volume: {BACKUP_VOLUME}')
print(f'Found projects: {len(PROJECTS)}')