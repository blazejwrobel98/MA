from scripts import create


class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password


if __name__ == '__main__':
    # username = input('Enter username: ')
    # password = input('Enter password: ')
    # user = user(username, password)
    user = user("xxx", "xxx")
    description = 'sources\description.txt'
    with open(description, 'r') as f:
        description = f.read().split('\n')

    options = {}
    for line in description:
        if line != '':
            tmp = line.split(':')
            if len(tmp) == 2:
                options[tmp[0].strip()] = tmp[1].strip()
            else:
                options[tmp[0].strip()] = ''
    for option in options:
        print(f'{option}: {options[option]}')

    if options['Action to be performed'] == 'Create internal static DNS A record':
        result = create.create_internal_static_dns_a_record(options, user)
        if result[0]:
            print('New A record created')
        else:
            print(f'Something went wrong: {result[1]}')

