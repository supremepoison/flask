from flask import Flask, render_template

app = Flask(__name__)

@app.route('/01-parent')
def parent():
    return render_template('01-parent.html')

@app.route('/02-child')
def child():
    return render_template('02-child.html')



if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')