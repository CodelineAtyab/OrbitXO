data = [
    "Name,Age,Salary",
    "Liam,31,72000",
    "Olivia,28,68000",
    "Noah,45,88000",
    "Emma,23,50000",
    "Ava,36,79000"
]

file = open("data.csv", "w")
for line in data:
    file.write(line + "\n")
file.close()

file = open("data.csv", "r")
lines = file.readlines()
file.close()

ages = []
salaries = []
filtered = []

for line in lines[1:]:
    name, age, salary = line.strip().split(",")
    age = int(age)
    salary = int(salary)
    ages.append(age)
    salaries.append(salary)
    if age > 30:
        filtered.append(line.strip()) #filtering ages > 30

print("Age: min =", min(ages), "max =", max(ages), "avg =", sum(ages)//len(ages))
print("Salary: min =", min(salaries), "max =", max(salaries), "avg =", sum(salaries)//len(salaries))

#Save filtered rows
file = open("filtered_tech_employees.csv", "w")
file.write(lines[0])  
for row in filtered:
    file.write(row + "\n")
file.close()
