import smtplib


def send_email(to_address, msg_body, subject="",
               FROM="Watering Reminder",
               SERVER="smtp.gmail.com", PORT=465,
               uname="plantbot1000@gmail.com",
               pwd="plantwatering194"):
    """ 
    Will send an email from an account to another with a message.

    Inputs:
        * from_address <str> => The email to send from
        * to_address <str> => The email to send to
        * message <str> => The message contained.

    Outputs:
        <bool> Exit code
    """
    try:
        server = smtplib.SMTP_SSL(SERVER, PORT)
        server.ehlo()
    except:
        print("Something went wrong, with the server set up!")
        return False
            
    try:
        server.login(uname, pwd)
    except smtplib.SMTPAuthenticationError as e:
       print("Couldn't Log in!")
       print(e.message)
       return False

    email_text = """\
From: %s
To: %s
Subject: %s

%s
    """ % (FROM, to_address, subject, msg_body)
    server.sendmail(FROM, to_address, email_text)

