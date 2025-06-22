from project_status import UPTODATE_CACHE
from settings import BACKUP_VOLUME, IGNORE_FILES
from colorama import Fore, Style
import os
import shutil
import time

def progress_bar(name, progress, i, total):
    term_width = shutil.get_terminal_size((80, 20)).columns
    bar_width = term_width - 40  # leave space for text
    
    progress = int(bar_width * min(max(progress, 0), 1))
    
    bar = f"[{'#' * progress}{'.' * (bar_width - progress)}]"
    
    if(progress == bar_width):
        print(f"{os.path.basename(name)[:20]:20} {bar} ({i + 1}/{total})")
    else:    
        print(f"{os.path.basename(name)[:20]:20} {bar} ({i + 1}/{total})", end='\r')

def backup(subdir, project, i, total):
    backup_path = os.path.join(BACKUP_VOLUME, project, os.path.basename(subdir))
    os.makedirs(backup_path, exist_ok=True)

  
    files_to_copy = []
    total_size = 0

    for root, dirs, files in os.walk(subdir):
        dirs[:] = [d for d in dirs if not any(ignored in os.path.join(root, d) for ignored in IGNORE_FILES)]
        for fname in files:
            src_file = os.path.join(root, fname)
            rel_path = os.path.relpath(src_file, subdir)
            dst_file = os.path.join(backup_path, rel_path)

            if any(ignored in src_file for ignored in IGNORE_FILES):
                continue

            try:
                src_stat = os.stat(src_file)
                dst_stat = os.stat(dst_file)
                if src_stat.st_size == dst_stat.st_size and int(src_stat.st_mtime) == int(dst_stat.st_mtime):
                    continue
            except FileNotFoundError:
                pass 

            files_to_copy.append((src_file, dst_file))
            total_size += os.path.getsize(src_file)
    
    copied_size = 0

    for src_file, dst_file in files_to_copy:
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)

        file_size = os.path.getsize(src_file)
        with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
            while True:
                chunk = fsrc.read(8192)
                if not chunk:
                    break
                fdst.write(chunk)
                copied_size += len(chunk)

                progress = copied_size / total_size if total_size else 1.0
                progress_bar(subdir, progress, i, total)
        shutil.copystat(src_file, dst_file)
    

for project in UPTODATE_CACHE:
    to_update = [subdir for subdir in UPTODATE_CACHE[project] if not UPTODATE_CACHE[project][subdir]]
    for i, subdir in enumerate(to_update):
        if not UPTODATE_CACHE[project][subdir]:
            backup(subdir, project, i, len(to_update))