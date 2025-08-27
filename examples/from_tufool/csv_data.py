data = [
    "Name,Age,Salary",
    "Liam,31,72000",
    "Olivia,28,68000",
    "Noah,45,88000",
    "Emma,23,50000",
    "Ava,36,79000"
]

# Write the data to CSV
with open("data.csv", "w") as file:
    for line in data:
        file.write(line + "\n")

# Read the data with error handling
try:
    with open("data.csv", "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print("Error: data.csv not found.")
    lines = []
except PermissionError:
    print("Error: Permission denied when accessing data.csv.")
    lines = []
except Exception as e:
    print(f"Unexpected error: {e}")
    lines = []

ages = []
salaries = []
filtered = []

if lines:
    # Check if the first line is a header
    first_line = lines[0].strip().split(",")
    has_header = not all(item.isdigit() for item in first_line[1:])  # "Age" or "Salary" won't be numeric

    # Use appropriate lines depending on header presence
    data_lines = lines[1:] if has_header else lines[:]

    for line in data_lines:
        try:
            name, age, salary = line.strip().split(",")
            age = int(age)
            salary = int(salary)
            ages.append(age)
            salaries.append(salary)

            # Filtering ages > 30
            if age > 30:
                filtered.append(line.strip())
        except ValueError:
            print(f"Skipping invalid line: {line.strip()}")

    # Only calculate if we have valid data
    if ages and salaries:
        print("Age: min =", min(ages), "max =", max(ages), "avg =", sum(ages)//len(ages))
        print("Salary: min =", min(salaries), "max =", max(salaries), "avg =", sum(salaries)//len(salaries))

        # Save filtered rows (with header if present)
        with open("filtered_tech_employees.csv", "w") as file:
            if has_header:
                file.write(lines[0])
            for row in filtered:
                file.write(row + "\n")
