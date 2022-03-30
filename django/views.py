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
        success = cursor.execute(strSql)
        rate_lacked = cursor.fetchall()

        strSql = "SELECT count(*) FROM competition"
        success = cursor.execute(strSql)
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


def getInfraSido(sido):
    # sido 입력받으면 그 sido에
    # {name: 'park', gu_list:[1구, 2구, 3구], data:[1구 name개수, 2구 name개수, 3구 name개수]}
    infra_list = ['school', 'subway', 'park', 'hospital', 'convinient']
    cursor = connection.cursor()
    result = list()

    # 이름 중복되지 않도록 namelist만듬
    name_dict = dict()
    for infra in infra_list:
        strSql = f"""select place from {infra} where place like '{sido}%' and place not like '%도붕구%';"""
        success = cursor.execute(strSql)
        convinient_list = list(cursor.fetchall())
        # gu를 키로 갖는 gu_dict 초기화
        for convinient in convinient_list:
            convinient = list(convinient)

            gu = convinient[0].split()[1]
            gu_find = gu.find('구')
            gun_find = gu.find('군')
            if gu_find > 0:
                name_dict[gu[:gu_find+1]] = 0
            elif gun_find > 0:
                name_dict[gu[:gun_find+1]] = 0

    name_list = list(name_dict.keys())

    # name_list에 따라 각각의 infra 카운트
    for infra in infra_list:
        strSql = f"""select place from {infra} where place like '{sido}%' and place not like '%도붕구%';"""
        success = cursor.execute(strSql)
        convinient_list = list(cursor.fetchall())

        gu_dict = dict()
        for name in name_list:
            gu_dict[name] = 0

        # 각각의 gu cnt
        for convinient in convinient_list:
            convinient = list(convinient)
            gu = convinient[0].split()[1]
            gu_find = gu.find('구')
            gun_find = gu.find('군')
            if gu_find > 0:
                gu_dict[gu[:gu_find+1]] = gu_dict[gu[:gu_find+1]] + 1
            elif gun_find > 0:
                gu_dict[gu[:gun_find+1]] = gu_dict[gu[:gun_find+1]] + 1


        gu_dict2 = dict()
        gu_dict2['name'] = infra
        gu_dict2['gu_list'] = list(gu_dict.keys())
        gu_dict2['data'] = list(gu_dict.values())
        result.append(gu_dict2)

    connection.commit()
    connection.close()
    return result


