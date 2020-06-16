from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(chrome_options=chrome_options)
text = []
for page in range(50):
    if page==0:
        driver.get("https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&page=1&s=1&click=0")
    text.append(driver.page_source)
    next_page = driver.find_element_by_xpath("//span[@class='p-num']//a[@class='pn-next']")
    next_page.click()
    sleep(2)
with open("jd_data.txt", "w",encoding="utf-8") as f:
    f.write(str(text))
    
