#!/usr/bin/env python3
"""Run with Herdr closed after installing and launching it once."""
from pathlib import Path
import datetime,shutil,os
source=Path(__file__).resolve().parent/'config'
target=Path(os.environ.get('HERDR_APP_HOME',str(Path.home()/'.config/herdr-app'))).expanduser()
if source == target.resolve():
    raise SystemExit('Herdr already uses this checkout as its configuration directory.')
if not target.is_dir():
    raise SystemExit('Install and launch Herdr once, then quit it before running this installer.')
backup=target.with_name(target.name+'-before-transfer-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
backup.mkdir()
for name in ['layouts','themes','mods','keys.json','settings.json']:
    old=target/name
    if old.is_dir(): shutil.copytree(old,backup/name)
    elif old.exists(): shutil.copy2(old,backup/name)
for folder in ['layouts','themes','mods']:
    shutil.copytree(source/folder,target/folder,dirs_exist_ok=True)
for name in ['keys.json','settings.json']:
    shutil.copy2(source/name,target/name)
print('Installed. Backup:',backup)
print("Open Herdr, then run: herdr-app do layout.switch '{\"name\":\"zro\"}'")
