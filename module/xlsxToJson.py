import pandas as pd

location = './json/'
xlocation= '../data/TransportData/'
file_name = 'subway.xlsx'
json_name = 'subway.json'

def getXlsxToJson(location=location, file_name=file_name, json_name=json_name):
    xlsx_file = pd.read_excel(xlocation+file_name)
    xlsx_file.to_json(location+json_name, orient = 'table', indent=4, force_ascii=False)

if __name__ == '__main__':
    getXlsxToJson()