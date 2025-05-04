
print("Student Grade Tracker\n1. Add grade\n2. Remove grade\n3. Show statistics\n4. Sort grades\n5. Display all grades\n6. Exit")
option = input("\nChoose an option: ")

student_grades = []

while option != "6":
    if option == "1":
        grade = int(input("Enter a grade (0-100): "))
        if (grade >= 0 and grade <= 100):
            student_grades.append(grade)
            print("Grade added successfully!")
        else:
            print("Invalid Input!")
    if option == "2":
        remove_grade = int(input("Enter a grade (0-100) to be Removed: "))
        if (remove_grade >= 0 and remove_grade <= 100 and remove_grade in student_grades):
            student_grades.remove(remove_grade)
            print("Grade Removed successfully!")
        else:
            print("Invalid Input!")
    if option == "3":
        print(f"Statistics:\nAverage: {sum(student_grades)/len(student_grades)}\nMinimum: {min(student_grades)}\nMaximum: {max(student_grades)}")
    if option == "4":
        order = input("Sort order (1 for ascending, 2 for descending): ")
        if order == "1": 
            student_grades.sort()
            print(f"Grades sorted in ascending order: {student_grades}")
        else:
            student_grades.sort(reverse=True)
            print(f"Grades sorted in descending order: {student_grades}")
    if option == "5":
        print(f"Student Grades = {student_grades}")
    option = input("\nChoose an option: ")

