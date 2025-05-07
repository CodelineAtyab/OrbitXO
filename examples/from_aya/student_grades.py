def add_grades(grades):
    grade = int(input("Enter grade (0-100): "))
    if 0 <= grade <= 100:
        grades.append(grade)
        print("Grade added.")
    else:
        print("Invalid grade. Must be between 0 and 100.")

def remove_grades(grades):
    while True:
        grade = int(input("Enter grade to remove: "))
        if grade in grades:
            grades.remove(grade)
            print("Grade removed.")
        else:
            print("Grade not found.")
            break
    return grades

def show_statistics(grades):
    if len(grades) == 0:
        print("No grades available.")
    else:
        print("Statistics:")
        average = sum(grades) / len(grades)
        print("Average grade:", round(average, 2))
        print("Highest grade:", max(grades))
        print("Lowest grade:", min(grades))
        print("Number of grades:", len(grades))
        print("Grades:", grades)
        print("Sorted grades (ascending):", sorted(grades))
        print("Sorted grades (descending):", sorted(grades, reverse=True))
        print("Grades in reverse order (last entered first):", grades[::-1])

def show_all_grades(grades):
    if len(grades) == 0:
        print("No grades available.")
    else:
        print("All grades:", grades)

def sort_grades(grades):
    if len(grades) == 0:
        print("No grades to sort.")
        return
    order = input("Sort order (1 for ascending, 2 for descending): ")
    if order == "1":
        grades.sort()
        print("Grades sorted in ascending order:", grades)
    elif order == "2":
        grades.sort(reverse=True)
        print("Grades sorted in descending order:", grades)
    else:
        print("Invalid sort option.")


grades = []
while True:
    # Menu displayed here inside the loop
    print("\nStudent Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Show all grades")
    print("5. Sort grades")
    print("6. Exit")
    
    choice = input("Choose an option: ")
    if choice == "1":
        add_grades(grades)
    elif choice == "2":
        remove_grades(grades)
    elif choice == "3":
        show_statistics(grades)
    elif choice == "4":
        show_all_grades(grades)
    elif choice == "5":
        sort_grades(grades)
    elif choice == "6":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")

