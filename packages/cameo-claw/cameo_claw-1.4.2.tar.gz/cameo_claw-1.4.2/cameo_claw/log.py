from datetime import datetime
from cameo_claw.file import mkdir


def log(s):
    mkdir('./data/log')
    with open('./data/log/log.txt', 'a') as f:
        f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: {s}\n')
