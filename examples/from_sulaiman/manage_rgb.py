rgb_list = []

def manual_hex(color_code):
    hex_text = ""
    for i in range(len(color_code)):
        if color_code[i] > -1 and color_code[i] < 256:
            hex_code = {
                10 : "A",
                11 : "B",
                12 : "C",
                13 : "D",
                14 : "E",
                15 : "F",
                }
            ldigit = int(int(color_code[i]) / 16)
            rdigit = int(int(color_code[i]) % 16)
            if ldigit in hex_code:
                ldigit = hex_code[ldigit]
            if rdigit in hex_code:
                rdigit = hex_code[rdigit]
        hex_text += str(ldigit) + str(rdigit)
    return hex_text

while True:
    print("RGB Color Palette Manager\n"
    "1. Add color\n"
    "2. Display palette\n"
    "3. Convert to hex\n"
    "4. Manual hex function\n"
    "5. Match Color Pallete\n"
    "6. Exit\n")

    rgb_menu = int(input("Choose an option: "))
    if rgb_menu == 1:
        print("Enter RGB values:")
        red = int(input("Red: "))
        while red < 0 or red > 255:
            red = int(input("put a value between 0 and 255"))
        green = int(input("Green: "))
        while green < 0 or green > 255:
            green = int(input("put a value between 0 and 255"))
        blue = int(input("Blue: "))
        while blue < 0 or blue > 255:
            blue = int(input("put a value between 0 and 255"))
        rgb_list.append((red, green, blue))
        print("Added color pallet to list")
        print()
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
        print()
    elif rgb_menu == 4:
        index = int(input("Enter index: "))
        color = rgb_list[index]
        hexcolor = manual_hex(color)
        print(hexcolor)
        print()
    elif rgb_menu == 5:
        redt = int(input("Enter Red Value: "))
        while redt < 0 or redt > 255:
            redt = input("put a value between 0 and 255: ")
        greent = int(input("Enter Green Value: "))
        while greent < 0 or greent > 255:
            greent = input("put a value between 0 and 255: ")
        bluet = int(input("Enter Blue Value: "))
        while bluet < 0 or bluet > 255:
            bluet = int(input("put a value between 0 and 255: "))
        target = (redt, greent, bluet)
        closest_value = 255 * 3
        closest_rgb = ()
        for rgb in rgb_list:
            red_value = abs(target[0] - rgb[0])
            green_value = abs(target[1] - rgb[1])
            blue_value = abs(target[2] - rgb[2])
            comb_value = red_value + blue_value + green_value
            if comb_value < closest_value:
                closest_value = comb_value
                closest_rgb = rgb
        print(f"The closest pallet to {target} is {closest_rgb}")
        print()
    elif rgb_menu == 6:
        break
    else:
        print("You have to choose a number between 1 and 6")