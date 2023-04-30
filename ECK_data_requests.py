import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
import re



def scrape_data(ChartNo):
    ChartNo = ChartNo.zfill(10)
    # print(ChartNo)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    rs = requests.session()
    data = rs.get(f"http://172.20.110.185/login/RedirectHisCall?clerkid=MDIwMDM&chart={ChartNo}", headers = headers)
    soup = BeautifulSoup(data.text, "lxml")
    redirect_url = data.url
    code = redirect_url.split("=")[1]
    # print(code)
    payload = {"chart": str(code)}
    info = rs.post(f"http://172.20.110.185/home/BasePatientInfo", headers = headers, data = payload)
    # print(info.text)
    info = BeautifulSoup(info.text, "lxml")

    # 取得身高體重
    BMI = info.find(id = "BmiContainer")
    BMI = BMI.find_all("strong")[2]
    BH = str(BMI.text).split("/")[0]
    BW = str(BMI.text).split("/")[1]
    BH = BH.split(":")[1].strip()
    BW = BW.split(":")[1].strip()
    # print(f'{BH} cm')
    # print(f'{BW} kg')

    info = info.find_all("strong")
    name = str(info[0].text).strip()
    sex = str(info[2].text)
    age = str(info[4].text).split("歲")[0]
    # print(name)
    # print(sex)
    # print(age)

    dict = {
        "Name" : name,
        "Sex" : sex,
        "Age" : age,
        "BodyHeight" : BH,
        "BodyWeight" : BW
    }
    patient_info = json.dumps(dict, indent=4, ensure_ascii=False).encode('utf-8')
    patient_info = patient_info.decode()

    # print(patient_info)

    return soup, patient_info

labdata_key_dict = {
    '動態產生eGFR': 'CeGFR', 'Albumin': 'C6309038', 'Alk-P': 'C6309027', 'Amylase': 'C6309017', 'BE(B)': 'C6BEB', 'BNP': 'C6312193', 'BUN': 'C6309002', 'CA': 'C6309011', 'Cholesterol-T': 'C6309001', 'CK-MB': 'C6399086', 'CPK': 'C6309032', 'Creatinine': 'C6309015', 'Creatinine (U)': 'C6309016', 'CRP': 'C6312903', 'CTCO2': 'C7CTCO2', 'Glucose': 'C5GLUCO', 'Glucose,AC': 'C6309901', 'GOT (AST)': 'C6309025', 'GPT (ALT)': 'C6309026', 'HbA1C': 'C6309006', 'HCO3-ACT': 'C4HCO3A', 'HDL-C': 'C6309043', 'Iron': 'CIRON', 'K': 'C6309022', 'LDL-C': 'C6309044', 'Lipase': 'C6309064', 'Microalbumin (Nephelometry)': 'C6312111', 'NA': 'C6309021', 'O2SAT': 'C8O2SAT', 'pCO2': 'C3PCO2', 'pH': 'C3PH', 'pO2': 'C2PO2', 'r-GT': 'C6309031', 'T-Bilirubin': 'C6309029', 'TIBC': 'CTIBC', 'Triglyceride': 'C6309004', 'Troponin I': 'C6399035', 'Uric Acid': 'C6309013', 'Urine microalbumin/creatinine ratio': 'C6300012', 'A-Lym': 'C7ALYM', 'ABO Typing  自述血型:(     )': 'C6311001', 'APTT': 'C6308036', 'Band': 'C6BAND', 'Baso': 'C5BA', 'Blast': 'C8BLAST', 'Eosin': 'C4EO', 'Hb': 'C6308003', 'Ht': 'C6308004', 'Lym': 'C2LY', 'MCH': 'CMCH', 'MCHC': 'CMCHC', 'MCV': 'CMCV', 'Metamyelo': 'CAMETAMY', 'Mono': 'C3MO', 'Myelocyte': 'CBMYELO', 'Neutro': 'C1NE', 'NRBC': 'CCNRBC', 'Other': 'CUOTHER', 'Platelet': 'C6308006', 'Promyelo': 'C9PROMYE', 'PT': 'C6308026', 'RBC': 'C6308001', 'RH(D)': 'C6311003', 'WBC': 'C6308002', 'Anti-HAV IgM': 'C6314039', 'Anti-HBc': 'C6314037', 'Anti-HBs': 'C6314033', 'Anti-HCV': 'C6314051', 'Ferritin': 'C6327017', 'HBsAg': 'C6314032', 'Bacteria/HPF': 'CW4BACT', 'Bacteria/uL': 'CW4BACT1', 'Bilirubin': 'C8BILI', 'Cast': 'CWCAST', 'Clarity': 'C2CLARI', 'Color': 'C1COLOR', 'Crystal': 'CWCRYSTA', 'Epith.cell/HPF': 'CW3EPITH', 'Epith.cell/uL': 'CW3EPIT1', 'Fungi': 'CWFUNGI', 'Ketone': 'C6KETON', 'Leukocyte': 'CCLEUKO', 'Mucus': 'CW5MUCUS', 'Nitrite': 'CBNITR', 'OB': 'C9OB', 'Protein': 'C4PROTE', 'R.B.C./HPF': 'CW1RBC', 'R.B.C./uL': 'CW1RBC1', 'SP.GR.': 'C7SPGR', 'Stool-O.B.(定量免疫法)': 'C6399121', 'Synovial Crystal (關節液偏光檢查)': 'C6316013', 'Trichomonas': 'CWTRICHO', 'Urobilinogen': 'CAUROB', 'W.B.C./HPF': 'CW2WBC', 'W.B.C./uL': 'CW2WBC1', 'Blood culture': 'C6313016', 'Influenza A Ag': 'C6314065', 'Influenza B Ag': 'C6314066'
}


