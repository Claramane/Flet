import flet as ft
import time
import ECK_data_requests as rq
import json

def main(page):
    def request_data(e):
        ChartNo = input.value
        print(ChartNo)
        soup, patient_info = rq.scrape_data(ChartNo)
        patient_info = json.loads(patient_info)
        dict_img = rq.get_image(ChartNo, soup)
        last_data, simple_data = rq.get_last_labdata(soup)
        all_data = json.loads(rq.get_all_labdata(soup))
        print(patient_info)
        print(dict_img)
        t.value = all_data["Hb"][0][0]
        page.update()
    t = ft.Text()      
        
    input = ft.TextField(hint_text="請輸入病歷號：", autofocus=True,)    

    page.add(input, ft.FilledButton("button", on_click=request_data,), t)
        
        
    pass


ft.app(target=main)
