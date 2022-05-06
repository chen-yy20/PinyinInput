# 拼音输入法
这是一个基于二元和三元字模型和马尔可夫模型的简单的拼音输入法实现。
在python环境下运行。

## 如何运行
* 输入数据<br/>
1. 直接在`data`文件夹中修改`input.txt`文件
2. 修改程序运行参数 `input`为需要转换的文本文件的地址
* 输出数据<br/>
1. 默认输出于`/data/output.txt`中
2. 修改程序运行参数`output`为输出的文本文件的目标储存地址
* 输出准确率<br/>
需要有事先准备好的答案文本文件，每一行汉字对应`input.txt`中的拼音。<br/>
设置程序运行参数`ans_exist`为`True`,并设`ans_loc`为答案文本文件的地址。<br/>
* 运行字的**二元模型**<br/>
对应运行`/src/main_double.py`

* 运行字的**三元模型**<br/>
对应运行`/src/main_tripple.py`

* 命令行参数<br/>
详情请运行程序时用`-h` 或`--help` 参数自行了解。<br/>
即：`python ./src/main_tripple.py --help`<br/>
或： `python ./src/main_double.py -h `

* 参数 λ 设置<br/>
二元模型中有`lambda1`参数，三元模型有`lambda1`、`lambda2`和`lambda3`参数。
`lambda1`对应二字距离当中$P(O_i|O_{i-1})$所占权重，`lambda1`需小于1 。`1-lambda1`对应平滑处理中$P(O_i)$所占的权重。<br/>
`lambda2`对应三字距离当中$P(O_i|O_{i-1}O_{i-2})$所占权重，`lambda3`对应三字距离当中$P(O_i|O_{i-1})$所占权重,`1-lambda2-lambda3`对应平滑处理中$P(O_i)$所占的权重。自然`lambda1+lambda2`需小于1 。<br/>
## 代码目录
* `\data`: 储存输入和输出的文本文件，还有答案文本文件
* `\source`: 储存经过处理的语料库文件、拼音表和汉字表
* `\src`: 储存代码文件，包括了预处理文件和拼音转换文件。<br/>
    * `main_double.py`：二元模型拼音转换文件
    * `main_tripple.py`: 三元模型拼音转换文件
    * `preprocess.py`: 语料库和拼音表预处理文件，处理过后的文件储存在`./source`文件夹中。
    * `tanh_process.py`: 对单字进行了`tanh`函数预处理，获取了激活后的单字概率
