def string_to_array(string, split_by):
  string = string.replace("[", "")
  string = string.replace("]", "")
  string = string.replace("\"", "")

  return string.split(split_by)