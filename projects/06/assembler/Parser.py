class Parser:
  def __init__(self, input_file, output_file):
    self.resource = open(input_file, "r")
    self.destination = open(input_file, "w+")
    self.cmd_ind = -1
    if (not self.resource.open() or not self.destination.open()):
      print("Parser initialization failed, exit.")
      return -1
    else:
      return 0
  
  def get_codes(self):
    self.codes = self.resource.readlines()

  def get_next_cmd(self):
    if (self.cmd_ind < len(self.cmd_ind)):
      ind += 1
      self.current_cmd = self.codes[ind].strip()
      return True
    else:
      return False

  # return 0 for a command, 1 for c command
  def get_current_cmd_type(self): 
    return "@" not in self.current_cmd 
  
  def parse_a_command(self):
    return self.current_cmd[1:]

  def parse_c_command(self):
    cmd = self.current_cmd
    if "=" in cmd:
      cmd_list = cmd.split("=")
      dst = cmd_list[0].strip()
      cmd = cmd_list[1].strip()
    else:
      dst = "null"
    if ";" in cmd:
      cmd_list = cmd.split(";")
      jmp = cmd_list[1].strip()
      cmp = cmd_list[0].strip()
    else:
      jmp = "null"
      cmp = cmd.strip()
    return dst, cmp, jmp

  def write(self, cmd):
    self.destination.write(cmd)

  def close(self):
    self.resource.close()
    self.destination.close()