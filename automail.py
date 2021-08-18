import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
from datetime import datetime 
fromaddr = "kchakravarthi02@gmail.com"
toaddr = "kalyanchakri100@gmail.com"
def au():
# instance of MIMEMultipart
    msg = MIMEMultipart()

# storing the senders email address
    msg['From'] = fromaddr

# storing the receivers email address
    msg['To'] = toaddr
    now = datetime.now() # current date and time
    date_string = now.strftime("%y_%m_%d")

# storing the subject
    msg['Subject'] ="Attendence"

# string to store the body of the mail
    body = "Welcome To Royalev From Daiots Arc AI Smart Attendance!!!!!!!!!!"
# attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    

# open the file to be sent
    filename = f'Attendance/Attendence_{date_string}.csv'
    attachment = open(f'Attendance/Attendence_{date_string}.csv',"rb")

# instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

# To change the payload into encoded form
    p.set_payload((attachment).read())

# encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# attach the instance 'p' to instance 'msg'
    msg.attach(p)

# creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
    s.starttls()

# Authentication
    s.login(fromaddr, "kalyan100")

# Converts the Multipart msg into a string
    text = msg.as_string()

# sending the mail
    s.sendmail(fromaddr, toaddr, text)

# terminating the session
    s.quit()

