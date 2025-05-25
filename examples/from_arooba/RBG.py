def to_hex(n):
    high = n // 16
    low = n % 16
    HEX_MAP = "0123456789ABCDEF"
    return HEX_MAP[high] + HEX_MAP[low]

def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{to_hex(r)}{to_hex(g)}{to_hex(b)}"

palette=[]
while True:
    print("\nRGB Color Palette Manager:")
    print("1. Add Color")
    print("2. Display palette")
    print("3. Convert to hex ")
    print("4. find the closest color")
    print("5. Exit")

    choose=input("Choose an option:")

    if choose == "1":
        try:
            r = int(input("Enter the red value (0-255): "))
            g = int(input("Enter the green value (0-255): "))
            b = int(input("Enter the blue value (0-255): "))
            color= (r,g,b)
            palette.append(color)
            print(f"Color {color} added to palette")
        except:
            print("Invalid input. Please enter a number between 0 and 255.")

    elif choose=="2":
        print("\n2. Display palette")
        for i in range(len(palette)):
            print(f"{i+1}. {palette[i]}")

    elif choose=="3":
         indx = input("Enter color index: ")

         if indx.isdigit():
                idx = int(indx) - 1
                rgb = palette[idx]
                hex_code = rgb_to_hex(rgb)
                print(f"Hex code for {rgb}: {hex_code}")   
         else:
                print("Please enter a valid number.")


    elif choose =="4":
        print("4. find the closest color")
        if not palette:
                print("Palette is empty.")
        else:
                r = int(input("Enter red value: "))
                g = int(input("Enter green value: "))
                b = int(input("Enter blue value: "))
                closest = None
                min_distance = None

                for color in palette:
                    cr, cg, cb = color
                    #calculates the Euclidean distance squared between the input color and a palette: color.
                    dist = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2 
                    if min_distance is None or dist < min_distance:
                        min_distance = dist
                        closest = color

                print(f"The closest color to ({r}, {g}, {b}) is {closest}")

    elif choose=="5":
        print("Goodbye!!!!!!!!!!")
        break

    else:
        print("Invalid option. Please choose from 1 to 4.")
        
        



