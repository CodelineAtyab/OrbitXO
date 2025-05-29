# Step 1: Save data
data = [
    "Name,Age,Salary",
    "haya,26,50000",
    "marya,24,60000",
    "muzna,24,65000",
    "aya,22,45000",
    "arooba,24,52000"
]

with open("data.csv", "w") as file:
    file.write("\n".join(data))

# Step 2: Read and calculate
with open("data.csv", "r") as file:
    lines = file.readlines()

ages = []
salaries = []
filtered = []

for line in lines[1:]:
    name, age, salary = line.strip().split(",")
    age = int(age)
    salary = int(salary)
    ages.append(age)
    salaries.append(salary)
    if age > 22:
        filtered.append(line.strip())

# Step 3: Show results
print("Age: min =", min(ages), "max =", max(ages), "avg =", sum(ages) / len(ages))
print("Salary: min =", min(salaries), "max =", max(salaries), "avg =", sum(salaries) / len(salaries))

# Step 4: Save filtered rows
with open("filtered_output.csv", "w") as file:
    file.write(lines[0])  # write header
    file.write("\n".join(filtered))
    file.write("\n")
