grades = []
def add_grade():
        grade = int(input("Enter a grade (0-100): "))
        if 0 <= grade <= 100:
            grades.append(grade)
            print("Grade added")
        else:
            print("Invalid grade.")
def remove_grade():
    value_or_index = input("remove grade (1 for value, 2 for index): ")
    if value_or_index == '1':
        value = int(input("Enter the grade value to remove: "))
        grades.remove(value)
        print(f"Grade {value} removed.")
    if value_or_index == '2':
        index = int(input("Enter the grade value to remove: "))
        grades.pop(index)# pop is similar to remove
        print(f"Grade {grades[index]} removed.")
       
def show_statstic():
    if not grades:
        print("No grades available.") #it return if not grades
        return
    average = sum(grades) / len(grades)
    minimum = min(grades)
    maximum = max(grades)
    print("Statistics:")
    print(f"Average: {average}")
    print(f"Minimum: {minimum}")
    print(f"Maximum: {maximum}")
def sort_grade():
    sort = input("Sort order (1 for ascending, 2 for descending): ")
    if sort == '1':
        grades.sort()
        print(f"Grades sorted in ascending order: {grades}")
    elif sort == '2':
        grades.sort(reverse=True)
        print(f"Grades sorted in descending order: {grades}")
    else:
        print("Invalid choice.")
def display_all_grade():
    if not grades:
        print("No grades to display.")
    else:
        print("All Grades:", grades)
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Add grade")
        print("2. Remove grade")
        print("3. Show statistics")
        print("4. Sort grade")
        print("5. Display all grades")
        print("6. Exit")
        select = input("Enter your choice: ")
        if select.isdigit():
            select = int(select)
            if select == 1:
                add_grade()
            elif select == 2:
                remove_grade()
            elif select == 3:
                show_statstic()
            elif select == 4:
                sort_grade()
            elif select == 5:
                display_all_grade()
            elif select == 6:
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")
        else:
            print("Please enter a number between 1 and 6.")
main_menu()