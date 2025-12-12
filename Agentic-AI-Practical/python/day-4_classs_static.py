class Employee:
    company = "ZennialPro"

    def __init__(self, name, hourly_rate):
        self.name = name
        self.hourly_rate = hourly_rate
        self._hours_worked = 0

    def log_hours(self, hours):
        self._hours_worked += hours

    @property
    def total_salary(self):
        return self._hours_worked * self.hourly_rate

    @classmethod
    def company_name(cls):
        return f"the name for company is {cls.company}"

    @staticmethod
    def is_valid_rate(rate):
        return rate > 0

emp = Employee("ameyaan", 1000)
emp.log_hours(10)
emp.log_hours(10)

print(f"your total salary is: {emp.total_salary}")

print(f"my company name is : {Employee.company}")

print(Employee.is_valid_rate(500))


