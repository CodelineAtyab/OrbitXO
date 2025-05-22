# List to store colors as (R, G, B) tuples
palette = []

def add_color():
    r = int(input("Red (0-255): "))
    g = int(input("Green (0-255): "))
    b = int(input("Blue (0-255): "))
    color = (r, g, b)
    palette.append(color)
    print(f"Color {color} added to palette.")

def display_palette():
    print("Color Palette:")
    for i, color in enumerate(palette, 1):
        print(f"{i}. {color}")

def rgb_to_hex(color):
    r, g, b = color
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

def find_closest_color(target):
    closest = None
    smallest_diff = float('inf')
    for color in palette:
        diff = sum((a - b) ** 2 for a, b in zip(color, target))
        if diff < smallest_diff:
            smallest_diff = diff
            closest = color
    return closest

# Main menu loop
while True:
    print("\nRGB Color Palette Manager")
    print("1. Add color")
    print("2. Display palette")
    print("3. Convert to hex")
    print("4. Find closest color")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_color()
    elif choice == "2":
        display_palette()
    elif choice == "3":
        index = int(input("Enter color index: ")) - 1
        if 0 <= index < len(palette):
            hex_code = rgb_to_hex(palette[index])
            print(f"Hex code: {hex_code}")
        else:
            print("Invalid index.")
    elif choice == "4":
        r = int(input("Red: "))
        g = int(input("Green: "))
        b = int(input("Blue: "))
        target = (r, g, b)
        closest = find_closest_color(target)
        print(f"Closest color to {target} is {closest}")
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
