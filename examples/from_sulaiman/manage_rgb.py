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
    "5. Exit\n")

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
        index = int(input("Enter index: "))
        color = rgb_list[index]
        hexcolor = manual_hex(color)
        print(hexcolor)
    elif rgb_menu == 5:
        break
    else:
        print("You have to choose a number between 1 and 4")