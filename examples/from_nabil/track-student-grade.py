student_grades = []
while True:
    print("track student grades")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. Display all grades")
    print("6. Exit")

    x = input("Select an option: ")
    if x == "1":
        enter_grade = input("Enter your grades (0-100): ")
        numeric_grades = int(enter_grade)
        student_grades.append(numeric_grades)
        print("grade added successfully!")
        print(student_grades)

    elif x == "2":
        print("1. Enter grade to remove")
        print("2. Enter index to remove")


        y = input("select a choice: ")
        if y == "1":
            print(student_grades)
            remove_grades = int(input("Enter grade to remove: "))
            if remove_grades in student_grades:
                student_grades.remove(remove_grades)
                print("Grade Is Removed", remove_grades)
            else:
                print("Grade Not Found!")

        elif y == "2":
            print(student_grades)
            remove_index = int(input("Enter index to remove: "))
            if 0 <= remove_index < len(student_grades):
                rindex = student_grades.pop(remove_index)
                print("Grade index have been removed")
            else:
                print("Index Not Found")
            print(student_grades)
    elif x == "3":
            print("show statistics: ")
            print("Minimum: ", min(student_grades))
            print("maximum: ", max(student_grades))
            print("Average: ", sum(student_grades)/len(student_grades))
            print(student_grades)
    elif x == "4":
            print("1. Sort by asending")
            print("2. Sort by descending")
            a = input("select a choice: ")

            if a == "1":
                student_grades.sort()
                print(student_grades)
            elif a == "2":
                student_grades.sort(reverse =True)
                print(student_grades)

    elif x == "5":
            print(student_grades)

    elif x == "6":
            print("Exit")
            break
    else:
         print("select a number from 1 - 6")



