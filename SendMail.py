# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
import os
import datetime
import time
import subprocess




reload(sys)
sys.setdefaultencoding("utf-8")



#, "wangjianlong108@vip.qq.com"  "dupei1991@vip.qq.com",
mailto_list = ["wangjianlong108@vip.qq.com"]  #目标邮箱
mail_host = "smtp.163.com"
mail_user = "18600510929@163.com"
mail_pass = "wangge108"  #163邮箱smtp生成的密码



def send_mail(sub, content):
    me = "足球"+"<"+mail_user+">"
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, mailto_list, msg.as_string())
        server.close()
        print '发送成功'
        return True
    except Exception, e:
        print '发送失败 ' + str(e)
        return False

test = "广州富力vs贵州恒丰智诚"

print time.strftime('%Y-%m-%d', time.localtime(time.time()))

send_mail("2017-4-28", test)
