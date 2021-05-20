from twilio.rest import Client
import random
from flask_mail import Mail, Message
from flask import app,Flask
from twilio.rest import Client
import random


account_sid = 'ACea19680da775b5e8e1cb3b5ee392e020'
auth_token = '93627f8737efec41335842697b0b239b'
client = Client(account_sid, auth_token)

smsotp = random.randint(10000, 99999)


def sendPhoneOtp(number):
    message = client.messages \
                    .create(
                        body="Your Hospicare Phone Number verification Code is " + smsotp + " .Please Do Not Share",
                        from_='+15035361091',
                        to=number
                    )
    return smsotp
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '15b9d84efa3b80'
app.config['MAIL_PASSWORD'] = 'd318c0bfeeb11f'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


mailotp = random.randint(10000, 99999)

def sendMail(email):
   msg = Message('Hospicare', sender = '127036637c-54a7b5@inbox.mailtrap.io', recipients = [email])
   msg.body = "Your Hospicare Email verification Code is " + mailotp + " .Please Do Not Share"
   mail.send(msg)
   return mailotp