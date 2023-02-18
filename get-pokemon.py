from bs4 import BeautifulSoup
import urllib.error, os
import urllib.request
import time.datatime
import pandas as pd
import numpy as np


# 画像のURLを渡すとダウンロードする関数
def downloadimage(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)


# Webサイトの構造上、001~809までのリストを作成
number_list = ["{:04}".format(i) for i in range(1, 810)]

# URLを全て取得
url_list = [
    "https://zukan.pokemon.co.jp/detail/{0}".format(number) for number in number_list
]
# for url in url_list:
#     print(url)


# M1チップのMacのユーザーエージェント
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36"

# URLのHTMLから画像のURLを取得
req = urllib.request.Request(url_list[0], headers={"User-Agent": ua})
html = urllib.request.urlopen(req)

soup = BeautifulSoup(html, "html.parser")

soup

# 画像のURL取得
image = soup.find(class_="profile-photo").find("img")
image_url = "https://www.pokemon.jp" + image["src"]

# ポケモンNo.取得
number = soup.find(class_="num").get_text()

# ポケモンの名前を取得
pokemon = image["alt"]

# 保存場所とファイル名
download_dir = "donwload"
dst_path = os.path.join(download_dir, number + ".png")
