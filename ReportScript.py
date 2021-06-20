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

XueGH = '学工号：' + stuID

NowTime = datetime.datetime.now()
TodayStr = NowTime.strftime('%Y-%m-%d')
DeltaDay = datetime.timedelta(days=-1)
Yesterday = NowTime + DeltaDay
YesterdayStr = Yesterday.strftime('%Y-%m-%d')

js_date = 'document.getElementById("p1_BaoSRQ-inputEl").removeAttribute("readonly");'
js_value_today = 'document.getElementById("p1_BaoSRQ-inputEl").value="' + TodayStr + '"'
js_value_yesterday = 'document.getElementById("p1_BaoSRQ-inputEl").value="' + YesterdayStr + '"'

js_province = 'document.getElementById("p1_ddlSheng-inputEl").removeAttribute("readonly");'
js_province_value = 'document.getElementById("p1_ddlSheng-inputEl").value="上海"'

js_municipal = 'document.getElementById("p1_ddlShi-inputEl").removeAttribute("readonly");'
js_municipal_value = 'document.getElementById("p1_ddlShi-inputEl").value="上海市"'

js_district = 'document.getElementById("p1_ddlXian-inputEl").removeAttribute("readonly");'
js_district_value = 'document.getElementById("p1_ddlXian-inputEl").value="宝山区"'

file_obj = open('log.txt', 'a')
file_obj.write('\n' + NowTime.strftime('%Y/%m/%d %H:%M:%S') + '\t')

driver = webdriver.Chrome(options=Chrome_options)
driver.get("https://selfreport.shu.edu.cn/")
time.sleep(1)

#未读消息
try:
    driver.find_element_by_class_name('layui-layer-content') # 搜索“未读消息”弹窗
except:
    file_obj.write('没有未读消息' + '\t')
else:
    file_obj.write('打开未读消息' + '\t')
    ToReadNum = 0
    driver.find_element_by_class_name('layui-layer-btn0').click() # 未读消息“确定”按钮，自动进入消息中心
    MessageList = driver.find_elements_by_class_name('f-datalist-item-inner')
    for i in range(len(MessageList)):
        if MessageList[i].text.find("未读") != -1:
            ToReadNum += 1
    while ToReadNum > 0:
        MessageList = driver.find_elements_by_class_name('f-datalist-item-inner')
        MessageList[ToReadNum - 1].click()
        time.sleep(0.5)
        driver.find_element_by_id('p1_ctl00_btnReturn').click()
        ToReadNum -= 1
    driver.find_element_by_id('Panel1_ctl00_btnReturn').click()  # 点击“返回”按钮到主界面

# 清空输入框
driver.find_element_by_id("username").clear()
driver.find_element_by_id("password").clear()
# 填写账号、密码
driver.find_element_by_id("username").send_keys(stuID)
driver.find_element_by_id("password").send_keys(Password)
# 点击“登录”
driver.find_element_by_id("submit").click()

time.sleep(1)

