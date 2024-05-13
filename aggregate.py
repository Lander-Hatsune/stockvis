# coding: utf-8
import os
from glob import glob
import json

klines = {}
for path in glob("data/klines/*.json"):
    with open(path) as f:
        kline = json.load(f)
    symbol = kline["data"]["symbol"]
    kline_data = kline["data"]["item"][::10]
    klines[symbol] = kline_data
    
inds = {}
for path in glob("data/industries/*.json"):
    encode = os.path.splitext(os.path.split(path)[-1])[0]
    with open(path) as f:
        ind = json.load(f)
    inds[encode] = ind["data"]["list"]
    
comps = {}
for path in glob("data/companies/*.json"):
    symbol = os.path.splitext(os.path.split(path)[-1])[0]
    with open(path) as f:
        comp = json.load(f)
    comp = comp["data"]["company"]
    comps[symbol] = comp
    
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
}

with open("data.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)
    
