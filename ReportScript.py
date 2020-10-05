from selenium import webdriver
import time
import datetime

# 配置无界面模式
Chrome_options = webdriver.ChromeOptions()
Chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
Chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
Chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
Chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
Chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

file_read = open('config.txt', 'r')
info = file_read.read().splitlines()
stuID = info[0]
Password = info[1]
file_read.close()

XueGH = "学工号：" + stuID

NowTime = datetime.datetime.now()
TodayStr = NowTime.strftime('%Y-%m-%d')
DeltaDay = datetime.timedelta(days=-1)
Yesterday = NowTime + DeltaDay
YesterdayStr = Yesterday.strftime('%Y-%m-%d')

js = 'document.getElementById("p1_BaoSRQ-inputEl").removeAttribute("readonly");'
js_value_today = 'document.getElementById("p1_BaoSRQ-inputEl").value="' + TodayStr + '"'
js_value_yesterday = 'document.getElementById("p1_BaoSRQ-inputEl").value="' + YesterdayStr + '"'

file_obj = open('log.txt', 'a')
file_obj.write('\n' + NowTime.strftime('%Y/%m/%d %H:%M:%S') + '\t')

driver = webdriver.Chrome(options=Chrome_options)
driver.get("https://selfreport.shu.edu.cn/")
time.sleep(1)

# 需要登录的话
if driver.current_url == 'https://newsso.shu.edu.cn/login':
    # 清空输入框
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("password").clear()
    # 填写账号、密码
    driver.find_element_by_id("username").send_keys(stuID)
    driver.find_element_by_id("password").send_keys(Password)
    # 点击“登录”
    driver.find_element_by_id("login-submit").click()

time.sleep(1)

if driver.current_url == 'https://selfreport.shu.edu.cn/':
    # 学工号：17721999，则登录成功
    if driver.find_element_by_id("lbXueGH").text == XueGH:
        file_obj.write('登录成功' + '\t')
        # 点击“在校学生日报”
        driver.find_element_by_id("lnkReport").click()  # https://selfreport.shu.edu.cn/XueSFX/FanXRB.aspx
        time.sleep(1)
        # 点击“晨报”
        driver.find_element_by_id("p1_Button1").click()  #https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=1
        # 我承诺
        driver.find_element_by_id("p1_ChengNuo-inputEl-icon").click()
        # 身体状况：良好
        driver.find_element_by_id("fineui_0-inputEl-icon").click()
        # 日期控件处理：js去掉只读属性，输入日期
        driver.execute_script(js)
        driver.execute_script(js_value_today)
        time.sleep(0.5)
        # 体温：36
        driver.find_element_by_id("p1_TiWen-inputEl").clear()
        time.sleep(0.5)
        driver.find_element_by_id("p1_TiWen-inputEl").send_keys(36)
        # 随申码颜色：绿色
        driver.find_element_by_id("fineui_7-inputEl-icon").click()
        # 到食堂就餐：早餐
        driver.find_element_by_id("fineui_8-inputEl-icon").click()
        # 到食堂就餐：午餐
        driver.find_element_by_id("fineui_9-inputEl-icon").click()
        # 到食堂就餐：晚餐
        driver.find_element_by_id("fineui_10-inputEl-icon").click()
        # 点击“提交”
        driver.find_element_by_id("p1_ctl00_btnSubmit").click()
        time.sleep(0.5)
        # 弹窗-确定要提交吗：点击“确定”
        driver.find_element_by_id("fineui_14").click()
        time.sleep(1)
        # 弹窗-提交成功：点击“确定”
        driver.find_element_by_id("fineui_19").click()
        file_obj.write('晨报完成' + '\t')
        time.sleep(0.5)
    else:
        file_obj.write('晨报失败' + '\t')
        # -----------------------晨报完成----------------------------#

    if driver.find_element_by_id("lbXueGH").text == XueGH:
        # 点击“在校学生日报”
        driver.find_element_by_id("lnkReport").click()  # https://selfreport.shu.edu.cn/XueSFX/FanXRB.aspx
        time.sleep(0.5)
        # 点击“晚报”
        driver.find_element_by_id("p1_Button2").click()  # https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=2
        # 我承诺
        driver.find_element_by_id("p1_ChengNuo-inputEl-icon").click()
        # 日期控件处理：js去掉只读属性，输入日期
        driver.execute_script(js)
        driver.execute_script(js_value_yesterday)
        time.sleep(0.5)
        # 体温：36
        driver.find_element_by_id("p1_TiWen-inputEl").clear()
        time.sleep(0.5)
        driver.find_element_by_id("p1_TiWen-inputEl").send_keys(36)
        # 随申码颜色：绿色
        driver.find_element_by_id("fineui_7-inputEl-icon").click()
        # 点击“提交”
        driver.find_element_by_id("p1_ctl00_btnSubmit").click()
        time.sleep(0.5)
        # 弹窗-确定要提交吗：点击“确定”
        driver.find_element_by_id("fineui_14").click()
        time.sleep(1)
        if driver.find_element_by_class_name("f-messagebox-message").text == '提交成功':
            # 弹窗-提交成功：点击“确定”
            driver.find_element_by_id("fineui_19").click()
            file_obj.write('晚报完成' + '\t')
        else:
            file_obj.write('晚报失败' + '\t')
        time.sleep(0.5)
    else:
        file_obj.write('晚报失败' + '\t')
        # -----------------------晚报完成----------------------------#

if driver.current_url == 'https://selfreport.shu.edu.cn/Default.aspx':
    file_obj.write('两报完成')
else:
    file_obj.write('两报失败')

NowTime = datetime.datetime.now()
file_obj.write('\t' + NowTime.strftime('%Y/%m/%d %H:%M:%S'))

file_obj.close()
driver.quit()
