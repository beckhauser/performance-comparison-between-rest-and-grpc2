from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load existing books from JSON file
with open("books.json", "r") as f:
    books = json.load(f)


@app.route("/books", methods=["GET"])
def get_all_books():
    return jsonify(books), 200


@app.route("/books/<string:book_id>", methods=["GET"])
def get_one_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def post_one_book():
    new_book = request.json
    books.append(new_book)
    _update_db()
    return jsonify(new_book), 201


@app.route("/books/list", methods=["POST"])
def post_list_of_books():
    new_books = request.json
    books.extend(new_books)
    _update_db()
    return jsonify(new_books), 201


def _update_db():
    with open("books.json", "w") as f:
        json.dump(books, f, indent=4)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
