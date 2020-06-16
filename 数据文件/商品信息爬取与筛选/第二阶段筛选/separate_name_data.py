import jieba
from bs4 import BeautifulSoup
import re
class filter_tools:


    def find_keywords(self, filenames, keywords, new_filenames, keywords2=[None]):
        for index,filename in enumerate(filenames):
            with open(filename, "r", encoding="utf-8") as f:
                introduction = list(eval(f.read()))
                result = []
                for item in introduction:
                    if not keywords2[index]:
                        if isinstance(keywords[index],list)==False:
                            result.append(1 if keywords[index] in item else 0)
                        else:
                            if keywords[index][0] in item or keywords[index][1] in item:
                                result.append(1)
                            else:
                                result.append(0)
                    else:
                        if keywords[index] in item:
                            result.append(1)
                        elif keywords2[index] in item:
                            result.append(2)
                        else:
                            result.append(0)
                with open(new_filenames[index], "w", encoding="utf-8") as f:
                    f.write(str(result))
    
    def match_key(self,open_filename, new_filenames, formulars, remove_text, replace_text, index_number, filenames2=[None]):
        for index, formular in enumerate(formulars):
            with open(open_filename[index], "r", encoding="utf-8") as f:
                introduction = list(eval(f.read()))
            result = []
            if filenames2[index]:
                new_version_text=[]
            for item in introduction:
                element = re.search(re.compile(formular), item)
                if element:
                    if isinstance(remove_text[index], list):
                        add_text=element.group()
                        for number in range(len(remove_text[index])):
                            add_text = add_text.replace(remove_text[index][number], replace_text[index][number])
                        result.append(add_text[index_number[index]:])
                    else:
                        result.append(element.group().replace(remove_text[index], replace_text[index])[index_number[index]:])
                    if filenames2[index]:
                        new_version_text.append(item.replace(element.group()," ",1))
                else:
                    result.append(" ")
                    if filenames2[index]:
                        new_version_text.append(item)
            with open(new_filenames[index], "w", encoding="utf-8") as f:
                f.write(str(result))
            if filenames2[index]:
                with open(filenames2[index], "w", encoding="utf-8") as f:
                    f.write(str(new_version_text))

    def brands(self):
        with open('p-name.txt', "r", encoding="utf-8") as f:
            introduction = list(eval(f.read()))
        brands = []
        for item in introduction:
            if item[0:4] == "京品电脑":
                item = item[5::]
            if item[0:2] == "拍拍":
                item = item[3::]
            brand = item.find(" ")
            brand = item[:brand]
            remove_list = ["【", "(", "「"]
            fomular_list = [r"【.*】", r"\(.*\)", r"「.*」"]
            for index,tag in enumerate(remove_list):
                if tag in brand:
                    brand = re.sub(fomular_list[index], "", brand)
            fomular = "^".join(jieba.cut(brand))
            brands.append(fomular[0:fomular.find("^")] if "^" in fomular else brand)
        with open("brands.txt", "w", encoding="utf-8") as f:
            f.write(str(brands))

    def model(self):
        with open('p-name.txt', "r", encoding="utf-8") as f:
            introduction = list(eval(f.read()))
        models=[]
        for item in introduction:
            if item[0:4] == "京品电脑":
                item = item[5:]
            if item[0:2] == "拍拍":
                item = item[3:]
            remove_list = ["【", "英寸", "笔记本电脑", "笔记本", "戴尔DELL", "联想", "英特", "旗舰店", "锐龙"]
            fomular_list = [r"【.*】", r"[0-9]{2}[\.0-9]{0,2}英寸", r"笔记本电脑", r"笔记本", r"戴尔DELL", r"联想", r"英特.*", r"旗舰店", r"锐龙.*"]
            for index,tag in enumerate(remove_list):
                if tag in item:
                    item = re.sub(fomular_list[index], " ", item)
            item_list = re.split(r"[\s（）()，,]",item)
            for index, i in enumerate(item_list):
                if i == "gram" or "·" in i or i=="Ruby" :
                    models.append(i)
                    break
                if re.match(r".*[0-9]", i) and re.match(r"\D", i) and not re.match(r".*ook", i):
                    if "青春版" not in i:
                        models.append(re.match(r"^.*[0-9]*[0-9a-zA-Z]+", i).group())
                    else:
                        models.append(re.match(r"^.*[0-9]*[a-zA-Z]*", i).group())
                    break
                else:
                    if re.search(r"[a-zA-Z]*(ook)", i):
                        if not re.search(r".*[0-9]", i) and index<len(item_list)-1 and "pro" not in i and "Pro" not in i:
                            models.append(re.search(r"[a-zA-Z]*(ook)", i).group()
                                            +(re.match(r"[a-zA-Z0-9]{1,3}",item_list[index + 1]).group() if re.match(r"[a-zA-Z0-9]{1,3}[^a-zA-Z0-9]*",item_list[index + 1]) else ""))
                        elif re.search(r".*[0-9]", i):
                            models.append(re.search(r"[a-zA-Z]*(ook)[0-9]*", i).group())
                        else:
                            models.append(i)
                        break
            else:
                try:
                    models.append(item_list[1])
                except:
                    models.append(item_list[0])
        with open("models.txt", "w", encoding="utf-8") as f:
            f.write(str(models))

if __name__=="__main__":
    filter_tool = filter_tools()
    filter_tool.brands()
    filter_tool.model()
    filter_tool.find_keywords(['p-name.txt',"p-shop.txt",'p-name.txt','p-name.txt'],[["触",'平板'], "二手", "独显", "京品电脑"],
                              ["touch_control.txt", "used.txt", "display.txt", "Jingdong.txt"],
                              keywords2=[None, None, "集显", None])
    filter_tool.find_keywords(["p-shop.txt"],["自营"],["logistic.txt"])
    filter_tool.match_key(["p-name.txt", 'p-name.txt', "new.txt", 'new1.txt', 'new1.txt','p-icons.txt','p-icons.txt','p-name.txt','p-name.txt'],
                          ["processor.txt", "internal_storage.txt", "solid_storage.txt", "displayer.txt","video_memory.txt",'money_off.txt','discount.txt','screen_size.txt','version.txt'],
                          [r".*([iR]|锐龙)[3579]", r"[^iR0-9][1346-9]{1,2}(G|[+g])|[^iR0-9]12G",
                          r"\D128G.{0,8}\+[1-9]T|\D1T\+128G|\D512G\+32G|\D[1-9]{2,4}([Gg]|SSD|固态)|\D[1-9]T", r"[^0-9iR][0-9]G", r"(GTX|MX)[0-9]+",r'[0-9]+',r'-[0-9]*',r'[0-9]+\.*[0-9]*(英寸|寸)',r'[一二三四五六七八九十]代'],
                          ["锐龙", ['+',"g"], ['g',"SSD", '固态','1T+128G'], '','','','',['英寸','寸'],''],
                          ["R", ['G',"G"], ['G',"G", "G",'128GG+1T'], '','','','',['',''],''],
                          [-2,1,1,1,0,0,1,0,0],filenames2=[None,"new.txt","new1.txt",None,None,None,None,None,None])