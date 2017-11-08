import json
import os
import sys

def help():
    print("ls: list all existing marks")
    print("get name: get the dest dir for short cut 'name'")
    print("mark name: mark the current dir with the shortcut 'name'")
    print("unmark name: unmark the current dir with the shortcut 'name'")
    print("h or help: show help information")

def fail(msg):
    print(msg)
    exit(-1)

def get_file():
    if not ('HOME' in os.environ):
        fail('please set up HOME environment variable first')
    home_dir = os.environ['HOME']
    file_path = os.path.join(home_dir, '.pmarks')
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(json.dumps({}))
    return file_path

def get_existing_marks():
    file_path = get_file()
    data = ''
    with open(file_path) as f:
        data = f.read()
    if data == '':
        d = {}
    else:
        d = json.loads(data)
    return d

def list_marks():
    d = get_existing_marks()
    for k, v in d.items():
        print('{}\t->\t{}'.format(k, v))

def save_marks(d):
    file_path = get_file()
    with open(file_path, 'w') as f:
        f.write(json.dumps(d, indent=4, sort_keys=True))

def mark(name):
    d = get_existing_marks()
    if name in d:
        fail('{} already exists'.format(name))
    d[name] = os.getcwd()
    save_marks(d)

def unmark(name):
    d = get_existing_marks()
    if not (name in d):
        fail('{} not found'.format(name))
    del(d[name])
    save_marks(d)

def get_mark(name):
    d = get_existing_marks()
    if not (name in d):
        fail('{} not found'.format(name))
    print(d[name])

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == 'h' or sys.argv[1] == 'help':
        help()
    elif sys.argv[1] == 'ls':
        list_marks()
    elif sys.argv[1] == 'mark' and len(sys.argv) >= 3:
        mark(sys.argv[2])
    elif sys.argv[1] == 'unmark' and len(sys.argv) >= 3:
        unmark(sys.argv[2])
    elif sys.argv[1] == 'get' and len(sys.argv) >= 3:
        get_mark(sys.argv[2])
    else:
        fail("unknown command or missing command arguments, please check the help info")
    exit()
