from app import db


class User(db.Model):
    stuid = db.Column(db.String(12), unique=True,
                      nullable=False, primary_key=True)
    stuClass = db.Column(db.String(20), nullable=False)
    stuName = db.Column(db.String(20), unique=True, nullable=False)
    cellphone = db.Column(db.String(11), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.stuName


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return '<Work %r>' % self.type
