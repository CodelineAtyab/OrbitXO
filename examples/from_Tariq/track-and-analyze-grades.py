grades = []
while True:
    print("Student Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. show statistics")
    print("4. Sort grades")
    print("5. Display all grades")
    print("6. Exit")


    choice = input("Choose an option: ")
    if choice == '1':
        grade = int(input("Enter a grade (0-100): "))
        grades.append(grade)
        print(f"Grade {grade} added.")
        print("Grades:", grades)

    elif choice == '2':
        grade = int(input("Enter a grade (0-100) or grande index to remove : "))
        if grade in grades:
            grades.remove(grade)
            print(f"Grade {grade} removed.")
        elif 0 <= grade < len(grades):
            removed_grade = grades.pop(grade)
            print(f"Grade {removed_grade} removed from index {grade}.")
        else:
            print("Invalid grade or index.")

    elif choice == '3':
        print("Statistics:")
        print("Average:", sum(grades) / len(grades))
        print("Minimum:", min(grades))
        print("Maximum:", max(grades))
    
    elif choice == '4':
        c = input("sort by (1) ascending or (2) descending: ")
        if c == '1':
            grades.sort()
            print("Grades sorted in ascending order.")
            print(grades)
        elif c == '2':
            grades.sort(reverse=True)
            print("Grades sorted in descending order.")
            print(grades)
        else:
            print("Invalid choice.")
    elif choice == '5':
        print(grades)

    elif choice == '6':
        print("Exiting...")
        break
    


