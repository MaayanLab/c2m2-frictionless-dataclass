def slugify(s):
  import re
  return re.sub(r'[^A-Za-z0-9_]', '', s)
