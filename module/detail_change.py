import json
from convinient_change import savefile

def change_detail():
    with open("../data/json/detail.json", "r", encoding="utf-8") as f:
        rdr = json.load(f)
        change_list = []
        for i in rdr:
            temp_dict = {}
            temp_dict['HOUSE_MANAGE_NO'] = i['HOUSE_MANAGE_NO']
            temp_dict['HOUSE_NAME'] = i['HOUSE_NM']
            temp_dict['HOUSE_SECD'] = i['HOUSE_SECD']
            temp_dict['RENT_SECD'] = i['RENT_SECD']
            temp_dict['ADDRESS'] = i['HSSPLY_ADRES']
            temp_dict['SUPPLY_SIZE'] = i['TOT_SUPLY_HSHLDCO']
            temp_dict['PLACE_CODE'] = i['place_code']
            temp_dict['LAT'] = i['lat']
            temp_dict['LOT'] = i['lon']
            temp_dict['START_RECEIPT'] = i['RCEPT_BGNDE']
            temp_dict['BUILD_COMP'] = i['BSNS_MBY_NM']
            temp_dict['SPECLT_RDN_EARTH_AT'] = i['SPECLT_RDN_EARTH_AT']
            temp_dict['MDAT_TRGET_AREA_SECD'] = i['MDAT_TRGET_AREA_SECD']
            temp_dict['IMPRMN_BSNS_AT'] = i['IMPRMN_BSNS_AT']
            temp_dict['LRSCL_BLDLND_AT'] = i['LRSCL_BLDLND_AT']
            change_list.append(temp_dict)
    data1 = list(map(dict, set(tuple(sorted(d.items())) for d in change_list)))

    savefile(" ", "detail_change", data1)


if __name__ == "__main__":
    change_detail()
