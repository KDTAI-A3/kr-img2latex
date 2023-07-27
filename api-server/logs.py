import datetime


def log_format(text):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = f'[{current_time}] '
    return header + text


def log_write(text):
    with open('./api_log.log', 'a', encoding='utf-8') as log:
        log.write(log_format(text)+'\n')