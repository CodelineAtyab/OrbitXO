# Define two example strings
text = " Hello team  "
text2 = "start python programming"

# 1. Length of the string
print("1. Length of text:", len(text))

# 2. Concatenate (combine) strings
print("2. Concatenation:", text.strip() + "...")

# 3. Repeat a string
print("3. Repetition:", "Hi Team " * 3)

# 4. Change case of text
print("4. Uppercase:", text.upper())        # All letters become capital
print("5. Lowercase:", text.lower())         # All letters become small
print("6. Title Case:", text2.title())       # First letter of each word becomes capital

# 5. Search in text
print("7. Count 'l':", text.count("l"))        # Count how many times 'l' appears
print("8. Count 'l':", text.count("l"))         # Count how many times 'l' appears


# 6. Slice (cut) parts of the string
print("9. First 5 characters:", text[:5])
print("10. Last 3 characters:", text[-3:])


# 7. Split and join strings
words = text2.split()
print("11. Split into words:", words)
print("12. Join with dash:", "-".join(words))

# 8. Remove extra spaces
print("13. Strip spaces:", text.strip())

# 9. Replace words
print("14. Replace 'World' with 'Python':", text.replace("World", "Python"))

# 10. Format string using f-string
name = "Ghadeer"
score = 99.5
print(f"10. Hello {name}, your score is {score}")
