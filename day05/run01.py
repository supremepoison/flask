from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import or_
from sqlalchemy import func

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 为app指定数据库的配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/flask'

# 指定当视图执行完毕后,自动提交数据库操作
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 指定每次执行操作时打印原始的SQL语句
# app.config['SQLALCHEMY_ECHO']=True

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

    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email

    def __repr__(self):
        return '<Users:%r>' % self.username


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(30), nullable=False)
    sage = db.Column(db.Integer)

    def __init__(self, sname, sage):
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

    def __init__(self, tname, tage, tbirth):
        self.tname = tname
        self.tage = tage
        self.tbirth = tbirth

    def __repr__(self):
        return '<Teacher%r>' % self.tname


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(30), nullable=False)

    def __int__(self, cname):
        self.cname = cname

    def __recp__(self):
        return '<Course:%r>' % self.cname


# 将创建好的实体类映射回数据库
db.create_all()


@app.route('/01-add')
def add_views():
    # 创建users对象并插入到数据库中
    users = Users('in', 20, 'IN@123.com')
    db.session.add(users)
    db.session.commit()
    return 'Add OK'


@app.route('/02-register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('02-register.html')
    else:
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        users = Users(name, age, email)
        db.session.add(users)
        # db.session.commit()
        return 'Add Ok'


@app.route('/03-query')
def query_views():
    # query=db.session.query(Users,Student)
    # print(query)
    # users = db.session.query(Users).filter(Users.age>30,Users.id>1).all()
    # users = db.session.query(Users).filter(or_(Users.id==1,Users.age>30))
    # users = db.session.query(Users).filter(Users.email.like('%w%')).all()
    # users = db.session.query(Users).filter(Users.id.in_([2,4])).all()
    # users = db.session.query(Users).filter(Users.age.between(30,50)).all()
    # for i in users:
    #     print('%s,%s,%s' % (i.username,i.age,i.email))

    ####################
    # filter_by()#
    ###################

    user = db.session.query(Users).filter_by(id=1).first()



    ###############
    # 查询 users 表中的前两条数据
    ###############
    # users = db.session.query(Users).limit(2).all()

    # 获取users表中过滤前1条数据后剩余的前两条数据
    # users = db.session.query(Users).limit(2).offset(1).all()

    # 按照id列的值降序排序
    # users = db.session.query(Users).order_by('age desc').all()

    #分组查询 - group_by
    # users = db.session.query(Users.age).group_by('age').all()
    # print(users)

    #聚合函数
    # result = db.session.query(func.avg(Users.age)).all()
    # print(result)

    ##########
    #基于Models进行的查询
    #########
    # users = Users.query.all()
    # users = Users.query.filter(Users.id>1).all()
    # users = Users.query.filter_by(id=3).all()



    # for i in users:
    #     print('%s,%s,%s,%s' % (i.id,i.username, i.age, i.email))
    #
    # return '<script>alert("query ok")</script>'

@app.route('/04-queryall')

def queryall():
    users = Users.query.all()

    return render_template('04-queryall.html',users=users)

@app.route('/05-update')
def update_views():
    #接受前段传递过来的参数 id
    id = request.args.get('id')

    #根据id查询出对应的对象
    user = Users.query.filter_by(id=id).first()
    #将查询出来的对象发送到05-update.html中进行显示
    return  render_template('05-update.html',user=user)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
