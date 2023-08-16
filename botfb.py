import random
import time
import os
from selenium import webdriver
import configparser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.FirefoxOptions()
options.add_argument("-profile")
options.add_argument("D:/bot_facrbook/profile")
options.set_preference("general.useragent.override", "Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaX7-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba")
driver = webdriver.Firefox(options=options)

driver.get("http://mbasic.facebook.com")
config = configparser.ConfigParser()
config.read('config.ini')

email = config['Facebook']['email']
password = config['Facebook']['password']
Get = config['groups']['Get']
images_count = int(config['images']['image_count'])
image1 =config['images']['image1']
image2 = config['images']['image2']
image3 = config['images']['image3']
sleep_times = [int(x) for x in config.get('Sleep', 'times').split(',')]


if "welcome_search" in driver.page_source:
    print ("login")
else :    
    print("not login")
    email_field = driver.find_element("id","m_login_email")
    email_field.send_keys(email)

    pass_field = driver.find_element("name","pass")
    pass_field.send_keys(password)

    login_button = driver.find_element("name","login")
    login_button.click()

    submit_button = driver.find_element("xpath","//input[@type='submit']")
    submit_button.click()
    WebDriverWait(5)   
random_sleep_time = random.choice(sleep_times)
print(random_sleep_time)


driver.get("http://mbasic.facebook.com/groups/")
time.sleep(random_sleep_time)


for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random_sleep_time)
    group_links = [a.get_attribute("href") for a in driver.find_elements("css selector","a[href*='groups/']")]
    links = []

        
    for link in group_links:
            if "groups/?category=membership" not in link and "groups/create" not in link:
                links.append(link)
if(Get == 1) :
    with open ("facebook_group_links.txt","w")as file :
            for link in links :
                file.write(link +"\n")   
            file.close()   
    
else:        
    while True: 
        posted_links=[]
        with open("facebook_group_links.txt", "r") as f:
            for link in f.readlines() :
                with open("posted_links.txt" ,"r")as file:
                    if(link.strip() in file.read()):
                        print("Skipping group, already posted: " + link)
                        continue
                driver.get(link.strip())
                WebDriverWait(driver,5)
                #message = "what is the digital marketing"
                #time.sleep(400)
                #text_area = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@name='xc_message']")))
                #text_area.send_keys(message)
                #time.sleep(random_sleep_time)
                #post_button = driver.find_element("name","view_post")
                #post_button.click()

                if images_count > 0:
                    driver.find_element("name","view_photo").click()
                    WebDriverWait(driver, 15)
                    if images_count >= 1:
                        file_input=driver.find_element("name","file1")
                        file_input.send_keys(image1)
                        time.sleep(2)
                    if images_count >= 2:
                        file_input=driver.find_element("name","file2")
                        file_input.send_keys(image2)
                        time.sleep(2)
                    if images_count >= 3:
                        file_input=driver.find_element("name","file3")
                        file_input.send_keys(image3)
                        time.sleep(2)
                else:
                    caption = 'No photos to show.'

                driver.find_element("name","add_photo_done").click()
                WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.NAME, "xc_message"))
                                                            )
                caption= 'Check out these photos!'
                driver.find_element('name','xc_message').send_keys(caption)
                driver.find_element("name","view_post").click()
                time.sleep(10)
                posted_links.append(link)
                with open("posted_links.txt","a")as file :
                    file.write('\n'.join(posted_links))
                driver.close()            