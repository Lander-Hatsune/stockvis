# coding: utf-8
import os
from glob import glob
import json
from tqdm import tqdm
import jieba

klines = {}
for path in tqdm(glob("data/klines/*.json")):
    with open(path) as f:
        kline = json.load(f)
    symbol = kline["data"]["symbol"]
    kline_data = kline["data"]["item"][::10]
    klines[symbol] = kline_data

ind_dict = {}
with open("data/industries.json") as f:
    ind_dict = {
        ind["encode"]: ind["name"] for ind in json.load(f)["data"]["industries"]}

inds = {}
for path in glob("data/industries/*.json"):
    encode = os.path.splitext(os.path.split(path)[-1])[0]
    with open(path) as f:
        ind = json.load(f)
    l = []
    for stock in ind["data"]["list"]:
        if stock["symbol"] not in klines:
            print(stock["symbol"])
            continue
        l.append(stock["symbol"])
    inds[ind_dict[encode]] = l

comps = {}
for path in glob("data/companies/*.json"):
    symbol = os.path.splitext(os.path.split(path)[-1])[0]
    with open(path) as f:
        comp = json.load(f)
    comp = comp["data"]["company"]
    comps[symbol] = comp

provinces = {}
for symbol, comp in tqdm(comps.items()):
    if comp["provincial_name"] not in provinces:
        provinces[comp["provincial_name"]] = [symbol,]
    else:
        provinces[comp["provincial_name"]].append(symbol)
del provinces[None]

with open("stopwords.txt") as f:
    stopwords = set(f.read().split('\n'))


for k, comp in tqdm(comps.items()):
    s = comp["operating_scope"] or "" + \
        comp["main_operation_business"] or "" + \
        comp["org_cn_introduction"] or ""
    words = [w for w in jieba.lcut(s, HMM=True) if w not in stopwords]
    comp["words"] = list(set(words))

with open("data/list.json") as f:
    all_l = json.load(f)["data"]["list"]

with open("data/industries.json") as f:
    ind_l = json.load(f)["data"]["industries"]

data = {
    "all_list": all_l,
    "ind_list": ind_l,
    "industries": inds,
    "companies": comps,
    "klines": klines,
    "provinces": provinces,
}

with open("data.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)
