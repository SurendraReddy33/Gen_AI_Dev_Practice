#Problem Statement

#Developing code for printing weekdays

def week_days(day:str)->str:
    return {
        "Monday": "working_day",
        "Tuesday": "working_day",
        "Wednesday": "working_day",
        "Thursday": "working_day",
        "Friday": "working_day",
        "Saturday": "week_off",
        "Sunday": "week_off",
    }.get(day, "Enter the correct day:")

day=input('enter the weekday:'.strip())
print(week_days(day))