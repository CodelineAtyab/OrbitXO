from typing import List, Tuple

def validate_address_basic(addr: str) -> Tuple[bool, List[str]]:
    """Very simple validation:
    - Non-empty
    - Length >= 10
    - Contains at least one comma (e.g., "Street, City")
    """
    errors = []
    if not addr or not addr.strip():
        errors.append("Address cannot be empty.")
    if addr and len(addr.strip()) < 10:
        errors.append("Address seems too short.")
    if "," not in addr:
        errors.append("Address should include a comma, e.g., 'Street, City'.")
    return (len(errors) == 0, errors)
