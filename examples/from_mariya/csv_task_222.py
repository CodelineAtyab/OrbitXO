# Step 1: Read from original CSV
file = open("examples/from_mariya/csv_content.csv", "r")
csv_content = file.readlines()
file.close()

# Step 2: Parse lines into list of employees
employees = []
for line in csv_content:
    parts = line.strip().split(",")
    if len(parts) == 4:
        name, age, salary, company = parts
        employees.append({
            "name": name,
            "age": int(age),
            "salary": float(salary),
            "company": company.strip()
        })

# Step 3: Calculate statistics
def calculate_statistics(data, key):
    values = [emp[key] for emp in data]
    return {
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values)
    }

age_stats = calculate_statistics(employees, "age")
salary_stats = calculate_statistics(employees, "salary")

print("Statistics:")
print(f"Age -> Min: {age_stats['min']}, Max: {age_stats['max']}, Average: {age_stats['avg']}")
print(f"Salary -> Min: {salary_stats['min']}, Max: {salary_stats['max']}, Average: {salary_stats['avg']}")
print("\n")

# Step 4: Filter employees
filtered_employees = [emp for emp in employees if emp["age"] > 23]

print("Employees with Age > 23:\n")
for emp in filtered_employees:
    print(f"{emp['name']} | Age: {emp['age']} | Salary: {emp['salary']} | Company: {emp['company']}")

# Step 5: Write filtered employees to new CSV
file = open("examples/from_mariya/data.csv", "w")
for emp in filtered_employees:
    line = f"{emp['name']},{emp['age']},{emp['salary']},{emp['company']}"
    file.write(line + "\n")
file.close()

# Step 6: Read and print new file content
file = open("examples/from_mariya/data.csv", "r")
lines = file.readlines()
file.close()

print("\nRaw File Content (Filtered Data Written to New CSV):")
print(lines)