# 取得所有labdata的編碼 (偶爾要重抓一次，避免資訊室改編碼或是推出新的檢查)
# labdata_key = soup.find_all(class_ = "badge badge-pill badge-secondary labitem")
# for labdata_key in labdata_key:
#     data_code = str(labdata_key["data-code"])
#     data_labname = str(labdata_key["data-labname"])
#     data_labname = data_labname.strip()
#     labdata_key_dict[f"{data_labname}"] = data_code
#     # print(data_code + " " + data_labname)
# print(labdata_key_dict)


# 花式搜尋data
def get_all_labdata(soup):
    dict = {}
    trs = soup.find_all(class_ = re.compile("^groupCode"))
    # print(trs)
    for i in trs:
        labdata_name = str(i.find("b").text).strip()
        # print(labdata_name)
        datas = i.find_all("tbody")[1]
        data = datas.find_all("tr")
        list_all = []
        for i in data:
            time = str(i.find_all("td")[1].text)
            value = str(i.find_all("td")[2].text) 
            isNornal = i.find_all("td")[2].get("class")[0]
            list = [value, time, isNornal]
            list_all.append(list)
        dict[labdata_name] = list_all
        # print(list)
    # print(dict)
    all_data = json.dumps(dict, indent=4, ensure_ascii=False).encode('utf-8')
    all_data = all_data.decode()
    # print(all_data)
    return all_data


def get_last_labdata(soup):
    dict = {}
    trs = soup.find_all(class_ = re.compile("^groupCode"))
    # print(trs)
    for i in trs:
        labdata_name = str(i.find("b").text).strip()
        # print(labdata_name)
        datas = i.find_all("tbody")[1]
        data = datas.find_all("tr")[0] # 這行代表只取最新的值
        time = str(data.find_all("td")[1].text)
        value = str(data.find_all("td")[2].text)
        isNornal = data.find_all("td")[2].get("class")[0]
        # try:
        #     isNornal = i.find_all("td")[2].get("class")[0]
        # except:
        #     isNornal = "Null"
        dict1 = {
            "value": value,
            "time": time,
            "isNornal": isNornal}
        dict[labdata_name] = dict1
        # print(list)
    # print(dict)
    last_data = json.dumps(dict, indent = 4, ensure_ascii=False).encode('utf-8')
    last_data = last_data.decode()
    # print(last_data)
    dict_simple = {}
    simple_labdata_key_dict = {
        "GPT (ALT)": "C6309026", "Creatinine": "C6309015", "K": "C6309022", "Hb": "C6308003", "Platelet": "C6308006", "PT": "C6308026", "APTT": "C6308036"
    }
    # last_data, dict = get_last_labdata()
    for labdata_name, labdata_value in simple_labdata_key_dict.items():
        try:
            dict_simple[labdata_name] = dict[labdata_name]
        except:
            dict_simple[labdata_name] = "Null"
    # print(dict_simple)
    simple_data = json.dumps(dict_simple, indent = 4)
    # print(simple_data)
    return last_data, simple_data

# def get_simple_labdata():
#     dict_simple = {}
#     simple_labdata_key_dict = {
#         "GPT (ALT)": "C6309026", "Creatinine": "C6309015", "K": "C6309022", "Hb": "C6308003", "Platelet": "C6308006", "PT": "C6308026", "APTT": "C6308036"
#     }
#     last_data, dict = get_last_labdata()
#     for labdata_name, labdata_value in simple_labdata_key_dict.items():
#         try:
#             dict_simple[labdata_name] = dict[labdata_name]
#         except:
#             dict_simple[labdata_name] = "Null"
#     # print(dict_simple)
#     simple_data = json.dumps(dict_simple, indent = 4)
#     return simple_data
#     # print(simple_data)

