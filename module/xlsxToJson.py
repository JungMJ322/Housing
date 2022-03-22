import pandas as pd

location = './json/'

file_name = '역사정보.xlsx'
json_name = 'subway.json'

def getXlsxToJson(location=location, file_name=file_name, json_name=json_name):
    xlsx_file = pd.read_excel(location+file_name)
    xlsx_file.to_json(location+json_name, orient = 'table', indent=4, force_ascii=False)

if __name__ == '__main__':
    getXlsxToJson()