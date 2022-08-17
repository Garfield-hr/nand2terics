import sys


class Parser:
  def __init__(self, source_file:str) -> None:
    try:
      source_file = open(source_file, 'r')
      self.source_codes = source_file.readlines()
      source_file.close()
      self.ind = 0
      self.current_code = ""
    except:
      print("Parser failed to open source file, quit.")
      sys.exit(1)

  def has_next_code(self) -> bool:
    return self.ind < len(self.source_codes)

  def ignore_current_code(self) -> bool:
    if not self.current_code.strip() or self.current_code.strip().startswith("//"):
      return True
    else:
      return False
    
  def get_next_code(self) -> bool:
    if not self.has_next_code():
      return False
    self.current_code = self.source_codes[self.ind]
    self.ind += 1
    # loop until it's not comment
    while self.ignore_current_code():
      if not self.has_next_code():
        return False
      self.current_code = self.source_codes[self.ind]
      self.ind += 1

    if "//" in self.current_code:
        self.current_code = self.current_code.split("//")[0]
    return True
  
  def get_current_code(self) -> str:
    return self.current_code