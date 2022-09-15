from config import Config
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

app.config.from_object(Config)


@app.route("/")
def index():
    title = "Flask App"
    return render_template("index.html", title=title)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return '上传失败，文件名为空'
        if file and app.config.allowed_file(file.filename):
            filename = secure_filename(''.join(lazy_pinyin(file.filename)))
            name = request.form.get("name")
            type = request.form.get("type")
            stuID = request.form.get("stuID")
            title = request.form.get("title")
            suffix = "." + filename.rsplit('.', 1)[1].lower()
            if type == "形势与政策":
                filename = stuID + '-' + name + '-' + title + suffix
            elif type == "职业发展与就业指导2":
                filename = '2019计算机' + '-' + name + '-' + '就业指导2期末作业' + suffix
            # 最关键的代码，调用save函数，传入存储路径作为参数，用os.path.join拼接文件夹和文件名
            try:
                route = app.config['UPLOAD_FOLDER'] + '/' + type
                print(route)
                file.save(os.path.join(route, filename))
                return '上传成功'
            except:
                return '上传失败，请联系管理员'
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)
