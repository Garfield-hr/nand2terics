class Coder():
  CODE_LEN = 16
  def __init__(self):
    self.dst_dic = {}
    self.dst_dic['null'] = '000'
    self.dst_dic['M']    = '001'
    self.dst_dic['D']    = '010'
    self.dst_dic['MD']   = '011'
    self.dst_dic['A']    = '100'
    self.dst_dic['AM']   = '101'
    self.dst_dic['AD']   = '110'
    self.dst_dic['AMD']  = '111'

    self.jmp_dic = {}
    self.jmp_dic['null'] = '000'
    self.jmp_dic['JGT']  = '001'
    self.jmp_dic['JEQ']  = '010'
    self.jmp_dic['JGE']  = '011'
    self.jmp_dic['JLT']  = '100'
    self.jmp_dic['JNE']  = '101'
    self.jmp_dic['JLE']  = '110'
    self.jmp_dic['JMP']  = '111'

    self.cmp_dic = {}
    self.cmp_dic['0']    = '101010'
    self.cmp_dic['1']    = '111111'
    self.cmp_dic['-1']   = '111010'
    self.cmp_dic['D']    = '001100'
    self.cmp_dic['A']    = '110000'
    self.cmp_dic['!D']   = '001101'
    self.cmp_dic['!A']   = '110001'
    self.cmp_dic['-D']   = '001111'
    self.cmp_dic['-A']   = '110011'
    self.cmp_dic['D+1']  = '011111'
    self.cmp_dic['A+1']  = '110111'
    self.cmp_dic['D-1']  = '001110'
    self.cmp_dic['A-1']  = '110010'
    self.cmp_dic['D+A']  = '000010'
    self.cmp_dic['D-A']  = '010011'
    self.cmp_dic['A-D']  = '000111'
    self.cmp_dic['D&A']  = '000000'
    self.cmp_dic['D|A']  = '010101'

  def code_address(self, addr):
    bin_str_addr = str(bin(int(addr)))[2:]
    if len(bin_str_addr) < Coder.CODE_LEN:
      bin_str_addr = "0" * (Coder.CODE_LEN - len(bin_str_addr)) + bin_str_addr
      return bin_str_addr
    elif len(bin_str_addr) == Coder.CODE_LEN:
      return bin_str_addr
    else:
      return bin_str_addr[:16]
    
  def code_dst(self, dst):
    try:
      return self.dst_dic[dst]
    except:
      print("syntax error! ", dst, " is not a valid destination.")
  
  def code_cmp(self, cmp):
    try:
      return self.cmp_dic[cmp]
    except:
      print("syntax error! ", cmp, " is not a valid operation.")

  def code_jmp(self, jmp):
    try:
      return self.jmp_dic[jmp]
    except:
      print("syntax error! ", jmp, " is not a valid jump command.")
