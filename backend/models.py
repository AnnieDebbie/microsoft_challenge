import numbers
import os
from sqlalchemy import Column, String, Integer, DateTime, Numeric, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'library')
DB_PATH = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

print(f'pass {DB_PATH}')


# ALTER USER 'user_name'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password123'

# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Book

"""

# book_ID | book_title | book_edition | book_author | book_publisher | book_copies | book_costs | book_remarks


class Book(db.Model):
    __tablename__ = "Books"

    book_ID = Column(Integer, primary_key=True)
    book_title = Column(String(50))
    book_edition = Column(String(50))
    book_author = Column(String(50))
    book_publisher = Column(String(50))
    book_copies = Column(Integer)
    book_costs = Column(Numeric)
    book_remarks = Column(String(50))

    def __init__(self, title, edition, author, publisher, copies, costs, remarks):
        self.book_title = title
        self.book_edition = edition
        self.book_author = author
        self.book_publisher = publisher
        self.book_copies = copies
        self.book_costs = costs
        self.book_remarks = remarks

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "book_id": self.book_ID,
            "title": self.book_title,
            "edition": self.book_edition,
            "author": self.book_author,
            "publisher": self.book_publisher,
            "copies": self.book_copies,
            "costs": float(self.book_costs),
            "remarks": self.book_remarks,
        }


class LibraryStaff(db.Model):
    __tablename__ = "librarystaff"
    staff_ID = Column(Integer, primary_key=True)
    staff_firstname = Column(String(50))
    staff_lastname = Column(String(50))
    staff_mobilenumber = Column(Integer)
    staff_authsalt = Column(String(50))
    staff_category = Column(String(50))

    def __init__(self, staff_id, first_name, last_name, number, category):
        self.staff_ID = staff_id
        self.staff_firstname = first_name
        self.staff_lastname = last_name
        self.staff_mobilenumber = number
        self.staff_category = category

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "staff_id": self.staff_ID,
            "first_name": self.staff_firstname,
            "last_name": self.staff_lastname,
            "number": self.staff_mobilenumber,
            "category": self.staff_category,
        }


class Member(db.Model):
    __tablename__ = "members"
    member_ID = Column(Integer, primary_key=True)
    member_firstname = Column(String(50))
    member_lastname = Column(String(50))
    member_dateofbirth = Column(DateTime)
    member_gender = Column(String(50))
    member_mobile = Column(String(50))
    member_email = Column(String(50))

    def __init__(self, member_id, first_name, last_name, date_of_birth, gender, mobile, email):
        self.member_ID = member_id
        self.member_firstname = first_name
        self.member_lastname = last_name
        self.member_dateofbirth = date_of_birth
        self.member_gender = gender
        self.member_mobile = mobile
        self.member_email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "staff_id": self.member_ID,
            "first_name": self.member_firstname,
            "last_name": self.member_lastname,
            "date_of_birth": self.member_dateofbirth,
            "number": self.member_mobile,
            "email": self.member_email,

        }