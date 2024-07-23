import json


class Book:
    def __init__(self, book_id, name, author, amount):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.amount = amount

class Member:
    def __init__(self, member_id, name, subscription_time):
        self.member_id = member_id
        self.name = name
        self.subscription_time = subscription_time

class BorrowedBook:
    def __init__(self, book_id, member_id, book_name, borrowed_date, return_date):
        self.book_id = book_id
        self.member_id = member_id
        self.book_name = book_name
        self.borrowed_date = borrowed_date
        self.return_date = return_date

class Library:
    def __init__(self, books_file, members_file, borrowed_file):
        self.books_file = books_file
        self.members_file = members_file
        self.borrowed_file = borrowed_file

    def load_data(self, file_name):
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return {"books": [], "members": [], "borrowed": []}

    def save_data(self, file_name, data):
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)

    def add_book(self):
        books_data = self.load_data(self.books_file)
        count_time = int(input("How many books you want to add: "))
        count = 1

        while count <= count_time:
            name = input("Enter the name of the book: ")
            author = input("Enter the author of the book: ")
            book_id = input("Enter the ID of the book: ")
            amount = input("Enter the amount of the book: ")

            book = Book(book_id, name, author, int(amount))
            books_data["books"].append({"id": book_id, "name": name, "author": author, "amount": int(amount)})
            count += 1

        self.save_data(self.books_file, books_data)

    def remove_book(self):
        book_id = input("Enter the ID of the book you want to remove: ")
        books_data = self.load_data(self.books_file)
        updated_books = [book for book in books_data["books"] if book['id'] != book_id]
        books_data["books"] = updated_books
        self.save_data(self.books_file, books_data)

    def borrow_book(self):
        book_id = input("Enter the ID of the book you want to borrow: ")
        member_id = input("Enter your member ID: ")
        borrowed_date = input("Enter the borrowed date of the book (YYYY-MM-DD): ")
        return_date = input("Enter the return date of the book (YYYY-MM-DD): ")

        books_data = self.load_data(self.books_file)
        members_data = self.load_data(self.members_file)
        borrowed_data = self.load_data(self.borrowed_file)

        for book in books_data["books"]:
            if book["id"] == book_id:
                for member in members_data["members"]:
                    if member["id"] == member_id:
                        if book["amount"] > 0:
                            book["amount"] -= 1
                            self.save_data(self.books_file, books_data)
                            borrowed_data["borrowed"].append(BorrowedBook(book_id, member_id, book["name"], borrowed_date, return_date))
                            self.save_data(self.borrowed_file, borrowed_data)
                            print("Book borrowed successfully.")
                        else:
                            print("No more copies of this book available.")
                            return
                else:
                    print("Member not found!")
                    return
        else:
            print("Book not found.")

    def is_date_expired(self, date_str, current_date):
        date_parts = date_str.split("-")
        current_date_parts = current_date.split("-")

        for i in range(3):
            if int(date_parts[i]) < int(current_date_parts[i]):
                return True
            elif int(date_parts[i]) > int(current_date_parts[i]):
                return False

        return False

    def renew_borrowed(self):
        borrowed_data = self.load_data(self.borrowed_file)
        current_date = input("Enter the current date (YYYY-MM-DD): ")
        borrowed_id = input("Enter the ID of the borrowed book: ")

        for item in borrowed_data["borrowed"]:
            if item["borrow_book_id"] == borrowed_id:
                if self.is_date_expired(item["return_time"], current_date):
                    new_return_time = input("Enter new return time of the borrowed book (YYYY-MM-DD): ")
                    item["return_time"] = new_return_time
                    print(f"Borrowed time renewed for item {borrowed_id} successfully.")
                    self.save_data(self.borrowed_file, borrowed_data)
                    return
                else:
                    print("Borrowed time has not expired yet.")
                    return
        else:
            print("Borrowed book not found.")

    def add_member(self):
        members_data = self.load_data(self.members_file)
        count_time = int(input("How many members you want to add: "))
        count = 1

        while count <= count_time:
            name = input("Enter the name of the member: ")
            member_id = input("Enter the ID of the member: ")
            subscription_time = input("Enter the subscription time of the member (YYYY-MM-DD): ")

            member = Member(member_id, name, subscription_time)
            members_data["members"].append({"id": member_id, "name": name, "subscription_time": subscription_time})
            count += 1

        self.save_data(self.members_file, members_data)

    def remove_expired_members(self):
        members_data = self.load_data(self.members_file)
        current_date = input("Enter the current date in the format YYYY-MM-DD: ")

        updated_members = []
        for member in members_data["members"]:
            if self.is_subscription_expired(member["subscription_time"], current_date):
                updated_members.append(member)
            else:
                print("There is no member with an expired account right now.")

        members_data["members"] = updated_members
        self.save_data(self.members_file, members_data)

    def is_subscription_expired(self, subscription_time, current_date):
        sub_year, sub_month, sub_day = map(int, subscription_time.split("-"))
        cur_year, cur_month, cur_day = map(int, current_date.split("-"))

        if cur_year > sub_year or (cur_year == sub_year and (cur_month > sub_month or (cur_month == sub_month and cur_day > sub_day))):
            return True

        return False

    def renew_subscription(self):
        members_data = self.load_data(self.members_file)
        member_id = input("Enter member's ID: ")
        new_subscription_time = input("Enter updated subscription: ")

        for member in members_data["members"]:
            if member["id"] == member_id:
                member["subscription_time"] = new_subscription_time
                print(f"Subscription renewed for member {member['id']} successfully.")

        self.save_data(self.members_file, members_data)
