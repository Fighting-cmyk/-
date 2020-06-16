from bs4 import BeautifulSoup
def process_data(tagname):
    tags_list=[]
    for html in htmls:
        soup = BeautifulSoup(html, "lxml")
        tag_all = soup.find("div", {"class": "goods-list-v2 gl-type-1 J-goods-list", "id": "J_goodsList"})
        if tagname == "href":
            tags = tag_all.find_all("div", {"class": "p-name"})
            for tag in tags:
                tags_list.append(tag.find("a")["href"])
        else:
            tags = tag_all.find_all("div", {"class": tagname})
            for tag in tags:
                processed_tags = tag.text.replace("\n", "").replace("￥", "").replace("¥", "")
                if tagname=='p-price':
                    tags_list.append(processed_tags[0:7])
                else:
                    tags_list.append(processed_tags)
    with open(tagname+".txt", "w", encoding="utf-8") as f:
        f.write(str(tags_list))
    print(len(tags_list))

if __name__ == "__main__":
    with open("jd_data.txt", "r",encoding="utf-8") as f:
        htmls=f.read()
    htmls = list(eval(htmls))
    tag_finded = ["p-name", "p-icons", "p-price", "p-shop", "p-commit", "href"]
    for tag in tag_finded:
        process_data(tag)
