import selenium.webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = selenium.webdriver.Chrome()
driver.get("http://fpga.hdu.edu.cn/co/otherResourcePage.html?resourceTag=fpga")
driver.add_cookie({
    "name":
    "userInfo",
    "value":
    r''
})

driver.add_cookie({
    "name":
    "Admin-Token",
    "value":
    r''
})
driver.get("http://fpga.hdu.edu.cn/co/otherResourcePage.html?resourceTag=fpga")
driver.switch_to.frame("frame")
btns = driver.find_element(by=By.CLASS_NAME, value="el-message-box__wrapper")
bt = btns.find_element(by=By.CLASS_NAME, value="el-button")
bt.click()
wt=WebDriverWait(driver,timeout=10)
time.sleep(60)

switch_box = driver.find_element(
    by=By.XPATH, value=r'//*[@id="body-main"]/div[2]/div[1]/div/div[4]/div[1]')
switchs = switch_box.find_elements(by=By.CLASS_NAME, value="pointer")
bt_box = driver.find_element(
    by=By.XPATH,
    value=r'//*[@id="body-main"]/div[2]/div[1]/div/div[3]/div[2]/div[2]')
bts = bt_box.find_elements(by=By.CLASS_NAME, value="pointer")

bt_push_down = driver.find_element(
    by=By.CLASS_NAME, value="controls").find_element(by=By.CLASS_NAME,
                                                     value="el-button")

def f_2b(inn, base):
    s = ""
    if (type(inn) == int):
        s = (bin(inn))[2:].zfill(32)
    elif (base == 16):
        s = bin(int(inn, 16))[2:].zfill(32)
    elif (base == 10):
        s = bin(int(inn, 10))[2:].zfill(32)
    elif (base == 2):
        s = inn.zfill(32)
    return s


def switch_input(inn, base):
    s = f_2b(inn, base)
    for i in range(32):
        if (s[i] == '0' and switchs[i].get_attribute("src").count("on") == 1):
            wt.until(expected_conditions.element_to_be_clickable(switchs[i]))
            switchs[i].click()
        if (s[i] == '1' and switchs[i].get_attribute("src").count("off") == 1):
            wt.until(expected_conditions.element_to_be_clickable(switchs[i]))
            switchs[i].click()


def extract_name(s):
    l = s.rfind("/")
    r = s.find(".", l)
    return s[l + 1:r]





def get_output():
    wt.until(expected_conditions.element_to_be_clickable(bt_push_down))     
    ret = ""
    digit_box = driver.find_element(
        by=By.XPATH,
        value=r'//*[@id="body-main"]/div[2]/div[1]/div/div[3]/div[2]/div[1]/div'
    )
    digits = digit_box.find_elements(by=By.TAG_NAME, value="img")
    for i in range(8):
        s = digits[i].get_attribute("src")
        d_name = extract_name(s)
        if (d_name == "dash"):
            ret += "-"
        else:
            ret += d_name
    return ret


def get_led(i):
    wt.until(expected_conditions.element_to_be_clickable(bt_push_down))         
    ret = ""
    led_box = driver.find_element(
        by=By.XPATH,
        value=r'//*[@id="body-main"]/div[2]/div[1]/div/div[3]/div[1]')
    leds = led_box.find_elements(by=By.TAG_NAME, value="img")
    s = leds[i].get_attribute("src")
    if (s.count("Down") == 1):
        return '0'
    return '1'

def get_leds():
    ret = ""

    for i in range(32):
        ret+=get_led(i)
    ret=hex(int(ret,2))[2:].zfill(8)
    return ret
def push_down():
    wt.until(expected_conditions.element_to_be_clickable(bt_push_down))
    bt_push_down.click()


def button_press_once(i):
    wt.until(expected_conditions.element_to_be_clickable(bts[i]))         
    bts[i].click()
    push_down()
    wt.until(expected_conditions.element_to_be_clickable(bts[i]))             
    bts[i].click()
    push_down()


