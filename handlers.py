def is_float_digit(a:str):
    counter = 0
    if a[0] == '-':
        a = a[1:]
    for i in a:
      if i.isdigit() == False:
          if (i == '.' or i == ',') and counter == 0:
              counter += 1
          else:
              return False
    return True
