import csv
import sys

try:
    if sys.argv[1][-4:] == ".csv":
        path = "examples/from_sulaiman/csv_data_analyzer" + sys.argv[1]
    else:
        path = "examples/from_sulaiman/csv_data_analyzer" + sys.argv[1] + ".csv"
    try:
        dict_list = []
        csvfile = open(path, "r")
        csvdictread = csv.DictReader(csvfile)
        for dictread in csvdictread:
            dict_list.append(dictread)
        if sys.argv[2] == "read":
            if sys.argv[3] == "with_header":
                headers = ""
                for header in dict_list[0].keys():
                    headers += header + " "
                print(headers.strip())
            csv_values = ""
            for row in dict_list:
                for value in row.values():
                    csv_values += value + " "
                print(csv_values.strip())
        if sys.argv[2] == "max":
            if len(sys.argv) == 4:
                try:
                    if dict_list[0][sys.argv[3]].isnumeric():
                        max = 0
                        for row in dict_list:
                            if int(row[sys.argv[3]]) > max:
                                max = int(row[sys.argv[3]])
                        print("The maximum number for the " + sys.argv[3] + " column is:" + str(max))
                    else:
                        print(sys.argv[3] + "is not a numerical column")
                except TypeError:
                    print(sys.argv[3] + "is not a header")
            else:
                max_dict = {}
                for row in dict_list:
                    for headers in row.keys():
                        if row[header].isnumeric():
                            if int(max_dict[header]) < int(row[header]):
                                max_dict[header] = row[header]
                print("The maximum value of each numeric header:\n")
                for max_head in max_dict.keys():
                    print(max_head + "=>" + max_dict[max_head])
        if sys.argv[2] == "min":
            if len(sys.argv) == 4:
                try:
                    if dict_list[0][sys.argv[3]].isnumeric():
                        min = 10000000000000000
                        for row in dict_list:
                            if int(row[sys.argv[3]]) < min:
                                min = int(row[sys.argv[3]])
                        print("The maximum number for the " + sys.argv[3] + " column is:" + str(min))
                    else:
                        print(sys.argv[3] + "is not a numerical column")
                except TypeError:
                    print(sys.argv[3] + "is not a header")
            else:
                min_dict = {}
                for row in dict_list:
                    for headers in row.keys():
                        if row[header].isnumeric():
                            if int(min_dict[header]) > int(row[header]):
                                min_dict[header] = row[header]
                print("The maximum value of each numeric header:\n")
                for min_head in min_dict.keys():
                    print(min_head + "=>" + min_dict[min_head])
        if sys.argv[2] == "average":
            if len(sys.argv) == 4:
                try:
                    if dict_list[0][sys.argv[3]].isnumeric():
                        average = 0
                        for row in dict_list:
                            average += int(row[sys.argv[3]])
                        print("The maximum number for the " + sys.argv[3] + " column is:" + str(average))
                    else:
                        print(sys.argv[3] + "is not a numerical column")
                except TypeError:
                    print(sys.argv[3] + "is not a header")
            else:
                average_dict = {}
                for row in dict_list:
                    for headers in row.keys():
                        if row[header].isnumeric():
                            if not(header in average_dict):
                                average_dict[header] = 0
                            average_dict[header] += int(row[header])
                print("The maximum value of each numeric header:\n")
                for average_head in average_dict.keys():
                    print(average_head + "=>" + average_dict[average_head])

    except FileNotFoundError:
        print("CSV file doesn't exsist")
except IndexError:
    print("Missing Argument Error")
except FileNotFoundError:
    print("csv file doen't exsist")