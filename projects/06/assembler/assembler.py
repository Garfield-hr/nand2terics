import sys
from Parser import Parser


if __name__=="__main__":
  if (len(sys.argv) != 3):
    print("Usage: Python assembler.py inputFile.asm outputFile.hack")
    sys.exit(-1)
  parser = Parser(sys.argv[1], sys.argv[2])
  # coder = Coder()
  while (parser.get_next_cmd()):
    if (parser.get_current_cmd_type()):
      dst, cmp, jmp = parser.parse_c_command()
      # out_cmd = coder.translate_c_cmd(dst, cmp, jmp)
      print("c command, dst:", dst, " cmp:", cmp, " jmp", jmp)
    else:
      address = parser.parse_a_command()
      # out_cmd = coder.translate_a_cmd(address)
      print("a command, address:", address)
    # parser.write(out_cmd)
  parser.close()
