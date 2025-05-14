import sys
list_color = []
while True:
    print("RGB color palette Manager")
    print("1. Add a color")
    print("2. Diplay palette")
    print("3. Convert to hex")
    print("4. find the closest palette color")
    print("5. Exit")

    x = input("choose an option: ")

    if x == "1":
        r = int(input("Enter red value (0-255): "))
        g = int(input("Enter green value (0-255): "))
        b = int(input("Enter blue value (0-255): "))
        rgb = (r, g, b)
        print(f"Color {rgb} added to palette.")
        list_color.append(rgb)
    
    elif x == "2":
        print(f"latest palette: {rgb}")
        print(f"latest RGB values: Red: {r}, Green: {g}, Blue: {b}")
        print(f"RGB current list: {list_color}")

    elif x == "3":
        hex_color = "#"
        for color in rgb:
            hex_part = hex(color)[2:]
            if len(hex_part) < 2:
                hex_part = "0" + hex_part
            hex_color = hex_color + hex_part

        print(f"Hex color: {hex_color}")

    elif x == "4":
        target_r = int(input("Enter target red value (0-255): "))
        target_g = int(input("Enter target green value (0-255): "))
        target_b = int(input("Enter target blue value (0-255): "))
        target_rgb = (target_r, target_g, target_b)
        closest_color = list_color[0]
        min_distance = sys.maxsize
        for color in list_color:
            distance = (color[0] - target_r) ** 2 + (color[1] - target_g) ** 2 + (color[2] - target_b) ** 2
            if distance < min_distance:
                min_distance = distance
                closest_color = color
        print(f"Closest color in palette: {closest_color}")

    elif x == "5":
        print("Exiting...")
        break