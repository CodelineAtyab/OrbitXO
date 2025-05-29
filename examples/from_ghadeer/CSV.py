employees = [
    {"name": "Mariya", "age": 20, "salary": 3000, "company": "PDO"},
    {"name": "Hoor", "age": 36, "salary": 1200, "company": "Omantel"},
    {"name": "Arooba", "age": 25, "salary": 1400, "company": "Codeline"},
    {"name": "Haya", "age": 26, "salary": 900, "company": "OBB"},
    {"name": "Aya", "age": 24, "salary": 800, "company": "Infoline"},
    {"name": "Ghadeer", "age": 23, "salary": 1800, "company": "Asyad"}
]

file = open("examples/from_ghadeer/data.csv", "w")
for emp in employees:
    line = f"{emp['name']},{emp['age']},{emp['salary']},{emp['company'].strip()}"
    file.write(line + "\n")
file.close()

file = open("examples/from_ghadeer/data.csv", "r")
lines = file.readlines()
file.close()

print("Raw File Content:")
print(lines)

print("\nAll Employees:\n")
for emp in employees:
    print(f"{emp['name']} | Age: {emp['age']} | Salary: {emp['salary']} | Company: {emp['company']}")
print("\n")

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

print("Employees with Age > 23:\n")
for emp in employees:
    if emp["age"] > 23:
        print(f"{emp['name']} | Age: {emp['age']} | Salary: {emp['salary']} | Company: {emp['company']}")