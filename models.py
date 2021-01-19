
from datetime import datetime
from server import login_manager
from flask_login import UserMixin
import queries



@login_manager.user_loader
def load_patient(user_id):
    return queries.select("*", "patient", where="id = {}".format(user_id))


class patient(id, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(20), unique=True, nullable=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    mail = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return ("User('{}', '{}')",self.name,self.mail)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return ("Post('{}', '{}')",self.title,self.date_posted)
