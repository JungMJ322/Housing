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
    for i in range(1, 13):
        # with open("../data/sold_cost/20." + str(i) + ".csv", "r", encoding='euc-kr') as f:
        #     rdr = csv.reader(f)
        data = spark.read.json("/Housing/data/hadoop_upload/20."+str(i)+".csv", encoding="cp949", header=True)
        data_coll = data.collect()
        rdr = list()
        for j in data_coll:
            rdr.append(j.asDict())

        code_dict = create_code_dict()
        temp_list = []
        save_data = {}

        for i in rdr:
            temp = dict()
            temp['place'] = i[0]
            temp['area_grade'] = str(int(float(i[5]) // 10)) + '단위'
            try:
                temp['area_code'] = code_dict[i[0]]
            except KeyError:
                del temp
            temp['month'] = i[6]
            temp['cost'] = int(i[8].replace(",",""))
            temp_list.append(temp)

        month = temp['month']
        save_data[month] = temp_list

        with open(str(month)+'.json', 'w', encoding='utf-8') as f1:
            f1.write(json.dumps(temp_list, ensure_ascii=False))

    for i in range(1, 13):
        data = spark.read.json("/Housing/data/hadoop_upload/21."+str(i)+".csv", encoding="cp949", header=True)
        data_coll = data.collect()
        rdr = list()
        for j in data_coll:
            rdr.append(j.asDict())

        code_dict = create_code_dict()
        temp_list = []
        save_data = {}

        for i in rdr:
            temp = dict()
            temp['place'] = i[0]
            temp['area_grade'] = str(int(float(i[5]) // 10)) + '단위'
            try:
                temp['area_code'] = code_dict[i[0]]
            except KeyError:
                del temp
            temp['month'] = i[6]
            temp['cost'] = int(i[8].replace(",",""))
            temp_list.append(temp)

        month = temp['month']
        save_data[month] = temp_list

        with open(str(month)+'.json', 'w', encoding='utf-8') as f2:
            f2.write(json.dumps(temp_list, ensure_ascii=False))

    for i in range(1, 3):
        data = spark.read.json("/Housing/data/hadoop_upload/22."+str(i)+".csv", encoding="cp949", header=True)
        data_coll = data.collect()
        rdr = list()
        for j in data_coll:
            rdr.append(j.asDict())
        code_dict = create_code_dict()
        temp_list = []
        save_data = {}

        for i in rdr:
            temp = dict()
            temp['place'] = i[0]
            temp['area_grade'] = str(int(float(i[5]) // 10)) + '단위'
            try:
                temp['area_code'] = code_dict[i[0]]
            except KeyError:
                del temp
            temp['month'] = i[6]
            temp['cost'] = int(i[8].replace(",",""))
            temp_list.append(temp)

        month = temp['month']
        save_data[month] = temp_list

        with open(str(month)+'.json', 'w', encoding='utf-8') as f3:
            f3.write(json.dumps(temp_list, ensure_ascii=False))

    data1 = json.load(f1)
    data2 = json.load(f2)
    data3 = json.load(f3)

    with open("../data/sold_cost/sold_cost_data.json", "w") as sold_cost_data:
        json.dump(data1+data2+data3, sold_cost_data, ensure_ascii=False)

if __name__ == "__main__":
    save_json()