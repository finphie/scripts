# ニコニコ実況コメント結合ツール

import sys
import os
import codecs
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# 引数チェック（2個以上のxmlファイルのみ）
argv = sys.argv[1:]
if len(argv) < 2:
    sys.exit("2個以上のXMLファイルを指定してください。")
for path in argv:
    if not os.path.isfile(path) or os.path.splitext(path)[1] != ".xml":
        sys.exit("指定されたファイルは存在しないか、XMLファイルではありません。")

# 各ファイルの開始時間とコメント投稿時間、コメント内容、コメント件数を取得
unixtime_list, data, number = [], [], []
for path in argv:
    tree = ET.parse(path)
    root = tree.getroot()
    unixtime_list.append(int(root[0].get("date")))
    comment_data = [[int(e.get("date")), e.get("mail"), e.text] for e in root.iter("chat")]
    data.extend(comment_data)
    number.append(len(comment_data))

# 基準時間を取得（分単位）
[print(i + 1, datetime.fromtimestamp(unixtime), argv[i], number[i]) for i, unixtime in enumerate(unixtime_list)]
while True:
    num = int(input("> ")) - 1
    if 0 <= num < len(unixtime_list):
        break    
base_unixtime = round(unixtime_list[num] / 60) * 60
print("基準時間", datetime.fromtimestamp(base_unixtime))

# 基準時間との差を計算（分単位）
unixtime_list = [round((unixtime - base_unixtime) / 60) * 60 for unixtime in unixtime_list]

# 基準時間に合わせる
count = 0
for i, unixtime in enumerate(unixtime_list):
    for c in range(number[i]):
        data[count + c][0] -= unixtime
    count += number[i]

# 投稿時間が早い順にソート
data.sort(key = lambda x:x[0])

# コメント数、コメント投稿時間を表示
print("総コメント数", len(data))
print("最初のコメント", datetime.fromtimestamp(data[0][0]))
print("最後のコメント", datetime.fromtimestamp(data[-1][0]))

# コメント投稿時間、内容からXML作成
root = ET.Element("packet")
children = []
for d in data:
    child = ET.Element("chat")
    child.set("date", str(d[0]))
    if d[1] is not None and d[1] != "184":
        child.set("mail", d[1].strip("184").strip())
    child.text = d[2]
    children.append(child)
root.extend(children)

# ファイルに保存
xml = minidom.parseString(ET.tostring(root)).toprettyxml()
path = argv[num]
name, ext = os.path.splitext(os.path.basename(path))
dirname = os.path.dirname(path)
out_filename = os.path.join(dirname, name + "_out" + ext)
if os.path.isfile(out_filename):
    sys.exit(out_filename + "はすでに存在します。リネームするか削除してください。")
with codecs.open(out_filename, "w", "UTF-8") as f:
    f.write(xml)