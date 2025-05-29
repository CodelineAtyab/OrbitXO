# Contacts Backup Application
contact_book = dict() # Collection of key: value pairs

# List of contacts
[["92011497", "Atyab"], ["71143233", "Tariq"], ["95477222", "Arooba"]]

# Add Items to a dictionary
contact_book["92011497"] = "Atyab"
contact_book["71143233"] = "Tariq"
contact_book["95477222"] = "Arooba"
contact_book["71132323"] = "Ghadeer"


# Get a specific Item
# print(contact_book["12345678"])
print(contact_book.get("71143233", "ANONYMOUS"))

# Update an existing Item
contact_book["92011497"] = "Syed Atyab"

# Remove specific key value pair using the key
del contact_book["92011497"]



