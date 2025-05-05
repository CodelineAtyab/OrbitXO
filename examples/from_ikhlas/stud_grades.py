
grades = [] #list

while True:  #to print the tracker list
    print("\nStudent Grade Tracker")
    print("1.Add grade")
    print("2.Remove grade")
    print("3.Show statistics")
    print("4.Sort grades")
    print("5.Display all grades")
    print("6.Exit")
    option=input("Choose an option: ")


    if option == '1':
        grade_input=input("\nEnter a grade (0-100): ")
        if grade_input.isdigit():  #check that the input is number - integer 
            grade=int(grade_input) 
            if 0 <= grade <= 100:
                grades.append(grade)  #grade added 
                print("\nGrade added successfully!")
            else:
                print("Invalid grade. Must be between 0 and 100.") #for the grades les than 0 and greater than 1
        else:
            print("Invalid input. Please enter a number.") #input other than number


    elif option == '2':
        if len(grades) == 0:
            print("Grade list is empty.")
        else:
            print("Remove by (1) Value or (2) Index?")
            method = input("Choose method: ")
            if method == '1':
                val_input = input("Enter the grade value to remove: ")
                if val_input.isdigit():   #check that the input is number - integer 
                    val = int(val_input)
                    found = False
                    for num in grades:
                        if num == val:
                            grades.remove(val)
                            print("Grade removed.")
                            found = True
                            break
                    if not found:
                        print("Grade not found.")
                else:
                    print("Invalid input.")
            elif method == '2':
                index_input=input("Enter the index to remove: ")
                if index_input.isdigit():
                    index = int(index_input)
                    if 0 <= index < len(grades):
                        removed = grades.pop(index)  # remove the value and return 
                        print(f"Grade {removed} at index {index} removed.")
                    else:
                        print("Index out of range.")
                else:
                    print("Invalid input.")
            else:
                print("Invalid choice.") #choice other than 1 or 2 


    elif option == '3':
        if len(grades) == 0:
            print("No grades to show statistics.") #once the list is empty or no grades added 
        else:
            total = 0
            for g in grades:
                total += g
            average = total / len(grades)
            minimum = min(grades)
            maximum = max(grades)
            print("\nStatistics:")
            print("Average:", round(average, 2)) #print the average and round the decimal 
            print("Minimum:", minimum)
            print("Maximum:", maximum)


    elif option == '4':
        if len(grades) == 0:  #once the list is empty or no grades added 
            print("No grades to sort.")
        else:
            print("\nSort order (1 for ascending, 2 for descending):")
            order=input("Choose order: ")
            if order == '1':
                grades.sort()
                print("Grades sorted in ascending order:", grades)
            elif order == '2':
                grades.sort(reverse=True) #to print the grades in reverse mode 
                print("Grades sorted in descending order:", grades)
            else:
                print("Invalid sort option.")


    elif option == '5':
        if len(grades) == 0:
            print("No grades to display.")
        else:
            print("\nCurrent grades:", grades)

    elif option == '6':
        print("Exiting program.")
        break


    else:
        print("Invalid option. Please choose from 1 to 6.") #for options other than 1 to 6
