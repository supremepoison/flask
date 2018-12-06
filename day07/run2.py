from flask import Flask, make_response, request, render_template, session

app = Flask(__name__)
app.config['SECRET_KEY']='qwertyuiop'

@app.route('/01-setCookie')
def setCookie():
    resp=make_response('保存cookie成功')
    #保存 uname 进 cookie,值为 wangwc
    resp.set_cookie('uname','wangwc',3600)
    return resp

@app.route('/02-getCookie')
def getCookie():
    print(request.cookies)
    uname = request.cookies.get('uname')
    return 'uname的值为:%s' % uname

@app.route('/03-del')
def delete():
     resp = make_response('删除成功')
     resp.delete_cookie('name')
     return resp
     
@app.route('/03-login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        if request.cookies.get('name'):
            name = request.cookies.get('name')
            return '欢迎%s回来' % name
        else:
            return render_template('03-login.html')

    else:
        name = request.form['name']
        pwd = request.form['pwd']
        cookie = request.form.get('box')
        if name == 'admin' and pwd == 'admin' :
            resp=make_response('登陆成功')
            if 'cookie' == cookie:
                resp.set_cookie('name', 'admin', 3600 * 24 * 365)
            return resp
        else:
            return '用户不存在'

@app.route('/04-setSession')
def setSession():
    session['uname'] = 'Tarena'
    return '保存session成功'

@app.route('/05-getSession')
def getSession():
    if 'uname' in session:
        uname = session['uname']
        return  'uname:' + uname
    else:
        return 'No relative data in session'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')