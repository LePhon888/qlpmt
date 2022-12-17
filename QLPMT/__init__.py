from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary
import babel

app = Flask(__name__)
app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/qlpmt?charset=utf8mb4' % quote('le132132')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MEDICAL_REPORT_KEY'] = 'medical_reports'
app.config['MEDICAL_REPORT_MEDICINE_KEY'] = 'medical_report_medicine'
app.config['MEDICAL_REPORT_SAVE_KEY'] = 'medical_report_save'
app.config['MEDICAL_NAME_KEY'] = 'med_name'
cloudinary.config(cloud_name='dekbtaaxy', api_key='691138993619192', api_secret='QN2Nx3mDZy3sMIV0FOfmWFq3ez8')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)

@babel.localeselector
def load_locale():
    return 'vi'
