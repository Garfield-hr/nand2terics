from curses.ascii import isdigit


class Parser:
  REGISTER_START = 15
  def __init__(self, input_file, output_file):
    self.resource = open(input_file, "r")
    self.get_codes()
    self.destination = open(output_file, "w+")
    self.cmd_ind = -1
    self.label_dic = {}
    self.symbol_dic = {
      "R0" : 0,
      "R1" : 1,
      "R2" : 2,
      "R3" : 3,
      "R4" : 4,
      "R5" : 5,
      "R6" : 6,
      "R7" : 7,
      "R8" : 8,
      "R9" : 9,
      "R10" : 10,
      "R11" : 11,
      "R12" : 12,
      "R13" : 13,
      "R14" : 14,
      "R15" : 15,
      "SP" : 0,
      "LCL" : 1,
      "ARG" : 2,
      "THIS" : 3,
      "THAT" : 4,
      "SCREEN" : 16384,
      "KBD" : 24576
    }
  
  def get_codes(self):
    self.codes = self.resource.readlines()

  def pre_process(self):
    count = 0
    # first pass delete all comments blank and labels
    while count < len(self.codes):
      self.codes[count] = self.codes[count].strip()
      if (not self.codes[count]) or (self.codes[count].startswith("//")):
        del self.codes[count]
      elif self.codes[count].startswith("("):
        self.label_dic[self.codes[count][1:-1]] = count
        del self.codes[count]
      else:
        self.codes[count] = self.codes[count].split("//")[0].strip()
        count += 1
    #second pass: replace all symbols
    register_used = 0
    for ind in range(len(self.codes)):
      if "@" in self.codes[ind]:
        addr = self.codes[ind][1:]
        if not addr.isdigit():
          if addr in self.label_dic:
            self.codes[ind] = "@" + str(self.label_dic[addr])
          elif addr in self.symbol_dic:
            self.codes[ind] = "@" + str(self.symbol_dic[addr])
          else:
            register_used += 1
            self.symbol_dic[addr] = Parser.REGISTER_START + register_used
            self.codes[ind] = "@" + str(Parser.REGISTER_START + register_used)


  def get_next_cmd(self):
    if (self.cmd_ind + 1 < len(self.codes)):
      self.cmd_ind += 1
      self.current_cmd = self.codes[self.cmd_ind].strip()
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
    if "," in cmd:
      cmd_list = cmd.split(",")
      jmp = cmd_list[1].strip()
      cmp = cmd_list[0].strip()
    else:
      jmp = "null"
      cmp = cmd.strip()
    return dst, cmp, jmp

  def write(self, cmd):
    self.destination.write(cmd)
    self.destination.write("\n")

  def close(self):
    self.resource.close()
    self.destination.close()