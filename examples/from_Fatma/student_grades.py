grades = [ 30, 20 ,85, 55, 100]
while True:
    print  
    print("\n Student Grade Tracker")
    print("1. Add grade")
    print("2. Remove grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. Display all grades")
    print("6. Exit")
    choice = int(input("\nChoose an option: ")) 

# Add grade

    if choice == 1:
       grade = int (input("Enter a grade (0-100): "))
       if  0<= grade <=100:
          grades.append(grade)
          print("Grade added successfully!")
          print(grades)   

       else:
        print(" Grade must be between 0 and 100.")

    elif choice == 2:
        print(grades)
        grade = int (input ("Enter the grade to remove: "))
        if grade in grades:
           grades.remove(grade)
           print("Grade removed successfully!")   
           print(grades)  
        else:
           print("Grade not found.") 
           print(grades)   


# Show statistics
    elif choice == 3:
       if grades:
          average = sum (grades)/ len(grades)
          mainimum = min(grades)
          maximum =max(grades)
          print(f"Average: {average}")
          print(f"Mainimum: {mainimum}")
          print(f"Maximum: {maximum}")
       else:
          print("no grades")


# Sort grades 
    elif choice == 4:
        ascending = sorted(grades)
        descending = sorted(grades, reverse=True)
        print("Original: ", grades)
        print("Ascending: ", ascending)
        print("Descending: ", descending)


# Display all grades
    elif choice == 5:
       if grades: 
          print("All grades: ")
          for i in range(len(grades)):
             print(f"{i+1}.{grades[i]}")
       else:
          print("No grades to display!")

# Exit
    elif choice == 6:
       print(" Thank you!")
       break


    else:
       print("invalid input")
