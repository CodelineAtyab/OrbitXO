
def add_color_to_palette(palette, color):
    r=int(input("Red (0-255): "))
    g=int(input("Green (0-255): "))
    b=int(input("Blue (0-255): "))

    add_color_to_palette(palette, (r, g, b))
    palette.append(color)
    print(f"Color {color} added to palette")

def calculate_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def find_closest_color(palette, target_color):
    """Find the closest matching color in the palette to the given RGB value."""
    closest_color = None
    min_distance = float('inf')
    for color in palette:
        distance = calculate_distance(color, target_color)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

def rgb_to_hex(color):
    """Convert an RGB tuple to a hexadecimal color code."""
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

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
                    print("Invalid RGB values. Please enter values between 0 and 255.")
            except ValueError:
                print("Invalid input. Please enter integers only.")
        
        elif choice == "2":
            if palette:
                print("\nColor Palette:")
                for i, color in enumerate(palette, start=1):
                    print(f"{i}. {color}")
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
                    print("Invalid input. Please enter an integer.")
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
                        print("Invalid RGB values. Please enter values between 0 and 255.")
                except ValueError:
                    print("Invalid input. Please enter integers only.")
            else:
                print("The palette is empty.")
        
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()