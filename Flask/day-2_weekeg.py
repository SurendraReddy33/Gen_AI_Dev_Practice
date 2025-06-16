def get_week_day(day: str) -> str:
    return {
        'monday': 'workday',
        'tuesday': 'workday',
        'wednesday': 'workday',
        'thursday': 'weekend coming',
        'friday': 'plan for long weekend',
        'saturday': 'weekend',
        'sunday': 'Holiday'
    }.get(day, "enter correct day : ")

result = get_week_day("sunday")
print(result)