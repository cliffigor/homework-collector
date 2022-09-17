import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 上传的文件夹名称
    UPLOAD_FOLDER = 'files'
    # 上传的文件夹路径
    UPLOAD_PATH = os.path.join(basedir, UPLOAD_FOLDER)
    # 允许上传的文件格式
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg',
                          'gif', 'ppt', 'pptx', 'doc', 'docx', '7z', 'rar', 'zip'}
