# Import SMTP Library
import smtplib
import ssl

# Import email modules
from email.message import EmailMessage

# SMTP Server Configuration
server = 'smtp.gmail.com'
port = 587
user = 'yourname@gmail.com'
password = 'password'  # Replace with your actual password or app-specific password.

# Sender and Receiver
sender = 'yourname@gmail.com'
receivers = ['receiver@gmail.com']

# Message
message = EmailMessage()
message['From'] = sender
message['To'] = ', '.join(receivers)  # Join list of recipients into a single string
message['Subject'] = 'Welcome'
message.set_content('Welcome Guest !!', subtype='html')

# Create SSL context
context = ssl.create_default_context()

# Send email
try:
    smtpObj = smtplib.SMTP(server, port)
    smtpObj.ehlo()  # Identify yourself to the server
    smtpObj.starttls(context=context)  # Secure the connection
    smtpObj.ehlo()  # Re-identify as encrypted connection
    smtpObj.login(user, password)  # Log in
    smtpObj.send_message(message)  # Send email
    print("Email sent successfully.")
except smtplib.SMTPException as exc:
    print("Error sending email:", exc)
finally:
    try:
        smtpObj.quit()  # Close the connection
    except NameError:
        print("SMTP object not initialized. Unable to close the connection.")
