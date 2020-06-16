import re
import json

with open('bad_comment.txt', 'r',encoding='utf-8') as f:
    datas = f.read().split('      ok      ')
for data in datas:
    if data:
        m = data.split("creationTime")
        l=[]
        for i in m:
            if '"guid"' in i:
                x = re.findall(r'\{"id"\:[0-9]+\,"guid"\:".*"\,"content"\:".*",', i)
                str1 = re.sub(r"[A-Za-z0-9\!\%\[\]\,\。\&\;\$\-\"\{\:]", "", x[0])
                l.append(str1)
        with open('comment_bad.txt', 'a', encoding='utf-8') as f:
            f.write(str(l))
            f.write('kkkkkkkkkkkkkkkkkk')
    else:
        with open('comment_bad.txt', 'a', encoding='utf-8') as f:
            f.write('[]')
            f.write('kkkkkkkkkkkkkkkkkk')
# 这里的comment_median.txt文件的生成同理
'''with open('comment_median.txt', 'r', encoding = 'utf-8') as f:
    median = f.read().split('kkkkkkkkkkkkkkkkkk')
with open('comment_bad.txt', 'r', encoding = 'utf-8') as f:
    bad = f.read().split('kkkkkkkkkkkkkkkkkk')

for index, item in enumerate(median):
    with open('summar_comment.txt', 'a', encoding='utf-8') as f:
        f.write(str(eval(median[index])+eval(bad[index])))
        f.write('kkkkkkkkkkkkkkkkkk')'''


 