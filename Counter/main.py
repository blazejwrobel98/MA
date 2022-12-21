import json

source_files = ["demeesap2459.json", "demeesap2461.json", "demeesap2462.json"]


def main(source_file):
    with open(source_file, "r") as f:
        data = json.load(f)
        return data


def counter(data):
    counter_dict = {
        "cflow.inputint": 0,
        "cflow.outputint": 0,
        "cflow.octets": 0,
    }
    for i in data:
        if "cflow" in i["_source"]["layers"].keys():
            for headers in (i["_source"]["layers"]["cflow"].keys()):
                if headers.startswith("Set"):
                    for elm in (i["_source"]["layers"]["cflow"][headers].keys()):
                        if elm.startswith("Flow"):
                            for eleme in (i["_source"]["layers"]["cflow"][headers][elm].keys()):
                                if 'cflow.inputint' in eleme:
                                    counter_dict["cflow.inputint"] += int(
                                        i["_source"]["layers"]["cflow"][headers][elm]["cflow.inputint"])
                                if 'cflow.outputint' in eleme:
                                    counter_dict["cflow.outputint"] += int(
                                        i["_source"]["layers"]["cflow"][headers][elm]["cflow.outputint"])
                                if 'cflow.octets' in eleme:
                                    try:
                                        counter_dict["cflow.octets"] += int(
                                            i["_source"]["layers"]["cflow"][headers][elm]["cflow.octets"])
                                    except:
                                        pass

    return counter_dict


if __name__ == "__main__":
    for i in range(len(source_files)):
        data = main(source_files[i])
        counters = counter(data)
        print(source_files[i])
        print(counters)
        print(f"octets: {counters['cflow.octets']}")
        print(f"octets to bits: {int(counters['cflow.octets'])*8}")
        print(f"bits / time: {(int(counters['cflow.octets'])*8)/1020}")
        print(f"kbps: {((int(counters['cflow.octets'])*8)/1020)/1024}")
        print("\n")
