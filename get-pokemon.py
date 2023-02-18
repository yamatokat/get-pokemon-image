from bs4 import BeautifulSoup
import urllib.error, os
import urllib.request
import time, datetime
import pandas as pd
import numpy as np
import re

# 画像のURLを渡すとダウンロードする関数
def downloadimage(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)


# 辞書作る
class rdict(dict):
    def __getitem__(self, key):
        try:
            return super(rdict, self).__getitem__(key)
        except:
            try:
                ret=[]
                for i in self.keys()
                    m=re.match("^"+key+"$",i)
                    if m:ret.append(super(rdict, self).__getitem__(m.group(0)))
            except:raise(KeyError(key))
        return ret


# Webサイトの構造上、001~809までのリストを作成
number_list = ["{:04}".format(i) for i in range(1, 810)]

# URLを全て取得
url_list = [
    "https://zukan.pokemon.co.jp/detail/{0}.html".format(number) for number in number_list
]
# for url in url_list:
#     print(url)


# M1チップのMacのユーザーエージェント
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"

# URLのHTMLから画像のURLを取得
req = urllib.request.Request(url_list[0], headers={"User-Agent": ua})
html = urllib.request.urlopen(req)

soup = BeautifulSoup(html, "html.parser")
#soup

#script部分を取得
title_part = soup.find_all("script", {"type":"application/json"})

#タグの中のtext部分を指定
for i in title_part:
    title = i.get_text()

#各情報を辞書化
x = title.split(',')
dic = {}
for i in x:
    y = i.split(':')
    k = y[0].replace('"',"").replace('{',"").replace(" ","").replace("\u3000"," ").replace("\n","")
    v = ""
    for j in y[1:]:
        v+= j  
    v = v.replace('"',"").replace('{',"").replace(" ","").replace("\u3000"," ").replace("\\","").replace("https","https:")
    
    if not k in dic:
        dic[k] = v 

dic = rdict(dic)
#dic





# 画像のURL取得
image_url = dic['image_m']
image_url

# ポケモンNo.取得
number = dic['pokemon'].replace("no","")
number

# ポケモンの名前を取得
name = dic['name']

# 保存場所とファイル名
download_dir = "pokemon-image"
dst_path = os.path.join(download_dir, number + name + ".png")

print(dst_path)

downloadimage(image_url,dst_path)
print("成功")



