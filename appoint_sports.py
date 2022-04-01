from util import *
from datetime import datetime

username = sys.argv[1] # 登录账号
password = sys.argv[2] # 登录密码
screen_path = os.getcwd() + "/0.png"
img_path = os.getcwd() + "/1.png"

def save_img(src):
    img = requests.get(src)
    with open(img_path, "wb") as f:
        f.write(img.content)

@retry(stop_max_attempt_number=5)
def appoint():
    try:
        driver = get_web_driver()
        driver.get("https://elife.fudan.edu.cn/public/front/myServices.htm?id=2c9c486e4f821a19014f82381feb0001")
        driver.find_element_by_xpath('//*[@id="login_table_div"]/div[2]/input').click()
        time.sleep(1)
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("idcheckloginbtn").click()

        time.sleep(1)
        driver.get('https://elife.fudan.edu.cn/public/front/loadOrderForm_ordinary2.htm?type=resource&serviceContent.id=2c9c486e4f821a19014f82754b190058')
        #driver.get(
        #    'https://elife.fudan.edu.cn/public/front/toResourceFrame.htm?contentId=2c9c486e4f821a19014f826f2a4f0036')
        time.sleep(1)
        driver.maximize_window()
        driver.switch_to.frame("contentIframe")

        t = datetime.utcnow()
        day = t.isoweekday()
        if t.hour > 15:
            day = day+1
        if day > 5:
            driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/ul/li[10]').click()
            day = day-5
        else:
            day = day+2


        #添加开始时间 wait_util()

        driver.find_element_by_id("one"+str(day)).click()
        available = driver.find_elements_by_id("checkCodeDiv")
        if len(available)==0:
            print("约满")
        else:
            n = 11  #手动数
            for i in range(n,0,-1):
                element = driver.find_element_by_xpath('// *[ @ id = "con_one_1"] / table / tbody['+str(i)+'] / tr / td[6] / img')
                if EC.element_to_be_clickable(element):
                    element.click()
                    valid = Ocr_Captcha(driver, '// *[ @ id = "orderCommit"] / div / div[1] / div[2] / table / tbody / tr[5] / td[1] / img', img_path,screen_path)  # 验证码识别
                    print(valid)
                    driver.find_element_by_id("imageCodeName").send_keys(valid)
                    driver.find_element_by_id("btn_sub").click()
                    driver.switch_to.alert.accept()
                    break
                    print("完成")
    except:
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    appoint()

