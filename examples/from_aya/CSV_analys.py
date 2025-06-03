data = [
    "Name,Age,Salary",
    "John,28,48000",
    "Jane,34,57000",
    "Mike,45,72000",
    "Anna,22,40000",
    "Sophia,30,51000"
]

file = open("data.csv", "w")
for line in data:
    file.write(line + "\n")
file.close()

# Step 2: Read and calculate
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
        filtered.append(line.strip())

# Step 3: Show results
print("Age: min =", min(ages), "max =", max(ages), "avg =", sum(ages)//len(ages))
print("Salary: min =", min(salaries), "max =", max(salaries), "avg =", sum(salaries)//len(salaries))

# Step 4: Save filtered rows
file = open("filtered_output.csv", "w")
file.write(lines[0])  # write header
for row in filtered:
    file.write(row + "\n")
file.close()