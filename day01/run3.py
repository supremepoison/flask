from flask import Flask, render_template

app = Flask(__name__)

@app.route('/01-temp')
def temp():
    # 渲染01-temp.html模板并响应给客户端
    str = render_template('01-temp.html',name='xiaoxixi',age =25)
    print(str)
    return str

if __name__ == '__main__':
    app.run(debug=True)


