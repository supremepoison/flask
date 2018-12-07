from flask import Flask, request, session, make_response, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/flask'
db = SQLAlchemy(app)
app.config['SECRET_KEY']='qwertyuiop'

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(30), unique=True, nullable=False)
    lpwd = db.Column(db.String(30), nullable=False)
    uname = db.Column(db.String(30), unique=True, nullable=False)


db.create_all()

@app.route('/01-logout')
def logout():
    resp = redirect('/01-index')
    if 'id' in session and 'lname' in session:
        del session['id']
        del session['lname']
    if 'id' in request.cookies and 'lname' in request.cookies:
        resp.delete_cookie('id')
        resp.delete_cookie('lname')
    return resp

@app.route('/01-index')
def index():
    if 'id' in session and 'lname' in session:
        lname =session['lname']
        return render_template('01-index.html',lname=lname)
    else:
        if 'id' in request.cookies and 'lname' in request.cookies:
            id = request.cookies['id']
            lname = request.cookies['lname']
            session['id'] = id
            session['lname'] = lname
            return  render_template('01-index.html',lname=lname)
        else:
            return  render_template('01-index.html')

@app.route('/01-login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        # return render_template('01-login.html')
            if 'id' in session and 'lname' in session:
                #已经成功刚登陆过
                # return '欢迎来到首页'
                return redirect('/01-index')
            else:
                #判断cookies中登录信息
                if 'id' in request.cookies and 'lname' in request.cookies:
                    #cookies中有登录信息
                    id = request.cookies['id']
                    lname = request.cookies['lname']
                    session['id'] = id
                    session['lname'] = lname
                    # return '欢迎来到首页'
                    return redirect('/01-index')
                else:
                    #cookie中也没有登录信息
                    return render_template('01-login.html')


    else:
        # 处理post请求
        # 接受前段传来数据并验证是否成功
        name = request.form['name']
        pwd = request.form['pwd']
        cookie = request.form.get('box')
        login = Login.query.filter(Login.lname == name, Login.lpwd == pwd).first()
        if login:
            #登录成功

            session['lname'] = name
            session['id'] = login.id
            #创建响应对象
            resp=redirect('/01-index')

            #判断是否将数据存入cookie
            if cookie == 'cookie':
                resp.set_cookie('lname',name,3600*24*365)
                resp.set_cookie('id',str(login.id),3600*24*365)

            return resp


        else:
            #登录失败
            errMsg='用户名或密码不正确'
            return render_template('01-login.html',errMsg=errMsg)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
