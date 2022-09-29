import os
from re import search
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
from flask_cors import CORS


from models import *
BOOKS_PER_PAGE = 30


def paginate_books(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * BOOKS_PER_PAGE
    end = start + BOOKS_PER_PAGE
    # or end = page * QUESTIONS_PER_PAGE

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books


def format_items(selection):
    item = [item.format() for item in selection]

    return item


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    Set up CORS. Allow '*' for origins.
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, PUT')

        return response

    @app.route('/books', methods=['GET'])
    def get_books():
        books = Book.query.all()
        current_books = paginate_books(request, books)
        if len(current_books) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "books": current_books,
        })

    @app.route('/books/<int:book_id>', methods=['GET'])
    def get_book_by_id(book_id):

        book = Book.query.filter(
            Book.book_ID == book_id).one_or_none().format()

        if book is None:
            abort(404)

        return jsonify({
            "success": True,
            "book": book,
        })

    @app.route('/books/author', methods=['GET'])
    def get_books_by_author(author):
        books = Book.query.filter(Book.book_author == author).all()
        formatted_books = paginate_books(books)

        if books is None:
            abort(404)

        return jsonify({
            "success": True,
            "result": formatted_books,
            "books": len(books)
        })

    @app.route('/books/publisher', methods=['GET'])
    def get_books_by_publisher(publisher):
        books = Book.query.filter(Book.book_publisher == publisher).all()
        formatted_books = paginate_books(books)

        if books is None:
            abort(404)

        return jsonify({
            "success": True,
            "result": formatted_books,
            "books": len(books)
        })

    @app.route('/books/<int:book_id>', methods=['PUT'])
    def update_book(book_id):
        book = Book.query.filter(
            Book.book_ID == book_id).one_or_none().format()

        if book is None:
            abort(404)

        try:
            body = request.get_json()
            book.title = body.get("title", book.title)
            book.edition = body.get("edition", book.edition)
            book.author = body.get("author", book.author)
            book.publisher = body.get("publisher", book.publisher)
            book.copies = body.get("copies", book.copies)
            book.costs = float(body.get("costs", book.costs))
            book.remarks = body.get("remarks", book.remarks)

            book.update()

            return jsonify(
                {
                    "success": True,
                    # "updated": updated_book.id,
                    "total_books": len(Book.query.all())
                }
            )
        except:
            abort(422)

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(
                Book.id == book_id).one_or_none().format()

            if book is None:
                abort(404)

            book.delete()
            books = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, books)

            return jsonify({
                "success": True,
                "deleted": book_id,
                "current_books": current_books,
                "total_books": len(Book.query.all()),
            })
        except Exception:
            abort(422)

    @app.route("/books", methods=["POST"])
    def create_book():
        body = request.get_json()
        new_title = body.get("title", None)
        new_edition = body.get("edition", None)
        new_author = body.get("author", None)
        new_publisher = body.get("publisher", None)
        new_copies = body.get("copies", None)
        new_costs = body.get("costs", None)
        new_remarks = body.get("edition", None)

        try:
            book = Book(title=new_title, edition=new_edition, author=new_author,
                        publisher=new_publisher, copies=new_copies, costs=new_costs, remarks=new_remarks)
            book.insert()

            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": book.id,
                    "books": current_books,
                    "total_books": len(Book.query.all())
                }
            )
        except:
            abort(422)

    @app.route('/books/borrowed/last_30_days', methods=['GET'])
    def get_books_borrowed_last_30_days():
        books = get_books_borrowed_in_certain_time(db, flag=True)
        if books is None:
            abort(404)

        return jsonify({
            "success": True,
            "books": books,
        })

    @app.route('/books/borrowed/<int:start_date>/<int:end_date>', methods=['GET'])
    def get_books_borrowed_over_time_frame(start_date, end_date):
        books = get_books_borrowed_in_certain_time(db, start_date, end_date)
        if books is None:
            abort(404)

        return jsonify({
            "success": True,
            "books": books,
        })

    @app.route('/books/borrowed/<int:user_id>', methods=['GET'])
    def get_books_borrowed_by_user(user_id):
        books = get_books_borrowed_by_id(user_id, user=True)
        if books is None:
            abort(404)

        return jsonify({
            "success": True,
            "books": books,
        })

    @app.route('/books/borrowed/<int:book_id>', methods=['GET'])
    def get_books_borrowed_by_id(book_id):
        books = get_books_borrowed_by_id(book_id)
        if books is None:
            abort(404)

        return jsonify({
            "success": True,
            "books": books,
        })

    # ERROR HANDLING

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request",
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found",
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed",
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable",
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error",
        }), 500

    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app = create_app()
    app.run(port=port)
