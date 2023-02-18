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
                ret = []
                for i in self.keys():
                    m = re.match("^" + key + "$", i)
                    if m:
                        ret.append(super(rdict, self).__getitem__(m.group(0)))
            except:
                raise (KeyError(key))
        return ret


# Webサイトの構造上、001~1008までのリストを作成
from_no = 1
to_no = 1008
number_list = ["{:04}".format(i) for i in range(from_no, to_no + 1)]

# URLを全て取得
url_list = [
    "https://zukan.pokemon.co.jp/detail/{0}.html".format(number)
    for number in number_list
]

# M1チップのMacのユーザーエージェント
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"

# 保存場所とファイル名
download_dir = "pokemon-image"

# 0.2秒待ち
sleep_time_sec = 0.2
info = []

for url in url_list:
    # 待ち
    time.sleep(sleep_time_sec)

    # URLのHTMLから画像のURLを取得
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    html = urllib.request.urlopen(req)

    soup = BeautifulSoup(html, "html.parser")

    # script部分を取得
    title_part = soup.find_all("script", {"type": "application/json"})

    # タグの中のtext部分を指定
    for i in title_part:
        title = i.get_text()

    # 各情報を辞書化
    x = title.split(",")
    dic = {}
    for i in x:
        y = i.split(":")
        k = (
            y[0]
            .replace('"', "")
            .replace("{", "")
            .replace(" ", "")
            .replace("\u3000", " ")
            .replace("\n", "")
        )
        v = ""
        for j in y[1:]:
            v += j
        v = (
            v.replace('"', "")
            .replace("{", "")
            .replace(" ", "")
            .replace("\u3000", " ")
            .replace("\\", "")
            .replace("https", "https:")
        )

        if not k in dic:
            dic[k] = v

    dic = rdict(dic)

    # 画像のURL取得
    image_url = dic["image_m"]

    # ポケモンNo.取得
    number = dic["pokemon"].replace("no", "")

    # ポケモンの名前を取得
    name = dic["name"]

    # 保存場所とファイル名
    dst_path = os.path.join(download_dir, number + ".png")

    downloadimage(image_url, dst_path)
    print(number + name)

    # 他の情報をcsv格納
    text1 = dic["text_1"]
    text2 = dic["text_2"]

    types = dic["type_.*"]
    type_list = ""
    for i in types:
        if type_list == "":
            type_list += i
        else:
            type_list += "," + i

    bun = dic["bunrui"]
    toku = dic["tokusei_*"]
    toku_list = ""
    for i in types:
        if toku_list == "":
            toku_list += i
        else:
            toku_list += "," + i

    body = [dic["takasa"], dic["omosa"]]

    info.append(
        [number, name, type_list, bun, toku_list, body[0], body[1], text1, text2]
    )

df = pd.DataFrame(info)
df.columns = ["No.", "名前", "タイプ", "分類", "特性", "高さ", "重さ", "コメント1", "コメント2"]
df.to_csv("Pokemon1008.csv")
