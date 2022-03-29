from django.shortcuts import render, redirect
from .models import Busstop, SoldCostMean, Detail, Hospital, Infra, Mart, Park, School, Subway, PlaceCode
from .map import *


def extract_ByKeys(key_list, data):
    return_dict = {}
    count = 0
    for j in key_list:
        return_dict[j] = []

    for i in data:
        if count > 100:
            break
        for j in key_list:
            return_dict[j].append(i[j])
        count += 1
    return return_dict


def all_object_call(object_name):
    return object_name.objects.all().values()


# def extract_ByFilter(dict_list):
#     key_list = dict_list.keys()
#     value_list = dict_list.values()
#     for i in range(len(key_list)):

def load_detail_sido(sido):  ## In = sido: 서울, 광주 etc.. / Out = sido 위치 내 detail table datalist
    temp = Detail.objects.all().values()
    temp_list = []
    for i in temp:
        if i['address'].find(sido) != -1 and i['address'].find(sido) < 3:
            temp_list.append(i)

    return temp_list


def create_place_code_list(sido):
    place_code = PlaceCode.objects.all().values()
    place_code_list = []
    for i in place_code:
        if i['place'].find(sido) != -1 and i['place'].find(sido) < 3:
            place_code_list.append(i)
    return place_code_list


def sido_competition(sido):  # 시도별 경쟁률 min max값 리턴 In : 시도 2글자  Out: min_val, max_val 두개값 리턴 min의 경우 lack이 있으면 lack 반환
    temp = load_detail_sido(sido)
    house_manage_list = []
    for i in temp:
        house_manage_list.append(i['house_manage_no'])

    compet_list = []
    min_val = 0
    compet = Competition.objects.all().values()
    for i in compet:
        if i['house_manage_no'] in house_manage_list:
            if i['compet_rate'] != 'lacked':
                compet_list.append(float(i['compet_rate']))
            else:
                min_val = 'lack'

    if min_val == 0:
        min_val = min(compet_list)

    max_val = max(compet_list)

    print(compet_list)

    return min_val, max_val


def find_infra_count(
        sido):  # sido 별 각 infra 갯수, In : 시도이름, Out : dict {"school":0, "subway":0, "mart":0, "park":0, "hospital":0, 'busstop':0, 'convinient': 0}꼴
    detail_list = load_detail_sido(sido)
    house_manage_list = []
    infra_list = []
    infra_count = {"school": 0, "subway": 0, "mart": 0, "park": 0, "hospital": 0, 'busstop': 0, 'convinient': 0}
    for i in detail_list:
        house_manage_list.append(i["house_manage_no"])

    infra = Infra.objects.all().values()
    for i in infra:
        if i['house_manage_no'] in house_manage_list:
            infra_count['school'] += len(i['school'])
            infra_count['subway'] += len(i['subway'])
            infra_count['mart'] += len(i['mart'])
            infra_count['park'] += len(i['park'])
            infra_count['hospital'] += len(i['hospital'])
            infra_count['busstop'] += len(i['busstop'])
            infra_count['convinient'] += len(i['convinient'])

    return infra_count


def sido_supply_size(sido):  # sido 별 공급 규모 총합 / In : sido, Out : sum of supply_size
    temp = load_detail_sido(sido)
    supply_size = 0;
    for i in temp:
        supply_size += i['supply_size']

    print(supply_size)
    return supply_size


def load_sold_cost(sido, area_grade):  # sido, 면적 별 매매가 정보 날짜 오름차순 정리 In = sido, 면적 Out = 해당 data
    place_code = create_place_code_list(sido)
    place_code_list = []
    for i in place_code:
        place_code_list.append(i['place_code'])

    temp = SoldCostMean.objects.all().values()
    return_list = []
    for i in temp:
        if (i['place_code'] in place_code_list) and (i['area_grade'] == area_grade):
            return_list.append(i)

    sorted_list = sorted(return_list, key=lambda item: item['month'])

    return sorted_list



def index(request):
    # sigunmap('광주')
    return render(request, 'index.html')
