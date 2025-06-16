from services import Employee, Department, Role

def menu():
    while True:
        print("\n --------EMPLOYEE SYSTEM---------")
        print("1. Add Department")
        print("2. List Departments")
        print("3. Add Roles")
        print("4. List Roles")
        print("5. Add Employee")
        print("6. List Employees")
        print("7. Delete Employee")
        print("0. Exit")

        choice = input("Enter your choice : ")

        if choice == "1":
            Department.add_department()
        elif choice == "2":
            Department.list_departments()
        elif choice == "3":
            Role.add_role()
        elif choice == "4":
            Role.list_roles()
        elif choice == "5":
            Employee.add_employee()
        elif choice == "6":
            Employee.list_employees()
        elif choice == "7":
            Employee.delete_employee()
        elif choice == "0":
            print("\033[92mExiting... Bye\033[0m")
        else:
            print("\033[91mInvalid choice\033[0m")

            
if __name__ == "__main__":
    menu()