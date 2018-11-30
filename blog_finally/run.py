from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def fun():
    return render_template('list2.html')




if __name__ == '__main__':
    app.run(debug=True)