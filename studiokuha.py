from flask import Flask, render_template, url_for, request
from textblob import TextBlob
from flask_mail import Mail, Message
import os

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL'],
    "MAIL_PASSWORD": os.environ['MAILPASS']
}

app.config.update(mail_settings)
mail = Mail(app)

def great(name):
    return f'''
Dear {name}

We are glad you loved our service and will strive to keep up the performance

Regards
Studio Kuha

This is an auto-generated response. Please do not reply to it
'''

def good(name):
    return f'''
Dear {name}

We are glad you liked our service and we will try our best to improve

Regards
Studio Kuha

This is an auto-generated response. Please do not reply to it
'''

def bad(name):
    return f'''
Dear {name}

We are sorry we couldn't satisfy you. We will strive to improve our services in the future

Regards
Studio Kuha

This is an auto-generated response. Please do not reply to it
'''

def worst(name):
    return f'''
Dear {name}

We are deeply sorry we couldn't satisfy you. We will strive to improve our services in the future. For further clarifications, kindly contact Manisha Katti(+91 98453 28839) or mkstudiokuha@gmail.com.

Regards
Studio Kuha

This is an auto-generated response. Please do not reply to it
'''

def messageGen(name, service):
    return f'''
Dear {name}

Thank you for contacting us about {service}. We will look into your query and get back to you shortly.

Regards
Studio Kuha

This is an auto-generated response. Please do not reply to it
'''

def toMeGen(name, email, phNum, service, message):
    return f'''
Received Form Response

Name: {name}
E-Mail: {email}
Contact Number: {phNum}
Service: {service}
Message:
{message}'''

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=["GET",'POST'])
def contact():
    m = ""
    if request.method == "POST":
        data = request.form
        name = data['name']
        email = data['email']
        phNum = data['phNum']
        service = data['service']
        message = data['message']
        if service=="Feedback":
            replySubject = "Thank you for your valuable feedback"
            messageAnalysis = TextBlob(message)
            if messageAnalysis.sentiment.polarity > 0.5:
                replyMessage = great(name)
            elif messageAnalysis.sentiment.polarity <= 0.5 and messageAnalysis.sentiment.polarity > 0:
                replyMessage = good(name)
            elif messageAnalysis.sentiment.polarity <= 0 and messageAnalysis.sentiment.polarity > -0.5:
                replyMessage = bad(name)
            else:
                replyMessage = worst(name)
            # print(messageAnalysis.sentiment.polarity)
            # return str(replyMessage)
        elif service != "Other Service":
            replySubject = f"Thank you for contacting us"
            replyMessage = messageGen(name, service)
            # return replyMessage
        else:
            replySubject = f"Thank you for contacting us"
            replyMessage = messageGen(name, "Miscellaneous Services")
        toSender = Message(subject=replySubject,
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=[email],
                        body=replyMessage)
        mail.send(toSender)
        toMe = Message(subject="Website Form Response",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=['mkstudiokuha@gmail.com'],
                        body=toMeGen(name, email, phNum, service, message))
        mail.send(toMe)
        m = "Message Sent Successfully"
    return render_template('contact.html', message=m)

@app.route("/comingsoon") #coming soon page
def new():
    return render_template("studiokuha.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)