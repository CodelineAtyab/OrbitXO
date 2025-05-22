palette=[]
while True:
    print("\nRGB Color Palette Manager:")
    print("1. Add Color")
    print("2. Display palette")
    print("3. Convert to hex ")
    print("4. find the closest color")
    print("5. Exit")

    choose=input("Choose an option:")

    if choose == "1":
        try:
            r = int(input("Enter the red value (0-255): "))
            g = int(input("Enter the green value (0-255): "))
            b = int(input("Enter the blue value (0-255): "))
            color= (r,g,b)
            palette.append(color)
            print(f"Color {color} added to palette")
        except:
            print("Invalid input. Please enter a number between 0 and 255.")

    elif choose=="2":
        print("\n2. Display palette")
        for i in range(len(palette)):
            print(f"{i+1}. {palette[i]}")

    elif choose=="3":
        print("3. Convert to hex")
        for i in range(len(palette)):
            r,g,b=palette[i]             # get the i-th item (starting from 0) from that list.
            hex_color = '#{:02x}{:02x}{:02x}'.format(r,g,b)
            # 0 → pad with zeros if needed
            # 2 → make sure it’s 2 characters wide
            # x → convert the number to hexadecimal (using lowercase letters)
            # .format(r, g, b) to insert r,g,b values into the string().
            print(f"{i+1}. {palette[i]}: {hex_color}")


    elif choose =="4":
        print("4. find the closest color")
        if not palette:
                print("Palette is empty.")
        else:
                r = int(input("Enter red value: "))
                g = int(input("Enter green value: "))
                b = int(input("Enter blue value: "))
                closest = None
                min_distance = None

                for color in palette:
                    cr, cg, cb = color
                    #calculates the Euclidean distance squared between the input color and a palette: color.
                    dist = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2 
                    if min_distance is None or dist < min_distance:
                        min_distance = dist
                        closest = color

                print(f"The closest color to ({r}, {g}, {b}) is {closest}")

    elif choose=="5":
        print("Goodbye!!!!!!!!!!")
        break

    else:
        print("Invalid option. Please choose from 1 to 4.")
        
        



