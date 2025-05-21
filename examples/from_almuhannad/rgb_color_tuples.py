

def rgb_to_hex(color):
    r, g, b = color
    return "#{:02X}{:02X}{:02X}".format(r, g, b)


print("RGB Color Palette Manager")
while True:
        print("1. Add color")
        print("2. Display Palette")
        print("3. Convert to hex")
        print("4. Exit")

        a = input("Choose an option: ")

        if a == "1":
            print("Enter RGB colors:")
            red_value = int(input("Red (0-255): "))
            green_value = int(input("Green (0-255): "))
            blue_value = int(input("Blue (0-255): "))
            if all(0 <= val <= 255 for val in (red_value,green_value,blue_value)):
                color = (red_value,green_value,blue_value)
                palette = palette + (color,)
                print(f"Color {color} added.")
            else:
                print("Invalid RGB color ! Must be between 0 and 255")


        elif a == "2":
            if palette:
                print("Color palette:")
                for i , color in enumerate(palette, start=1):
                    print(f"{i} .{color}")
            else:   
                print("Palette is empty.")

        elif a == "3":
            if palette:
                index = int(input("Enter color index: ")) 

                if 1 <= index <= len(palette):
                    color = palette[index - 1]
                    hex_code = rgb_to_hex(color)
                    print(f"Hex code for {color}: {hex_code}")
                else:
                    print(f"❌ Invalid index. Enter a number between 1 and {len(palette)}.")

        elif a == "4":
            print("Exiting")
            False
            break

