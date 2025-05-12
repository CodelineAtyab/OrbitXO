rgb_list = []

while True:
    print("RGB Color Palette Manager\n"
    "1. Add color\n"
    "2. Display palette\n"
    "3. Convert to hex\n"
    "4. Exit\n")

    rgb_menu = int(input("Choose an option: "))
    if rgb_menu == 1:
        print("Enter RGB values:")
        red = int(input("Red: "))
        green = int(input("Green: "))
        blue = int(input("Blue: "))
        rgb_list.append((red, green, blue))

    elif rgb_menu == 2:
        for i in range(len(rgb_list)):
            print(f"{str(i + 1)}. {rgb_list[i]}")
        print()
    elif rgb_menu == 3:
        index = int(input("Enter index: "))
        color = rgb_list[index]
        hexcolor = ""
        for i in range(3):
            hexpart = hex(color[i])[2:]
            if len(hexpart) < 2:
                hexcolor += "0"
            hexcolor += hexpart
        print(hexcolor)
    elif rgb_menu == 4:
        break
    else:
        print("You have to choose a number between 1 and 4")