def to_hex(n):
    high = n // 16
    low = n % 16
    HEX_MAP = "0123456789ABCDEF"
    return HEX_MAP[high] + HEX_MAP[low]

def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{to_hex(r)}{to_hex(g)}{to_hex(b)}"




palette = [ ]
while True:
        print("RGB Color Palette Manager\n")
        print("1. Add color")
        print("2. Display palette")
        print("3. Convert to hex")
        print("4. Color Matching")
        print("5. Exit")
        
        choice:int = input("Choose an option: ")

        if choice == '1':
            r = int(input("Red (0-255): "))
            g = int(input("Green (0-255): "))
            b = int(input("Blue (0-255): "))
            palette.append((r, g, b))
            print(f"Color {(r, g, b)} added to palette.\n")

        elif choice == '2':
            count=1
            for  color in palette:
                print(f"{count}. {color}")
                count +=1

        elif choice == '3':
            indx = input("Enter color index: ")

            if indx.isdigit():
                idx = int(indx) - 1
                rgb = palette[idx]
                hex_code = rgb_to_hex(rgb)
                print(f"Hex code for {rgb}: {hex_code}")   
            else:
                print("Please enter a valid number.")

        elif choice == '4':
            r1 = int(input("Enter Red palette: "))
            g1 = int(input("Enter Green palette: "))
            b1 = int(input("Enter Blue palette: "))

            min_dist = float('inf') ## Initially 
            closest_color = None

            for color in palette:
                r2, g2, b2 = color
                dist = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    closest_color = color
            print(f"The closest color to ({r1}, {g1}, {b1}) is {closest_color}\n")

            pass
        elif choice == '5':
            print("Goodbye!")
            break
        else:
           print("Invalid option. Choose between 1-5")

