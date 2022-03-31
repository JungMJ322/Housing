from django.shortcuts import render, redirect
from .models import Busstop, SoldCostMean, Detail, Hospital, Infra, Mart, Park, School, Subway, PlaceCode, Competition
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.db import connection
import folium
seven_sido_list = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종']


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

def gu_count(sido):
    detail_list = load_detail_sido(sido)
    temp_list = []
    count_dict = {}
    for i in detail_list:
        gu = i['address'].split(' ')[1]
        temp_list.append(gu)
    temp_list = list(set(temp_list))


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

    # print(compet_list)

    return min_val, max_val

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



def find_infra_count(sido):  # sido 별 각 infra 갯수, In : 시도이름, Out : dict {"school":0, "subway":0, "mart":0, "park":0, "hospital":0, 'busstop':0, 'convinient': 0}꼴
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
        supply_size += int(i['supply_size'])

    # print(supply_size)
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


def make_pie_chart_params(dict_list):
    total = 0
    key_list = dict_list.keys()
    series = {"type": 'pie', 'name': 'test'}
    data_list = []
    for i in key_list:
        total += dict_list[i]
    for i in key_list:
        data_list.append([i, round((dict_list[i] / total) * 100, 1)])

    # print(data_list)
    series['data'] = data_list
    return series


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




def make_bar_chart_params(dict_list):
    temp_dict = {}
    temp_dict['type'] = 'column'
    temp_dict['colorByPoint'] = True
    temp_dict['data'] = dict_list
    temp_dict['showInLegend'] = False
    return temp_dict


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


def count_sido_hssply():
    total_dict = {}
    total_list = []
    for i in seven_sido_list:
        total_dict[i] = 0
        temp = load_detail_sido(i)
        for j in temp:
            total_dict[i] += int(j['supply_size'])
        total_list.append(total_dict[i])

    return total_list


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
            # print(sum)
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

def find_type_percent(sido, table_kind, table_data):
    temp_list = []
    for i in table_data:
        if i['place'].find(sido) != -1 and i['place'].find(sido) < 3:
            temp_list.append(i)
    temp_dict = {}
    if table_kind == 'school':
        for i in temp_list:
            try:
                temp_dict[i['school_kind']] += 1
            except KeyError:
                temp_dict[i['school_kind']] = 0
    else:
        for i in temp_list:
            try:
                temp_dict[i['park_type']] += 1
            except KeyError:
                temp_dict[i['park_type']] = 0

    return temp_dict

def getRateSido(sido):
    # "CMPET_RATE": "lacked"
    # 전체 데이터 개수를 구하고
    # "lacked"개수를 구하고
    # 경쟁률 있는 매물 개수 = (1) - (2)
    # {'total': int, 'lack': int, 'non_lack': int}
    cursor = connection.cursor()

    strSql = f"""select count(*)
                from competition join detail on (competition.house_manage_no = detail.house_manage_no)
                where address like '{sido}%'
                and compet_rate = 'lacked'"""
    success = cursor.execute(strSql)
    rate_lacked = cursor.fetchall()

    strSql = f"""select count(*)
                from competition join detail on (competition.house_manage_no = detail.house_manage_no)
                where address like '{sido}%'"""
    success = cursor.execute(strSql)
    rate_all = cursor.fetchall()

    connection.commit()
    connection.close()

    result = dict()
    total = int(rate_all[0][0])
    result['lacked'] = int(rate_lacked[0][0])
    result['non_lacked'] = total - result['lacked']

    return result


def rankCompet(sido, max_count=5):
    cursor = connection.cursor()

    strSql = f"""select house_name, compet_rate
                from competition join detail on (competition.house_manage_no = detail.house_manage_no)
                where address like '{sido}%' and compet_rate != 'lacked'"""
    success = cursor.execute(strSql)
    rank_all = list(cursor.fetchall())

    rank_list = list()
    for rank in rank_all:
        rank_list.append(list(rank))

    for rank in rank_list:
        rank[1] = float(rank[1])

    rank_list.sort(key=lambda x: -x[1])

    result = list()
    for i in range(max_count):
        re_dict = dict()
        re_dict['rank'] = i + 1
        re_dict['name'] = rank_list[i][0]
        re_dict['compet'] = rank_list[i][1]
        result.append(re_dict)

    return result



def index(request):

    #temp= rankCompet("대구")
    #print(temp)

    return render(request, 'index.html')


