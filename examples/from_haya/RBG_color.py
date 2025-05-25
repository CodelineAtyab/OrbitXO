color_palette = []


def add_color():
    RED = input("Enter RED value (0-255): ")
    GREEN = input("Enter GREEN value (0-255): ")
    BLUE = input("Enter BLUE value (0-255): ")

    if RED.isdigit() and GREEN.isdigit() and BLUE.isdigit():  #i use isdigit to make sure that only can enter numbers 
        RED = int(RED)
        GREEN = int(GREEN)
        BLUE = int(BLUE)

        if 0 <= RED <= 255 and 0 <= GREEN <= 255 and 0 <= BLUE <= 255:
            color = (RED, GREEN, BLUE)
            color_palette.append(color)
            print("Color added ")
        else:
            print(" Values must be between 0 and 255.")
    else:
        print("Please enter valid integer numbers.")


def display_palette():
    if not color_palette:
        print("Palette is empty.")
    else:
        print("Color Palette:")
        index = 1 
        for color in color_palette:
            print(f"{index}. {color}")
            index += 1


def convert_hex():
    if not color_palette:
        print("The palette is empty")
    else:
        print("\nAvailable Colors:") #first disply the color platte
        display_palette()

        index = input("\nEnter the number of the color to convert to HEX: ") #user shoud enter the color number from disply color function
        if index.isdigit():
            index = int(index)
            if 1 <= index <= len(color_palette):
                r, g, b = color_palette[index - 1]

                if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):  #RGB should be in this range
                    print("RGB values must be between 0 and 255.")
                    return

                hex_digits = "0123456789ABCDEF"

                red_hex = hex_digits[r // 16] + hex_digits[r % 16]
                green_hex = hex_digits[g // 16] + hex_digits[g % 16]
                blue_hex = hex_digits[b // 16] + hex_digits[b % 16]

                hex_code = f"#{red_hex}{green_hex}{blue_hex}"
                print(f"\nRGB: ({r}, {g}, {b}) to HEX: {hex_code}")
            else:
                print("Invalid choice")
        else:
            print("Please enter a valid number.")
            

def closest_color():
    if not color_palette:
        print("The palette is empty, add colors first.")
        return

    RED = input("Enter Red palette: ")
    GREEN = input("Enter Green palette: ")
    BLUE = input("Enter Blue palette: ")

    if RED.isdigit() and GREEN.isdigit() and BLUE.isdigit():
        RED = int(RED)
        GREEN = int(GREEN)
        BLUE = int(BLUE)

        if not (0 <= RED <= 255 and 0 <= GREEN <= 255 and 0 <= BLUE <= 255):
            print("Values must be between 0 and 255.")
            return

        print("searching the list")

        min_distance = float("inf")
        closest = None

        for color in color_palette:
            r, g, b = color
            x = abs(RED - r) + abs(GREEN - g) + abs(BLUE - b)  
            if x < min_distance:
                min_distance = x
                closest = color

        print(f"The closest color to ({RED}, {GREEN}, {BLUE}) is {closest}")

    else:
        print("Please enter valid integer numbers.")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Add color")
        print("2. Display palette")
        print("3. Convert to HEX")
        print("4. Closest color")
        print("5. Exit")

        select = input("Enter your choice: ")
        if select.isdigit():
            select = int(select)
            if select == 1:
                add_color()
            elif select == 2:
                display_palette()
            elif select == 3:
                convert_hex()
            elif select == 4:
                closest_color()
            elif select == 5:
                print("Exiting program")
                break
            else:
                print("Invalid choice")
        else:
            print("Please enter a number between 1 and 5.")

main_menu()
