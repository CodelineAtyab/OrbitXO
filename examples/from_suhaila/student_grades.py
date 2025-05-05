marks = []
marks_menu = True 
while marks_menu:
    print("\nStudent Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort marks")
    print("5. Display all marks")
    print("6. Exit")

    option = input("Choose an option: ")

    if option == '1':
        grade = float(input("Enter a grade (0-100): "))
        if 0 <= grade <= 100:
            marks.append(grade)
            print("Grade added successfully!")
        else:
            print("Invalid grade. Please enter a value between 0 and 100.")

    elif option == '2':
        if not marks:
            print("No marks to remove.")
        else:
            method = input("Remove by value or index? (v/i): ").lower()
            if method == 'v':
                value = float(input("Enter grade value to remove: "))
                marks.remove(value)
                print("Grade removed successfully!")
            elif method == 'i':
                index = int(input("Enter index of grade to remove: "))
                if 0 <= index < len(marks):
                    removed = marks.pop(index)
                    print(f"Removed grade: {removed}")
                else:
                    print("Invalid index.")
            else:
                print("Invalid option.")


    elif option == '3':
        if not marks:
            print("No marks available to calculate statistics.")
        else:
            average = sum(marks) / len(marks)
            print("\nStatistics:")
            print(f"Average: {average:.2f}")
            print(f"Minimum: {min(marks)}")
            print(f"Maximum: {max(marks)}")

    elif option == '4':
        if marks == []:
            print("No marks to sort.")
        else:
            order = input("Sort order (1 for ascending, 2 for descending): ")
            if order == '1':
                marks.sort()
                print("marks sorted in ascending order:", marks)
            elif order == '2':
                marks.sort(reverse=True)
                print("marks sorted in descending order:", marks)
            else:
                print("Invalid sort option.")

    elif option == '5':
        if marks:
            print("All marks:", marks)
        else:
            print("No marks to display.")

    elif option == '6':
        print("Exiting , Goodbye!")
        marks_menu = False
    else:
        print("Invalid option. Please choose a number between 1 and 6.")
