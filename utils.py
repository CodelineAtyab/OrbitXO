def convert_two_digit_string_to_tuple(given_str):
  """
  Convert the given string that would contain only two numeric digits into Tuple of integers
  Returns: Tuple of two integers
  """
  tuple_to_return = (0, 0)

  if given_str.isdigit() and len(given_str) >= 2:
    tuple_to_return = (int(given_str[0]), int(given_str[1]))

  return tuple_to_return

if __name__ == "__main__":
  print(convert_two_digit_string_to_tuple("01"))
  print(convert_two_digit_string_to_tuple("0121212"))
  print(convert_two_digit_string_to_tuple(""))
  print(convert_two_digit_string_to_tuple("asdsada"))