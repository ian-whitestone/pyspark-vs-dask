import os

from datetime import datetime
import argparse

def parse_line(line):
    parts = line.split('|')
    data = {}
    data['ts'] = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S,%f')
    data['text'] = parts[-1].split(':')[-1].strip()
    return data

def parse_log(filename):
    lines = []

    with open(filename, 'r') as f_in:
        content = f_in.read()
        tests = content.split(' BEGIN: Running test:')
        tests = [test for test in tests if ' dsk_filter_' in test]

        for test in tests:
            process_test(test)

def process_test(test):
    test_name = test.split('\n')[0].strip()
    lines = []
    for line in test.split('\n'):
        if len(line.split('|')) == 3 and \
            ('START' in line or 'FINISH' in line):
            lines.append(parse_line(line))

    for i in range(0, len(lines), 2):
        start = lines[i]['ts']
        finish = lines[i + 1]['ts']
        secs = (finish - start).total_seconds()
        print ('%d (s) %0.2f (min): %s' % (secs, secs/60, lines[i]['text']))

    total_secs = (lines[-1]['ts'] - lines[0]['ts']).total_seconds()
    print ('%d (s) %0.2f (min): Total time for test: %s'
           % (total_secs, total_secs/60, test_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse some logs')
    parser.add_argument('filename', metavar='f', type=str,
                        help='Path to the log file')
    args = parser.parse_args()
    parse_log(args.filename)
