from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///from data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80))
    author = db.Column(db.String(120))
    publisher = db.Column(db.string(40))



@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'id': book.id, 'name' : book.book_name, 'author' : book.author, 'publisher' : book.publisher}
        output.append(book_data)
    return{"books": output}

@app.route('/books/<id>')
def find_books(id):
    book = Book.query.get_or_404(id)
    return{"id": book.id, 'name': book.book_name}

@app.route('books', methods=['POST'])
def add_book():
    book = Book(id=request.json['id'], book_name=request.json['name'])
    db.session.add(book)
    db.session.commit
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_drink(id):
    book = Book.query.get(id)
    if book is None:
        return {"404"}
    db.session.delete(book)
    db.session.commit()
    return 'Successful'

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "404"}, 404
    book.name = request.json['name']
    book.description = request.json['description']
    db.session.commit()
    return {'id': book.id, 'name': book.name, 'description': book.description}