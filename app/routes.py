from flask import render_template, request, redirect, flash
from app import app, db
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin
from app.models import Work
import os


@app.route("/")
def index():
    title = "Flask App"
    return render_template("index.html", title=title)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    workTypes = []
    for i in range(len(Work.query.all())):
        workTypes.append(Work.query.all()[i].type)
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

        # flash("add success")
    return render_template("admin.html", workTypes=workTypes)
