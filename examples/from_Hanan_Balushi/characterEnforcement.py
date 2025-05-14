text = input("Enter your text: ")

if len(text) >= 280:
    text = text[:280] + "..."

print(f"\n\nTruncated Text: {text}")