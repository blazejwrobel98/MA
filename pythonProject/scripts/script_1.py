# WAN devices assigned to the wrong sitecode #

source_file = "./source_files/script_1.csv"
destination_file = "./output_files/script_1.csv"


def read_file(file):
    with open(file, "r") as f:
        list = []
        data = f.readlines()
        for line in data:
            list.append(line.replace('"','').replace('\n','').split(","))
        return list


def write_file(file, data):
    with open(file, "w") as f:
        for line in data:
            f.write(line + "\n")


def main(data):
    # check if Network sitecode is same as Name[:5]
    # if not, add whole entry to list
    list = []
    for line in data:
        if line[1] != line[2][:5]:
            list.append(line[2])
    return list


if __name__ == "__main__":
    data = read_file(source_file)
    output = main(data)
    write_file(destination_file, output)
