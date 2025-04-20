"""
2 x 1 = 2
2 x 2 = 4
2 x 3 = 6
2 x 4 = 8
2 x 5 = 10
"""

# DRY RUN IT FIRST
"Hello " + "Team Code " + "Orbit" + "3"
"Hello Team Code Orbit"

# Step 1: Assign next value to current day
# current_day = "Wednesday"
for current_num in range(1, 6):  # 1 -- 2 
    # Step 2: Go inside and do anything with current_day
    result = 2 *current_num  # 2 -- 4
    print("2 x " + str(current_num) + " = " + str(result))
    # 2 x 1 = 2 -- 2 x 2 = 4
    # Step 3: Go inside again if there is a next value

print("I am finally outside of the loop")