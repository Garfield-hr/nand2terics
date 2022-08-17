import sys, re


class Tokenizer:
    def __init__(self, source_file: str) -> None:
        try:
            source_file = open(source_file, 'r')
            self.text = source_file.read()
            source_file.close()
            # remove comments
            self.text = re.sub("//.*\n", "", self.text)
            self.text = re.sub("/\*\*(.*?)\*/", "", self.text, flags=re.S)
            
            self.keywords = ["class", "method", "function", "constructor", "int", "boolean", "char", "void", "var",
                             "static", "field", "let", "do", "if", "else", "while", "return", "true", "false", "null", "this"]
            self.symbols = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
            self.token_specification = [
                ("integerConstant", r"\d+(\.d*)?"),
                ("identifier", r"\w+"),
                ("stringConstant", r"\".*\""),
                ("skip", r"[\s]+"),
                ("symbol", r"[{}()[\].,;+\-*/&|<>=~]"),
                ("mismatch", r".")
            ]
            self.tok_regex = "|".join("(?P<%s>%s)" % pair for pair in self.token_specification)
        except:
            print("Tokenizer failed to open source file, quit.")
            sys.exit(1)
            
    def tokenize(self) -> iter:
        for mo in re.finditer(self.tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "identifier" and value in self.keywords:
                kind = "keyword"
            elif kind == "stringConstant":
                value = value[1:-1]
            elif kind == "skip":
                continue
            elif kind == "mismatch":
                raise RuntimeError(f"{value} mismatch.")
            yield (kind, value)