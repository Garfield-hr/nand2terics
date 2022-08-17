from JackTokenizer import Tokenizer
from jackCompileEngine import CompileEngine
import sys, os
from xml.dom.minidom import Document

def tokenize_one_file(file_name:str) -> None:
  tk = Tokenizer(file_name)
  output_xml_name = file_name.replace(".jack", "M.xml")
  tg = tokenIter(tk.tokenize())
  ce = CompileEngine(tg, output_xml_name)
  ce.compile_class()

class tokenIter:
  def __init__(self, tokenizer_generator) -> None:
    self.tg = tokenizer_generator
    self.cache = []
    
  def next(self) -> tuple:
    if not self.cache:
      return next(self.tg)
    else:
      return self.cache.pop()
    
  def back(self, pair:tuple) -> None:
    self.cache.append(pair)
    
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: Python jackCompiler.py source.")
    
  file_names = []
  if os.path.isfile(sys.argv[1]):
    file_names.append(sys.argv[1])
  else:
    f_list = os.listdir(sys.argv[1])
    for file in f_list:
      if os.path.splitext(file)[1] == ".jack":
        file_names.append(sys.argv[1] + "\\" + file)  
        
  for file_name in file_names:
    tokenize_one_file(file_name)
