import json

with open('./data/hongshanlou.json', 'r',encoding="utf-8") as f:
    data = json.load(f)
    aa = []
    for i in data:
        aa.append(i["name"].split("[")[0])
    aa = json.dumps(aa,ensure_ascii=False,)
    print(aa)
