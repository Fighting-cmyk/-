from time import sleep 
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=option)
text = []
with open("href.txt", "r", encoding="utf-8") as f:
    hrefs = list(eval(f.read()))
for href in hrefs[0:1970]:
    try:
        sleep(5)
        driver.get("https:" + href + "#comment")
        sleep(20)
        element = driver.find_element_by_xpath("//label[@for='comm-curr-sku']")
        ActionChains(driver).move_to_element(element).click().perform()
        sleep(12)
        comments_number = driver.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|allpingjia']")
        good_percentage = driver.find_element_by_xpath("//div[@class='percent-con']")
        f=open("jd_data24.txt","a",encoding="utf-8")
        f.write(str(comments_number.text))
        f.write(str(good_percentage.text))
        f.write("------")
        f.close()
    except:
        f=open("jd_data24.txt","a",encoding="utf-8")
        f.write(' ')
        f.write("------")
        f.close()