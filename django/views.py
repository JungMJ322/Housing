from django.shortcuts import render, redirect
from django.db import connection
from .models import *
from django.core import serializers
import json
import matplotlib.pyplot as plt

def getRate():
    # "CMPET_RATE": "lacked"
    # 전체 데이터 개수를 구하고
    # "lacked"개수를 구하고
    # 경쟁률 있는 매물 개수 = (1) - (2)
    # {'all': int, 'lacked': int, 'rate': int}
    try:
        cursor = connection.cursor()

        strSql = "SELECT count(*) FROM competition WHERE compet_rate='lacked'"
        result = cursor.execute(strSql)
        rate_lacked = cursor.fetchall()

        strSql = "SELECT count(*) FROM competition"
        result = cursor.execute(strSql)
        rate_all = cursor.fetchall()

        connection.commit()
        connection.close()
    except:
        connection.rollbak()
        print('얘 db랑 연결이 잘 안됐단다')

    result = dict()
    result['all'] = int(rate_all[0][0])
    result['lacked'] = int(rate_lacked[0][0])
    result['rate'] = result['all'] - result['lacked']

    return result


def getInfra():
    # {'data' : {'house_manage_no': int, 'school': {'id': []}, 'subway': {'id': []}, 'mart': {'id': []},
    #       'park': {'id': []}, 'hospital': {'id': []}, 'busstop': {'id': []}, 'convinient': {'id': []}},
    # 'cnt': {'total': int,'school': int, 'subway': int, 'mart': int, 'park': int, 'hospital': int, 'busstop': int, 'convinient': }}
    temp = Infra.objects.all().values()
    infra_list = list(temp)

    infra_keys = list(infra_list[0].keys())
    infra_keys.pop(0)

    sub_list = list()
    cnt_dict = dict()

    cnt_dict['total'] = 0
    for key in infra_keys:
        cnt_dict[key] = 0

    for infra in infra_list:
        sub_dict = dict()

        sub_dict['house_manage_no'] = infra['house_manage_no']
        for key in infra_keys:
            sub_dict[key] = json.loads(json.loads(json.dumps(infra[key])))
            cnt_dict[key] = cnt_dict[key] + len(sub_dict[key]['id'])
        sub_list.append(sub_dict)

        cnt_dict['total'] = cnt_dict['total'] + 1

    result = dict()
    result['data'] = sub_list
    result['cnt'] = cnt_dict

    return result

def getSoldMean():
    #[{name: '1~3', data: [얼마, 얼마, 얼마, 얼마]}, {name: 'n단위', data: [얼마, 얼마, 얼마, 얼마]},
    # {name: 'n단위', data: [얼마, 얼마, 얼마, 얼마]}]

    cursor = connection.cursor()

    ranks = [[1,2,3], [4,5,6], [7,8,9], [10,11,12], [13,14,15], [16,17,18], [19,20,21]]
    quarters = [['01','02','03'], ['04','05','06'], ['07','08','09'], ['10','11','12']]
    years = [20, 21, 22]

    result = list()
    for rank in ranks:
        ran = f'{rank[0]}~{rank[2]}'
        maen_dict = dict()
        mean_list = list()
        for year in years:
            for quarter in quarters:
                strSql = f"""SELECT avg(mean_cost)
                            FROM sold_cost_mean 
                            WHERE (area_grade like '{rank[0]}__' or area_grade like '{rank[1]}__' or area_grade like '{rank[2]}__' )
                            and (month like '__{year}{quarter[0]}' or month like '__{year}{quarter[1]}' or month like '__{year}{quarter[2]}')"""
                result = cursor.execute(strSql)
                sold_mean = cursor.fetchall()
                mean = sold_mean[0][0]
                if mean == None:
                    mean_list.append(0)
                else:
                    mean_list.append(round(mean, 2))
        maen_dict['name'] = ran
        maen_dict['data'] = mean_list
        print(maen_dict)
        # result.append(maen_dict)

    connection.commit()
    connection.close()

    print(result)


def index(request):
    # temp = Infra.objects.all().values()
    # try:
    #     cursor = connection.cursor()
    #
    #     strSql = "SELECT count(*) FROM competition WHERE compet_rate='lacked'"
    #     result = cursor.execute(strSql)
    #     print(result)
    #     infra = cursor.fetchall()
    #     print(infra)
    #     connection.commit()
    #     connection.close()
    # except:
    #     connection.rollbak()
    #     print('얘 db랑 연결이 잘 안됐단다')
    #
    # print(list(infra[0]))
    # rate_dict = getRate()
    # infra_dict = getInfra()
    getSoldMean()

    return render(request, 'index.html')

