
def calculate_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5

def find_closest_color(palette, target_color):
    closest_color = None
    min_distance = float('inf')  # start with a very large number
    for color in palette:
        distance = calculate_distance(color, target_color)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color


def rgb_to_hex(color):
    def to_hex(x):
        hex_digits = "0123456789ABCDEF"
        return hex_digits[x // 16] + hex_digits[x % 16]
    r, g, b = color
    return f"#{to_hex(r)}{to_hex(g)}{to_hex(b)}"


def main():
    palette = []

    while True:
        print("\nRGB Color Palette Manager")
        print("1. Add color")
        print("2. Display palette")
        print("3. Convert to hex")
        print("4. Find closest color")
        print("5. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
        
            try:
                r = int(input("Red (0-255): "))
                g = int(input("Green (0-255): "))
                b = int(input("Blue (0-255): "))
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                    color = (r, g, b)
                    palette.append(color)
                    print(f"Color {color} added to palette")
                else:
                    print("Values must be between 0 and 255.")
            except ValueError:
                print("Please enter valid numbers.")

        elif choice == "2":
        
            if palette:
                print("\nColor Palette:")
                i = 1
                for color in palette:
                    print(f"{i}. {color}")
                    i += 1
            else:
                print("The palette is empty.")

        elif choice == "3":

            if palette:
                try:
                    index = int(input("Enter color index: ")) - 1
                    if 0 <= index < len(palette):
                        color = palette[index]
                        hex_code = rgb_to_hex(color)
                        print(f"Hex code for {color}: {hex_code}")
                    else:
                        print("Invalid index.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("The palette is empty.")

        elif choice == "4":
           
            if palette:
                try:
                    r = int(input("Enter Red value (0-255): "))
                    g = int(input("Enter Green value (0-255): "))
                    b = int(input("Enter Blue value (0-255): "))
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        target_color = (r, g, b)
                        closest_color = find_closest_color(palette, target_color)
                        print(f"The closest color to {target_color} is {closest_color}")
                    else:
                        print("Values must be between 0 and 255.")
                except ValueError:
                    print("Please enter valid numbers.")
            else:
                print("The palette is empty.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
