import requests
import os

def download_track():
    
    lines = open("query_result_2019-12-22T21_20_22.078Z.csv", "r").readlines()
    for line in lines[1:]:
        url = line.split(",")[1][:-1]
        filename = "data_22122019"+ os.sep + url[url.rfind("/") + 1:]
        open(filename,"wb").write(requests.get(url).content)

