from Parser import Parser

parser = Parser("C:\\code\\nand2tetris\\projects\\06\\assembler\\Max.asm", "C:\\code\\nand2tetris\\projects\\06\\assembler\\max.hack")
count = 0
label_dic = {}
while count < len(parser.codes):
  parser.codes[count] = parser.codes[count].strip()
  if (not parser.codes[count]) or (parser.codes[count].startswith("//")):
    del parser.codes[count]
  elif parser.codes[count].startswith("("):
    label_dic[parser.codes[count][1:-1]] = count
    del parser.codes[count]
  else:
    parser.codes[count] = parser.codes[count].split("//")[0].strip()
    count += 1

print(parser.codes)
