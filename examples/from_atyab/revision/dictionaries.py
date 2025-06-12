contact_book = {
  "92013225": {"name": "Mr.A", "belongings": [
      {"id": 123, "codes": [{"type": "pin", "value": "1234"}]}, 
      {"id": 123, "codes": [{"type": "pin", "value": "1234"}]}, 
      {"id": 123, "codes": [{"type": "pin", "value": "1234"}]}
    ]}
}

print(contact_book["92013225"]["belongings"][0]["codes"][0]["value"])

d = {"name": {"a": 1, "b": 2}}