while True:
    print("RGB color palette Manager")
    print("1. Add a color")
    print("2. Diplay palette")
    print("3. Convert to hex")
    print("4. Exit")

    x = input("choose an option: ")

    if x == "1":
        r = int(input("Enter red value (0-255): "))
        g = int(input("Enter green value (0-255): "))
        b = int(input("Enter blue value (0-255): "))
        rgb = (r, g, b)
        print(f"Color {rgb} added to palette.")

    elif x == "2":
        print(f"Current palette: {rgb}")
        print(f"RGB values: Red: {r}, Green: {g}, Blue: {b}")

    
    elif x == "3":
        hex_color = "#"
        for color in rgb:
            hex_part = hex(color)[2:]
            if len(hex_part) < 2:
                hex_part = "0" + hex_part
            hex_color = hex_color + hex_part

        print(f"Hex color: {hex_color}")
    
    elif x == "4":
        print("Exiting...")
        break