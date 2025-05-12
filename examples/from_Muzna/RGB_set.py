def to_hex(n):
    # Convert 0–255 to two-digit hex using division & remainder
    high = n // 16
    low = n % 16
    HEX_MAP = "0123456789ABCDEF"
    return HEX_MAP[high] + HEX_MAP[low]

def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{to_hex(r)}{to_hex(g)}{to_hex(b)}"



def rgb_Using_set():
    palette = [ ]
    while True:
        print("RGB Color Palette Manager\n")
        print("1. Add color")
        print("2. Display palette")
        print("3. Convert to hex")
        print("4. Exit")
        
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
            print("Goodbye!")
            break
        else:
           print("Invalid option. Choose between 1-4")

rgb_Using_set()

