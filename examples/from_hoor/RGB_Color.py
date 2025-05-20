import math
pass
# Store colors as (R, G, B) tuples
palette = []

# Add a new color
def add_color():
    r = int(input("Red (0-255): "))
    g = int(input("Green (0-255): "))
    b = int(input("Blue (0-255): "))
    color = (r, g, b)
    palette.append(color)
    print(f"Color {color} added to palette")

# Display all colors
def display_palette():
    if not palette:
        print("Palette is empty.")
    else:
        print("Color Palette:")
        for i, color in enumerate(palette, 1):
            print(f"{i}. {color}")

# Convert RGB to Hex without using hex()
def rgb_to_hex(rgb):
    hex_digits = "0123456789ABCDEF"
    r, g, b = rgb

    def to_hex(n):
        return hex_digits[n // 16] + hex_digits[n % 16]

    return "#" + to_hex(r) + to_hex(g) + to_hex(b)

# Convert a color to hex
def convert_to_hex():
    index = int(input("Enter color index: "))
    if 1 <= index <= len(palette):
        color = palette[index - 1]
        hex_code = rgb_to_hex(color)
        print(f"Hex code for {color}: {hex_code}")
    else:
        print("Invalid index.")

# Find closest color in the palette
def find_closest_color():
    r = int(input("Enter Red pallete: "))
    g = int(input("Enter Green pallete: "))
    b = int(input("Enter Blue pallete: "))
    target = (r, g, b)

    if not palette:
        print("Palette is empty.")
        return

    def distance(c1, c2):
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

    closest = min(palette, key=lambda color: distance(color, target))
    print(f"The closest color to {target} is {closest}")

# Main menu
def menu():
    while True:
        print("\nRGB Color Palette Manager")
        print("1. Add color")
        print("2. Display palette")
        print("3. Convert to hex")
        print("4. Color Matching")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_color()
        elif choice == "2":
            display_palette()
        elif choice == "3":
            convert_to_hex()
        elif choice == "4":
            find_closest_color()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1–5.")

# Run the program
menu()
