grades = []

while True:
    print("\nGrade Manager")
    print("1. Add grade")
    print("2. Delete grade")
    print("3. Show statistics")
    print("4. Sort grades")
    print("5. View grades")
    print("6. Exit")

    option = input("Select a number: ")

    if option == '1':
        g = int(input("Enter a grade (0 to 100): "))
        if g >= 0 and g <= 100:
            grades.append(g)
            print("Added!")
        else:
            print("Invalid grade!")
    
    elif option == '2':
        if grades != []:
            way = input("Remove by value (v) or index (i): ")
            if way == 'v':
                val = int(input("Enter grade to remove: "))
                grades.remove(val)
                print("Removed!")
            elif way == 'i':
                pos = int(input("Enter index: "))
                removed = grades.pop(pos)
                print("Deleted:", removed)

    elif option == '3':
        if grades != []:
            avg = sum(grades) / len(grades)
            print("\nStats:")
            print("Avg:", avg)
            print("Min:", min(grades))
            print("Max:", max(grades))

    elif option == '4':
            sort_order = input("1 = Ascending, 2 = Descending: ")
            if sort_order == '1':
                grades.sort()
                print("Sorted (asc):", grades)
            elif sort_order == '2':
                grades.sort(reverse=True)
                print("Sorted (desc):", grades)

    elif option == '5':
        print("Grades list:", grades)

    elif option == '6':
        print("Goodbye!")
        break