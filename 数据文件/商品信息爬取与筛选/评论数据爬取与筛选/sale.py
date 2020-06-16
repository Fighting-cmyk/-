import re
comments_numbers = []
good_percentages=[]
for number in range(20,25):
    with open("jd_data"+str(number)+".txt", "r", encoding="utf-8") as f:
        comments = f.read()
    comments = comments.split("------")[:-1]
    for comment in comments:
        if comment == ' ':
            good_percentages.append(' ')
            comments_numbers.append(' ')
        else:
            if "万" in comment:
                comments_number = eval(re.search(r"\([0-9]*", comment).group()[1:]) * 10000
            else:
                comments_number = eval(re.search(r"\([0-9]*", comment).group()[1:])
            good_percentage = re.search(r"[0-9]*%", comment).group()
            good_percentages.append(good_percentage[0:-1])
            comments_numbers.append(comments_number)
with open("percentage.txt", "a", encoding="utf-8") as f:
    f.write(str(good_percentages))
with open("sale.txt", "a", encoding="utf-8") as f:
    f.write(str(comments_numbers))
    