# Script to export device names from list exported for script_3.py #

src = "./source_files/script_3.csv"
dst = "./output_files/script_4.csv"


def read_file(src):
    with open(src, "r") as f:
        list = []
        data = f.readlines()
        for line in data:
            list.append(line.replace('"', '').replace('\n', ''))
        return list


def write_file(dst, data):
    with open(dst, "w") as f:
        for line in data:
            f.write(line + "\n")


if __name__ == "__main__":
    data = read_file(src)
    output = []
    for line in data:
        output.append(line)
    devices = []
    for el in output:
        if len(el.strip().replace(' ', '')) > 5:
            if el.strip().replace(' ', '')[5] == '-':
                devices.append(el)

    devices = list(dict.fromkeys(devices))
    print(devices)
    print("Total: " + str(len(devices)))
    write_file(dst, devices)
