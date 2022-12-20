from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os

class Alert:
    subject: str
    body: str
    msg_main_multipart: MIMEMultipart
    from_addr: str
    send_to: list

    def __init__(self, subject: str, body: str):
        self.subject = subject
        self.body = body

    def get(self):
        return self.msg_main_multipart

class EmailManager:
    def __init__(self):
        self.smtp = None
        self.template_incident = "../emails/template_incident.html"
        self.template_change = "../emails/template_change.html"
        self.from_addr = "josepadial@correo.ugr.es"
        self.send_to = "josepadial@correo.ugr.es"
        self.connect()

    def connect(self):
        self.smtp = smtplib.SMTP("localhost", 25)

    def make_message(self, data, incidencias=False):
        if incidencias:
            template = Template(open(self.template_incident, encoding='utf-8').read())
            html = template.render(incident=data)
        else:
            template = Template(open(self.template_change, encoding='utf-8').read())
            html = template.render(change=data)
        return html

    def send_email(self, data, subject, incidencias=False):
        html = self.make_message(data, incidencias)
        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = self.send_to
        message["To"] = self.from_addr
        html_email_part = MIMEText(html, 'html')
        message.attach(html_email_part)
        self.smtp.sendmail(self.send_to, self.from_addr, message.as_string())