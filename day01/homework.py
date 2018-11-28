from flask import Flask, render_template

app = Flask(__name__)

@app.route('/homework')
def music():
    str = render_template('01-homework.html',name='绿光',lyrics='宝强',write='乃亮',singer='羽凡')
    return str

if __name__ == ('__main__'):
    app.run(debug=True)