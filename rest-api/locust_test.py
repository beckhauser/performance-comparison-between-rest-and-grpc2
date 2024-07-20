import json
from locust import HttpUser, task, between
import random
import string
import time


class BookApiUser(HttpUser):
    wait_time = between(1, 1)
    host = "http://localhost:5000"  # Update this to the correct host and port

    # @task
    # def get_all_books(self):
    #     self.client.get("/books")

    @task(1)
    def get_one_book(self):
        start_time = time.time()
        book_id = "0"
        with self.client.get(f"/books/{book_id}", catch_response=True) as response:
            total_time = int((time.time() - start_time) * 1000)
            status_code = response.status_code

    # @task
    # def post_one_book(self):
    #     new_book = {
    #         "id": "".join(random.choice(string.ascii_letters) for i in range(5)),
    #         "title": "A random book",
    #         "author": "Random Author",
    #         "isbn": "123-456-789",
    #         "description": "A very random book",
    #         "price": "9.99",
    #     }
    #     self.client.post("/books", json=new_book)

    # @task
    # def post_list_of_books(self):
    #     new_books = [
    #         {
    #             "id": "".join(random.choice(string.ascii_letters) for i in range(5)),
    #             "title": "Another random book",
    #             "author": "Another Random Author",
    #             "isbn": "987-654-321",
    #             "description": "Another very random book",
    #             "price": "19.99",
    #         },
    #         {
    #             "id": "".join(random.choice(string.ascii_letters) for i in range(5)),
    #             "title": "Yet Another random book",
    #             "author": "Yet Another Random Author",
    #             "isbn": "456-123-789",
    #             "description": "Yet Another very random book",
    #             "price": "29.99",
    #         },
    #     ]
    #     self.client.post("/books/list", json=new_books)
