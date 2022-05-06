import json
import numpy as np

with open("./source/single_dict.json",'r') as k:
    dict = json.load(k)
total = 0
for _,cnt in dict.items():
    total += cnt
print("汉字总数：",total)
for key,value in dict.items():
    # k=100时 概率数量级为1e-3
    dict[key] = np.tanh(8*value/total)
    # kprint("原概率：",value/total)
    #print("处理后概率：",dict[key])

with open("./source/single_dict_10tanh.json", "w") as f:
    f.write(json.dumps(dict, ensure_ascii=False, indent=4, separators=(',', ':')))
print("--单字再处理完成，文件已储存在./source/single_dict_10tanh.json文件中")
