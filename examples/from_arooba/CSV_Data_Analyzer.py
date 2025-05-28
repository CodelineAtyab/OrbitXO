INPUT_FILE = "data.csv"
OUTPUT_FILE = "filtered_output.csv"

sample_data = [
    ["Name", "Age", "Salary"],
    ["Alice", "29", "50000"],
    ["Bob", "35", "60000"],
    ["Carol", "40", "65000"],
    ["Dave", "25", "45000"],
    ["Eve", "32", "52000"]
]

def create_sample_csv(file_path):
    try:
        f = open(file_path, "w")
        for row in sample_data:
            f.write(",".join(row) + "\n")
        f.close()
        print(f"Sample '{file_path}' created.\n")
    except:
        print("Error creating sample CSV.")

def read_csv(file_path):
    try:
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
        headers = lines[0].strip().split(",")
        data = []
        for line in lines[1:]:
            values = line.strip().split(",")
            row = {}
            for i in range(len(headers)):
                row[headers[i]] = values[i]
            data.append(row)
        return data, headers
    except:
        print("Error reading CSV.")
        return [], []

def is_numeric(val):
    if val == "":
        return False
    try:
        float(val)
        return True
    except:
        return False

def calculate_statistics(data, fields):
    stats = {}
    for field in fields:
        nums = []
        for row in data:
            if is_numeric(row[field]):
                nums.append(float(row[field]))
        if nums:
            total = 0
            for n in nums:
                total += n
            stats[field] = {
                "min": min(nums),
                "max": max(nums),
                "avg": total / len(nums)
            }
    return stats

def filter_rows(data, column, threshold):
    result = []
    for row in data:
        try:
            if float(row[column]) > threshold:
                result.append(row)
        except:
            continue
    return result

def write_csv(file_path, headers, data):
    try:
        f = open(file_path, "w")
        f.write(",".join(headers) + "\n")
        for row in data:
            f.write(",".join([row[h] for h in headers]) + "\n")
        f.close()
        print(f"Filtered data saved to '{file_path}'")
    except:
        print("Error writing CSV.")

def main():
    try:
        f = open(INPUT_FILE, "r")
        f.close()
    except:
        create_sample_csv(INPUT_FILE)

    data, headers = read_csv(INPUT_FILE)
    if not data:
        return

    numeric_cols = []
    for h in headers:
        if all(is_numeric(row[h]) for row in data):
            numeric_cols.append(h)

    print("Statistics:\n")
    stats = calculate_statistics(data, numeric_cols)
    for col in stats:
        print(f"{col}:")
        print(f"  Min: {stats[col]['min']}")
        print(f"  Max: {stats[col]['max']}")
        print(f"  Avg: {round(stats[col]['avg'], 2)}")
        print()

    print("Filtering rows where Age > 30...\n")
    filtered = filter_rows(data, "Age", 30)
    write_csv(OUTPUT_FILE, headers, filtered)

main()
