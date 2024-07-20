import grpc
import json
from concurrent import futures
import books_pb2
import books_pb2_grpc


class BookService(books_pb2_grpc.BookServiceServicer):
    def __init__(self):
        with open("books.json", "r") as f:
            self.books = json.load(f)

    def GetAll(self, request, context):
        return books_pb2.GetAllResponse(
            books=[self._json_to_book(book) for book in self.books]
        )

    def GetOne(self, request, context):
        book = next((b for b in self.books if b["id"] == request.id), None)
        if book:
            return books_pb2.GetOneResponse(book=self._json_to_book(book))
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Book not found")
            return books_pb2.GetOneResponse()

    def PostOne(self, request, context):
        new_book = self._book_to_json(request.book)
        self.books.append(new_book)
        self._update_db()
        return books_pb2.PostOneResponse(book=self._json_to_book(new_book))

    def PostList(self, request, context):
        new_books = [self._book_to_json(book) for book in request.books]
        self.books.extend(new_books)
        self._update_db()
        return books_pb2.PostListResponse(
            books=[self._json_to_book(book) for book in new_books]
        )

    def _json_to_book(self, json_book):
        return books_pb2.Book(
            id=json_book["id"],
            title=json_book["title"],
            author=json_book["author"],
            isbn=json_book["isbn"],
            description=json_book["description"],
            price=json_book["price"],
        )

    def _book_to_json(self, book):
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "description": book.description,
            "price": book.price,
        }

    def _update_db(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f, indent=4)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookServiceServicer_to_server(
        BookService(), server
    )  # Corrected this line
    server.add_insecure_port("[::]:50051")
    print("Server running at port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
