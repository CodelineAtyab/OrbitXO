def sleep_in(weekday, vacation):
  if not weekday or vacation: 
    return True
  if weekday or not vacation:
    return False 