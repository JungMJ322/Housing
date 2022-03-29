from django.shortcuts import render, redirect
from .models import Busstop, SoldCostMean, Detail, Hospital, Infra, Mart, Park, School, Subway, Competition, PlaceCode


def extract_ByKeys(key_list, data):
    return_dict = {}
    count=0
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

def load_detail_sido(sido): ## In = sido: 서울, 광주 etc.. / Out = sido 위치 내 detail table datalist
    temp = Detail.objects.all().values()
    temp_list=[]
    for i in temp:
        if i['address'].find(sido) != -1 and i['address'].find(sido) < 3:
            temp_list.append(i)

    return temp_list


def create_place_code_list(sido):
    place_code = PlaceCode.all().values()
    place_code_list = []
    for i in place_code:
        if i['place'].find(sido) != -1 and i['place'].find(sido) < 3:
            place_code_list.append(i)
    return place_code_list


def sido_competition(sido): # In : 시도 2글자  Out: min_val, max_val 두개값 리턴 min의 경우 lack이 있으면 lack 반환
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







def index(request):
    a, b = sido_competition('광주')
    print(a, b)
    return render(request, 'index.html')