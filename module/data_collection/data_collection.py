import competition_rate
import cu
import detailed_inquiry
import getHospital
import getInfra
import sevenEleven
import xlsxToJson
import GS25


if __name__ == "__main__":
    # cu.js_save()
    print(0)
    detailed_inquiry.getDetailedAPI()
    print(0)
    detailed_inquiry.append_location()
    print(0)
    competition_rate.save_data(0)
    print(0)
    getHospital.getHospital()
    print(0)
    # GS25.data_save(GS25.crawling())
    # print(0)
    # sevenEleven.data_save()
    # print(0)
    xlsxToJson.getXlsxToJson()
    print(0)
