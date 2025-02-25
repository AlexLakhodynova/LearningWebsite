from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import flask_login
db = SQLAlchemy()
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(15), unique = True)
    user_name = db.Column(db.String(15))
    password = db.Column(db.String(10))
    points = db.Column(db.Integer)
    total_user_correct_answers = db.Column(db.Integer)
    total_possible_correct_answers = db.Column(db.Integer)
    task_date = db.Column(db.String(1000))

    def __init__(self, login, password, user_name):
        self.login = login
        self.user_name = user_name
        self.password = password
        self.points = 0
        self.total_user_correct_answers = 0
        self.total_possible_correct_answers = 0
        self.task_date = ''

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25))
    title = db.Column(db.String())
    text = db.Column(db.String())
    userid = db.Column(db.String())
    def __init__(self,name, title, text, userid):
        self.name = name
        self.title = title
        self.text = text
        self.userid = userid
class Devise:
    def __init__(self, description, languageDevise):
        self.description = description
        self.languageDevise = languageDevise
        self.color = ""
        self.answer = ""



def give_points(user_id, total_points, points):
    user = User.query.filter_by(id=user_id).first()
    total_user_correct_answers = user.total_user_correct_answers
    total_possible_correct_answers = user.total_possible_correct_answers
    user.total_user_correct_answers = total_user_correct_answers + points
    user.total_possible_correct_answers = total_possible_correct_answers + total_points
    db.session.add(user)
    db.session.commit()

def get_points(user_id):
    user = User.query.filter_by(id=user_id).first()
    total_user_correct_answers = user.total_user_correct_answers
    total_possible_correct_answers = user.total_possible_correct_answers
    return total_user_correct_answers, total_possible_correct_answers


def total_points(user_id, points):
    user = User.query.filter_by(id=user_id).first()
    total_points = user.points
    user.points =  total_points + points
    db.session.add(user)
    db.session.commit()

def reset_points(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.total_user_correct_answers = 0
    user.total_possible_correct_answers = 0
    db.session.add(user)
    db.session.commit()
