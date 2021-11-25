def string_to_array(string, split_by):
  string = string.replace("[", "")
  string = string.replace("]", "")
  string = string.replace("\"", "")

  return string.split(split_by)

"""
[{tesla,bleh}, {covid}]
"""

def string_objects_to_array(in_str):
  in_str = in_str.replace("[", "")
  in_str = in_str.replace("]", "")
  in_str = in_str.replace("\"", "")
  
  result = []
  for i in in_str.split("{"):
    if i:
      i = i.replace("{", "")
      i = i.replace("}", "")
      i = i.strip()
      i = i.rstrip(",")
      temp_arr = []
      for a in i.split(","):
        temp_arr.append(a)
      result.append(temp_arr)

  return result  
