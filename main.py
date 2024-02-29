from selenium.webdriver.common.by import By
from auth import login, password
from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
from colorama import Fore
import undetected_chromedriver as uc

browser = uc

_hashtag = input("Enter your hashtag: ")


def login_chrome(login, password):
    global browser
    lang_eng = webdriver.ChromeOptions()
    lang_eng.add_argument("--lang=eng")
    """browser = webdriver.Chrome(options=lang_eng)  default webdriver use"""
    browser = uc.Chrome(options=lang_eng)
    browser.implicitly_wait(3)
    browser.get('https://www.instagram.com')
    time.sleep(random.randrange(2, 4))

    try:
        _cookie = browser.find_element(By.XPATH,
                                       '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]')
        time.sleep(random.randrange(2, 4))
        _cookie.click()

    except :
        print("cookie popup not found")

    time.sleep(random.randrange(2, 4))

    _login = browser.find_element(By.NAME, "username")
    _login.clear()
    _login.send_keys(login)

    time.sleep(random.randrange(1, 2))

    _password = browser.find_element(By.NAME, "password")
    _password.clear()
    time.sleep(random.randrange(2, 4))
    _password.send_keys(password)

    time.sleep(random.randrange(3, 5))

    _password.send_keys(Keys.ENTER)
    time.sleep(random.randrange(3, 5))
    # Блок пропуска сохранить данные и вкл выкл уведомления!!
    try:
        save_data = browser.find_element(By.XPATH,
                                         '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div['
                                         '2]/section/main/div/div/div/section/div/button')
        time.sleep(random.randrange(2, 4))
        save_data.click()

    except:
        print("save data pop up not found")

    time.sleep(random.randrange(2, 4))

    try:
        notifications = browser.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div['
                                                       '2]/div/div/div[3]/button[2]')
        time.sleep(random.randrange(2, 4))
        notifications.click()
    except:
        print("notifications pop up not found")

    time.sleep(random.randrange(2, 4))


def close_browser():
    global browser
    browser.close()
    browser.quit()


def search_by_hashtag(_hashtag):
    global browser
    browser.get(f"https://www.instagram.com/explore/tags/{_hashtag}/")

    for i in range(1, 10):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randrange(2, 5))

    hrefs = browser.find_elements(by=By.TAG_NAME, value='a')
    urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
    print(urls)

    for url in urls:
        browser.get(url)
        time.sleep(random.randrange(2, 5))

        like = browser.find_element(by=By.CLASS_NAME, value='xp7jhwk')
        soup = bs(like.get_attribute('innerHTML'), 'html.parser')
        if soup.find('svg')['aria-label'] == 'Like':
            like.click()
            print(Fore.GREEN + "Like!")
        else:
            print(Fore.RED + "can't find a like button or post is allready liked")

        time.sleep(random.randrange(5, 10))

        try:
            followbutton = browser.find_element(By.XPATH, value="//*[text()='Follow']")
            followbutton.send_keys(Keys.PAGE_UP)
            followbutton.click()
            print(Fore.BLUE + "Subscribed to a new account!")
        except:
            print(Fore.RED + "Allready following!")

        time.sleep(random.randrange(3, 5))


login_chrome(login, password)
search_by_hashtag(_hashtag)
time.sleep(1000)
close_browser()
