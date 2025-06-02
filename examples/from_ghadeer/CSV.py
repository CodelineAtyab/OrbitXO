employees = [
    {"name": "Mariya", "age": 20, "salary": 3000, "company": "PDO"},
    {"name": "Hoor", "age": 36, "salary": 1200, "company": "Omantel"},
    {"name": "Arooba", "age": 25, "salary": 1400, "company": "Codeline"},
    {"name": "Haya", "age": 26, "salary": 900, "company": "OBB"},
    {"name": "Aya", "age": 24, "salary": 800, "company": "Infoline"},
    {"name": "Ghadeer", "age": 23, "salary": 1800, "company": "Asyad"}
]

# 🔹 Step 1: Write the CSV with headers
try:
    with open("examples/from_ghadeer/data.csv", "w") as file:
        file.write("name,age,salary,company\n")
        for emp in employees:
            line = f"{emp['name']},{emp['age']},{emp['salary']},{emp['company'].strip()}"
            file.write(line + "\n")
except Exception as e:
    print("Error writing to file:", e)

# 🔹 Step 2: Read CSV and detect header
parsed_employees = []
try:
    with open("examples/from_ghadeer/data.csv", "r") as file:
        lines = file.readlines()

    # Check if first line is a header (non-numeric values)
    first_line = lines[0].strip().split(",")
    has_header = not any(word.strip().isnumeric() for word in first_line)

    data_lines = lines[1:] if has_header else lines

    for line in data_lines:
        parts = line.strip().split(",")
        if len(parts) != 4:
            continue  # skip malformed lines
        try:
            parsed_employees.append({
                "name": parts[0],
                "age": int(parts[1]),
                "salary": int(parts[2]),
                "company": parts[3]
            })
        except ValueError:
            print(f"Skipping line due to parsing error: {line.strip()}")

except FileNotFoundError:
    print("File not found.")
except Exception as e:
    print("Error reading from file:", e)

# 🔹 Step 3: Calculate statistics
def calculate_statistics(data, key):
    try:
        values = [emp[key] for emp in data]
        return {
            "min": min(values),
            "max": max(values),
            "avg": round(sum(values) / len(values), 2)
        }
    except Exception as e:
        print("Error calculating statistics:", e)
        return {"min": None, "max": None, "avg": None}

age_stats = calculate_statistics(parsed_employees, "age")
salary_stats = calculate_statistics(parsed_employees, "salary")

# 🔹 Step 4: Filter employees with Age > 23
filtered_employees = [emp for emp in parsed_employees if emp["age"] > 23]

# 🔹 Step 5: Write filtered results to new CSV
try:
    with open("examples/from_ghadeer/filtered_employees.csv", "w") as out_file:
        out_file.write("name,age,salary,company\n")
        for emp in filtered_employees:
            out_file.write(f"{emp['name']},{emp['age']},{emp['salary']},{emp['company']}\n")
except Exception as e:
    print("Error writing filtered results:", e)

# 🔹 Step 6: Show Final Output in Console
print("\nStatistics:")
print(f"Age -> Min: {age_stats['min']}, Max: {age_stats['max']}, Average: {age_stats['avg']}")
print(f"Salary -> Min: {salary_stats['min']}, Max: {salary_stats['max']}, Average: {salary_stats['avg']}")

print("\nEmployees with Age > 23:\n")
for emp in filtered_employees:
    print(f"{emp['name']} | Age: {emp['age']} | Salary: {emp['salary']} | Company: {emp['company']}")
