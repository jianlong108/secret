# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# SMTP 服务器信息
smtp_server = 'smtp.163.com'
smtp_port = 465

class MailHelper:
    def __init__(self):
        self.mailtoList = "87322568@qq.com"  # 目标邮箱
        self.mailHost = "smtp.163.com"
        self.mailUser = "18600510929@163.com"
        self.mailPassWord = "JKRFOFFGGNXUJBNV"  # 163邮箱smtp生成的密码

    def sendMailWithPlainText(self,title,body):
        msg = MIMEMultipart('')
        msg['Subject'] = title
        msg['From'] = self.mailUser
        msg['To'] = self.mailtoList
        # msg.attach(MIMEText(str(content), contentType, 'utf-8'))
        msg.attach(MIMEText(body, 'plain'))
        # msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
        try:
            # 连接到 SMTP 服务器
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用 SMTP_SSL 而不是 starttls
            server.login(self.mailUser, self.mailPassWord)  # 登录
            server.sendmail(self.mailUser, self.mailtoList, msg.as_string())  # 发送邮件
            print('邮件发送成功')
        except Exception as e:
            print(f'邮件发送失败: {e}')
        finally:
            server.quit()  # 断开连接

    def sendMailWithHtml(self,title,body):
        msg = MIMEMultipart('')
        msg['Subject'] = title
        msg['From'] = self.mailUser
        msg['To'] = self.mailtoList
        # msg.attach(MIMEText(str(content), contentType, 'utf-8'))
        # msg.attach(MIMEText(body, 'plain'))

        msg.attach(MIMEText(body, 'html', 'utf-8'))
        try:
            # 连接到 SMTP 服务器
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # 使用 SMTP_SSL 而不是 starttls
            server.login(self.mailUser, self.mailPassWord)  # 登录
            server.sendmail(self.mailUser, self.mailtoList, msg.as_string())  # 发送邮件
            print('邮件发送成功')
        except Exception as e:
            print(f'邮件发送失败: {e}')
        finally:
            server.quit()  # 断开连接

if __name__ == '__main__':
    mail = MailHelper()
    # mail.sendMailWithPlainText('测试','hhh')

    content = """
                <!DOCTYPE html>
                    <html lang="en">
                    <head><meta charset="UTF-8"><title>预测展示</title>
                    </head>
                    <body>
                        <table bgcolor=#333333 cellspacing="1px" width="375px" align="center">
                            <caption style="color:red;"><h2>今日小说排行榜</h2></caption>
                            <caption style="color:red;"><h5>亚盘</h5></caption>
                            <tr bgcolor=#663399>
                                <th>博彩公司</th><th>盘口</th><th>总数</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th>
                            </tr>
                            <tr bgcolor="white" >
                                <td>1</td><td align="left">暴走大事件</td> <td><img src="images/up.jpg"></td><td>623557</td><td>4088311</td>
                                <td><a >贴吧</a><a >图片</a><a >百科</a></td>
                            </tr>
                            <tr bgcolor="white" align="center">
                                <td>1</td><td align="left">暴走大事件</td><td><img src="images/up.jpg"></td><td>623557</td><td>4088311</td><td><a >贴吧</a><a >图片</a><a >百科</a></td>
                            </tr>
                        </table>
                    </body>
                </html>
              """
    mail.sendMailWithHtml('html',content)

#, "wangjianlong108@vip.qq.com"  "dupei1991@vip.qq.com",  "jiqimao3528@vip.qq.com"
# mailto_list = ["87322568@qq.com"]  #目标邮箱
# mail_host = "smtp.163.com"
# mail_user = "18600510929@163.com"

# def send_mail(sub, content,contentType = 'plain'):
#     me = "足球"+"<"+mail_user+">"
#     # msg = MIMEText(str(content), 'plain', 'utf-8')
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = sub
#     msg['From'] = me
#     msg['To'] = ";".join(mailto_list)
#     msg.attach(MIMEText(str(content), contentType, 'utf-8'))
#     # msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))
#     try:
#         server = smtplib.SMTP()
#         server.connect(mail_host,25)
#         server.login(mail_user, mail_pass)
#         server.sendmail(me, mailto_list, msg.as_string())
#         server.close()
#         print('发送成功')
#         return True
#     except Exception as e:
#         print('发送失败 ', e)
#         return False
#
# contentstr = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>预测展示</title></head>" \
#              "<body>" \
#              "<table bgcolor=\"black\"cellspacing=\"1px\"width=\"375px\" align=\"center\"><caption style=\"color:red;\"><h2>今日小说排行榜</h2></caption>" \
#              "<caption style=\"color:red;\"><h5>亚盘</h5></caption><tr bgcolor=#663399><th>博彩公司</th><th>盘口</th><th>总数</th><th>赢盘</th><th>走盘</th><th>输盘</th><th>胜</th><th>平</th><th>负</th></tr>" \
#              "<tr bgcolor=\"white\" ><td>1</td><td align=\"left\">暴走大事件</td> <td><img src=\"images/up.jpg\"></td><td>623557</td><td>4088311</td>" \
#             "<td><a >贴吧</a><a >图片</a><a >百科</a></td></tr>" \
#              "<tr bgcolor=\"white\" align=\"center\"><td>1</td><td align=\"left\">暴走大事件</td><td><img src=\"images/up.jpg\"></td><td>623557</td><td>4088311</td><td><a >贴吧</a><a >图片</a><a >百科</a></td>" \
#              "</table></body></html>"
#
#
#
# send_mail("测试","123")