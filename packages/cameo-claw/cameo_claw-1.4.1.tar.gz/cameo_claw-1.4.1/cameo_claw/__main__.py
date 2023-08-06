import sys

from cameo_claw import lst_demo_url

help_message = f'''
python3 -m pip install cameo_claw --upgrade
python3 -c "
from cameo_claw import it_filter_group
lst_url={lst_demo_url}
target_directory = './data/topic_filter_group/'
int_total=len(lst_url)
lst_distinct_column = ['deviceId', 'localTime', 'sensorId']
lst_column_match = [['sensorId', 'pm2_5'], ['sensorId', 'voc']]
sort_column = 'localTime'
lst_group_by_column = ['deviceId']
for int_progress, done_url in it_filter_group(lst_url, target_directory, lst_distinct_column, lst_column_match, sort_column, lst_group_by_column):
        pass
"
'''


def show_help():
    if len(sys.argv) == 1:
        print(help_message)


if __name__ == '__main__':
    show_help()
