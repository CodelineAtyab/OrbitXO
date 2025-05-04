list_of_grades = []
while True:

    print("Student Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. show statistics")
    print("4. sort grades")
    print("5. Display all grades")
    print("6. Exit")

    a = input("Choose an option: ")
    if a == "1":
        input_grade = input("Enter your grades (0-100): ")
        numeric_grade = int(input_grade)
        list_of_grades.append(numeric_grade)
        print("Grade added successfully!")
        print(list_of_grades)

    elif a == "2":
        print("Remove Grade")
        print(list_of_grades)
        grade_to_remove = int(input("enter a grade to remove: "))
        if grade_to_remove in list_of_grades:
            list_of_grades.remove(grade_to_remove)
            print("Grade is removed ",grade_to_remove)
        else:
             print("Grade not found!")
        print(list_of_grades)

    elif a == "3":
        print("show statistics: ")
        print(min(list_of_grades))
        print(max(list_of_grades))
        print(list_of_grades)
        print(sum(list_of_grades))

    elif a == "4":
        print("Sorting Grades")
        print(sorted(list_of_grades))

    elif a == "5":
        print(list_of_grades)

    elif a == "6":
        break




        

