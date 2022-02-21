#exec(open('index.py').read())
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_mail_(reciver):
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        mail_content = "Thanks for applying for volunteer role,Admin will send message to you "
        # The mail addresses and password
        sender_address = 'cpatil27112001@gmail.com'
        sender_pass = 'Monu@123'
        receiver_address = reciver
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'About volunteer selection in blood donation camp.'  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')

    except Exception as e:
        print(e)


def send_mail_w_attach(reciver,name):
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        mail_content = "Thanks for give your valuable time as volunteer in our blood donation campain "
        # The mail addresses and password
        sender_address = 'cpatil27112001@gmail.com'
        sender_pass = 'Monu@123'
        receiver_address = reciver
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'About volunteer selection in blood donation camp. Here is your certificate'  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))

        file_path = r"C:\Users\mypc\PycharmProjects\Blood Camp Management\certificate_pdf"
        attach_file_name = '{}.pdf'.format(name)
        attach_file = open(file_path+"\\"+attach_file_name, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream',name=attach_file_name)
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)

        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')

    except Exception as e:
        print(e)

def generate_certificate(name):
    import cv2
    import numpy as np
    certificate_template_image = cv2.imread(r'C:\Users\mypc\PycharmProjects\Blood Camp Management\certificate_vol.jpg')
    m = cv2.putText(certificate_template_image, name, (1166, 1350), cv2.FONT_HERSHEY_SIMPLEX, 4,(0, 0, 250), 13, cv2.LINE_AA)
    cv2.imwrite(r"C:\Users\mypc\PycharmProjects\Blood Camp Management\Certificates\{}.jpg".format(name), certificate_template_image)
    to_pdf(name)
    print("execute")

def to_pdf(name):
    from PIL import Image
    im1 = Image.open(r"C:\Users\mypc\PycharmProjects\Blood Camp Management\Certificates\{}.jpg".format(name))
    pdf1_filename = r"C:\Users\mypc\PycharmProjects\Blood Camp Management\certificate_pdf\{}.pdf".format(name)
    im1.save(pdf1_filename, "PDF", resolution=100.0, save_all=True)

def print_c(name):
    import os
    generate_certificate(name)
    file = r"C:\Users\mypc\PycharmProjects\Blood Camp Management\certificate_pdf\{}.pdf".format(name)
    os.startfile(file,'print')
print_c("Narendra Modi")
#generate_certificate("Ram Charan")
#send_mail_w_attach("2019bcs041@sggs.ac.in")

