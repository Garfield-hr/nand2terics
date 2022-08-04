class CodeWriter:
  def __init__(self, dest_file:str) -> None:
    self.dest_file = open(dest_file, "w+")

  def write_code(self, code:str) -> None:
    self.dest_file.write(code)
    self.dest_file.write("\n")

  def close(self) -> None:
    self.dest_file.close()