def get_image(ChartNo, soup):
    dict_img = {}
    rs = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    data = rs.get(f"http://172.20.110.185/login/RedirectHisCall?clerkid=MDIwMDM&chart={ChartNo}", headers = headers)

    radiation = soup.find_all('tr', attrs={'data-xrayhead': re.compile("^p")})
    exam_img = soup.find_all('tr', attrs={'data-examhead': re.compile("^p")})
    # print(radiation)

    # 取得影像的psHash值
    psHash = soup.find_all("script", text = re.compile(".*psHash.*", flags=re.DOTALL))[1].text
    psHash = psHash.split("psHash")[1]
    psHash = psHash.split("'")[1]
    # print(psHash)
    
    radiation_list = []
    exam_img_list = []

    for i in radiation: 
        accessionNumber = str(i.find_all("td")[6].text)
        exam_name = str(i.find("span").text)
        # exam_catalogy = str(i.find_all("td")[1].text).strip()
        time = str(i.find_all("td")[1].text)
        img_url = f"http://172.23.0.10/html5/ShowImage.html?psHash={psHash}&accessionNumber={accessionNumber}"
        report_url = f"http://172.20.110.185/home/XrayDataByApplyNo?applyNo={accessionNumber}"

        def get_report():
            r = rs.get(report_url, headers = headers) # 取得報告
            report_content = BeautifulSoup(r.text, "lxml")
            return report_content
            # print(report_content)
            
        # report_content = get_report()
        # exam_name = str(report_content.find("tbody").find_all("td")[1].text).strip()
        # report = str(report_content.find_all("pre")[0].text).strip()
        # impression = str(report_content.find_all("pre")[1].text).strip()

        dict = {
            "exam_name": exam_name,
            "accessionNumber": accessionNumber,
            "img_url": img_url,
            "report_url" : report_url,
            # "report": report,
            # "impression": impression,
            "time": time
        }
        radiation_list.append(dict)

    for i in exam_img:
        accessionNumber = str(i.find_all("td")[7].text)
        exam_name = str(i.find_all("td")[0].text).strip()
        time = str(i.find_all("td")[2].text)
        img_url = f"http://172.23.0.10/html5/ShowImage.html?psHash={psHash}&accessionNumber={accessionNumber}"
        report_url = f"http://172.20.110.185/home/ExamDataByApplyNo?applyNo={accessionNumber}"

        def get_report():
            r = rs.get(report_url, headers = headers) # 取得報告
            report_content = BeautifulSoup(r.text, "lxml")
            return report_content
        
        # report_content = get_report()
        # report = str(report_content.find_all("pre")[0].text).strip()
        # impression = str(report_content.find_all("pre")[1].text).strip()
        
        dict = {
            "exam_name": exam_name,
            "accessionNumber": accessionNumber,
            "img_url": img_url,
            "report_url": report_url,
            # "report": report,
            # "impression": impression,
            "time": time
        }
        exam_img_list.append(dict)
    img_list = radiation_list + exam_img_list # 合併放射影像和檢查影像
    # print(img_list)


    for i in img_list: # 增加timestamp
        # 輸入民國紀年的時間字串
        minguo_str = i["time"]
        # print(minguo_str)
        # 將民國紀年轉換為西元紀年
        year = int(minguo_str.split("/")[0]) + 1911
        month = int(minguo_str.split("/")[1])
        a = minguo_str.split("/")[2]
        day = int(a.split(" ")[0])
        b = a.split(" ")[1]
        hour = int(b.split(":")[0])
        minute = int(b.split(":")[1])
        timestamp = str(datetime.datetime(year, month, day, hour, minute).timestamp()).split(".")[0]
        timestamp = timestamp.zfill(11) # 不然等等在sort的時候會有問題
        i["timestamp"] = timestamp
        # print(timestamp)

    def sort_time(element):
        return element["timestamp"]

    img_list.sort(key = sort_time, reverse = True)


    dict_img = {
        "Image": img_list
    }

    dict_img = json.dumps(dict_img, indent = 4, ensure_ascii = False).encode('utf-8')
    dict_img = dict_img.decode()
    return dict_img
    # print(dict_img)





# while True:
    # 病例號放這邊，補0到十個數字
    # 48251
    # 5426687
    # 7782912
    # 1676165
    # 6279364
    # ChartNo = input("請輸入病例號: ")
# ChartNo = "3577558"
# t1 = time.time()
# soup, patient_info = scrape_data(ChartNo)
# get_image(ChartNo)
# get_last_labdata()
# get_all_labdata()
# data = get_all_labdata()
# data = json.loads(data)
# print(data["Hb"])


# t2 = time.time()
# print("Time spend: ", t2-t1)






