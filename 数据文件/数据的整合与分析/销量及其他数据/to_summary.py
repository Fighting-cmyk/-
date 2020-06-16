def to_list(document):
    documentx = open(document+".txt", "r", encoding="utf-8")
    return list(eval(documentx.read()))
with open("summary.csv","a",encoding="utf_8_sig") as summary:
    summary.write("Brands,Model,Price,money_off,discount,Internal Storage,Solid State Storage,Display,Shop,Shop Type,Video Memory,JingDong,href,used,Display_type,Processor,Version,Touch control,Screen size,Sale,Favorable rate\n")
    brands = to_list("brands")
    model = to_list("models")
    price=to_list("p-price")
    money_off = to_list("money_off")
    discount=to_list('discount')
    internal_storage = to_list("internal_storage")
    solid_storage = to_list("solid_storage")
    Display = to_list("video_memory")
    shop = to_list("p-shop")
    shop_type = to_list("logistic")
    video_memory = to_list("displayer")
    jingdong = to_list("Jingdong")
    href = to_list("href")
    used = to_list("used")
    Display_type = to_list("display")
    processor = to_list("processor")
    version=to_list('version')
    Touch_control = to_list("touch_control")
    screen_size=to_list('screen_size')
    sale = to_list("sale")
    Favorable_rate=to_list('percentage')
    for i in range(0, 1970):
        summary.write(brands[i] + "," + model[i] + "," + price[i] + "," +money_off[i]+','+discount[i]+','+ internal_storage[i] + ","
                  + solid_storage[i] + "," + Display[i] + "," + shop[i] + ','
                  + str(shop_type[i]) + "," + video_memory[i] + "," + str(jingdong[i]) + ","
                  + href[i] + "," + str(used[i]) + "," + str(Display_type[i]) + "," + processor[i] + ","
                  + version[i]+','+str(Touch_control[i]) + "," +screen_size[i]+',' +str(sale[i]) +','+ str(Favorable_rate[i])+"\n")
                


    