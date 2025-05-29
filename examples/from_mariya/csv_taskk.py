employees = [
    {"name": "Mariya", "age": 24, "salary": 4000, "company": "PDO"},
    {"name": "Hoor", "age": 32, "salary": 3000, "company": "Omantel"},
    {"name": "Arooba", "age": 20, "salary": 2800, "company": "Codeline "},
    {"name": "Haya", "age": 30, "salary": 3200, "company": "OBB"},
    {"name": "Aya", "age": 21, "salary": 2600, "company": "Infoline"},
    {"name": "Ghadeer", "age": 22, "salary": 2200, "company": "Asyad"}
]

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

filtered_employees = []
for emp in employees:
    if emp["age"] > 23:
        filtered_employees.append(emp)

print("Employees with Age > 23:\n")
for emp in filtered_employees:
    print(f"{emp['name']} | Age: {emp['age']} | Salary: {emp['salary']} | Company: {emp['company']}")