import os


# load file to_find.txt to find_list


def load_file(param):
    with open(param, 'r') as f:
        find_list = f.read().splitlines()
    return find_list


if __name__ == '__main__':
    find_list = load_file('to_find.txt')
    # look for find_list elements in all files in "files" directory and subdirectories
    for root, dirs, files in os.walk('files'):
        for file in files:
            with open(os.path.join(root, file), 'r') as f:
                try:
                    for line in f:
                        for find in find_list:
                            if find in line:
                                if "Deny" in line:
                                    with open('found.txt', 'a', encoding='utf-8') as f:
                                        f.write(os.path.join(root, file) + line + '\n')
                                    break
                except UnicodeDecodeError:
                    pass
