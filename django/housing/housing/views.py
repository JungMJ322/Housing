from django.shortcuts import render, redirect
from .models import Busstop, SoldCostMean, Detail, Hospital, Infra, Mart, Park, School, Subway


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

def load_detail_sido(sido):
    temp = Detail.objects.all().values()
    temp_list=[]
    for i in temp:
        if i['address'].find(sido) != -1 and i['address'].find(sido) < 3:
            temp_list.append(i)

    return temp_list

def index(request):
    temp = load_detail_sido("울산")
    print(temp)
    return render(request, 'index.html')