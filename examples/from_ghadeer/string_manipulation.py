# Define two example strings
text = " Hello, team  "
text2 = "start python programming"

# 1. Length of the string
print("1. Length of text:", len(text))

# 2. Concatenate (combine) strings
print("2. Concatenation:", text.strip() + "...")

# 3. Repeat a string
print("3. Repetition:", "Hi Team " * 3)

# 4. Change case of text
print("4. Uppercase:", text.upper())        # All letters become capital


# 5. Search in text
print("5. Count 'l':", text.count("l"))        # Count how many times 'l' appears

# 6. Slice (cut) parts of the string
print("6. First 5 characters:", text[:5])


# 7. Split and join strings
words = text2.split()
print("7. Split into words:", words)


# 8. Remove extra spaces
print("8. Strip spaces:", text.strip())

# 9. Replace words
print("9. Replace 'World' with 'Python':", text.replace("World", "Python"))

# 10. Format string using f-string
name = "Ghadeer"
score = 98.5
print(f"10. Hello {name}, your score is {score}")
