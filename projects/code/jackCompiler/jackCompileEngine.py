from xml.dom.minidom import Document


class CompileEngine:
    def __init__(self, tg:iter, file_name:str) -> None:
        self.tg = tg
        self.doc = Document()
        self.file_name = file_name
        
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
            self.compile_token(parent=varDec_node, expected_token={"keyword": type_keywords, "identifier": []}, allow_missing=True)
            self.compile_token(parent=varDec_node, expected_token={"identifier": []})
            while self.compile_token(parent=varDec_node, expected_token={"symbol": [","]}, allow_missing=True):
                self.compile_token(parent=varDec_node, expected_token={"keyword": type_keywords, "identifier": []})
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