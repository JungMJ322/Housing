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
    detailed_inquiry.getDetailedAPI()
    detailed_inquiry.append_location()
    competition_rate.save_data()
    # getHospital.getHospital()
    # GS25.data_save(GS25.crawling())
    sevenEleven.data_save()
    xlsxToJson.getXlsxToJson()
