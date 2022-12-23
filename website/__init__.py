from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
import MySQLdb.cursors
from .models import User
# initializing...basic syntax
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'njoro'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'mosh'
    # cursor= u.mydb.cursor()
    mysql = MySQL(app)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM sign_up WHERE id=%s',(id,))
        
        user = cur.fetchone()
        return User(user)

    return app