from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 为app指定数据库的配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/flask'

# 创建SQLAlchemy 的数据库是实例
db = SQLAlchemy(app)


# 创建一个模型类- Users,映射到数据库叫 users 表
# 创建字段 id, 主键, 自增
# 创建字段 username ,长度为80的字符串,不允许为空,值要唯一
# 创建字段 age,整数
# 创建字段 email,长度为120的字符串,必须唯一
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique=True)

    def __init__(self,username,age,email):
        self.username=username
        self.age=age
        self.email=email

    def __repr__(self):
        return '<Users:%r>' % self.username


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(30), nullable=False)
    sage = db.Column(db.Integer)

    def __init__(self,sname,sage):
        self.sname = sname
        self.sage = sage

    def ___repr__(self):
        return '<Student%r>' % self.sname


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(30), nullable=False)
    tage = db.Column(db.Integer)
    tbirth = db.Column(db.Date)

    def __init__(self,tname,tage,tbirth):
        self.tname=tname
        self.tage=tage
        self.tbirth=tbirth

    def __repr__(self):
        return '<Teacher%r>' % self.tname


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(30), nullable=False)

    def __int__(self,cname):
        self.cname=cname

    def __recp__(self):
        return '<Course:%r>' % self.cname


# 将创建好的实体类映射回数据库
db.create_all()


@app.route('/')
def index():
    print(db)
    return '创建成功'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
