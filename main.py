import flet as ft
from flet import (
    Page,
    UserControl,
)
import time
import ECK_data_requests as rq
import json

def request_data(e): 
    # 連結背後的API抓取data
    ChartNo = input.value
    print(ChartNo)
    soup, patient_info = rq.scrape_data(ChartNo)
    patient_info = json.loads(patient_info)
    dict_img = rq.get_image(ChartNo, soup)
    last_data, simple_data = rq.get_last_labdata(soup)
    all_data = json.loads(rq.get_all_labdata(soup))
    print(patient_info)
    print(dict_img)
    return patient_info, dict_img, last_data, simple_data, all_data
    # data抓取結束
    
class App(UserControl):
    def build(self):
        return None
    
    

def main(page: Page):
    # patient_info, dict_img, last_data, simple_data, all_data = request_data(e)
        
        
    # # 這邊以下開始拉資料出來，一一排列需要的資料
    # name.value = patient_info["Name"]
    # sex.value = patient_info["Sex"]
    # age.value = patient_info["Age"]
    # BH.value = patient_info["BodyHeight"]
    # BW.value = patient_info["BodyWeight"]
    page.update()
    
    
    
    # request_data()這個function外面的東西是要開始做排版
    name = ft.Text() 
    sex = ft.Text()
    age = ft.Text()
    BH = ft.Text()
    BW = ft.Text()      
     
    input = ft.TextField(
        hint_text="請輸入病歷號：", 
        autofocus=True, 
        keyboard_type="NUMBER", 
        max_length=10,
        on_submit=request_data
        )
    
    page.add(input)

ft.app(target=main) 
