# script to check if name of device is in node id #

# load file

src = "./source_files/script_5.csv"
dst = "./output_files/script_5.csv"


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
        if "ANIRA" in el.split(',')[1]:
            if el.split(',')[0] not in el.split(',')[1].replace(':', ''):
                devices.append(el.split(',')[1])
        if "AVPN" in el.split(',')[1]:
            if el.split(',')[0] not in el.split(',')[1]:
                devices.append(el.split(',')[1])

    devices = list(dict.fromkeys(devices))
    print(devices)
    print("Total: " + str(len(devices)))
    write_file(dst, devices)
