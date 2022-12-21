import os


def available_scripts(path):
    scripts = os.listdir(path)
    return scripts


def scripts_launcher(files, path):
    print(f'Available scripts: ')
    for i in range(len(files)):
        with open(f'{path}/{files[i]}', 'r') as f:
            print(f'{i + 1} - {files[i]} - {f.readline().strip()}')
    print(f'For exit press 0')

    while True:
        try:
            script_number = int(input('Enter script number: ')) - 1
            if script_number in range(len(files)) or script_number == -1:
                break
            else:
                print('Wrong number!')
        except ValueError:
            print('Wrong number!')
    return script_number


def main():
    path = "./scripts/"
    files = available_scripts(path)
    while True:
        script_number = scripts_launcher(files, path)
        if script_number == -1:
            print("Bye!")
            break
        os.system(f'python {path}/{files[script_number]}')


if __name__ == "__main__":
    main()
