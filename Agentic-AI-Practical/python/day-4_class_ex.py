class Employee:
    company = "Zennialpro"
    all_employees = []

    def __init__(self, name, hourly_rate):
        self.name = name
        self._hourly_rate = hourly_rate
        self.hours_worked = 0
        Employee.all_employees.append(self)

    def __str__(self):
        return f"Employee: {self.name}"

    def __repr__(self):
        return f"employee(name='{self.name}', rate={self.hourly_rate})"

    def __len__(self):
        return self.hours_worked

    def __getitem__(self,key):
        return getattr(self, key, None)

    def __setitem__(self,key,value):
        setattr(self,key,value)

    def __eq__(self,other):
        return isinstance(other, Employee) and self.name ==other.name

    def __call__(self):
        print(f"{self.name} works at {self.company}")

    def __del__(self):
        print(f"deleted employee: {self.name}")

    def log_hours(self,hours):
        self.hours_worked += hours

    #lambda to return uppercase name
    get_uppercase = lambda self:self.name.upper()

    #property to calculate salary
    @property
    def salary(self):
        return self.hours_worked * self._hourly_rate

    #setter to safely update rate
    @salary.setter
    def salary(self, new_rate):
        if new_rate >0 :
            self.hourly_rate = new_rate

    #class method for company info
    @classmethod
    def total_employees(cls):
        return len(cls.all_employees)

    #static method for validation
    @staticmethod
    def is_valid_name(name):
        return isinstance(name,str) and len(name.strip()) > 2

    #alternate constructor
    @classmethod
    def from_string(cls, data_str):
        name,rate = data_str.split(":")
        return cls(name.strip(),float(rate))

#command level demo

#create employees using regular and alternate constructors
e1 = Employee("Ameet", 1000)
e2 = Employee.from_string("pavan: 1200")

#log hours
e1.log_hours(5)
e2.log_hours(8)

#access using property
print(e1.salary)

#update hourly rate
e1.salary = 1100
print(e1.salary)

#property like access with __getitem__
print(e1["name"])

#lambda
print(e2.get_uppercase())

#class and static method
print(Employee.total_employees())
print(Employee.is_valid_name("A!"))

#__call__
e1()

#__eq__check
print(e1 == Employee("Ameet", 900))

#Highest paid
highest = max(Employee.all_employees, key= lambda e: e.salary)
print(f"Highest paid: {highest.name}, {highest.salary}")

#__len__
print(len(e2))


# __repr__ and __str__
print(repr(e1))
print(e1)


#del
del e2