def getSoldMean(sido):
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
                            FROM sold_cost_mean join place_code on (sold_cost_mean.place_code = place_code.place_code)
                            WHERE (area_grade like '{rank[0]}__' or area_grade like '{rank[1]}__' or area_grade like '{rank[2]}__' )
                            and (month like '__{year}{quarter[0]}' or month like '__{year}{quarter[1]}' or month like '__{year}{quarter[2]}')
                            and place like '{sido}%'"""
                success = cursor.execute(strSql)
                sold_mean = cursor.fetchall()
                mean = sold_mean[0][0]
                if mean == None:
                    mean_list.append(0)
                else:
                    mean_list.append(round(mean, 2))
        maen_dict['name'] = ran
        maen_dict['data'] = mean_list
        result.append(maen_dict)

    connection.commit()
    connection.close()

    return result


def getSupplySize(sido):
    # sido 입력받으면 그 sido에
    # {gu_list:[1구, 2구, 3구], data:[1구 name개수, 2구 name개수, 3구 name개수]}
    cursor = connection.cursor()
    result = list()

    name_dict = dict()
    # 이름 중복되지 않도록 namelist만듬
    strSql = f"""select address, supply_size from detail
                where address like '{sido}%';"""
    success = cursor.execute(strSql)
    supply_names = list(cursor.fetchall())

    # gu를 키로 갖는 gu_dict 초기화
    for name in supply_names:
        name = list(name)
        gu = name[0].split()[1]
        gu_find = gu.find('구')
        gun_find = gu.find('군')
        if gu_find > 0:
            name_dict[gu[:gu_find + 1]] = 0
        elif gun_find > 0:
            name_dict[gu[:gun_find + 1]] = 0

    name_list = list(name_dict.keys())

    gu_dict = dict()
    for name in name_list:
        gu_dict[name] = 0

    # 각각의 gu의 supply_sum
    for supply in supply_names:
        supply = list(supply)
        gu = supply[0].split()[1]
        gu_find = gu.find('구')
        gun_find = gu.find('군')
        if gu_find > 0:
            gu_dict[gu[:gu_find + 1]] = gu_dict[gu[:gu_find + 1]] + supply[1]
        elif gun_find > 0:
            gu_dict[gu[:gun_find + 1]] = gu_dict[gu[:gun_find + 1]] + supply[1]

    gu_dict2 = dict()
    gu_dict2['gu_list'] = list(gu_dict.keys())
    gu_dict2['data'] = list(gu_dict.values())
    result.append(gu_dict2)

    connection.commit()
    connection.close()
    return result


def getSupplySize(sido):
    # sido 입력받으면 그 sido에
    # {gu_list:[1구, 2구, 3구], data:[1구 name개수, 2구 name개수, 3구 name개수]}
    cursor = connection.cursor()
    result = list()

    name_dict = dict()
    # 이름 중복되지 않도록 namelist만듬
    strSql = f"""select address, supply_size from detail
                where address like '{sido}%';"""
    success = cursor.execute(strSql)
    supply_names = list(cursor.fetchall())
    print(supply_names)
    # gu를 키로 갖는 gu_dict 초기화
    for name in supply_names:
        name = list(name)
        gu = name[0].split()[1]
        gu_find = gu.find('구')
        gun_find = gu.find('군')
        if gu_find > 0:
            name_dict[gu[:gu_find + 1]] = 0
        elif gun_find > 0:
            name_dict[gu[:gun_find + 1]] = 0

    name_list = list(name_dict.keys())

    gu_dict = dict()
    for name in name_list:
        gu_dict[name] = 0

    # 각각의 gu의 supply_sum
    for supply in supply_names:
        supply = list(supply)
        gu = supply[0].split()[1]
        gu_find = gu.find('구')
        gun_find = gu.find('군')
        if gu_find > 0:
            gu_dict[gu[:gu_find + 1]] = gu_dict[gu[:gu_find + 1]] + supply[1]
        elif gun_find > 0:
            gu_dict[gu[:gun_find + 1]] = gu_dict[gu[:gun_find + 1]] + supply[1]

    gu_dict2 = dict()
    gu_dict2['gu_list'] = list(gu_dict.keys())
    gu_dict2['data'] = list(gu_dict.values())
    result.append(gu_dict2)

    connection.commit()
    connection.close()
    return result


def getQuarterSupply(sido):
    #[{name: '1~3', data: [얼마, 얼마, 얼마, 얼마]}, {name: 'n단위', data: [얼마, 얼마, 얼마, 얼마]},
    # {name: 'n단위', data: [얼마, 얼마, 얼마, 얼마]}]
    cursor = connection.cursor()

    quarters = [['01','02','03'], ['04','05','06'], ['07','08','09'], ['10','11','12']]
    years = [20, 21, 22]

    result = list()
    sum_dict = dict()
    sum_list = list()
    for year in years:
        for quarter in quarters:
            strSql = f"""SELECT sum(supply_size)
                        FROM detail
                        WHERE (START_RECEIPT like '__{year}-{quarter[0]}%' or START_RECEIPT like '__{year}-{quarter[1]}%' 
                                or START_RECEIPT like '__{year}-{quarter[2]}%')
                        and ADDRESS like '{sido}%'"""
            success = cursor.execute(strSql)
            supply_size_sum = cursor.fetchall()
            sum = supply_size_sum[0][0]
            print(sum)
            if sum == None:
                sum_list.append(0)
            else:
                sum_list.append(int(sum))
    sum_dict['name'] = sido
    sum_dict['data'] = sum_list
    result.append(sum_dict)

    connection.commit()
    connection.close()

    return result


def index(request):
    # temp = Infra.objects.all().values()
    # try:
    #     cursor = connection.cursor()
    #
    #     strSql = "SELECT count(*) FROM competition WHERE compet_rate='lacked'"
    #     success = cursor.execute(strSql)
    #     print(result)
    #     infra = cursor.fetchall()
    #     print(infra)
    #     connection.commit()
    #     connection.close()
    # except:
    #     connection.rollbak()
    #     print('얘 db랑 연결이 잘 안됐단다')
    #
    # rate_dict = getRate()
    # infra_dict = getInfra()
    # sold_mean = getSoldMean('대전')
    # infra_sido = getInfraSido('서울')
    # supply_size = getSupplySize('서울')
    quarter_supply = getQuarterSupply('서울')
    print(quarter_supply)

    return render(request, 'index.html')

