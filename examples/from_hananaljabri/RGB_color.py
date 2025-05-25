color_list = []

def num_to_hex(n):
    hex_dig = "0123456789ABCDEF"
    value1 = n // 16
    value2 = n % 16
    return hex_dig[value1] + hex_dig[value2]

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

        choose = input("Choose an option from the above: ")

        if choose == "1":
            r = int(input("Enter red color value (0 - 255): "))
            g = int(input("Enter green color value (0 - 255): "))
            b = int(input("Enter blue color value (0 - 255): "))

            if (0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <= 255):
                palette.append((r, g, b))
                print(f"Color {(r, g, b)} added.")
            else:
                print("Invalid RGB values!")

        elif choose == "2":
            if not palette:
                print("No colors yet!")
            else:
                print("Color Palette:")
                for i in range(len(palette)):
                    print(f"{i + 1}. {palette[i]}")

        elif choose == "3":
            if not palette:
                print("No colors to convert.")
            else:
                index = int(input("Enter color index (1, 2, ...): "))
                if 1 <= index <= len(palette):
                    r, g, b = palette[index - 1]
                    print(f"Hex code for {(r, g, b)} is {RGB_to_hex((r, g, b))}")
                else:
                    print("Invalid index!")

        elif choose == "4":
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
                    dist = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
                    if min_distance is None or dist < min_distance:
                        min_distance = dist
                        closest = color

                print(f"The closest color to ({r}, {g}, {b}) is {closest}")

        elif choose == "5":
            print("Exiting, Goodbye")
            break
        else:
            print("Invalid choice, please try again :)")

palette_color(color_list)