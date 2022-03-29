from django.shortcuts import render, redirect
from .models import Busstop, SoldCostMean, Detail, Hospital, Infra, Mart, Park, School, Subway


def extract(key_list, data):
    return_dict = {}
    count=0
    for j in key_list:
        return_dict[j] = []

    for i in data:
        if count > 100:
            break
        for j in key_list:
            return_dict[j].append(i[j])
        count+=1

    return return_dict


def index(request):
    stops = SoldCostMean.objects.all().values()
    output = extract(['place_code', 'area_grade'], stops)
    print(output)

    return render(request, 'index.html')