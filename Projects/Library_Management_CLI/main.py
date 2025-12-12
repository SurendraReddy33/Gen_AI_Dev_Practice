from app.models.book import Book
from app.models.student import Student
from app.service.book_service import add_book, update_book, list_books, search_books_by_title, delete_book 
from app.service.student_service import add_student, list_students, delete_students, search_student_by_name, update_student
from app.service.issue_service import issue_book, return_book, list_record_books

def show_menu():
    while True:
        print("\n ---- Library Management ---- ")
        print("1. Add Student")
        print("2. Update Student")
        print("3. List Students")
        print("4. Delete Student")
        print("5. Search Student by name")
        print("6. Add Book")
        print("7. Update Book")
        print("8. List Books")
        print("9. Search Book by title")
        print("10. Delete Book")
        print("11. Issue Book")
        print("12. Return Book")
        print("13. List Issued Books")
        print("0. Exit")

        choice = input("Enter Your choice : ")

        if choice == "1":
            student = Student(
                student_id=input("student ID: "),
                name = input("name: "),
                department = input("department: "),
                year= input("Year: ")
            )
            add_student(student)

        elif choice == "2":
            sid = input("Enter Student ID to Update: ")
            print("Leave Blank to Skip updating a field")
            name = input("New name: ")
            dept = input("New Department: ")
            year = input("New year: ")
            updates = {}
            if name: updates["name"] = name
            if dept: updates["department"] = dept
            if year: updates["year"] = year
            update_student(sid, updates)

        elif choice == "3":
            list_students()

        elif choice == "4":
            student_id = input("Enter student id to delete: ")
            delete_students(student_id)

        elif choice == "5":
            name = input("Enter name to search: ")
            search_student_by_name(name)

        elif choice == "6":
            book = Book(
                book_id=input("Book ID: "),
                title = input("Title: "),
                author = input("Author: "),
                category = input("category: "),
                available=True
            )
            add_book(book)

        elif choice == "7":
            bid = input("Enter Book ID to Update: ")
            print("Leave Blank to Skip updating a field")
            title = input("New Title: ")
            author = input("New Author: ")
            category = input("New Category: ")
            updated_data = {}
            if title: updated_data["title"] = title
            if author: updated_data["author"] = author
            if category: updated_data["category"] = category
            update_book(bid, updated_data)


        elif choice == "8":
            list_books()

        elif choice == "9":
            title = input("Enter book title to search: ")
            search_books_by_title(title)

        elif choice == "10":
            book_id = input("Enter book ID to delete: ")
            delete_book(book_id)

        elif choice == "11":
            sid = input("Student_ID: ")
            bid = input("Book_ID: ")
            issue_book(sid, bid)

        elif choice == "12":
            sid = input("Student_ID: ")
            bid = input("Book_ID: ")
            return_book(sid, bid)

        elif choice == "13":
            list_record_books()

        elif choice == "0":
            print("Exiting Library Management CLI...")
            break

        else:
            print("Invalid choice. please enter a number from 1 to 9: ")

if __name__ == "__main__":
    show_menu()
        