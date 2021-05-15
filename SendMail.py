# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys

reload(sys)
sys.setdefaultencoding("utf-8")




class MailHelper:
    def __init__(self):
        self.mailtoList = ["wangjianlong108@vip.qq.com"]  # 目标邮箱
        self.mailHost = "smtp.163.com"
        self.mailUser = "18600510929@163.com"
        self.mailPassWord = "wangge108"  # 163邮箱smtp生成的密码

    def sendMail(self,sub, content, contentType = 'plain'):
        me = "足球" + "<" + mail_user + ">"
        # msg = MIMEText(str(content), 'plain', 'utf-8')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(self.mailtoList)
        msg.attach(MIMEText(str(content), contentType, 'utf-8'))
        # msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
        try:
            server = smtplib.SMTP()
            server.connect(self.mailHost)
            server.login(self.mailUser, self.mailPassWord)
            server.sendmail(me, self.mailtoList, msg.as_string())
            server.close()
            print '发送成功'
            return True
        except Exception, e:
            print '发送失败 ' + str(e)
            return False


#, "wangjianlong108@vip.qq.com"  "dupei1991@vip.qq.com",  "jiqimao3528@vip.qq.com"
mailto_list = ["wangjianlong108@vip.qq.com"]  #目标邮箱
mail_host = "smtp.163.com"
mail_user = "18600510929@163.com"
mail_pass = "wangge108"  #163邮箱smtp生成的密码

def send_mail(sub, content,contentType = 'plain'):
    me = "足球"+"<"+mail_user+">"
    # msg = MIMEText(str(content), 'plain', 'utf-8')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    msg.attach(MIMEText(str(content), contentType, 'utf-8'))
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

# contentstr = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>预测展示</title></head>" \
#              "<body>" \
#              "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\"><caption style=\"color:red;\"><h2>今日小说排行榜</h2></caption>" \
#              "<caption style=\"color:red;\"><h5>亚盘</h5></caption><tr bgcolor=#663399><th>博彩公司</th><th>盘口</th><th>总数</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th></tr>" \
#              "<tr bgcolor=\"white\" ><td>1</td><td align=\"left\">暴走大事件</td> <td><img src=\"images/up.jpg\"></td><td>623557</td><td>4088311</td>" \
#             "<td><a >贴吧</a><a >图片</a><a >百科</a></td></tr>" \
#              "<tr bgcolor=\"white\" align=\"center\"><td>1</td><td align=\"left\">暴走大事件</td><td><img src=\"images/up.jpg\"></td><td>623557</td><td>4088311</td><td><a >贴吧</a><a >图片</a><a >百科</a></td>" \
#              "</table></body></html>"
# send_mail('测试',contentstr,'html')