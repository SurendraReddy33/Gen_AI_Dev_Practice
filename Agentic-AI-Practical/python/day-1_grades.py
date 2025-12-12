#create a grade analyzer
def analyze_grades():

    #get scores
    math_score=float(input("Enter the math score (0-100): "))
    science_score=float(input("Enter the science score (0-100): "))

    #calculate average
    average=(math_score + science_score) / 2

    #determine performance level
    if average > 90:
        performance="Outstanding"
    elif average > 75:
        performance = "excellent"
    else:
        performance="Needs Improvement"

    #display results
    print(f"\nResults: ")
    print(f"Math score: {math_score}")
    print(f"science score: {science_score}")
    print(f"averafe: {average}")
    print(f"performance: {performance}")


#run the grade analyzer
analyze_grades()