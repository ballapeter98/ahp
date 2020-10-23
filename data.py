import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import codecs, json
import sys
import numpy as np

def main():

    #############################
    ###### ADATOK BETÖLTÉSE #####
    #############################
    mobile_list = ["Huawei-P40-Lite", "Samsung-Galaxy-A71", "Apple-iPhone-11", "Apple-iPhone-SE", "Samsung-Galaxy-A21S", "Samsung-Galaxy-S10", "Samsung-Galaxy-A51", "Samsung-Galaxy-S20", "Xiaomi-Redmi-9", "Huawei-P30-Lite", "Xiaomi-Redmi-Note-9-Pro", "Xiaomi-Redmi-Note-8T", "Samsung-Galaxy-Note-20-Ultra", "Apple-iPhone-11-Pro-Max", "Apple-iPhone-11-Pro", "Samsung-Galaxy-S20-Ultra", "Samsung-Galaxy-A41", "Apple-iPhone-XR", "Samsung-Galaxy-A20e", "Huawei-P30-Pro", "Huawei-P40-Pro", "Xiaomi-Redmi-Note-9", "Xiaomi-Mi-Note-10", "Samsung-Galaxy-S20-Plus", "Xiaomi-Mi-Note-10-Lite", "Honor-20-Lite", "Samsung-Galaxy-Note-20", "Huawei-P30", "Samsung-Galaxy-Note-10-Lite", "Honor-20", "Honor-20-Pro", "Honor-8A", "OnePlus-7T", "LG-K40s", "TCL-10-PRO", "Sony-Xperia-5", "Huawei-Y6P", "TCL-10L", "Samsung-Galaxy-Z-Flip", "Alcatel-3X", "LG-V50-Thinq"]
    #test_list = ["Huawei-P40-Lite", "Samsung-Galaxy-A71", "Apple-iPhone-11", "Apple-iPhone-SE"]
    mobile_price = [94820, 144760, 297660, 179960, 71500, 236500, 122540, 321200, 59840, 84040, 104940, 74800, 484880, 452540, 410960, 476300, 99880, 254540, 57640, 230120, 343200, 84920, 199980, 386760, 159940, 61160, 389840, 163900, 223300, 99880, 153780, 44000, 189860, 47520, 153340, 243760, 53460, 88000, 590260, 58960, 407440]
    #test_price = [94820, 144760, 297660, 179960]
    camera = [None] * len(mobile_list)
    log_cam = [None] * len(mobile_list)
    storage = [None] * len(mobile_list)
    ram = [None] * len(mobile_list)
    battery = [None] * len(mobile_list)
    pic = [None] * len(mobile_list)
    perf = [325777, 233090, 435295, 458034, 119043, 329546, 195380, 525029, 202330, 141600, 279129, 167395, 474536, 456786, 460784, 524200, 162826, 303307, 116120, 285595, 466900, 207559, 266785, 500114, 253271, 131461, 513717, 289754, 341212, 290788, 376278, 86352, 378797, 76500, 215000, 354695, 95000, 171000, 448286, 35000, 434000]
    j = 0
    for i in mobile_list:
        url = "https://www.gadgetsnow.com/mobile-phones/" + i
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        #camera[j] = eval(re.sub(" MP", "", re.sub(" MP ", "", soup.find("tr", attrs = {"data-nd": "rear_camera"}).find("td", attrs={"class": "val"}).get_text())))
        camera[j] = int(soup.find("tr", attrs = {"data-nd": "rear_camera"}).find("td", attrs={"class": "val"}).get_text().split(" MP", 1)[0])
        log_cam[j] = np.log(camera[j])
        print(camera[j])
        print(log_cam[j])

        storage[j] = int(re.sub("[^0-9]", "", soup.find("tr", attrs = {"data-nd": "storage"}).find("td", attrs = {"class": "val"}).get_text()))
        print(storage[j])

        battery[j] = int(re.sub("[^0-9]", "", soup.find("tr", attrs = {"data-nd": "battery"}).find("td", attrs = {"class": "val"}).get_text()))
        print(battery[j])

        ram[j] = int(re.sub("[^0-9]", "", soup.find("tr", attrs = {"data-nd": "ram"}).find("td", attrs = {"class": "val"}).get_text()))
        print(ram[j])

        pic[j] = soup.find("div", attrs = {"class": "img_block active_thumb"}).find("img")["src"]

        def write_json(data, filename='conf.json'): 
            with open(filename,'w') as f: 
                json.dump(data, f, indent=4)

        with open('conf.json') as json_file: 
            data = json.load(json_file)
            temp = data['devices']
            y = {
                "device": {
                    "name": mobile_list[j],
                    "price": mobile_price[j],
                    "camera": camera[j],
                    "log_cam": log_cam[j],
                    "storage": storage[j],
                    "battery": battery[j],
                    "ram": ram[j],
                    "perf": perf[j],
                    "pic": pic[j]
                }
            }
            temp.append(y)
        write_json(data)
        j+=1
    print('adatok betöltése kész')
    
    #############################
    ##### MÁTRIX FELTÖLTÉSE #####
    #############################

    pwc = np.zeros((len(mobile_list), len(mobile_list)))
    pwc2 = np.zeros((len(mobile_list), len(mobile_list)))
    pwc3 = np.zeros((len(mobile_list), len(mobile_list)))
    pwc4 = np.zeros((len(mobile_list), len(mobile_list)))
    pwc5 = np.zeros((len(mobile_list), len(mobile_list)))
    print(pwc)

    with open('conf.json', 'r') as f:
        config = json.load(f)

    for i in range(0,len(mobile_list)):
        for j in range(0,len(mobile_list)):
            pwc[i][j] = 1 / (list(config['devices'][i].items())[0][1]['price'] / list(config['devices'][j].items())[0][1]['price'])
            pwc2[i][j] = list(config['devices'][i].items())[0][1]['log_cam'] / list(config['devices'][j].items())[0][1]['log_cam']
            pwc3[i][j] = list(config['devices'][i].items())[0][1]['storage'] / list(config['devices'][j].items())[0][1]['storage']
            pwc4[i][j] = list(config['devices'][i].items())[0][1]['battery'] / list(config['devices'][j].items())[0][1]['battery']
            pwc5[i][j] = list(config['devices'][i].items())[0][1]['perf'] / list(config['devices'][j].items())[0][1]['perf']
            j+=1
        i+=1

    print('price')
    print(pwc)
    print('log_cam')
    print(pwc2)
    print('storage')
    print(pwc3)
    print('battery')
    print(pwc4)
    print('perf')
    print(pwc5)
    print('Mátrixok sikeresen feltöltve')

    #############################
    ####### JSON TÖLTÉSE ########
    #############################

    def write_json(data, filename='pwc.json'): 
            with open(filename,'w') as f: 
                json.dump(data, f, indent=4)

    with open('pwc.json') as json_file: 
        data = json.load(json_file) 
        temp = data['matrices']
        pwc = pwc.tolist()
        pwc2 = pwc2.tolist()
        pwc3 = pwc3.tolist()
        pwc4 = pwc4.tolist()
        pwc5 = pwc5.tolist()
        temp.append(pwc)
        temp.append(pwc2)
        temp.append(pwc3)
        temp.append(pwc4)
        temp.append(pwc5)
    write_json(data)
    print('JSON fájl töltése kész')

main()