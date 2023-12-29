import os
import re
import shutil
from datetime import datetime

from win32_setctime import setctime


reg = re.compile(r'\w+_(\d+@)?(?P<date>\d{1,2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2}|\d{8}_\d{6})(?P<move>.*_thumb.*)?.*')

for path, dirs, files in os.walk('photos'):
    for fil in files:
        if not (match := reg.match(fil)):
            continue

        file_path = os.path.join(path, fil)
        relative_path = os.path.relpath('photos', path)
        if match.group('move'):
            shutil.move(file_path, os.path.join('thumb', relative_path, fil))
            print(f'Moved {fil}')
            continue

        print(file_path)
        creation_str = match.group('date')
        try:
            creation_dt = datetime.strptime(creation_str, '%d-%m-%Y_%H-%M-%S').timestamp()
        except ValueError:
            creation_dt = datetime.strptime(creation_str, '%Y%m%d_%H%M%S').timestamp()
        # print('\t', datetime.fromtimestamp(os.path.getctime(file_path)))
        os.utime(file_path, (creation_dt, creation_dt))
        setctime(file_path, creation_dt)
