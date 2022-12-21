# Script to get all Network sitecodes from list exported from solarwinds report "all nodes all ip" #

src = "./source_files/script_3.csv"
dst = "./output_files/script_3.csv"


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
    sitecodes = []
    for el in output:
        if len(el.strip().replace(' ', '')) > 5:
            if el.strip().replace(' ', '')[5] == '-':
                if "ANIRA" in el or "AVPN" in el or "VCE" in el:
                    sitecodes.append(el.strip()[:5])

    sitecodes = list(dict.fromkeys(sitecodes))
    print(sitecodes)
    print("Total: " + str(len(sitecodes)))
    write_file(dst, sitecodes)
