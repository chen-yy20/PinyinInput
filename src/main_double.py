import numpy as np
import json
import argparse

# 对每两个字计算对数距离,q为平滑操作的λ参数 0<q<=1
def log_distance(word1,word2,q=0.9):
    assert(q>0 and q<=1), print("参数输入有误")
    #print("当前词： "+word1+word2)
    if word1 not in single_dict:
        return 114514
    count1 = single_dict[word1]
    if count1==0:
        return 114514
    if (word1+word2) not in double_dict:
        return 114514
    count2 = double_dict[word1+word2]
    # print(word1+word2+"出现频率:",str(count2))
    p3 =tanhpro_dict[word2]
    p = q*(count2/count1)+(1-q)*p3
    #print("当前概率：",p)
    dis = -np.log(p)
    # print("距离:",str(dis))
    return dis
# 参数sentence格式：[['我','沃'],['哎','爱'],['逆','你']]
def viterbi(sentence,q):
    dict_list = []
    sentence_dict = {}
    for word in sentence[0]:    # 加入第一列
        sentence_dict[word] = ('',0)
    dict_list.append(sentence_dict)
    for index,word_list in enumerate(sentence[1:]):
        sentence_dict = {}

        for word in word_list: # 找到每一个字到起点的最短路径
            word_exist = 1
            if word not in single_dict:
                #print("查无此字:",word)
                word_exist =0
                continue
            word_cnt = tanhpro_dict[word]
            forward_word = list(dict_list[index])[0] #上一列的第一个字
            shortest_distance = dict_list[index][forward_word][1]+log_distance(forward_word,word,q)+word_cnt
            #print("初始化：",forward_word,shortest_distance)
            for key,(forward,dis) in dict_list[-1].items():
                if(key+word) not in double_dict:
                    #print(key+word+"不可组词，跳过")
                    continue
                temp_distance = dis+log_distance(key,word,q)
                # if temp_distance<114514:
                #     print(key,word,temp_distance)
                if (temp_distance<shortest_distance):
                    shortest_distance = temp_distance
                    forward_word = key
            # print("更新词:",forward_word+word)
            # print("当前最短:",shortest_distance)
            if word_exist:
                sentence_dict[word] = (forward_word,shortest_distance)
        dict_list.append(sentence_dict)
    
    # 获取总距离的最小值
    final_sentence = []
    last_word = list(dict_list[-1])[0]
    min_value = dict_list[-1][last_word][1]
    min_forward = dict_list[-1][last_word][0]
    for key,value in dict_list[-1].items():
        if (value[1]<min_value):
            min_value = value[1]
            last_word = key
            min_forward = value[0]

    # print("最后一个字："+last_word+"  最小距离："+str(min_value))
    final_sentence.append(last_word)
    final_sentence.append(min_forward)

    # 迭代获取前驱
    i = len(dict_list)-2
    while(i != 0):
        current = final_sentence[-1]
        #print(current)
        final_sentence.append(dict_list[i][current][0]) # 加入前驱
        i -= 1
    
    # 反转列表,输出最终生成的句子
    real_final_sentence = final_sentence[::-1]
    ans = ''.join(real_final_sentence)   
   
    return ans
     


# ==========================运行程序============================

# input <string>: 读入拼音txt文件的地址
input = './data/input.txt'
# output <string>: 输出转换txt文件的地址
output = './data/output.txt'
# ans_exist <bool>: 是否存在标准输出
ans_exist = True
# 若ans_exist == True :
# ans_loc <string>: 读入答案txt文件的地址，系统会在转换完成后自动计算准确率
ans_loc = './data/std_output.txt'
# 距离参数q
# 计算二元距离：二字单字占比，不可超过1
lambda1 = 0.9

parser = argparse.ArgumentParser(description='Args for main_double.py')
parser.add_argument('--input', '-i', help='input <string>: 读入拼音txt文件的地址',default=input)
parser.add_argument('--output', '-o', help='output <string>: 输出转换txt文件的地址', default=output)
parser.add_argument('--lambda1','-l1',help="计算二元距离：二字单字占比，不可超过1",default = lambda1)
parser.add_argument('--ans_exist', '-ae', help='ans_exist <bool>: 是否存在标准输出,默认为假', default=ans_exist)
parser.add_argument('--ans_loc', '-al', help='ans_loc <string>: 读入答案txt文件的地址，系统会在转换完成后自动计算准确率（若ans_exist为真，则必须填入）', default=ans_loc)
args = parser.parse_args()


if __name__ == '__main__':
 # 读入json字典
    with open("./source/single_dict.json",'r') as k:
        single_dict = json.load(k)
    with open('./source/single_dict_10tanh.json','r') as k:
        tanhpro_dict = json.load(k)
    with open("./source/double_dict.json",'r') as f:
        double_dict = json.load(f)

    # 读入一二级汉字表和拼音表
    with open("./source/一二级汉字表.txt",'r') as g:
        all_words = g.read()
    with open("./source/pinyin_dict.json", "r") as g:
        dict = json.load(g)

    # 按行读取input的文本
    with open(args.input,"r") as f:
        lines = f.readlines()
    if args.ans_exist:
        try:
            with open(args.ans_loc,'r',encoding='utf-8') as g:
                std_ans = g.readlines()
        except:
            print("请输入正确的标准输出地址！或者将ans_exist参数设置为False!")
            exit(0)

    # 删除文本中的换行号
    temp = []
    input_lines = []
    for line in lines:
        line = line.replace("\n","").replace("\t","")
        temp = line.split(" ")
        input_lines.append(temp)


    # 根据拼音获取对应的输入列表,储存在word_list当中
    sentence_list = []
    #print(input_lines)
    for line in input_lines:
        temp = []
        for word in line:
            try:
                temp.append(dict[word])
            except KeyError:
                print("输入错误:",word)
                continue

        sentence_list.append(temp)
    ans_list = []
    for sentence in sentence_list:
        ans_list.append(viterbi(sentence,args.lambda1))
    with open(args.output,'w') as f:
        for ans in ans_list:
            f.write(ans+'\n')
    print("转换已完成,结果储存在"+args.output) 

    
    if args.ans_exist:
        whole_right = 0
        count = 0
        right = 0
        for index, ans in enumerate(ans_list):
            print(ans,std_ans[index].replace("\n", ""))
            if ans == std_ans[index].replace("\n", ""):
                whole_right += 1
            for dex,word in enumerate(list(ans)):
                count += 1

                if word == std_ans[index][dex]:
                    right += 1
        print("句准确率："+str(whole_right*100/len(std_ans))+"%")
        print("词准确率:"+str(right*100/count)+"%")
   