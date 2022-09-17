from flask import render_template, request, redirect, flash
from app import app, db
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
from app.models import Work
import os
from config import Config


@app.route("/")
def index():
    title = "Flask App"
    return render_template("index.html", title=title)


def allowed_file(filename):
    # 拆解filename，获取后缀并判断是否允许上传

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    workTypes = []
    for i in range(len(Work.query.all())):
        workTypes.append(Work.query.all()[i].type)
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(''.join(lazy_pinyin(file.filename)))
            name = request.form.get("name")
            type = request.form.get("type")
            stuID = request.form.get("stuID")
            title = request.form.get("title")
            suffix = "." + filename.rsplit('.', 1)[1].lower()

            # 调用save函数，传入存储路径作为参数，用os.path.join拼接文件夹和文件名
            try:
                route = Config.UPLOAD_FOLDER + '/' + type
                if not os.path.exists(route):
                    os.mkdir(route)
                file.save(os.path.join(route, filename))
                flash("上传成功", category='success')
            except:
                flash("上传失败", category='danger')

        else:
            flash("上传出现问题，文件名非法", category='danger')

    return render_template("upload.html", workTypes=workTypes)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    workTypes = []
    for i in range(len(Work.query.all())):
        workTypes.append(Work.query.all()[i].type)
    if request.method == 'POST':
        addType = request.form.get("addWorkType")
        delType = request.form.get("delWorkType")
        if addType is not None:
            try:
                work = Work(type=addType)
                db.session.add(work)
                db.session.commit()
                return redirect("/admin")
            except:
                return "出现错误"
        if delType is not None:
            try:
                temp = Work.query.filter_by(type=delType).first()
                db.session.delete(temp)
                db.session.commit()
                return redirect("/admin")
            except:
                return "出现错误"

    return render_template("admin.html", workTypes=workTypes)
