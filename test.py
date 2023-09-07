import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_PASSWORD = 'nnfjtvhcampxisou'


# send the email

# Email configuration
sender_email = 'askwesley589@gmail.com'
sender_password = GMAIL_PASSWORD
recipient_email = '23072152@student.uwa.edu.au'
subject = 'test'
message = 'body_t'

# Create a MIMEText object for the email content
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

# SMTP server configuration (for Gmail)
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Establish a connection to the SMTP server
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print('Email sent successfully')

except Exception as e:
    print(f'An error occurred: {str(e)}')

finally:
    # Close the SMTP server connection
    server.quit()