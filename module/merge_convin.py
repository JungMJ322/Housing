import json
from getLocation import kakao_location
from convinient_change import savefile


def convin_change(count_relay, file_name):
    with open("../data/json/" + file_name,'r', encoding="utf-8") as f:
        rdr = json.load(f)
        count = count_relay
        total_list = []
        for i in rdr:
            try:
                loc = kakao_location(i['place'])
            except:
                continue
            i['id'] = count
            i['lat'] = loc['lat']
            i['lot'] = loc['lot']
            total_list.append(i)
            count += 1
        return count, total_list


def convin_merge():
    total_list = []
    count, list_temp = convin_change(0, "cu.json")
    total_list.append(list_temp)
    count, list_temp = convin_change(count, "GS25.json")
    total_list.append(list_temp)
    count, list_temp = convin_change(count, "sevenEleven.json")
    total_list.append(list_temp)
    total_list = sum(total_list, [])
    savefile("asd", "convinient", total_list)


if __name__ == "__main__":
    convin_merge()
