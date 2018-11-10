# アニメの放送日時を取得する
# しょぼいカレンダー様（http://cal.syoboi.jp/）を利用
# このスクリプトを利用する際には、サーバー負荷をかけないように注意

import sys
import os
import xml.etree.ElementTree as ET
from urllib.request import urlretrieve, urlopen

base_url = "http://cal.syoboi.jp/db.php?Command="
title_url = base_url + "TitleLookup"
tid_url = title_url + "&Fields=Title&TID=*"
subtitle_url = title_url + "&Fields=SubTitles&TID="
prog_url = base_url + "ProgLookup&Fields=StTime,ChID&TID="

tid_filepath = "tid.xml"

# TIDファイルがない場合は取得
if not os.path.isfile(tid_filepath):
    urlretrieve(tid_url, tid_filepath)

# TIDファイル読み込み
tree = ET.parse(tid_filepath)
root = tree.getroot()
data = {e.get("id"): e.find("Title").text for e in root.iter("TitleItem")}

# アニメタイトル取得
title_name = input("アニメタイトル名> ")

# アニメタイトルからTIDを取得（複数一致する場合あり）
title_list = [title for title in data.items() if title[1].find(title_name) > -1]

# 複数一致した場合は絞り込む
print("No.", "TID", "タイトル名")
if len(title_list) > 1:
    [print(i + 1, tid, title) for i, (tid, title) in enumerate(title_list)]
    while True:
        num = int(input("> ")) - 1
        if 0 <= num < len(title_list):
            break
    title = title_list[num]
else:
    title = title_list[0]
tid = title[0]

# サブタイトル取得
with urlopen(subtitle_url + tid) as res:
    xml = res.read().decode("UTF-8")
tree = ET.fromstring(xml)
data = tree.findtext(".//SubTitles").replace("\n", "").split("*")[1:]
data = [data[i:i + 2] for i in range(0, len(data), 2)]
[print(count, subtitle) for (count, subtitle) in data]
while True:
    num = input("> ")
    if num in [x[0] for x in data]:
        break

# 放送日時取得
prog_url += tid + "&Count=" + num
with urlopen(prog_url) as res:
    xml = res.read().decode("UTF-8")
tree = ET.fromstring(xml)
[print(e.find("StTime").text, e.find("ChID").text) for e in tree.iter("ProgItem")]