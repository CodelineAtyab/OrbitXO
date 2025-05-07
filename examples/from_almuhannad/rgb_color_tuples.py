palette = ()


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


        if a == "2":
            if palette:
                print("Color palette:")
                for i , color in enumerate(color,start="a"):
                    print(f"{i} .{color}")
            else:   
                print("Palette is empty.")
