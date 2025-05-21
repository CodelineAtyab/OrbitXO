def num_to_hex(n):
    hex_dig = "0123456789ABCDEF"
    return hex_dig[n // 16] + hex_dig[n % 16]

def RGB_to_hex(color):
    r, g, b = color
    return "#" + num_to_hex(r) + num_to_hex(g) + num_to_hex(b)

def palette_color(palette):
    while True:
        print("\nManage RGB Color Palettes Using Tuples")
        print("1. Add color")
        print("2. Display palette")
        print("3. Convert to hex")
        print("4. Color matching")
        print("5. Exit")

        choice = input("Choose an option from the above: ")

        if choice == "1":
            try:
                r = int(input("Enter red color value (0 - 255): "))
                g = int(input("Enter green color value (0 - 255): "))
                b = int(input("Enter blue color value (0 - 255): "))
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    palette.append((r, g, b))
                    print(f"Color {(r, g, b)} added.")
                else:
                    print("Invalid RGB values!")
            except ValueError:
                print("Please enter numbers only.")

        elif choice == "2":
            if not palette:
                print("No colors yet!")
            else:
                print("Color Palette:")
                for i, color in enumerate(palette, start=1):
                    print(f"{i}. {color}")

        elif choice == "3":
            if not palette:
                print("No colors to convert.")
            else:
                try:
                    index = int(input("Enter color index (1, 2, ...): "))
                    if 1 <= index <= len(palette):
                        color = palette[index - 1]
                        print(f"Hex code for {color} is {RGB_to_hex(color)}")
                    else:
                        print("Invalid index!")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == "4":
            if not palette:
                print("Palette is empty.")
            else:
                try:
                    r = int(input("Enter red value: "))
                    g = int(input("Enter green value: "))
                    b = int(input("Enter blue value: "))
                    closest = min(palette, key=lambda c: (r - c[0])**2 + (g - c[1])**2 + (b - c[2])**2)
                    print(f"The closest color to ({r}, {g}, {b}) is {closest}")
                except ValueError:
                    print("Please enter valid numbers.")

        elif choice == "5":
            print("Exiting... bye bye.")
            break
        else:
            print("Invalid choice, please try again.")

# Start the program
color_list = []
palette_color(color_list)