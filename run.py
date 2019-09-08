import requests
import os
import re
import hashlib
import line_notify

if not os.path.isfile('page_list.txt'):
    print('You must to edit file page_list.txt to run this system.')
    exit()

line_regex = re.compile(r'^.*?\|https?://([\w\W\.\-]*?)/?')
url_regex = re.compile(r'^https?://([\w\W\.\-]*?)/?')

urls = []

f = open('page_list.txt', 'r')
for line in f.readlines():
    if line == '':
        continue
    line = line.replace('\n', '')
    line = line.replace('\r', '')
    lr = line_regex.match(line)
    ur = url_regex.match(line)
    if lr:
        # print('Okay\n\t', line.split('|')[1])
        urls.append(tuple(line.split('|')[:2]))
    elif ur:
        # print('You\'ve provided only url. Assume as find everything.')
        # print('\t', line)
        urls.append(('*', line))
    else:
        print('IDK This line:')
        print('\t', line)
        exit()
f.close()

urls = list(set(urls))

print('Load hash history.')

history = {}

if os.path.isfile('history.txt'):
    f = open('history.txt', 'r')
    for line in f.readlines():
        if line == '':
            continue
        line = line.replace('\n', '')
        line = line.replace('\r', '')
        history[line.split('|')[0]] = str(line.split('|')[1])

for cond, site in urls:
    print('Get: ', site)
    site_data = requests.get(site)
    site_text = site_data.text
    new_hash = hashlib.md5(site_text.encode('utf-8')).hexdigest()
    if site not in history:
        history[site] = ''
    if new_hash != history[site]:
        print('\tThere is new update.')
        if cond == '*' or cond in site_text:
            print('\t\tUpdate is acceptable.')
            msg = site
            msg += '\nHas updated the content.'
            line_notify.send(msg)
    else:
        print('\tNo update')
    history[site] = new_hash

f = open('history.txt', 'w')
for site, hash_val in history.items():
    f.write(site)
    f.write('|')
    f.write(hash_val)
    f.write('\n')
