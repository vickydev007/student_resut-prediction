def students(attendance):
  if attendance>=75:
    return "Continue"
  elif 60<=attendance<75:
    return "low"
  else:
    return "Drop"

def validate(unit_test):
  weak=[]
  for unit in range(1,6):
    if unit_test[unit-1]<50:
      weak.append(f"Unit_{unit}")
  return weak
  