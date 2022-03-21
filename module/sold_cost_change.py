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
    with open('../data/sold_cost/sold_cost_test.csv', 'r', encoding='euc-kr') as f:
        code_dict = create_code_dict()
        rdr = csv.reader(f)
        temp_list = []
        save_data = {}

        for i in rdr:
            temp = dict()
            temp['place'] = i[0]
            temp['area_grade'] = str(int(float(i[5]) // 10)) + '단위'
            try:
                temp['area_code'] = code_dict[i[0]]
            except KeyError:
                temp['area_code'] = 'unknown'
            temp['month'] = i[6]
            temp['cost'] = i[8]
            temp_list.append(temp)

        month = temp['month']
        save_data[month] = temp_list

    with open('./json/sold_data'+str(month)+'.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(save_data, ensure_ascii=False))

if __name__ == "__main__":
    save_json()