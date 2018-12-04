import datetime

from flask import Flask, request, render_template
import os

app = Flask(__name__)


@app.route('/01-file', methods=['GET', 'POST'])
def file_views():
    if request.method == 'GET':
        return render_template('01-file.html')
    else:
        # 处理的上传的文件
        # 1.得到上传的文件
        f = request.files['uimg']
        # # 2.将文件保存到指定的目录处
        # f.save('static/' + f.filename)
        #
        # 3.将文件保存进指定的目录[绝对路径]
        # 获取当前文件的所在目录
        basedir = os.path.dirname(__file__)
        # print('当前文件所在目录的绝对路径:'+basedir)
        ftime =datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        print(ftime)
        #获取文件的扩展名
        ext = f.filename.split('.')[1]
        print(ext)
        filename = ftime + '.' + ext
        path = os.path.join(basedir,'static',filename)
        f.save(path)
        return 'save ok'


if __name__ == '__main__':
    app.run(debug=True)
