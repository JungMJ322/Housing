from django.shortcuts import render, redirect
from .models import Busstop, SoldCostMean, Detail, Hospital, Infra, Mart, Park, School, Subway


def extract_ByKeys(key_list, object_name):
    return_dict = {}
    for i in key_list:
        temp_list = object_name.objects.values_list(i)
        return_dict[i] = temp_list
    return return_dict

    # return_dict = {}
    # count=0
    # for j in key_list:
    #     return_dict[j] = []
    #
    # for i in data:
    #     if count > 100:
    #         break
    #     for j in key_list:
    #         return_dict[j].append(i[j])
    #     count += 1


def all_object_call(object_name):
    return object_name.objects.all().values()


# def extract_ByFilter(dict_list):
#     key_list = dict_list.keys()
#     value_list = dict_list.values()
#     for i in range(len(key_list)):


def index(request):
    output = SoldCostMean.objects.filter(area_grade='3단위').filter(mean_cost=5200.0).values()
    print(output)

    return render(request, 'index.html')