from flask import Flask
from flask import url_for

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/<int:num>')
@app.route('/index/<int:num>')
def index(num=None):
    if num is None:
        return '1'

    else:
        return '%d' % num


@app.route('/method',methods = ['post','get'])
def method():
    return '这是使用post/get请求提交过来的'

@app.route('/admin/login/form/show')
def show():
    return '这是admin/login/form/show'

@app.route('/url')
def url():
    url = url_for('show')

    return "<a href='%s'>去往show</a>" % url

@app.route('/admin/login/form/show/<name>/<age>')
def show1(name,age):
    return '参数为name%s, age%s' %(name,age)

@app.route('/url1')
def url1():
    url = url_for('show1',name='你好',age='222')

    return "<a href='%s'>去往show1</a>" % url

if __name__ == '__main__':
    app.run(debug=True,port=1234,)
