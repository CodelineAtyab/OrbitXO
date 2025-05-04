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
        print("1. Enter a grade to remove")
        print("2. Enter index to remove")
        
        c = input("Enter a chooice: ")

        if c == "1":

            print(list_of_grades)
            grade_to_remove = int(input("Enter a grade to remove: "))
            if grade_to_remove in list_of_grades:
                list_of_grades.remove(grade_to_remove)
                print("Grade is removed ",grade_to_remove)
            else:
                print("Grade not found!")

        elif c == "2":
            print(list_of_grades)
            index_to_remove = int(input("Enter index to remove: "))
            if 0 <= index_to_remove < len(list_of_grades):
                rindex = list_of_grades.pop(index_to_remove)
                print("Grade index have been removed")
            else:
                print("Index not found")
        print(list_of_grades)

    elif a == "3":
        print("show statistics: ")
        print("Minimum: ", min(list_of_grades))
        print("Maximum: ", max(list_of_grades))
        print("Average: ", sum(list_of_grades)/len(list_of_grades))
        print(list_of_grades)

    elif a == "4":
        print("1. Sort by Asending")
        print("2. Sort by Descending")
        x = input("Enter ur choice: ")

        if x == "1":
            list_of_grades.sort()
            print(list_of_grades)
        elif x == "2":
            list_of_grades.sort(reverse=True)
            print(list_of_grades)

    elif a == "5":
        print(list_of_grades)

    elif a == "6":
        break




        

