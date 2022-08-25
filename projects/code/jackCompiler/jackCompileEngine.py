from xml.dom.minidom import Document, Element
from symbolTable import SymbolTable
from jackWriter import jackCodeWriter

os_allocate_func = "Memory.alloc"
os_string_new = "String.new"
os_string_append = "String.appendChar"

class VmVarKind:
    argument = "argument"
    local = "local"
    static = "static"
    constant = "constant"
    this = "this"
    that = "that"
    pointer = "pointer"
    temp = "temp"

class CompileEngine:
    def __init__(self, tg:iter, file_name:str, out_xml=False) -> None:
        self.tg = tg
        self.file_name = file_name
        self.out_xml = out_xml
        if out_xml:
          self.doc = Document()

    def compile_file(self) -> None:
      if self.out_xml:
        self.compile_class()
      else:
        self.compile_class_vm()
        
    def compile_class(self) -> None:
        root = self.doc.createElement("class")
        self.doc.appendChild(root)
        self.compile_token(parent=root, expected_token={"keyword": ["class"]})
        self.compile_token(parent=root, expected_token={"identifier": []})
        self.compile_token(parent=root, expected_token={"symbol": ["{"]})
        while self.compile_classVarDec(parent=root):
            pass
        while self.compile_subroutine_dec(parent=root):
            pass
        self.compile_token(parent=root, expected_token={"symbol": ["}"]})
        
        f = open(self.file_name, "w")
        self.doc.writexml(f, indent="\t", newl="\n", addindent="\t", encoding="utf-8")
        f.close()
              
    def compile_token(self, parent, expected_token:dict, allow_missing=False) -> bool:
        pair = self.tg.next()
        if not pair: # null, reach the end of the file
            return False
        kind, value = pair
        if (kind in expected_token) and (not expected_token[kind] or value in expected_token[kind]):
            node = self.doc.createElement(kind)
            node_text = self.doc.createTextNode(" " + value + " ")
            node.appendChild(node_text)
            parent.appendChild(node)
            return True
        else:
            if allow_missing:
                self.tg.back(pair)
                return False
            else:
                f = open(self.file_name, "w")
                self.doc.writexml(f, indent="\t", newl="\n", addindent="\t", encoding="utf-8")
                f.close()
                raise RuntimeError(f"Syntax error, expect {expected_token}, but get kind: {kind}, value: {value}")
        
    def compile_classVarDec(self, parent) -> bool:
        var_dec_node = self.doc.createElement("classVarDec")
        # (static | field ) 
        # type(int | char | boolean | className(identifier)) 
        # varName(identifier)
        # (, varName)*
        # ; 
        valid_keywords = ["static", "field"]
        if self.compile_token(parent=var_dec_node, expected_token={"keyword": valid_keywords}, allow_missing=True):
            type_keywords = ["int", "char", "boolean"]
            self.compile_token(parent=var_dec_node, expected_token={"keyword": type_keywords, "identifier": []})
            self.compile_token(parent=var_dec_node, expected_token={"identifier": []})
            while (self.compile_token(parent=var_dec_node, expected_token={"symbol": [","]}, allow_missing=True)):
                self.compile_token(parent=var_dec_node, expected_token={"identifier": []})
            self.compile_token(parent=var_dec_node, expected_token={"symbol": [";"]})
            parent.appendChild(var_dec_node)
            return True
        else:
            return False
    
    def compile_subroutine_dec(self, parent) -> bool:
        subroutine_dec_node = self.doc.createElement("subroutineDec")
        # (constructor | function | method)
        # (void | type)
        # subroutineName
        # (
        # parameterList
        # )
        # subroutineBody
        if self.compile_token(parent=subroutine_dec_node, expected_token={"keyword": ["constructor", "function", "method"]}, allow_missing=True):
            return_type = ["void", "int", "char", "boolean"]
            self.compile_token(parent=subroutine_dec_node, expected_token={"keyword": return_type, "identifier": []})
            self.compile_token(parent=subroutine_dec_node, expected_token={"identifier": []})
            self.compile_token(parent=subroutine_dec_node, expected_token={"symbol": ["("]})
            self.compile_parameterList(parent=subroutine_dec_node)
            self.compile_token(parent=subroutine_dec_node, expected_token={"symbol": [")"]})
            self.compile_subroutineBody(parent=subroutine_dec_node)
            parent.appendChild(subroutine_dec_node)
            return True
        else:
            return False
        
    def compile_parameterList(self, parent) -> None:
        parameterList_node = self.doc.createElement("parameterList")
        # (type varName (, type varName)*)?
        type_keywords = ["int", "char", "boolean"]
        if self.compile_token(parent=parameterList_node, expected_token={"keyword": type_keywords, "identifier": []}, allow_missing=True):
            self.compile_token(parent=parameterList_node, expected_token={"identifier": []})
            while self.compile_token(parent=parameterList_node, expected_token={"symbol", [","]}, allow_missing=True):
                self.compile_token(parent=parameterList_node, expected_token={"keyword": type_keywords, "identifier": []})
                self.compile_token(parent=parameterList_node, expected_token={"identifier": []})
        else:
            blank = self.doc.createTextNode("\n")
            parameterList_node.appendChild(blank)
        parent.appendChild(parameterList_node)
        
    def compile_subroutineBody(self, parent) -> None:
        subroutineBody_node = self.doc.createElement("subroutineBody")
        # { varDec* statements }
        self.compile_token(parent=subroutineBody_node, expected_token={"symbol": ["{"]})
        while self.compile_varDec(parent=subroutineBody_node):
            pass
        self.compile_statements(parent=subroutineBody_node)
        self.compile_token(parent=subroutineBody_node, expected_token={"symbol": ["}"]})
        parent.appendChild(subroutineBody_node)
        
    def compile_varDec(self, parent) -> bool:
        varDec_node = self.doc.createElement("varDec")
        # var type varName (, type varName)* ;
        if self.compile_token(parent=varDec_node, expected_token={"keyword": ["var"]}, allow_missing=True):
            type_keywords = ["int", "char", "boolean"]
            self.compile_token(parent=varDec_node, expected_token={"keyword": type_keywords, "identifier": []})
            self.compile_token(parent=varDec_node, expected_token={"identifier": []})
            while self.compile_token(parent=varDec_node, expected_token={"symbol": [","]}, allow_missing=True):
                self.compile_token(parent=varDec_node, expected_token={"identifier": []})
            self.compile_token(parent=varDec_node, expected_token={"symbol": [";"]})
            parent.appendChild(varDec_node)
            return True
        else:
            return False
    
    def compile_statements(self, parent) -> None:
        statements_node = self.doc.createElement("statements")
        while self.compile_statement(parent=statements_node):
            pass
        parent.appendChild(statements_node)
        pass
    
    def compile_statement(self, parent) -> bool:
        pair = self.tg.next()
        if not pair: # null, reach the end of the file
            return False
        _, value = pair
        self.tg.back(pair)
        if value == "let":
            self.compile_letStatement(parent=parent)
            return True
        elif value == "if":
            self.compile_ifStatement(parent=parent)
            return True
        elif value == "while":
            self.compile_whileStatement(parent=parent)
            return True
        elif value == "do":
            self.compile_doStatement(parent=parent)
            return True
        elif value == "return":
            self.compile_returnStatement(parent=parent)
            return True
        else:
            return False
            
    def compile_letStatement(self, parent) -> None:
        letStatement_node = self.doc.createElement("letStatement")
        # let varName ([ expression ])? = expression ;
        self.compile_token(parent=letStatement_node, expected_token={"keyword": ["let"]})
        self.compile_token(parent=letStatement_node, expected_token={"identifier": []})
        if self.compile_token(parent=letStatement_node, expected_token={"symbol": ["["]}, allow_missing=True):
            self.compile_expression(parent=letStatement_node)
            self.compile_token(parent=letStatement_node, expected_token={"symbol": ["]"]})
        self.compile_token(parent=letStatement_node, expected_token={"symbol": ["="]})
        self.compile_expression(parent=letStatement_node)
        self.compile_token(parent=letStatement_node, expected_token={"symbol": [";"]})
        parent.appendChild(letStatement_node)
    
    def compile_ifStatement(self, parent) -> None:
        ifStatement_node = self.doc.createElement("ifStatement")
        # if ( expression ) { statements } (else { statements })?
        self.compile_token(parent=ifStatement_node, expected_token={"keyword": ["if"]})
        self.compile_token(parent=ifStatement_node, expected_token={"symbol": ["("]})
        self.compile_expression(parent=ifStatement_node)
        self.compile_token(parent=ifStatement_node, expected_token={"symbol": [")"]})
        self.compile_token(parent=ifStatement_node, expected_token={"symbol": ["{"]})
        self.compile_statements(parent=ifStatement_node)
        self.compile_token(parent=ifStatement_node, expected_token={"symbol": ["}"]})
        if self.compile_token(parent=ifStatement_node, expected_token={"keyword": ["else"]}, allow_missing=True):
            self.compile_token(parent=ifStatement_node, expected_token={"symbol": ["{"]})
            self.compile_statements(parent=ifStatement_node)
            self.compile_token(parent=ifStatement_node, expected_token={"symbol": ["}"]})
        parent.appendChild(ifStatement_node)
    
    def compile_whileStatement(self, parent) -> None:
        whileStatement_node = self.doc.createElement("whileStatement")
        # while ( expression ) { statements }
        self.compile_token(parent=whileStatement_node, expected_token={"keyword": ["while"]})
        self.compile_token(parent=whileStatement_node, expected_token={"symbol": ["("]})
        self.compile_expression(parent=whileStatement_node)
        self.compile_token(parent=whileStatement_node, expected_token={"symbol": [")"]})
        self.compile_token(parent=whileStatement_node, expected_token={"symbol": ["{"]})
        self.compile_statements(parent=whileStatement_node)
        self.compile_token(parent=whileStatement_node, expected_token={"symbol": ["}"]})        
        parent.appendChild(whileStatement_node)
    
    def compile_doStatement(self, parent) -> None:
        doStatement_node = self.doc.createElement("doStatement")
        # do subroutineCall ;
        self.compile_token(parent=doStatement_node, expected_token={"keyword": ["do"]})
        self.compile_subroutineCall(parent=doStatement_node)
        self.compile_token(parent=doStatement_node, expected_token={"symbol": [";"]})
        parent.appendChild(doStatement_node)
        pass
    
    def compile_returnStatement(self, parent) -> None:
        return_node = self.doc.createElement("returnStatement")
        # return (expression)? ;
        self.compile_token(parent=return_node, expected_token={"keyword": ["return"]})
        if self.compile_token(parent=return_node, expected_token={"symbol": [";"]}, allow_missing=True):
            pass
        else:
            self.compile_expression(parent=return_node)
            self.compile_token(parent=return_node, expected_token={"symbol": [";"]})
        parent.appendChild(return_node)
    
    def compile_expression(self, parent) -> None:
        expression_node = self.doc.createElement("expression")
        self.compile_term(parent=expression_node)
        symbol_op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
        while self.compile_token(parent=expression_node, expected_token={"symbol": symbol_op}, allow_missing=True):
            self.compile_term(parent=expression_node)
        parent.appendChild(expression_node)
    
    def compile_expressionList(self, parent) -> None:
        expressionList_node = self.doc.createElement("expressionList")
        # expression (, expression)*
        self.compile_expression(parent=expressionList_node)
        while self.compile_token(parent=expressionList_node, expected_token={"symbol": [","]}, allow_missing=True):
            self.compile_expression(parent=expressionList_node)
        parent.appendChild(expressionList_node)
    
    def compile_term(self, parent) -> None:
        term_node = self.doc.createElement("term")
        # integerConstant     |
        # stringConstant      |
        # keywordConstant     |
        # varname             |
        # varName[expression] |
        # subroutineCall      |
        # (expression)        |
        # unaryOp term    
        pair = self.tg.next()
        if not pair: # null, reach the end of the file
            raise RuntimeError("syntax error, reach end of file and expect term")
        kind, value = pair
        self.tg.back(pair)    
        if kind == "integerConstant":
            self.compile_token(parent=term_node, expected_token={"integerConstant": []})
        elif kind == "stringConstant":
            self.compile_token(parent=term_node, expected_token={"stringConstant": []})
        elif kind == "keyword":
            keywordConstant = ["true", "false", "null", "this"]
            self.compile_token(parent=term_node, expected_token={"keyword": keywordConstant})
        elif kind == "symbol" and value == "(":
            self.compile_token(parent=term_node, expected_token={"symbol": ["("]})
            self.compile_expression(parent=term_node)
            self.compile_token(parent=term_node, expected_token={"symbol": [")"]})
        elif kind == "symbol" and value in ["-", "~"]:
            unaryOp = ["-", "~"]
            self.compile_token(parent=term_node, expected_token={"symbol": unaryOp})
            self.compile_term(parent=term_node)
        else:
            # kind == identifier
            pair1 = self.tg.next()
            pair2 = self.tg.next()
            if not pair2: # null, reach the end of the file
                # varName case
                self.tg.back(pair)
                self.compile_token(parent=term_node, expected_token={"identifier": []})
                return 
            _, value2 = pair2
            self.tg.back(pair2)
            self.tg.back(pair1)
            if value2 == "[":
                # varName[expression] case
                self.compile_token(parent=term_node, expected_token={"identifier": []})
                self.compile_token(parent=term_node, expected_token={"symbol": ["["]})
                self.compile_expression(parent=term_node)
                self.compile_token(parent=term_node, expected_token={"symbol": ["]"]})
            elif value2 in [".", "("]:
                # subroutineCall case
                self.compile_subroutineCall(parent=term_node)
            else:
                # varName case
                self.compile_token(parent=term_node, expected_token={"identifier": []})
        
        parent.appendChild(term_node)
                
    def compile_subroutineCall(self, parent) -> None:
        # no node in xml
        # (className | varname .) subroutineName ( expressionList )
        self.compile_token(parent=parent, expected_token={"identifier": []})
        if self.compile_token(parent=parent, expected_token={"symbol": ["."]}, allow_missing=True):
            self.compile_token(parent=parent, expected_token={"identifier": []})
        self.compile_token(parent=parent, expected_token={"symbol": ["("]})
        pair = self.tg.next()
        if not pair:
            raise RuntimeError("syntax error, reach end of file and expect )")
        _, value = pair
        self.tg.back(pair)
        if value == ")":
            expressionList_node = self.doc.createElement("expressionList")
            blank = self.doc.createTextNode("\n")
            expressionList_node.appendChild(blank)
            parent.appendChild(expressionList_node)
        else:
            self.compile_expressionList(parent=parent)
        self.compile_token(parent=parent, expected_token={"symbol": [")"]})

    def compile_class_vm(self) -> None:
        self.wr = jackCodeWriter(self.file_name)
        self.symbol_table = SymbolTable()
        self.label_num = 0

        self.symbol_table.construct_next_symbol_table()
        self.class_var_ind = {"static": 0, "this": 0}
        self.eat_token(expected_token={"keyword": ["class"]})
        _, self.class_name = self.eat_token(expected_token={"identifier": []})
        self.eat_token(expected_token={"symbol": ["{"]})
        while self.compile_classVarDec_vm():
            pass
        while self.compile_subroutineDec_vm():
            pass
        self.eat_token(expected_token={"symbol": ["}"]})

        self.wr.close()

    def eat_token(self, expected_token:dict, allow_missing=False) -> tuple:
        pair = self.tg.next()
        if not pair:
            return False
        kind, value = pair
        if (kind in expected_token) and (not expected_token[kind] or value in   expected_token[kind]):
            return True, value
        else:
            if allow_missing:
                self.tg.back(pair)
                return False, None
            else:
                raise RuntimeError(f"Syntax error, expect {expected_token}, but get kind: {kind}, value: {value}")
    
    def compile_classVarDec_vm(self) -> bool:
        # (static | field ) 
        # type(int | char | boolean | className(identifier)) 
        # varName(identifier)
        # (, varName)*
        # ;
        valid_keywords = ["static", "field"]
        has_var_dec, value = self.eat_token(expected_token={"keyword": valid_keywords}, allow_missing=True)
        if has_var_dec:
            kind = VmVarKind.static if value == "static" else VmVarKind.this
            type_keywords = ["int", "char", "boolean"]
            _, var_type = self.eat_token(expected_token={"keyword": type_keywords, "identifier": []})
            _, symbol_name = self.eat_token(expected_token={"identifier": []})
            self.symbol_table.add_symbol(symbol_name, var_type, kind, self.class_var_ind[kind])
            self.class_var_ind[kind] += 1
            has_next_var, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
            while has_next_var:
                _, symbol_name = self.eat_token(expected_token={"identifier": []})
                self.symbol_table.add_symbol(symbol_name, var_type, kind, self.class_var_ind[kind])
                self.class_var_ind[kind] += 1
                has_next_var, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
            self.eat_token(expected_token={"symbol": [";"]})
            return True
        else:
            return False

    def compile_subroutineDec_vm(self) -> bool:
        # (constructor | function | method)
        # (void | type)
        # subroutineName
        # (
        # parameterList
        # )
        # subroutineBody
        has_subroutine, function_type = self.eat_token(expected_token={"keyword": ["constructor", "function", "method"]}, allow_missing=True)
        if has_subroutine:
            self.symbol_table.construct_next_symbol_table()
            return_type = ["void", "int", "char", "boolean"]
            self.eat_token(expected_token={"keyword": return_type, "identifier": []})
            _, subroutine_name = self.eat_token(expected_token={"identifier": []})
            self.eat_token(expected_token={"symbol": ["("]})
            if function_type == "method":
                arg_num = self.compile_parameterList_vm(has_this=True)
            else:
                arg_num = self.compile_parameterList_vm(has_this=False)
            self.eat_token(expected_token={"symbol": [")"]})
            self.wr.write_function(self.class_name + "." + subroutine_name, arg_num)
            if function_type == "constructor": # call alloc to initialize obj
                self.wr.write_push(VmVarKind.constant, self.class_var_ind["this"])
                self.wr.write_call(os_allocate_func, 1)
                self.wr.write_push(VmVarKind.pointer, 0)
            self.compile_subroutineBody_vm()
            self.wr.write_code("") # add a blank line between functions
            self.symbol_table.pop_last_symbol_table()
            return True
        elif function_type == "function":
            pass
        else:
            return False

    def compile_parameterList_vm(self, has_this) -> int:
        # (type varName (, type varName)*)?
        type_keywords = ["int", "char", "boolean"]
        has_next_arg, arg_type = self.eat_token(expected_token={"keyword": type_keywords, "identifier": []}, allow_missing=True)
        arg_ind = 1 if has_this else 0
        if has_next_arg:
            symbol_kind = VmVarKind.argument
            _, arg_name = self.eat_token(expected_token={"identifier": []})
            self.symbol_table.add_symbol(arg_name, arg_type, symbol_kind, arg_ind)
            arg_ind += 1
            has_next_arg, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
            while has_next_arg:
                _, arg_type = self.eat_token(expected_token={"keyword": type_keywords, "identifier": []})
                _, arg_name = self.eat_token(expected_token={"identifier": []})
                self.symbol_table.add_symbol(arg_name, arg_type, symbol_kind, arg_ind)
                arg_ind += 1
                has_next_arg, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
        return arg_ind

    def compile_subroutineBody_vm(self) -> None:
        self.eat_token(expected_token={"symbol": ["{"]})
        self.local_ind = 0
        while self.compile_varDec_vm():
            pass
        self.compile_statements_vm()
        self.eat_token(expected_token={"symbol": ["}"]})

    def compile_varDec_vm(self) -> bool:
        has_var_dec, _ = self.eat_token(expected_token={"keyword": ["var"]}, allow_missing=True)
        if has_var_dec:
            var_kind = VmVarKind.local
            type_keywords = ["int", "char", "boolean"]
            _, var_type = self.eat_token(expected_token={"keyword": type_keywords, "identifier": []})
            _, var_name = self.eat_token(expected_token={"identifier": []})
            self.symbol_table.add_symbol(var_name, var_type, var_kind, self.local_ind)
            self.local_ind += 1
            has_next_var, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
            while has_next_var:
                _, var_name = self.eat_token(expected_token={"identifier": []})
                self.symbol_table.add_symbol(var_name, var_type, var_kind, self.local_ind)
                self.local_ind += 1
                has_next_var, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
            self.eat_token(expected_token={"symbol": [";"]})
            return True
        else:
            return False

    def compile_statements_vm(self) -> None:
        while self.compile_statement_vm():
            pass

    def compile_statement_vm(self) -> None:
        pair = self.tg.next()
        if not pair:
            return False
        _, value = pair
        self.tg.back(pair)
        if value == "let":
            self.compile_letStatement_vm()
            return True
        elif value == "if":
            self.compile_ifStatement_vm()
            return True
        elif value == "while":
            self.compile_whileStatement_vm()
            return True
        elif value == "do":
            self.compile_doStatement_vm()
            return True
        elif value == "return":
            self.compile_returnStatement_vm()
            return True
        else:
            return False

    def compile_letStatement_vm(self) -> None:
        # a ([exp1])? = exp2
        self.eat_token(expected_token={"keyword": ["let"]})
        _, symbol_name = self.eat_token(expected_token={"identifier": []})
        symbol_val = self.symbol_table.get_symbol_val(symbol_name)
        has_middle_bracket, _ = self.eat_token(expected_token={"symbol": ["["]}, allow_missing=True)
        if has_middle_bracket: # exp1
            self.wr.write_push(symbol_val.kind, symbol_val.ind)
            self.compile_expression_vm()
            self.wr.write_arithmetic("+")
            self.eat_token(expected_token={"symbol": ["]"]})
        self.eat_token(expected_token={"symbol": ["="]})
        self.compile_expression_vm() # exp2
        self.eat_token(expected_token={"symbol": [";"]})
        if has_middle_bracket:
            self.wr.write_pop(VmVarKind.temp, 0)
            self.wr.write_pop(VmVarKind.pointer, 1)
            self.wr.write_push(VmVarKind.temp, 0)
            self.wr.write_pop(VmVarKind.that, 0)
        else:
            self.wr.write_pop(symbol_val.kind, symbol_val.ind)

    def compile_ifStatement_vm(self) -> None:
        self.eat_token(expected_token={"keyword": ["if"]})
        self.eat_token(expected_token={"symbol": ["("]})
        self.compile_expression_vm()
        self.wr.write_arithmetic("~")
        label_else = "label" + str(self.label_num)
        self.label_num += 1
        label_end_if = "label" + str(self.label_num)
        self.label_num += 1
        self.wr.write_if(label_else)
        self.eat_token(expected_token={"symbol": [")"]})
        self.eat_token(expected_token={"symbol": ["{"]})
        self.compile_statements_vm()
        self.wr.write_goto(label_end_if)
        self.eat_token(expected_token={"symbol": ["}"]})
        self.wr.write_label(label_else)
        has_else, _ = self.eat_token(expected_token={"keyword": ["else"]}, allow_missing=True)
        if has_else:
            self.eat_token(expected_token={"symbol": ["{"]})
            self.compile_statements_vm()
            self.eat_token(expected_token={"symbol": ["}"]})
        self.wr.write_label(label_end_if)

    def compile_whileStatement_vm(self) -> None:
        label_while_cond = "label" + str(self.label_num) 
        self.label_num += 1
        label_out = "label" + str(self.label_num)
        self.label_num += 1
        self.eat_token(expected_token={"keyword": ["while"]})
        self.eat_token(expected_token={"symbol": ["("]})
        self.wr.write_label(label_while_cond)
        self.compile_expression_vm()
        self.wr.write_arithmetic("~")
        self.wr.write_if(label_out)
        self.eat_token(expected_token={"symbol": [")"]})
        self.eat_token(expected_token={"symbol": ["{"]})
        self.compile_statements_vm()
        self.wr.write_goto(label_while_cond)
        self.wr.write_label(label_out)
        self.eat_token(expected_token={"symbol": ["}"]})

    def compile_doStatement_vm(self) -> None:
      self.eat_token(expected_token={"keyword": ["do"]})
      self.compile_subroutineCall_vm()
      self.eat_token(expected_token={"symbol": [";"]})

    def compile_returnStatement_vm(self) -> None:
        self.eat_token(expected_token={"keyword": ["return"]})
        is_comma, _ = self.eat_token(expected_token={"symbol": [";"]}, allow_missing=True)
        if is_comma:
            self.wr.write_push(VmVarKind.constant, 0)
        else:
            self.compile_expression_vm()
            self.eat_token(expected_token={"symbol": [";"]})
        self.wr.write_return()

    def compile_expression_vm(self) -> None:
        self.compile_term_vm()
        symbol_op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]
        has_op, op = self.eat_token(expected_token={"symbol": symbol_op}, allow_missing=True)
        while has_op:
            self.compile_term_vm()
            self.wr.write_arithmetic(op)
            has_op, op = self.eat_token(expected_token={"symbol": symbol_op}, allow_missing=True)

    def compile_expressionList_vm(self) -> int:
        arg_num = 1
        self.compile_expression_vm()
        has_comma, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
        while has_comma:
            arg_num += 1
            self.compile_expression_vm()
            has_comma, _ = self.eat_token(expected_token={"symbol": [","]}, allow_missing=True)
        return arg_num

    def compile_term_vm(self) -> None:
        pair = self.tg.next()
        if not pair:
            raise RuntimeError("syntax error, reach end of file and expect term")
        kind, value = pair
        self.tg.back(pair)    
        if kind == "integerConstant":
            self.eat_token(expected_token={"integerConstant": []})
            self.wr.write_push(VmVarKind.constant, int(value))
        elif kind == "stringConstant":
            self.eat_token(expected_token={"stringConstant": []})
            self.wr.write_push(VmVarKind.constant, len(value))
            self.wr.write_call(os_string_new, 1)
            for char in value:
                self.wr.write_push(VmVarKind.constant, ord(char))
                self.wr.write_call(os_string_append, 2)
        elif kind == "keyword":
            keywordConstant = ["true", "false", "null", "this"]
            _, keyword = self.eat_token(expected_token={"keyword": keywordConstant})
            if keyword == "true":
                self.wr.write_push(VmVarKind.constant, 1)
            elif keyword == "false":
                self.wr.write_push(VmVarKind.constant, 0)
            elif keyword == "null":
                self.wr.write_push(VmVarKind.constant, 0)
            else: # this
                self.wr.write_push(VmVarKind.pointer, 0)
        elif kind == "symbol" and value == "(":
            self.eat_token(expected_token={"symbol": ["("]})
            self.compile_expression_vm()
            self.eat_token(expected_token={"symbol": [")"]})
        elif kind == "symbol" and value in ["-", "~"]:
            unaryOp = ["-", "~"]
            _, op = self.eat_token(expected_token={"symbol": unaryOp})
            self.compile_term_vm()
            if op == "-":
                self.wr.write_arithmetic("neg")
            else:
                self.wr.write_arithmetic("~")
        else:
            # kind == identifier
            pair1 = self.tg.next()
            pair2 = self.tg.next()
            if not pair2: # null, reach the end of the file
                # varName case
                self.tg.back(pair)
                _, symbol = self.eat_token(expected_token={"identifier": []})
                symbol_val = self.symbol_table.get_symbol_val(symbol)
                self.wr.write_push(symbol_val.kind, symbol_val.ind)
                return 
            _, value2 = pair2
            self.tg.back(pair2)
            self.tg.back(pair1)
            if value2 == "[":      
                # varName[expression] case
                _, arr_p = self.eat_token(expected_token={"identifier": []})
                arr_val = self.symbol_table.get_symbol_val(arr_p)
                self.wr.write_push(arr_val.kind, arr_val.ind)
                self.eat_token(expected_token={"symbol": ["["]})
                self.compile_expression_vm()
                self.wr.write_arithmetic("+")
                self.wr.write_pop(VmVarKind.pointer, 1)
                self.wr.write_push(VmVarKind.that, 0)
                self.eat_token(expected_token={"symbol": ["]"]})
            elif value2 in [".", "("]:
                # subroutineCall case
                self.compile_subroutineCall_vm()
            else:
                # varName case
                _, symbol = self.eat_token(expected_token={"identifier": []})
                symbol_val = self.symbol_table.get_symbol_val(symbol)
                self.wr.write_push(symbol_val.kind, symbol_val.ind)
                  
    def compile_subroutineCall_vm(self) -> None:
        _, func_name = self.eat_token(expected_token={"identifier": []})
        has_dot, _ = self.eat_token(expected_token={"symbol": ["."]}, allow_missing=True)
        if has_dot:
            _, func_name_after = self.eat_token(expected_token={"identifier": []})
            func_name += "." + func_name_after
        self.eat_token(expected_token={"symbol": ["("]})
        pair = self.tg.next()
        if not pair:
            raise RuntimeError("syntax error, reach end of file and expect )")
        _, value = pair
        self.tg.back(pair)
        arg_num = 0
        if value != ")":
            arg_num = self.compile_expressionList_vm()
        self.eat_token(expected_token={"symbol": [")"]})
        self.wr.write_call(func_name, arg_num)
        
