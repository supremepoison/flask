from flask import Flask, request, render_template,redirect
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
    isActive =db.Column(db.Boolean,default=True)
    wife = db.relationship('Wife', backref='user',uselist=False)

    def __init__(self, username, age, email):
        self.username = username
        self.age = age
        self.email = email

    def __repr__(self):
        return '<Users:%r>' % self.username

class Wife(db.Model):
    __tablename__ = 'wife'
    id = db.Column(db.Integer,primary_key=True)
    wname = db.Column(db.String(30))
    #增加对 USers的  一对一的引用关系
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    tname = db.Column(db.String(30), nullable=False)
    tage = db.Column(db.Integer)
    tbirth = db.Column(db.Date)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))

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

    #关系属性和反向引用关系
    #关联属性: course对象中通过哪个属性能够得到对应的所有的teacher对象
    #反向引用: 在teacher对象中通过哪个属性能够得到他对应的Course

    teachers = db.relationship('Teacher',backref='course', lazy='dynamic')

    def __init__(self, cname):
        self.cname = cname

    def __repr__(self):
        return '<Course:%r>' % self.cname


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(30), nullable=False)
    sage = db.Column(db.Integer)
    class_id = db.Column(db.Integer,db.ForeignKey('classes.id'))

    def __init__(self, sname, sage):
        self.sname = sname
        self.sage = sage

    def ___repr__(self):
        return '<Student%r>' % self.sname

class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(30), nullable=False)
    students = db.relationship('Student',backref = 'classes', lazy='dynamic')

    def __init__(self,cname):
        self.cname = cname

    def __repr__(self):
        return '<Classes%r>' % self.cname



# 将创建好的实体类映射回数据库
db.create_all()


@app.route('/01-add')
def add_views():
    # 创建users对象并插入到数据库中
    users = Users('superman', 333, 'I33@123.com')
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
    users = Users.query.filter_by(isActive=True).all()

    return render_template('04-queryall.html',users=users)

@app.route('/05-update',methods=['GET','POST'])
def update_views():


    if request.method == 'GET':
        #接受前段传递过来的参数 id
        id = request.args.get('id')

        #根据id查询出对应的对象
        user = Users.query.filter_by(id=id).first()
        #将查询出来的对象发送到05-update.html中进行显示
        return  render_template('05-update.html',user=user)
    else:
        id = request.form['id']
        name = request.form['uname']
        age = request.form['uage']
        email = request.form['email']

        user = Users.query.filter_by(id=id).first()

        user.username = name
        user.age=age
        user.email=email
        db.session.add(user)

        return redirect('/04-queryall')

@app.route('/06-delete')
def update_users():
    id = request.args['id']
    user = Users.query.filter_by(id=id).first()
    # db.session.delete(user)
    user.isActive = False
    db.session.add(user)
    #将users的isActive的值更改为False来表示删除
    return redirect('/04-queryall')

@app.route('/08-insert')
def insert_views():
    c1 = Course('钢管舞')
    c2 = Course('爵士舞')
    db.session.add(c1)
    db.session.add(c2)
    return 'Insert ok'

@app.route('/09-register-teacher')
def register_teacher():
    # #方案1:关联属性
    # tea1 = Teacher('魏老师',50,'1985-10-01')
    # tea1.course_id = 1
    # db.session.add(tea1)
    # db.session.add(tea1)

    #方案2:通过反向引用属性关联属性
    tea2= Teacher('王老师',45,'1975-10-01')
    #查询id为1的Courese信息
    course = Course.query.filter_by(id=1).first()
    tea2.course = course
    db.session.add(tea2)
    return 'Register Teacher Ok'

@app.route('/10-query')
def query10_views():
    # #通过course对象查询对应所有的teacher们
    # course = Course.query.filter_by(id=1).first()
    # #teachers提供了对应的teacher的查询
    # teachers = course.teachers.all()
    #
    # print('课程名称:'+course.cname)
    # print('对应的老师们:')
    # for tea in teachers:
    #     print('姓名:%s,生日:%s' % (tea.tname,tea.tbirth))

    #通过 teacher 得到对应的course
    tea = Teacher.query.filter_by(id=1).first()
    course = tea.course
    print('教师姓名:%s'% tea.tname)
    print('所教课程:%s'% course.cname)
    return  'Query Ok'




@app.route('/11-register-stu',methods=['GET','POST'])
def register_stu():
    if request.method == 'GET':
        #查询classes表中所有的数据
        list = Classes.query.all()
        return render_template('11-register-stu.html',list=list)
    else:
        name = request.form['name']
        age = request.form['age']
        classes = request.form['class']


        #构建Student对象
        student = Student(name,age)
        student.class_id = classes
        #将对象保存进数据库
        db.session.add(student)
        return redirect('/12-students')

@app.route('/12-students')
def student():
    list = Student.query.all()

    return render_template('12-students.html',list=list)

@app.route('/13-wife')
def wife_users():
    #通过wife找users
    wife = Wife.query.filter_by(id=7).first()
    user = wife.user
    print('Wife:%s' % wife.wname)
    print('User:%s' % user.username)
    return 'query ok '

    #通过users找wife




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
