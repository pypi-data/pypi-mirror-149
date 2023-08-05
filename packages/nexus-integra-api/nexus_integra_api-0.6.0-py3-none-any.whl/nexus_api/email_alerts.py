import smtplib, ssl
from email.message import EmailMessage
import os
import socket
import mimetypes
from pathlib import Path


class EmailAlerts:
    def __init__(self, smtp_address, email_port, email_sender, email_password,
                 email_receiver, environment=None, attachments=None):
        self.attachments = attachments
        if attachments is None:
            self.attachments = []
        self.environment = environment
        self.message = None
        self.subject = None
        self.smtp_address = smtp_address
        self.email_password = email_password
        self.email_port = email_port
        self.email_sender = email_sender
        self.email_receiver = email_receiver

    def send_email(self, subject=None, message=None):
        """
        Send an email alert. The subject and body of the email can be set by the user or leave blank to use the
        default values.
        args:
            subject: The subject of the email alert.
            body: The body of the email alert.
        """
        msg = EmailMessage()
        msg['From'] = self.email_sender
        msg['To'] = self.email_receiver
        if subject is None:
            msg['Subject'] = self.subject
        else:
            msg['Subject'] = subject
        if message is None:
            msg.set_content(self.message)
        else:
            msg.set_content(message)
        if self.attachments:
            for attachment in self.attachments:
                self._add_attachment(attachment, msg)

        with smtplib.SMTP(self.smtp_address, self.email_port) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
            smtp.login(self.email_sender, self.email_password)
            smtp.send_message(msg)
            print("Email sent successfully")

    def set_message(self, message):
        self.message = message

    def set_subject(self, subject):
        self.subject = subject

    def set_environment(self, environment):
        self.environment = environment

    def set_email_alert_info(self, subject, message, environment):
        """
        Set the message, subject and environment for the email alert all in one function.
        """
        self.set_environment(environment)
        self.set_message(message)
        self.set_subject(subject)

    def set_attachments(self, attachments: list):
        self.attachments = attachments

    def add_attachment(self, attachment):
        self.attachments.append(attachment)

    @staticmethod
    def _add_attachment(path, msg):
        """
        Add an attachment to the email alert as path to the file.
        """
        # Check if the file exists and is not a directory
        if not path.is_file():
            print("File does not exist")
            return False
        filename = os.path.basename(path)
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)

    def reset_email_alert_info(self):
        """
        Reset the email alert info to default values.
        """
        self.set_message(None)
        self.set_subject(None)
        self.set_environment(None)

    def email_alert_decorator(self, fnc):
        """
        Wrapper function for email alerts. The contents of the email can be set by the user
        using the set_message set_subject functions, and set_environment function.
        If None is passed to any of these functions, the default values will be used.
        """

        def wrapper(*args, **kwargs):
            try:
                return fnc(*args, **kwargs)
            except Exception as e:
                if self.environment is None:
                    self.environment = "Production"
                if self.message is None:
                    self.message = \
                        f"ERROR: {e}\n\
                        DEVICE: {socket.gethostname()}\n\
                        FILE: {os.path.abspath(__file__)}\n\
                        "
                if self.subject is None:
                    self.subject = f"Email alert: Error in: {self.environment}"

                self.send_email(self.subject, self.message)

        return wrapper
