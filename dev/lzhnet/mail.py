# -*- coding: UTF-8 -*-
# Public package
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
# Private package
# Internal package


def get_server_qqmail():
    output = smtplib.SMTP_SSL('smtp.qq.com', 465)
    output.login('791397845@qq.com', 'ujjrszxropnzbedb')
    return output, '791397845@qq.com'


def get_server_incmail():
    output = smtplib.SMTP('smtp.exmail.qq.com', timeout=30)
    output.login('leizuohong@haoxingtrade.com', 'LZHkandejia9638')
    return output, 'leizuohong@haoxingtrade.com'


class Mail:
    def __init__(self, *args, **argv):
        self.server = args[0]
        self.sender = args[1]
        self.data = MIMEMultipart()
        self.title = 'Default_title'
        self.name_receiver = 'Default_receiver'
        self.text = ''
        self.image_id = 0

    def add_text(self, text):
        self.text += text.replace('\n', '<br />')
        self.text += '<br />'

    def add_pandas(self, df):
        self.text += df.to_html()

    def add_image(self, filename, width=400, height=300):
        with open(filename, 'rb') as infile:
            image = MIMEImage(infile.read())
        image_name = '%d' % (self.image_id)
        self.image_id += 1
        image.add_header('Content-ID', '<image_%s>' % (image_name))
        self.data.attach(image)
        self.text += '<img src="cid:image_%s" width="%d", height="%d">' % (image_name, width, height)

    def add_attachment(self, filename):
        with open(filename, 'rb') as infile:
            attachment = MIMEApplication(infile.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        self.data.attach(attachment)

    def send(self, receivers):
        self.data['Subject'] = Header(self.title, 'utf-8')
        self.data['From'] = self.sender
        self.data['To'] = Header(self.name_receiver, 'utf-8')
        self.data.attach(MIMEText(self.text, 'html', 'utf-8'))
        self.server.sendmail(self.sender, receivers, self.data.as_string())
