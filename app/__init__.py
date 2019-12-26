from flask import Flask
from config import Config
from flask_mail import Mail,Message
app = Flask(__name__)
app.config.from_object(Config)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'edh.ncp12@gmail.com'
app.config['MAIL_PASSWORD'] = 'Edh12345@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER']='edh.ncp12@gmail.com'
from app import routes
