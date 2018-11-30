from flask import Flask

'''将当前运行的主程序构建成FLASK应用 以便接受用户的请求'''

app = Flask(__name__)

'''

'''


# @app.route('/')
# def index():
#     return '你好'


# 带参数的路由以及师徒处理函数
# @app.route('/show/<name>')
# def show1(name):
#     return '<h1>传递进来的参数为:%s</h1>' % name
#
#
# # 路径 localhost:5000/show/wang/25
# @app.route('/show/<name>/<age>')
# def show2(name, age):
#     return '姓名:%s 年龄:%s' % (name, age)



@app.route('/index/<num>')
@app.route('/index/<int:num>')
@app.route('/index/<num>/<int:num1>')
@app.route('/index/<num>/<num1>')
def index(num):
    if num.type == int:
        return '%d' %num
    elif num1.type == int:
        return '%d' % num
    else:
        return '1'



if __name__ == '__main__':
    app.run(debug=True)
