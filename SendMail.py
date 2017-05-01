# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
import string





reload(sys)
sys.setdefaultencoding("utf-8")



#, "wangjianlong108@vip.qq.com"  "dupei1991@vip.qq.com",, "112627297@qq.com"
mailto_list = ["dupei1991@vip.qq.com", "wangjianlong108@vip.qq.com", "jiqimao3528@vip.qq.com"]  #目标邮箱
mail_host = "smtp.163.com"
mail_user = "18600510929@163.com"
mail_pass = "wangge108"  #163邮箱smtp生成的密码



def send_mail(sub, content):
    me = "足球"+"<"+mail_user+">"
    # msg = MIMEText(str(content), 'plain', 'utf-8')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ",".join(mailto_list)
    msg.attach(MIMEText(str(content), 'plain', 'utf-8'))
    # msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
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


# print time.strftime('%Y-%m-%d', time.localtime(time.time()))
#
# tempStr = ''.join(['a', 'b', 'c'])
#
# send_mail("射雕", '群发邮件测试')
