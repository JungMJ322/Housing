import csv
import json



def create_code_dict():
    with open('../data/sold_cost/area_code.txt', 'r', encoding='euc-kr') as f:
        rdr = csv.reader(f, delimiter='\t')
        count = 0
        code_dict = {}
        for row in rdr:
            code_dict[row[1]] = row[0]
        return code_dict



def save_json():

    temp_list = []

    for i in range(1, 13):
        with open("../data/sold_cost/20." + str(i) + ".csv", "r", encoding='euc-kr') as f:
            code_dict = create_code_dict()
            rdr = csv.reader(f)

            for i in rdr:
                temp = dict()
                temp['place'] = i[0]
                temp['area_grade'] = str(int(float(i[5]) // 10)) + '단위'
                try:
                    temp['area_code'] = code_dict[i[0]]
                except KeyError:
                    continue
                temp['month'] = i[6]
                temp['cost'] = int(i[8].replace(",",""))
                temp_list.append(temp)


    for i in range(1, 13):
        with open("../data/sold_cost/21." + str(i) + ".csv", "r", encoding='euc-kr') as f:
            code_dict = create_code_dict()
            rdr = csv.reader(f)

            for i in rdr:
                temp = dict()
                temp['place'] = i[0]
                temp['area_grade'] = str(int(float(i[5]) // 10)) + '단위'
                try:
                    temp['area_code'] = code_dict[i[0]]
                except KeyError:
                    continue
                temp['month'] = i[6]
                temp['cost'] = int(i[8].replace(",",""))
                temp_list.append(temp)



    for i in range(1, 3):
        with open("../data/sold_cost/22." + str(i) + ".csv", "r", encoding='euc-kr') as f:
            code_dict = create_code_dict()
            rdr = csv.reader(f)

            for i in rdr:
                temp = dict()
                temp['place'] = i[0]
                temp['area_grade'] = str(int(float(i[5]) // 10)) + '단위'
                try:
                    temp['area_code'] = code_dict[i[0]]
                except KeyError:
                    continue
                temp['month'] = i[6]
                temp['cost'] = int(i[8].replace(",",""))
                temp_list.append(temp)


    with open('sold_cost_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(temp_list, ensure_ascii=False))


if __name__ == "__main__":
    save_json()