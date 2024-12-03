import json
import os

from faker import Faker

faker = Faker()



class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Publication year: {self.year}"


class BookManager:
    def __init__(self):
        self.books = []

    @staticmethod
    def custom_serializer(obj):
        if isinstance(obj, Book):
            return {
                "Title": obj.title,
                "Author": obj.author,
                "Publication Year": obj.year
            }
        return obj

    @staticmethod
    def custom_deserializer(json_data):
        return Book(json_data["Title"], json_data["Author"], json_data["Publication Year"])

    @staticmethod
    def write_data(book_list):
        with open("books.json", "w") as json_file:
            json.dump(book_list, json_file, default=BookManager.custom_serializer, indent=4)

    @staticmethod
    def read_data():
        with open("books.json", "r") as json_file:
            book_data = json.load(json_file, object_hook=BookManager.custom_deserializer)
            return book_data

    def add_book(self, title, author, year):
        self.books = self.read_data()
        self.books.append(Book(title, author.capitalize(), year))
        self.write_data(self.books)
        print(f"Book with the Title '{title}' has been added successfully.")

    def display_all_books(self):
        self.books = self.read_data()
        if self.books:
            print("Full book list:")
            for book in self.books:
                print(book)

    def search_book_by_title(self, book_name):
        self.books = self.read_data()
        found_book = [book for book in self.books if book.title.lower() == book_name.lower()]

        if found_book:
            print(f"Search result for books titled '{book_name}': ")
            for book in found_book:
                print(book)
        else:
            print(f"No books found with the title '{book_name}'")

    @staticmethod
    def json_is_empty(json_file):
        return not os.path.exists(json_file) or os.path.getsize(json_file) == 0

    def create_fake_books(self, num_books):
        self.books = []
        for _ in range(num_books):
            title = faker.catch_phrase()
            author = faker.name()
            publication_year = int(faker.year())
            self.books.append(Book(title, author, publication_year))
        self.write_data(self.books)

def main():

    manager = BookManager()

    if manager.json_is_empty("books.json"):
        manager.create_fake_books(10)

    while True:
        print("\nMenu:")
        print("1. Add New Book")
        print("2. View All Books")
        print("3. Search Book by Title")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of the book: ")

            while True:
                try:
                    author = input("Enter the author of the book: ").capitalize()
                    if not author.replace(" ", "").isalpha():
                        raise ValueError("Invalid author. Author can only contain letters and spaces.")
                    break
                except ValueError as e:
                    print(str(e))

            while True:
                try:
                    publication_year = int(input("Enter the publication year of the book: "))
                    if not (publication_year <= 2025):
                        raise ValueError("Invalid publication year. Publication year can't be 2025 or higher")
                    break
                except ValueError as e:
                    print(str(e))

            books = manager.read_data()
            found_book = [book for book in books
                          if book.title.lower() == title.lower() and book.author.lower() == author.lower()]

            if found_book:
                print(f"There is already a book named '{found_book[0]}'")
            else:
                manager.add_book(title, author, publication_year)


        elif choice == "2":
            manager.display_all_books()

        elif choice == "3":
            title = input("Enter the title to search: ")
            manager.search_book_by_title(title)

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == '__main__':
    main()
