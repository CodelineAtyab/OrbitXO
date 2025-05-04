grade_tracker_function = True
grades_list = []

while grade_tracker_function:
    print("Student Grade Tracker\n"
    "1. Add grade\n"
    "2. Remove grade\n"
    "3. Show statistics\n"
    "4. Sort grades\n"
    "5. Display all grades\n"
    "6. Exit")

    option = input("\nChoose an option: ")

    if option == "1":
        print("\nAdd Grade:")
        grade = int(input("Enter a grade (0-100): "))
        grades_list.append(grade)
        print("Grade added successfully!\n")
    elif option == "2":
        print("\nRemove Grade:")
        if grades_list == []:
            print("list is empty")
        else:
            method = input("Remove by value or index?: ")
            while method not in ["index", "value"]:
                method = input("\nType value of index: ")
            if method == "index":
                grade_index = int(input("\nEnter the grade index: "))
                while grade_index > len(grades_list) or grade_index < 0:
                    grade_index = int(input("\nInvalid index, do it again: "))
                grades_list.pop(grade_index - 1)
            if method == "value":
                grade_value = int(input("Enter the grade value: "))
                while grade_value not in grades_list:
                    grade_value = int(input("grade value not in the list, do it again: "))
                grades_list.remove(grade_value)
        print()
    elif option == "3":
        if grades_list == []:
            print("list is empty")
        else:
            print("\nShow Statistics:")
            print("Maximum grade: " + str(max(grades_list)))
            print("Minimum grade: " + str(min(grades_list)))
            print("Average grade: " + str(int(sum(grades_list)/len(grades_list))))
        print()
    elif option == "4":
        if grades_list == []:
            print("list is empty")
        else:
            print("\nSort Gardes:")
            grade_sort = input("Accending or Descending?: ").lower()
            while grade_sort not in ["accending", "descending"]:
                grade_sort = input("Type Accending or Descending: ").lower()
            if grade_sort == "accending":
                grades_list.sort()
            elif grade_sort == "descending":
                grades_list.sort(reverse=True)
        print()
    elif option == "5":
        if grades_list == []:
            print("list is empty")
        else:
            print("Display All Grades")
            print(grades_list)
        print()
    elif option == "6":
        print("Exit program")
        print("Thank you for using our software")
        grade_tracker_function = False
    else:
        print("\nYou have to choose numbers between 1 and 6")