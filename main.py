import os
import re
import shutil
from datetime import datetime

from win32_setctime import setctime

reg = re.compile(r'photo_(\d+)@(\d{1,2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})(_thumb)?.jpg')

for path, dirs, files in os.walk('photos'):
    for fil in files:
        file_path = os.path.join(path, fil)
        relative_path = os.path.relpath('photos', path)
        if not (match := reg.match(fil)):
            continue
        if match.group(3):
            shutil.move(file_path, os.path.join('thumb', relative_path, fil))
            print(f'Moved {fil}')
            continue

        print(file_path)
        creation_dt = datetime.strptime(match.group(2), '%d-%m-%Y_%H-%M-%S').timestamp()
        # print('\t', datetime.fromtimestamp(os.path.getctime(file_path)))
        os.utime(file_path, (creation_dt, creation_dt))
        setctime(file_path, creation_dt)
