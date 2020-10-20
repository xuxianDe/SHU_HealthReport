# SHU_HealthReport
## 上海大学在校学生每日两报

个人习惯在起床后完成当天早报和前一天晚报，故脚本实现的功能是每日两报，即上报当天和前一天健康状态。

在本人电脑设置的是当天凌晨01:00的定时任务，一次完成两报。

脚本输出日志文件log.txt




+ 登录需要账号（学生卡号）、密码，将账号、密码换行写入config.txt中


+ 脚本(ReportScript.py)使用Chrome浏览器，确认本地Chrome版本，并使用相匹配的chromedriver版本。


+ 最后，将ReportScript.py、chromedriver.exe、config.txt放在同一目录下即可


**PS：**

PC端登录网址:https://selfreport.shu.edu.cn/

chromedriver下载地址:https://npm.taobao.org/mirrors/chromedriver



2020年10月14日更新：

删除登录判断，“登录”按钮的元素id由“login_submit”改为“submit”



2020年10月20日更新：

增加打开未读消息的功能