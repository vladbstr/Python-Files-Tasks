import os
import time
import subprocess
import json
import argparse


def scan():

    mydict={}

    for root, dirs, files in os.walk('.', topdown=True):
        dirs.clear()
        for file in files:
            file_size = os.stat(file).st_size
            changed_time = time.strftime('%Y/%m/%d-%H:%M', time.gmtime(os.path.getmtime(file)))
            output = subprocess.check_output(['attrib', file],shell=False, universal_newlines=True)[:9]
            attrs = {'H':0, 'R':0}
            for char in output:
                if char in attrs:
                    attrs[char] = 1      
            data={'FileSize':file_size,'Changed':changed_time,'Hidden':attrs['H'],'ReadOnly':attrs['R']}
            mydict[file] = data
    
    with open('cache.json', 'w') as fp:
        json.dump(mydict, fp)


def query():
    try:
        with open('cache.json', 'rb') as fp:
            data_json = json.load(fp)
    except FileNotFoundError:
        scan()
        with open('cache.json', 'rb') as fp:
            data_json = json.load(fp)

    files_number = 0
    hidden_files = 0
    readonly_files = 0

    for key in data_json.keys():
        files_number += 1
        if data_json[key]['Hidden'] == 1:
            hidden_files += 1
        if data_json[key]['ReadOnly'] == 1:
            readonly_files += 1
    
    percent_readonly = (readonly_files/files_number)*100
    percent_hidden = (hidden_files/files_number)*100

    print('Number of files: '+str(files_number))
    sorted_dict = sorted(data_json.items(), key = lambda x: -x[1]['FileSize'])

    if files_number >= 5:
        print('Top 5 largest files: '+str(sorted_dict[4][0])+', '+str(sorted_dict[3][0])+', '+str(sorted_dict[2][0])+', '+str(sorted_dict[1][0])+', '+str(sorted_dict[0][0]))
    else:
        print('Number of files is less than 5.... :(')

    print('{:.2f}'.format(percent_hidden)+'% are hidden')
    print('{:.2f}'.format(percent_readonly)+'% are read-only')

    contor_dict={}
    for key in data_json.keys():
        if data_json[key]['Changed'][:7] in contor_dict:
            contor_dict[data_json[key]['Changed'][:7]] += 1
        else:
            contor_dict[data_json[key]['Changed'][:7]] = 1
         
    sorted_items = sorted(contor_dict.items()) 

    for item in sorted_items:
        print(item[0]+': '+str(item[1])+' modified files')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Internship preselection task',
        epilog='To complete the action, enter the following commands: scan or query' 
    )

    parser.add_argument('command',help='scan/query : py Run.py')
    args = parser.parse_args()

    if args.command == 'scan':
        scan()
    elif args.command == 'query':
        query()
    else:
        raise argparse.ArgumentTypeError('Invalid Command!')










