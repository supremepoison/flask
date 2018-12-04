from flask import Flask, render_template,request,make_response,redirect

app = Flask(__name__)

@app.route('/')
def fun():
    return render_template('list2.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        #去看login.html模板
        return render_template('login.html')
    else:
        #接受前段请求提交的数据
        username = request.form.get('username','')
        password = request.form.get('password','')
        # 如果用户名是admin并且密码也是admin 去 / 路径
        if username == 'admin' and password == 'admin':

            #登录成功,重定向到 '/'
            return redirect('/')
        else:
                #使用显影对象输出'用户名或密码不正确'
            resp = make_response('用户名或密码不正确')
            return  resp

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        url = request.form['url']
        password = request.form['password']
        return '用户名:%s,email:%s,url:%s,password:%s' % (username,email,url,password)








if __name__ == '__main__':
    app.run(debug=True)