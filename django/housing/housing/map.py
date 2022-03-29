
from .models import Busstop, SoldCostMean, Detail, Hospital, Infra, Mart, Park, School, Subway,Competition
import folium
import json
from .views import *


def sigunmap(sido):
    # 시도 센터 베이스 맵
    map_list={"서울":[11,[37.52709816646034, 126.97901707971378]],
                "인천":[28,[37.502878144962544, 126.60311587249441]],
                "세종":[17,[36.52148014975415, 127.25144476071442]],
                "대전":[30,[36.35095437682017, 127.39386502081653]],
                "대구":[27,[35.85974265376218, 128.5815381066346]],
                "울산":[31,[35.528728550499906, 129.28214674523906]],
                "광주":[29,[35.137331918132126, 126.84698460809767]],
                "부산":[26,[35.17289405279072, 129.03210838811316]]}
    center = map_list[f'{sido}'][1]
    m = folium.Map(location=center,
                   tiles='cartodbpositron',
                   zoom_start=8)
    sido_cd = map_list[f'{sido}'][0]



    geoSigun = '../status/sigun.json'
    with open(f'{geoSigun}', 'r', encoding="utf-8") as f:
        json_data = json.load(f)



    style = {
             'weight': 2,
             'opacity': 1,
             'color': 'black',
             'fillOpacity': 0
    }
    getlist = json_data["features"]
    for feature in getlist:
        if feature["properties"]["SIG_CD"][0:2] == sido_cd:
            folium.GeoJson(feature, name=f'{sido}', tooltip ="<b>"+feature["properties"]["SIG_ENG_NM"]+"</b>", style_function=lambda x : style, zoom_on_click=True).add_to(m)

    h_list = load_detail_sido(sido)

    for h in h_list:
        lat=float(h['lat'])
        lng=float(h['lot'])
        tooltip=h['house_manage_no']
        color='#E77E00'
        folium.CircleMarker(location=[lat,lng],tooltip=tooltip,radius= 100, color=color,fill=True,fill_opacity=0.4,stroke=False ).add_to(m)


    print(m)
    m.save(f'{sido}.html')
    print('됐음')
    pass

#h_list = load_detail_sido("광주")
#print(h_list)