# 学工号：XXXXXXXX，则登录成功
if driver.find_element_by_id("lbXueGH").text == XueGH:
    file_obj.write('登录成功' + '\t')
    # 点击“在校学生日报”
    driver.find_element_by_id("lnkReport").click()  # https://selfreport.shu.edu.cn/XueSFX/FanXRB.aspx
    time.sleep(1)
    # 点击“晨报”
    driver.find_element_by_id("p1_Button1").click()  # https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx?t=1
    # 我承诺
    driver.find_element_by_id("p1_ChengNuo-inputEl-icon").click()
    # 报送日期：日期输入控件处理：js去掉只读属性，输入当天日期
    driver.execute_script(js_date)
    driver.execute_script(js_value_today)
    time.sleep(0.5)
    # 身体状况：良好
    driver.find_element_by_id("fineui_0-inputEl-icon").click()
    # 体温：36
    driver.find_element_by_id("p1_TiWen-inputEl").clear()
    time.sleep(0.5)
    driver.find_element_by_id("p1_TiWen-inputEl").send_keys(36)
    # 当天是否在校：宝山校区
    driver.find_element_by_id("fineui_6-inputEl-icon").click()
    # 当天所在省：输入控件处理：js去掉只读属性，输入上海
    driver.execute_script(js_province)
    driver.execute_script(js_province_value)
    time.sleep(0.5)
    # 当天所在市：输入控件处理：js去掉只读属性，输入上海市
    driver.execute_script(js_municipal)
    driver.execute_script(js_municipal_value)
    time.sleep(0.5)
    # 当天所在县区：输入控件处理：js去掉只读属性，输入宝山区
    driver.execute_script(js_district)
    driver.execute_script(js_district_value)
    time.sleep(0.5)
    # 具体地址
    driver.find_element_by_id("p1_XiangXDZ-inputEl").clear()
    time.sleep(0.5)
    driver.find_element_by_id("p1_XiangXDZ-inputEl").send_keys('XXXXXX')
    # 是否在中高风险地区逗留：否
    driver.find_element_by_id("fineui_11-inputEl-icon").click()
    # 同住人员是否来自中高风险地区：否
    driver.find_element_by_id("fineui_13-inputEl-icon").click()
    # 是否接触来自中高风险地区人员：否
    driver.find_element_by_id("fineui_17-inputEl-icon").click()
    # 是否途径中高风险地区：否
    driver.find_element_by_id("fineui_19-inputEl-icon").click()
    # 当天是否隔离：否
    driver.find_element_by_id("fineui_21-inputEl-icon").click()
    # 健康码颜色：绿色
    driver.find_element_by_id("fineui_26-inputEl-icon").click()
    # 健康码14天连续绿色：是
    driver.find_element_by_id("fineui_27-inputEl-icon").click()
    # 点击“提交”
    driver.find_element_by_id("p1_ctl00_btnSubmit").click()
    time.sleep(0.5)
    # 弹窗-确定要提交吗：点击“确定”
    driver.find_element_by_id("fineui_32").click()
    time.sleep(1)
    # 弹窗-提交成功：点击“确定”
    driver.find_element_by_id("fineui_37").click()
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
    # 报送日期：日期输入控件处理：js去掉只读属性，输入当天日期
    driver.execute_script(js_date)
    driver.execute_script(js_value_yesterday)
    time.sleep(0.5)
    # 身体状况：良好
    driver.find_element_by_id("fineui_0-inputEl-icon").click()
    # 体温：36
    driver.find_element_by_id("p1_TiWen-inputEl").clear()
    time.sleep(0.5)
    driver.find_element_by_id("p1_TiWen-inputEl").send_keys(36)
    # 当天是否在校：宝山校区
    driver.find_element_by_id("fineui_6-inputEl-icon").click()
    # 当天所在省：输入控件处理：js去掉只读属性，输入上海
    driver.execute_script(js_province)
    driver.execute_script(js_province_value)
    time.sleep(0.5)
    # 当天所在市：输入控件处理：js去掉只读属性，输入上海市
    driver.execute_script(js_municipal)
    driver.execute_script(js_municipal_value)
    time.sleep(0.5)
    # 当天所在县区：输入控件处理：js去掉只读属性，输入宝山区
    driver.execute_script(js_district)
    driver.execute_script(js_district_value)
    time.sleep(0.5)
    # 具体地址
    driver.find_element_by_id("p1_XiangXDZ-inputEl").clear()
    time.sleep(0.5)
    driver.find_element_by_id("p1_XiangXDZ-inputEl").send_keys('XXXXX')
    # 是否在中高风险地区逗留：否
    driver.find_element_by_id("fineui_11-inputEl-icon").click()
    # 同住人员是否来自中高风险地区：否
    driver.find_element_by_id("fineui_13-inputEl-icon").click()
    # 是否接触来自中高风险地区人员：否
    driver.find_element_by_id("fineui_17-inputEl-icon").click()
    # 是否途径中高风险地区：否
    driver.find_element_by_id("fineui_19-inputEl-icon").click()
    # 当天是否隔离：否
    driver.find_element_by_id("fineui_21-inputEl-icon").click()
    # 健康码颜色：绿色
    driver.find_element_by_id("fineui_26-inputEl-icon").click()
    # 健康码14天连续绿色：是
    driver.find_element_by_id("fineui_27-inputEl-icon").click()
    # 点击“提交”
    driver.find_element_by_id("p1_ctl00_btnSubmit").click()
    # 弹窗-确定要提交吗：点击“确定”
    driver.find_element_by_id("fineui_32").click()
    time.sleep(1)
    if driver.find_element_by_class_name("f-messagebox-message").text == '提交成功':
        # 弹窗-提交成功：点击“确定”
        driver.find_element_by_id("fineui_37").click()
        file_obj.write('晚报完成' + '\t')
    else:
        file_obj.write('晚报失败' + '\t')
    time.sleep(0.5)
else:
    file_obj.write('晚报失败' + '\t')
        # -----------------------晚报完成----------------------------#

if driver.current_url == 'https://selfreport.shu.edu.cn/Default.aspx':
    file_obj.write('两报完成, ')
else:
    file_obj.write('两报失败, ') # 9：35 dev0620  comment

NowTime = datetime.datetime.now()
file_obj.write(NowTime.strftime('%Y/%m/%d %H:%M:%S'))
#woshi shabi!
file_obj.close()
driver.quit()
