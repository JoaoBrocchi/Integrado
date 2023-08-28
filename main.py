from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy, session

app = Flask(__name__)
app.app_context().push()
##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'



all_books = db.session.query(Book).all()



@app.route('/')
def home():
    global all_books
    return render_template("index.html",books=all_books)

@app.route("/add",methods=["POST","GET"])
def add():
    Book_Name = request.form.get("Book_Name")
    Author_Name = request.form.get("Author_Name")
    rating = request.form.get("rating")
    if request.method == "POST":
        with app.app_context():
            db.create_all()
            new_book = Book(title=Book_Name, author=Author_Name, rating=int(rating))
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template("add.html")

if __name__ == "__main__":
    app.run(debug=True)

