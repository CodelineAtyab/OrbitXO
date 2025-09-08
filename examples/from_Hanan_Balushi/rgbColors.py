
palette = []
print("RGB Color Palette Manager\n1. Add color\n2. Display palette\n3. Convert to hex\n4. Exit\n")

option = input("Choose Option: ")

while option != "4":
    if option.isdigit:
        if option == "1":
            print("\nEnter RGB values: ")
            r = int(input("Red (0-255): "))
            g = int(input("Green (0-255): "))
            b = int(input("Blue (0-255): "))
            color = (r,g,b)
            palette.append(color)
            print(f"Color {color} added to palette")
        elif option == "2":
            print("\nColor Palette: ")
            for i in range(len(palette)):
                print(f"{i+1}. {palette[i]}")
        elif option == "3":
            index = int(input("Enter color index: "))
            print(f"Hex code for {palette[index-1]}: {'#{:02X}{:02X}{:02X}'.format(*palette[index-1])}")

    else:
        print("Invalid input! please enter a number")
    
    option = input("\nChoose Option: ")