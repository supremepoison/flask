from flask import Flask, render_template
from flask import request


app = Flask(__name__,template_folder='muban',static_folder='sta',static_url_path='/s')

@app.route('/01-parent')
def parent():
    return render_template('01-parent.html')

@app.route('/02-child')
def child():
    return render_template('02-child.html')

@app.route('/03-request')
def request_views():
    #print(dir(request))
    #获取请求方式(协议)
    scheme = request.scheme
    #获取请求方式
    method = request.method
    #获取get请求的数据
    args = request.args
    #获取post请求数据
    form = request.form
    #获取cookies中的数据
    cookies = request.cookies
    #获取所有的请求消息头
    headers = request.headers
    #获取请求资源的路径
    path = request.path
    #获取请求资源的路径(参数)
    full_path = request.full_path
    #获取请求 的路径
    url = request.url
    #获取具体的请求消息头
    referer = request.headers.get('Referer','/')
    ua = request.headers['User-Agent']

    return render_template('03-request.html',params=locals())

@app.route('/04-form')
def form():
    return render_template('04-form.html')

@app.route('/05-get',methods=['POST','GET'])
def get_views():
    # 接受04-form.html 传递过来的数据
    if request.method == 'GET':
        uname = request.args.get('uname','')
        upwd = request.args.get('upwd','')
    if request.method == 'POST':
        uname = request.form.get('uname','')
        upwd = request.form.get('upwd','')
    return '<h2>用户名: %s , 密码 : %s </h2>' %(uname,upwd)

@app.route('/06-form',methods=['POST','GET'])
def get_form():
    if request.method == 'GET':

        return  render_template('06-form.html')
    if request.method == 'POST':
        uname =request.form.get('uname','')
        upwd = request.form.get('upwd','')
        email =request.form.get('email','')
        rname = request.form.get('rname','')
        print('uname:%s,upwd:%s,email:%s,rname:%s' % (uname, upwd, email, rname))
        return 'successful'





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run(debug=True,port=1234)