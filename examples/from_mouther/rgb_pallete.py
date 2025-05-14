palette = []
HEX_MAP = "0123456789ABCDEF"
def to_hex(value):
    big = value // 16
    small = value % 16
    return HEX_MAP[big] + HEX_MAP[small]

def rgb_to_hex(r, g, b):
    return "#" + to_hex(r) + to_hex(g) + to_hex(b)

while True:
    print("\nRGB Color Palette Manager")
    print("1. Add color")
    print("2. Display palette")
    print("3. Convert to hex")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        r = int(input("Red (0-255): "))
        g = int(input("Green (0-255): "))
        b = int(input("Blue (0-255): "))
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            color = (r, g, b)
            palette.append(color)
            print(f"Color {color} added to palette")
        else:
            print("Each value must be between 0 and 255.")


    elif choice == '2':
        counter = 1
        if not palette:
            print("Palette is empty.")
        else:
            print("Color Palette:")
            for color in palette:
                print(f"{counter}. {color}")
                counter += 1

    elif choice == '3':
        if not palette:
            print("Palette is empty.")
        else:
            index = int(input("Enter color index: ")) - 1
            if 0 <= index < len(palette):
                r, g, b = palette[index]
                hex_code = rgb_to_hex(r, g, b)
                print(f"Hex code for {palette[index]}: {hex_code}")
            else:
                print("Invalid index.")


    elif choice == '4':
        print("Exiting...")
        break
    else:
        print("Invalid option. Please try again.")
