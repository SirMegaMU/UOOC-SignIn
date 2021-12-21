from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
from os import system
from sys import exit

print("更多信息，请访问：\nhttps://megamu.icu/\n")


with open("account&pwd.txt","r") as file:
    text=file.readlines()
    account=text[0][10:-1:]
    pwd=text[1][6:-1:]
    print("本次登陆账号和密码分别为：")
    print(account,"  ",pwd[:2:]+"****"+pwd[-2::])

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(".\chromedriver.exe",options=option)


browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", 
    {
        "source": """Object.defineProperty(
            navigator, 
            'webdriver', 
            {get: () => undefined}
            )"""
    })



browser.get('http://www.uooc.net.cn/home#/center/course/learn')

login_account = browser.find_element_by_id('account')
login_account.click()
sleep(0.5)
login_account.send_keys(account)
sleep(0.5)

login_pwd=browser.find_element_by_id('password')
sleep(0.5)
login_pwd.click()
sleep(0.5)
login_pwd.send_keys(pwd)
sleep(0.5)

captcha=browser.find_element_by_id("SM_BTN_1")
captcha.click()
sleep(5)
# /html/body/div/div[2]/form/button
# .btn
login_button=browser.find_element_by_css_selector('.btn')
print("进行登陆中")
login_button.click()
sleep(4)
print(browser.title,browser.current_url)
n=0
if browser.title=="优课联盟——共建共享，学分互认":
    print('登录成功')

    # /html/body/div[3]/div[4]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/a
    classbuttons=browser.find_elements_by_xpath('/html//div/div[2]/div[3]/a')
    clstotal=len(classbuttons)-1
    print("你选择的课程总共有{}门：".format(clstotal))
    Urls=[]
    for clsbutton in classbuttons:
        lessonUrl=clsbutton.get_attribute("href")
        Urls.append(lessonUrl)
        print(clsbutton,"\n",lessonUrl,"\n\n")
    for clsurl in Urls[:-1:]:
        try:
            browser.get(clsurl)
            sleep(2)
            enterlesson=browser.find_element_by_css_selector('a.btn:nth-child(1)')
            enterlesson.click()
            sleep(3)
            print("课程签到成功！")
            n+=1
        except Exception as e:
            print("课程进入失败！\n失败原因：")
            print(e,"\n")
    browser.close()
    print("""课程签到完毕！\n总共有{}门课程\n成功签到{}门""".format(clstotal,n))
    system('pause')
    exit()

else:
    print("登陆失败！\n请检查密码是否正确，网络是否正常连接")
