import smtplib
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM


class EmailSender_163:

    def __init__(self, sender='python_is_fun@163.com', mail_password='AIJUYLCFLGLZHOXN'):
        """
        :param sender: the sender email (@163.com) you wish to use
        :param mail_password: IMAP/SMTP Code of your email
        """

        # Set the host
        self.mail_host = 'smtp.163.com'

        # Set the sender
        self.sender = sender

        # Set user and IMAP/SMTP Code
        self.mail_user = self.sender.split('@')[0]
        self.mail_password = mail_password

    def send_single_email(self, receiver, subject, html):
        """
        Send a single email through 163 mail.
        :param receiver: The receiver email you wish to send to.
        :param subject: The Subject of the email you wish to name.
        :param html: The html format content you wish to be the body of the email
        :return: Print Success msg if the email is sent successfully, otherwise print error msg.
        """
        msg = MM()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = receiver

        # Import html file as the content
        with open(html, 'r')as b:
            content = b.read()

        # Create a html MIMEText object
        MTObj = MT(content, "html")
        msg.attach(MTObj)

        try:
            server = smtplib.SMTP()
            # Connect to the server
            server.connect(self.mail_host, 25)
            # Login the email
            server.login(self.mail_user, self.mail_password)
            # Send the email
            server.sendmail(self.sender, receiver, msg.as_string())
            # Quit
            server.quit()
            return 1
        except smtplib.SMTPException:
            return -1

    def send_batch_emails(self, receivers, subject, html):
        """
        Send a batch of emails through 163 mail.
        :param receivers: an array of receivers' emails you wish to send to.
        :param subject: The Subject of the email you wish to name.
        :param html: The html format content you wish to be the body of the email
        :return: Print Success msg if the emails are sent successfully, otherwise print error msg.
        """
        for receiver in receivers:
            self.send_single_email(receiver, subject, html)
