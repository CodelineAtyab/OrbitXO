import csv

def read_csv_file(filename):
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print("File not found:", filename)
        return []
    except Exception as e:
        print("Error reading file:", e)
        return []

def calculate_statistics(data, column_name):
    try:
        numbers = [float(row[column_name]) for row in data if row[column_name].strip()]
        if numbers:
            return {
                "min": min(numbers),
                "max": max(numbers),
                "avg": sum(numbers) / len(numbers)
            }
        else:
            return {}
    except Exception as e:
        print(f"Error calculating stats for {column_name}:", e)
        return {}

def filter_rows(data, column_name, condition_func):
    try:
        return [row for row in data if condition_func(float(row[column_name]))]
    except Exception as e:
        print("Error filtering rows:", e)
        return []

def write_to_csv(filename, data):
    try:
        if data:
            with open(filename, "w", newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print("Filtered data written to", filename)
        else:
            print("No data to write.")
    except Exception as e:
        print("Error writing file:", e)

def main():
    input_file = "examples/from_mariya/employees.csv"
    output_file = "filtered_employees.csv"

    data = read_csv_file(input_file)

    if data:
        print("Statistics for 'age':", calculate_statistics(data, "age"))
        print("Statistics for 'salary':", calculate_statistics(data, "salary"))

        filtered_data = filter_rows(data, "age", lambda age: age > 27)

        write_to_csv(output_file, filtered_data)

if __name__ == "__main__":
    main()