def sidomap(request):

    sido = request.GET['sido']

    if sido:
        map_list = {"서울": [11, [37.53709816646034, 126.97901707971378]],
                    "인천": [28, [37.502878144962544, 126.60311587249441]],
                    "세종": [17, [36.52148014975415, 127.25144476071442]],
                    "대전": [30, [36.35095437682017, 127.39386502081653]],
                    "대구": [27, [35.85974265376218, 128.5815381066346]],
                    "울산": [31, [35.528728550499906, 129.28214674523906]],
                    "광주": [29, [35.137331918132126, 126.84698460809767]],
                    "부산": [26, [35.17289405279072, 129.03210838811316]]}
        center = map_list[f'{sido}'][1]
        m = folium.Map(location=center,
                       tiles='cartodbpositron',        #cartodbpositron
                       zoom_start=11, width='100%', height='100%')
        h_list = load_detail_sido(sido)

        for h in h_list:
            try:
                lat = float(h['lat'])
                lng=float(h['lot'])
                tooltip='<b>'+h['house_name']+'</b>'
                color= '#6ABBEA'    #6ABBEA
                folium.CircleMarker(location=[lat, lng], tooltip=tooltip, radius= 10, color=color,fill=True,fill_opacity=0.5,stroke=True ).add_to(m)
            except:
                pass
        map = m._repr_html_()

        result=rankCompet(sido)

        context = {
            'map': map,
            'rank1': result[0], 'rank2': result[1], 'rank3': result[2], 'rank4': result[3], 'rank5': result[4]
        }

        return render(request, 'city.html', context)

    else:
        return redirect('index')


def ajax_return(request):
    if request.method == 'POST':
        request_list = []
        for temp, b in request.POST.items():
            request_list.append(b)
        sido = request.POST['sidoname']

        if request_list[1] == '1':
            temp = find_infra_count(sido)
            return_first_tab = {'type':'first'}
            return_first_tab['fst'] = make_pie_chart_params(temp)

            temp_quarter = getQuarterSupply(sido)
            temp_quarter[0]['data'] = temp_quarter[0]['data'][0:10]
            return_first_tab['trd'] = temp_quarter

            return_first_tab = json.dumps(return_first_tab, ensure_ascii=False)
            return HttpResponse(return_first_tab)

        if request_list[1] == '2':
            return_sec_tab = {'type': 'second'}
            json_data = getSoldMean(sido)
            for i in json_data:
                i['data'] = i['data'][0:9]
            print(json_data)
            return_sec_tab['fst'] = json_data

            temp = getSupplySize(sido)
            list_temp = make_bar_chart_params(temp[0]['data'])
            temp[0]['data'] = list_temp
            return_sec_tab['snd'] = temp
            # print(return_sec_tab)



            return_sec_tab = json.dumps(return_sec_tab, ensure_ascii=False)
            return HttpResponse(return_sec_tab)

        if request_list[1] == '3':
            return_thi_tab = {'type': 'third'}
            data_school = School.objects.all().values()
            temp = find_type_percent(sido, 'school', data_school)
            return_school = make_pie_chart_params(temp)
            return_thi_tab['trd'] = return_school

            temp_half = getRateSido(sido)
            temp_half_pie = make_pie_chart_params(temp_half)
            return_thi_tab['fth'] = temp_half_pie

            data_park = Park.objects.all().values()
            temp_park = find_type_percent(sido, 'park', data_park)
            return_park = make_pie_chart_params(temp_park)
            return_thi_tab['fiveth'] = return_park

            temp2 = getInfraSido(sido)
            list_temp = []
            for i in temp2:
                temp_dict = {}
                if i['name'] == '도붕구':
                    continue
                temp_dict['name'] = i['name']
                temp_dict['data'] = i['data']
                list_temp.append(temp_dict)

            return_thi_tab['sixth_data'] = list_temp
            return_thi_tab['sixth_list'] = temp2[0]['gu_list']

            return_thi_tab = json.dumps(return_thi_tab, ensure_ascii=False)
            return HttpResponse(return_thi_tab)
        else:
            return HttpResponse(1)


        # if request.POST['chart_kind'] == 'pie':
        #     sido = request.POST['sidoname']
        #     temp = find_type_percent('서울', 'park', Park.objects.all().values())
        #     temp_return = make_pie_chart_params(temp)
        #     series = json.dumps(temp_return, ensure_ascii=False)
        #     return HttpResponse(series)
        # if request.POST['chart_kind'] == 'bar':
        #     return_json = count_sido_hssply()
        #     return_data = make_bar_chart_params(return_json)
        #     return_data = json.dumps(return_data, ensure_ascii=False)
        #     print(return_data)
        #     return HttpResponse(return_data)
