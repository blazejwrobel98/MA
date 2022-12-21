# script to compare data about sites between iris and cmdb #


source_files = ['source_files/iris.csv', 'source_files/cmdb_locations.csv']
output_files = 'output_files/script_2.csv'


def main():
    """
    main function
    """
    iris_data = get_iris_data(source_files[0])
    cmdb_data = get_cmdb_data(source_files[1])
    compared = compare_data(iris_data, cmdb_data)
    for site in compared:
        print(site, compared[site])


def get_iris_data(file_name):
    """
    get iris data
    """
    iris_data = []
    with open(file_name, 'r') as iris_file:
        for line in iris_file:
            line = line.strip().split(';')
            iris_data.append([line[0], line[3]])
    return iris_data


def get_cmdb_data(file_name):
    """
    get cmdb data
    """
    cmdb_data = []
    with open(file_name, 'r') as cmdb_file:
        for line in cmdb_file:
            line = line.strip().replace('"','').split(',')
            cmdb_data.append([line[0], line[2], line[3]])
    return cmdb_data


def compare_data(iris_data, cmdb_data):
    compared_data = {}
    for iris_site in iris_data:
        compared_data[iris_site[0]] = {'iris': iris_site[1], 'cmdbL': '', 'cmdbR': ''}
    for cmdb_site in cmdb_data:
        if cmdb_site[0] in compared_data:
            compared_data[cmdb_site[0]]['cmdbL'] = cmdb_site[1]
            compared_data[cmdb_site[0]]['cmdbR'] = cmdb_site[2]
        else:
            compared_data[cmdb_site[0]] = {'iris': '', 'cmdbL': cmdb_site[1], 'cmdbR': cmdb_site[2]}
    return compared_data


if __name__ == '__main__':
    main()
