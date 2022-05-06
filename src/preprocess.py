import json
import os
import re

# 储存拼音字典
dict = {}
data_list = [] # 储存分割后的拼音字符串
with open('拼音汉字表.txt',"r") as tran:
    data = tran.readlines()
for data_line in data:
    data_list = data_line.replace("\n","").split(" ")
    dict[data_list[0]] = data_list[1:]
with open("./source/pinyin_dict.json", "w") as f:
    f.write(json.dumps(dict, ensure_ascii=False, indent=4, separators=(',', ':')))
print("拼音字典储存完成。")

# 读入一二级汉字表

with open("一二级汉字表.txt",'r') as g:
    all_words = g.read()

# 读入语料库并进行切割处理
url = re.compile('", "url": "http:.*')

word_source = []
for file in os.listdir('./source'):
    with open("./source/"+file, "r") as h:
        temp = h.readlines()
        for line in temp:
            line = line.replace('{"html": "原标题：','')
            line = line.replace('", "time":','')
            line = line.replace(', "title": "','')
            line = re.sub(url,'',line)
            #word_source.append(line)
            # print(line)
            # 按照特殊符号切割字符
            news_list = re.split(r'[,，:：；。、\s*（）()”“？‘’/]',line)
            for a in news_list:
                word_source.append(a)
                #print(a)
whole_source = word_source
print("--语料库切割完成，开始搜索")
length = len(whole_source)
print("--总长度："+str(len(whole_source)))
input("是否开始？")
# 搜索单字
single_dict = {}
cnt = 0
for line in whole_source:
    i=0
    while(True):
        try:
            #print(line[i])
            if(line[i] not in all_words):
                i+=1
                continue
            curr = line[i]
            if curr in single_dict:
                single_dict[curr] += 1
            else:
                single_dict[curr] = 1
        except IndexError:
            break
        i+= 1
    cnt+=1
    if (cnt%1000000==0):
        print("完成"+str(cnt))
# 将读出的数据储存在本地
with open("./source/single_dict.json", "w") as f:
    f.write(json.dumps(single_dict, ensure_ascii=False, indent=4, separators=(',', ':')))
print("--单字搜索完成，文件已储存在./source/single_dict.json文件中")

# 搜索双字
double_dict = {}
for line in whole_source:
    i=0
    while(True):
        try:
            if (line[i] not in all_words or line[i+1] not in all_words):
                i+=1
                continue
            curr = line[i]+line[i+1]
            if curr in double_dict:
                double_dict[curr] += 1
            else:
                double_dict[curr] = 1
        except IndexError:
            break
        i+=1
# 将读出的数据储存在本地
with open("./source/double_dict.json", "w") as f:
    f.write(json.dumps(double_dict, ensure_ascii=False, indent=4, separators=(',', ':')))
print("--双字搜索完成，文件已储存在./source/double_dict.json文件中")

# 搜索三字
tripple_dict = {}
cnt  = 0
for line in whole_source:
    i=0
    while(True):
        try:
            if (line[i] not in all_words or line[i+1] not in all_words or line[i+2] not in all_words):
                i+=1
                continue
            curr = line[i]+line[i+1]+line[i+2]
            #print(curr)
            if curr in tripple_dict:
                tripple_dict[curr] += 1
            else:
                tripple_dict[curr] = 1
        except IndexError:
            break
        i+=1
    cnt+=1
    if (cnt%1000 == 0):
        print("已完成："+str(cnt)+"/"+str(length))
# 将读出的数据储存在本地
with open("./source/tripple_dict.json", "w") as f:
    f.write(json.dumps(tripple_dict, ensure_ascii=False, indent=4, separators=(',', ':')))
print("--三字搜索完成，文件已储存在./source/tripple_dict.json文件中")



# # 读入汉语拼音的字典
# dict = {}
# data_list = [] # 储存分割后的拼音字符串
# with open('拼音汉字表.txt',"r") as tran:
#     data = tran.readlines()
# for data_line in data:
#     data_list = data_line.replace("\n","").split(" ")

#     # 去除不在一二级汉字表中的元素，其实好像没有
#     for word in data_list[1:]:
#         if word not in all_words:
#             data_list.remove(word)

#     dict[data_list[0]] = data_list[1:]
# print(dict)

# 生成单个汉字的数量统计
# word_num = []
# length = len(all_words)
# for i in range(10):
#     print("当前字符："+all_words[i])
#     print("进度:"+str(i)+"/"+str(length))
#     word_num.append(whole_source.count(all_words[i]))
# a= np.array(word_num,dtype=np.int32)
# np.save("./source/word_num.npy",a)

# 对语料库进行切分和精简


# print(a)



