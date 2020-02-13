import csv
import numpy as np
# file_name - with data File name for
def load_data(file_name):
    with open(file_name, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    # Fix for Weird error on csvfile
    #data[0][0] = data[0][0][3:]
    
    data_map_list = []
    for i in range(1, len(data)):
        student_data = {}
        for j in range(len(data[0])):
            student_data[data[0][j]] = data[i][j]
        data_map_list.append(student_data)

    return data_map_list

def get_character_list(data_maps, catagory, unique=False, sort=False):
    res  = []
    for data in data_maps:
        res.append(data[catagory])

    if unique:
        res = list(set(res))
    if sort:
        res.sort()
    return res

def save_to_csv(data, name):
    f = open(name, "w+")
    res = ''
    if isinstance(data[0], list):
        for i in range(len(data)):
            for j in range(len(data[0])):
                res += str(data[i][j]) + ','
            res = res[:-1] + '\n'
        res = res[:-1]

    else:

        for i in range(len(data)):
            res += str(data[i]) + '\n'
        res = res[:-1]

    f.write(res)

    f.close()


#res = load_data('GTIA-EA-2020.csv')
#save_to_csv((get_character_list(res, 'Major-Primary', unique=True,sort=True)), 'represented_majors.csv')
