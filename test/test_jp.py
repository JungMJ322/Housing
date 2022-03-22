import requests
#
# url = "http://cu.bgfretail.com/store/list_Ajax.do"
# data = {
#     'pageIndex': 1,
#     'listType':'',
#     'jumpoCode':'',
#     'jumpoLotto':'',
#     'jumpoToto': '',
#     'jumpoCash': '',
#     'jumpoHour': '',
#     'jumpoCafe': '',
#     'jumpoDelivery':'',
#     'jumpoBakery': '',
#     'jumpoFry': '',
#     'jumpoMultiDevice':'',
#     'jumpoPosCash':'' ,
#     'jumpoBattery':'' ,
#     'jumpoAdderss':'' ,
#     'jumpoSido': '서울특별시',
#     'jumpoGugun':'' ,
#     'jumpodong':'' ,
#     'user_id': '',
#     'sido': '서울특별시',
#     'Gugun': '',
#     'jumpoName':''
# }
# res = requests.post(url, data=data)
#
# print(dir(res.request))
# print(res.request.body)

url = "http://cu.bgfretail.com/store/list_Ajax.do?pageIndex=1&listType=&jumpoCode=&jumpoLotto=&jumpoToto=&jumpoCash=&jumpoHour=&jumpoCafe=&jumpoDelivery=&jumpoBakery=&jumpoFry=&jumpoMultiDevice=&jumpoPosCash=&jumpoBattery=&jumpoAdderss=&jumpoSido=&jumpoGugun=&jumpodong=&user_id=&sido=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&Gugun=&jumpoName="
res = requests.post(url)
print(res.text)