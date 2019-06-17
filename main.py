import re
import sys
class Node:
    """
    DO NOT CREATE A NODE OBJECT, this class defines what a node is.
    """
    def __init__(self):
        self.value = None
        self.children = None
    
    def Evaluate(self, symbolTable):
        pass

class Identifier(Node):
    """
    Value: name of the identifier
    Children: None
    Evaluate: Returns its value
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        try:
            return symbolTable.get(self.value)
        except:
            raise ValueError("Identifier: ", self.value, " does not exists")

class Assignment(Node):
    """
    Value: None
    Children: 2 (0: Identifier, 1: RelExpression)
    Evaluate: sets 'identifier' value in symbolTable with value 'RelExpression'
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable): #receber SymbolTable
        relExp = self.children[1].Evaluate(symbolTable)
        currentType = symbolTable.get(self.children[0].value)[1] #Cobre o erro de nao existir 
        if(currentType == "BOOLEAN" and relExp[1] == "BOOLEAN"): #Cobre erro de unmatch de tipos
            symbolTable.setValue(self.children[0].value, relExp[0])
        elif(currentType == "INTEGER" and relExp[1] == "INTEGER"):
            symbolTable.setValue(self.children[0].value, relExp[0])
        else:
            raise ValueError(f"Can't assign value {relExp[0]} to {self.children[0].value}, types do not match")
        return 1

class Print(Node):
    """
    Value: None
    Children: 1 (0: RelExpression)
    Evaluate: print on terminal children[0].Evaluate()
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        print(self.children[0].Evaluate(symbolTable)[0])
        return 

class Statements(Node):
    """ 
    Value: None
    Children: All SubDecs and FuncDecs of program
    Evaluate: Evaluate of each children and call a FunCall for Main Function
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        for children in self.children:
            children.Evaluate(symbolTable)


class While(Node):
    """
    Value: None
    Children: 2 (0: BinOp, 1: [Statements])
    Evaluate: while children[0].Evaluate() == True:
                children[1].Evaluate()
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        if(self.children[0].Evaluate(symbolTable)[1] == "BOOLEAN"):
            while self.children[0].Evaluate(symbolTable)[0]:
                for child in self.children[1]:
                    child.Evaluate(symbolTable)
        else:
            raise ValueError("Invalid type for while clause")

class If(Node):
    """
    Value: None
    Children: 2 without else statement (0: BinOp, 1: Statements) | 
              3 with else statement    (0: BinOp, 1: Statements, 2: Statements)
    Evaluate: If children[0].Evaluate() == True
                children[1].Evaluate()
              Else, if children[2] exists:
                children[2].Evaluate()
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        child0 = self.children[0].Evaluate(symbolTable)
        if(child0[1] == "BOOLEAN"):
            if(self.children[0].Evaluate(symbolTable)[0]):
                for child in self.children[1]:
                    child.Evaluate(symbolTable)
            else:
                if(len(self.children) == 3):
                    for child in self.children[2]:
                        child.Evaluate(symbolTable)
        else:
            raise ValueError("Invalid type for while clause")


class Input(Node):
    """
    Value: None
    Children: 0
    Evaluate: Get terminal input
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def Evaluate(self, symbolTable):
        try:
            return [int(input()), "INTEGER"]
        except:
            raise ValueError("Input can't accepts values that are not INTEGER")

class BinOp(Node):
    """
    Value: Operation
    Children: 2 (0: RelExpression, 1: RelExpression)
    Evaluate: returns children[0].Evaluate Operation children[1].Evaluate
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        child0 = self.children[0].Evaluate(symbolTable)
        child1 = self.children[1].Evaluate(symbolTable)
        if(self.value == "PLUS"):
            if(child0[1] == "INTEGER" and child1[1] == "INTEGER"):
                return (child0[0] + child1[0], "INTEGER")
            else:
                raise ValueError("Can't sum two not INTEGERs values")
            
        elif(self.value == "MINUS"):
            if(child0[1] == "INTEGER" and child1[1] == "INTEGER"):
                return (child0[0] - child1[0], "INTEGER")
            else:
                raise ValueError("Can't subtract two not INTEGERs values")
        
        elif(self.value == "MULT"):
            if(child0[1] == "INTEGER" and child1[1] == "INTEGER"):
                return (child0[0] * child1[0], "INTEGER")
            else:
                raise ValueError("Can't multiply two not INTEGERs values")
        
        elif(self.value == "DIV"):
            if(child0[1] == "INTEGER" and child1[1] == "INTEGER"):
                return (child0[0] // child1[0], "INTEGER")
            else:
                raise ValueError("Can't divide two not INTEGERs values")
        
        elif(self.value == "GREATERTHAN"):
            if(child0[1] == "INTEGER" and child1[1] == "INTEGER"):
                return (child0[0] > child1[0], "BOOLEAN")
            else:
                raise ValueError("Can't compare two not INTEGER values")
        
        elif(self.value == "LESSTHAN"):
            if(child0[1] == "INTEGER" and child1[1] == "INTEGER"):
                return (child0[0] < child1[0], "BOOLEAN")
            else:
                raise ValueError("Can't compare two not INTEGER values")

        elif(self.value == "OR"):
            if(child0[1] == "BOOLEAN" and child1[1] == "BOOLEAN"):
                return (child0[0] or child1[0], "BOOLEAN")
            else:
                raise ValueError("Can't compare two not BOOLEAN values")
        
        elif(self.value == "AND"):
            if(child0[1] == "BOOLEAN" and child1[1] == "BOOLEAN"):
                return (child0[0] and child1[0], "BOOLEAN")
            else:
                raise ValueError("Can't compare two not BOOLEAN values")
        
        elif(self.value == "EQUAL"):
            if(child0[1] == child1[1]):
                return (child0[0] == child1[0], "BOOLEAN")
            else:
                raise ValueError("Can't compare INTEGER with BOOLEAN")

class UnOp(Node):
    """
    Value: None
    Children: 1 (1: IntVal)
    Evaluate: -|+|not int
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        child = self.children[0].Evaluate(symbolTable)
        if(self.value == "MINUS"):
            if(child[1] == "INTEGER"):
                return [-child[0], child[1]]
            else:
                raise ValueError("Invalid type for operation MINUS")

        elif(self.value == "PLUS"):
            if(child[1] == "INTEGER"):
                return [+child[0], child[1]]
            else:
                raise ValueError("Invalid type for operation PLUS")
        
        elif(self.value == "NOT"):
            if(child[1] == "BOOLEAN"):
                return [not child[0], child[1]]
            else:
                raise ValueError("Invalid type for operation NOT")

class IntVal(Node):
    """
    Value: int
    Children: None
    Evaluate: returns its value
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        if(isinstance(self.value, int)):
            return [self.value, "INTEGER"]
        else:
            raise ValueError(f"Value: {self.value} not valid")

class NoOp(Node):
    """
    Value: None
    Children: None
    Evaluate: pass
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        pass
    
class Type(Node):
    """
    Value: BOOLEAN | INTEGER)
    Children: None
    Evaluate: returns its value
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        return self.value

class BoolVal(Node):
    """
    Value: True | False 
    Children: None
    Evaluate: returns its value
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        return (self.value, "BOOLEAN")

class VarDec(Node):
    """
        Variable Declaration
        Value: None
        Children: 2 (0: Identifier, 1: Type)
        Evaluate: create the identifier key and its type inside SymbolTable
    """
    def __init__(self, value, children): 
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        symbolTable.create(self.children[0].value, self.children[1].Evaluate(symbolTable))
    
class SubDec(Node):
    """
        Sub Declaration
        Value: Sub name
        Children: n (0: Type, n-1: Statements)
        Evaluate: Declare itself in Symbol Table, with your type and a pointer for itself.
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        symbolTable.create(self.value, "SUB")#nome, tipo, valor
        symbolTable.setValue(self.value, self)

class FuncDec(Node):
    """
        Func Declaration
        Value: Function name
        Children: n (0: Type, n-1: Statements)
        Evaluate: Declare itself in Symbol Table, with your type and a pointer for itself.
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        symbolTable.create(self.value, "FUNC")#nome, tipo, valor
        symbolTable.setValue(self.value, self)

class SubFuncCall(Node):
    """
        Sub Call
        Value: Sub Name
        Children: n, where n is the number of arguments that SubDec specifies.
        Evaluate: run SubDec.
            1) Recupera o nó na symbolTable
            2) Cria uma nova ST
                - Coloca o nome na ST com o tipo do 1o filho
            3) Evaluate do 2o filho ate o n-1 (VarDecs), populando a ST
                - Popular a ST com os argumentos de entrada
            4) Evaluate do n-esimo filho (stmts)
            5) Se Func, retorna a variavel com o nome "value" ST 
    """
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        pointer, type = symbolTable.getPointer(self.value) #0: Value, 1: Type
        if(type == "SUB"):
            st = SymbolTable(parent=symbolTable)
            # st.create(self.value, "SUB")
            n = 0
            for child in pointer.children[0:-1]: #Evaluate dos VarDecs
                child.Evaluate(st) 
                try:
                    st.setValue(child.children[0].value, self.children[n].Evaluate(symbolTable)[0])
                    n += 1
                except:
                    raise ValueError(f"""Sub {self.value} expected {len(pointer.children[1:-2])} arguments
                                       but {len(self.children)} were given""")
            pointer.children[-1].Evaluate(st)

        elif(type == "FUNC"):
            st = SymbolTable(parent=symbolTable)
            st.create(self.value, pointer.children[0].Evaluate(st))
            n = 0 #variavel de deslocamento dos childrens do subcall em relacao ao children[1:-2]
            for child in pointer.children[1:-1]: #Evaluate dos VarDecs
                child.Evaluate(st) 
                try:
                    st.setValue(child.children[0].value, self.children[n].Evaluate(symbolTable)[0])
                    n += 1
                except:
                    raise ValueError(f"""Sub {self.value} expected {len(pointer.children[1:-2])} arguments
                                       but {len(self.children)} were given""")
            pointer.children[-1].Evaluate(st)
            return st.get(self.value)
           

class Token:
    def __init__(self, t, v,):
        self.type = t
        self.value = v

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        current_token = ""

        #Verifica se nao esta no final do arquivo
        if(self.position == len(self.origin)):
            new_token = Token("EOF", "EOF")
            self.actual = new_token
            return new_token

        #maquina de estados de procurar os tokens
        while ( self.position < len(self.origin) ):

            aux = self.origin[self.position]
            if(aux == ' '):
                self.position += 1

            elif(aux == "+"):
                new_token = Token("PLUS", "+")
                self.position += 1
                self.actual = new_token
                return new_token

            elif(aux == "-"):
                new_token = Token("MINUS", "-")
                self.position += 1
                self.actual = new_token
                return new_token

            elif(aux == "/"):
                new_token = Token("DIV", "/")
                self.position += 1
                self.actual = new_token
                return new_token

            elif(aux == "*"):
                new_token = Token("MULT", "*")
                self.position += 1
                self.actual = new_token
                return new_token

            elif(aux == "("):
                new_token = Token("(", "(")
                self.position += 1
                self.actual = new_token
                return new_token

            elif(aux == ")"):
                new_token = Token(")", ")")
                self.position += 1
                self.actual = new_token 
                return new_token

            elif(aux == "="):
                new_token = Token("ASSIGNMENT", "=")
                self.position += 1
                self.actual = new_token 
                return new_token

            elif(aux == ">"):
                new_token = Token("GREATERTHAN", ">")
                self.position += 1
                self.actual = new_token 
                return new_token
            
            elif(aux == "<"):
                new_token = Token("LESSTHAN", "<")
                self.position += 1
                self.actual = new_token 
                return new_token
            
            elif(aux == ","):
                new_token = Token("COMMA", ",")
                self.position += 1
                self.actual = new_token 
                return new_token

            elif(aux.isdigit()):
                while ( (self.position < len(self.origin) ) and (self.origin[self.position]).isdigit()):
                    current_token += self.origin[self.position]
                    self.position += 1
                
                new_token = Token("INT", int(current_token))
                self.actual = new_token
                return new_token

            elif(aux.isalpha()):
                while ( (self.position < len(self.origin)) and ( self.origin[self.position].isalpha() or self.origin[self.position].isdigit() or self.origin[self.position] == '_') ):
                    current_token += self.origin[self.position]
                    self.position += 1
                
                if(current_token.upper() == "BEGIN"):
                    new_token = Token("BEGIN", "BEGIN")
                    self.actual = new_token
                    return new_token

                elif(current_token.upper() == "END"):
                    new_token = Token("END", "END")
                    self.actual = new_token
                    return new_token
                    
                elif(current_token.upper() == "PRINT"):
                    new_token = Token("PRINT", "PRINT")
                    self.actual = new_token
                    return new_token

                elif(current_token.upper() == "OR"):
                    new_token = Token("OR", "OR")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "WHILE"):
                    new_token = Token("WHILE", "WHILE")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "WEND"):
                    new_token = Token("WEND", "WEND")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "IF"):
                    new_token = Token("IF", "IF")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "THEN"):
                    new_token = Token("THEN", "THEN")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "ELSE"):
                    new_token = Token("ELSE", "ELSE")
                    self.actual = new_token
                    return new_token

                elif(current_token.upper() == "AND"):
                    new_token = Token("AND", "AND")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "INPUT"):
                    new_token = Token("INPUT", "INPUT")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "NOT"):
                    new_token = Token("NOT", "NOT")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "SUB"):
                    new_token = Token("SUB", "SUB")
                    self.actual = new_token
                    return new_token

                # elif(current_token.upper() == "MAIN"):
                #     new_token = Token("MAIN", "MAIN")
                #     self.actual = new_token
                #     return new_token

                elif(current_token.upper() == "INTEGER"):
                    new_token = Token("TYPE", "INTEGER")
                    self.actual = new_token
                    return new_token

                elif(current_token.upper() == "BOOLEAN"):
                    new_token = Token("TYPE", "BOOLEAN")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "DIM"):
                    new_token = Token("DIM", "DIM")
                    self.actual = new_token
                    return new_token

                elif(current_token.upper() == "AS"):
                    new_token = Token("AS", "AS")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "TRUE"):
                    new_token = Token("BOOL", "TRUE")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "FALSE"):
                    new_token = Token("BOOL", "FALSE")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "FUNCTION"):
                    new_token = Token("FUNCTION", "FUNCTION")
                    self.actual = new_token
                    return new_token
                
                elif(current_token.upper() == "CALL"):
                    new_token = Token("CALL", "CALL")
                    self.actual = new_token
                    return new_token

                else:
                    new_token = Token("IDENTIFIER", current_token)
                    self.actual = new_token
                    return new_token

            elif(aux == "\n"):
                new_token = Token("EOL", "\n")
                self.position += 1
                self.actual = new_token
                return new_token

            else:
                raise ValueError("Invalid Token", aux)


class Parser:
    @staticmethod
    def parseExpression():
        res = Parser.parseTerm()
        while(Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR"):
            if(Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                children1 = Parser.parseTerm()
                res = BinOp("PLUS", [res, children1])
            elif(Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                children1 = Parser.parseTerm()
                res = BinOp("MINUS", [res, children1])
            
            elif(Parser.tokens.actual.type == "OR"):
                Parser.tokens.selectNext()
                children1 = Parser.parseTerm()
                res = BinOp("OR", [res, children1])

        return res

    @staticmethod
    def parseTerm():
        res = Parser.parseFactor()
        while(Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND"):
            if(Parser.tokens.actual.type == "MULT"):
                Parser.tokens.selectNext()
                children1 = Parser.parseFactor()
                res = BinOp("MULT", [res, children1])

            elif(Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                children1 = Parser.parseFactor()
                res = BinOp("DIV", [res, children1])

            elif(Parser.tokens.actual.type == "AND"):
                Parser.tokens.selectNext()
                children1 = Parser.parseFactor()
                res = BinOp("AND", [res, children1])
            
        return res
    
    @staticmethod
    def parseFactor():
        # res = 0
        if(Parser.tokens.actual.type == "INT"):
            new_node = IntVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            return new_node

        elif(Parser.tokens.actual.type == "("):
            Parser.tokens.selectNext()
            new_node = Parser.parseRelExpression()
            if(Parser.tokens.actual.type == ")"):
                Parser.tokens.selectNext()
                return new_node
            else:
                raise ValueError("Invalid Sintax, Missing ')'")

        elif(Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "NOT"):
            if(Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                new_node = UnOp("MINUS", [Parser.parseFactor()])
                return new_node

            elif(Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                new_node = UnOp("PLUS", [Parser.parseFactor()])
                return new_node
            
            elif(Parser.tokens.actual.type == "NOT"):
                Parser.tokens.selectNext()
                new_node = UnOp("NOT", [Parser.parseFactor()])
                return new_node

            else:
                raise ValueError("Invalid Token, expecting INT, received: ", Parser.tokens.actual.type)

        elif(Parser.tokens.actual.type == "BOOL"):
            if(Parser.tokens.actual.value == "TRUE"):
                new_node = BoolVal(True, None)
                Parser.tokens.selectNext()
                return new_node
            elif(Parser.tokens.actual.value == "FALSE"):
                new_node = BoolVal(False, None)
                Parser.tokens.selectNext()
                return new_node

        elif(Parser.tokens.actual.type == "IDENTIFIER"):
            name = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "("):
                Parser.tokens.selectNext()
                children = []
                while True:
                    if(Parser.tokens.actual.type == ")"):
                        Parser.tokens.selectNext()
                        break
                    else:
                        children.append(Parser.parseRelExpression())
                        if(Parser.tokens.actual.type == "COMMA"):
                            Parser.tokens.selectNext()
                new_node = SubFuncCall(name, children)
            else:
                new_node = Identifier(name, [])
            return new_node
        
        #implementar
        elif(Parser.tokens.actual.type == "INPUT"):
            new_node = Input("Input", [])
            Parser.tokens.selectNext()
            return new_node
        
        elif(Parser.tokens.actual.type == "BOOL"):
            new_node = BoolVal(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            return new_node

        else:
            raise ValueError("Invalid Token: ", Parser.tokens.actual.type)
    
    @staticmethod
    def parseStatements():
        children = []
        while(Parser.tokens.actual.type != "EOF"):
            if(Parser.tokens.actual.type == "SUB"):
                children.append(Parser.parseSubDec())
            elif(Parser.tokens.actual.type == "FUNCTION"):
                children.append(Parser.parseFuncDec())
            else:
                Parser.tokens.selectNext()
        statements = Statements(None, children)
        return statements

    @staticmethod
    def parseType():
        if(Parser.tokens.actual.type == "TYPE" and Parser.tokens.actual.value == "INTEGER"):
            Parser.tokens.selectNext()
            new_node = Type("INTEGER", "INTEGER")
            return new_node
        elif(Parser.tokens.actual.type == "TYPE" and Parser.tokens.actual.value == "BOOLEAN"):
            Parser.tokens.selectNext()
            new_node = Type("BOOLEAN", "BOOLEAN")
            return new_node
        else:
            raise ValueError("Type not supported")
    
    @staticmethod
    def parseStatement():
        if(Parser.tokens.actual.type == "IDENTIFIER"):
            child1 = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "ASSIGNMENT"):
                Parser.tokens.selectNext()
                new_node = Assignment("=", [child1, Parser.parseRelExpression()]) 
                return new_node

        elif(Parser.tokens.actual.type == "PRINT"):
            Parser.tokens.selectNext()
            print_node = Print("Print", [Parser.parseRelExpression()])
            return print_node
        
        elif(Parser.tokens.actual.type == "WHILE"):
            children = []
            Parser.tokens.selectNext()
            relExp = Parser.parseRelExpression()
            children.append(relExp)
            if(Parser.tokens.actual.type == "EOL"):
                    Parser.tokens.selectNext()
            
            statements = []
            while(Parser.tokens.actual.type != "WEND"):
                child = Parser.parseStatement()
                statements.append(child)
                if(Parser.tokens.actual.type == "EOL"):
                    Parser.tokens.selectNext()
            
            Parser.tokens.selectNext()
            children.append(statements)
            while_node = While("WHILE", children)
            return while_node

        elif(Parser.tokens.actual.type == "IF"):
            children = []
            Parser.tokens.selectNext()
            relExp = Parser.parseRelExpression()
            children.append(relExp)

            if(Parser.tokens.actual.type == "THEN"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "EOL"):
                    Parser.tokens.selectNext()
                    if_children = []
                    else_children = []
                    while(Parser.tokens.actual.type != "ELSE" and Parser.tokens.actual.type != "END"):
                        child = Parser.parseStatement()
                        if_children.append(child)
                        if(Parser.tokens.actual.type == "EOL"):
                            Parser.tokens.selectNext()
                    
                    if(Parser.tokens.actual.type == "ELSE"):
                        Parser.tokens.selectNext()
                        if(Parser.tokens.actual.type == "EOL"):
                            Parser.tokens.selectNext()
                        while(Parser.tokens.actual.type != "END"):
                            child = Parser.parseStatement()
                            else_children.append(child)
                            if(Parser.tokens.actual.type == "EOL"):
                                Parser.tokens.selectNext()
                                
                    Parser.tokens.selectNext() #Consumir o END que ja foi verificado nos whiles
                    if(Parser.tokens.actual.type == "IF"):
                        Parser.tokens.selectNext()
                        if(len(if_children) > 0):
                            children.append(if_children)
                        if(len(else_children) > 0):
                            children.append(else_children)
                        if_node = If("IF", children)
                        return if_node

        elif(Parser.tokens.actual.type == "DIM"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "IDENTIFIER"):
                ident_node = Identifier(Parser.tokens.actual.value, [])
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "AS"):
                    Parser.tokens.selectNext()
                    type_node = Parser.parseType()
                    return VarDec(None, [ident_node, type_node])
        elif(Parser.tokens.actual.type == "CALL"):
            Parser.tokens.selectNext()
            children = []
            if(Parser.tokens.actual.type == "IDENTIFIER"):
                name = Parser.tokens.actual.value.lower()
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "("):
                    Parser.tokens.selectNext()
                    while True:
                        if(Parser.tokens.actual.type == ")"):
                            Parser.tokens.selectNext()
                            break
                        else:
                            children.append(Parser.parseRelExpression())
                            if(Parser.tokens.actual.type == "COMMA"):
                                Parser.tokens.selectNext()
            node = SubFuncCall(name, children)
            return node

        else:
            Parser.tokens.selectNext()
            new_node = NoOp(None, [])
            return new_node

    @staticmethod
    def parseRelExpression():
        res = Parser.parseExpression()
        while(Parser.tokens.actual.type == "ASSIGNMENT" or Parser.tokens.actual.type == "GREATERTHAN" or Parser.tokens.actual.type == "LESSTHAN"):
            if(Parser.tokens.actual.type == "ASSIGNMENT"):
                Parser.tokens.selectNext()
                children1 = Parser.parseExpression()
                res = BinOp("EQUAL", [res, children1])

            elif(Parser.tokens.actual.type == "GREATERTHAN"):
                Parser.tokens.selectNext()
                children1 = Parser.parseExpression()
                res = BinOp("GREATERTHAN", [res, children1])
            
            elif(Parser.tokens.actual.type == "LESSTHAN"):
                Parser.tokens.selectNext()
                children1 = Parser.parseExpression()
                res = BinOp("LESSTHAN", [res, children1])

        return res

    @staticmethod
    def parseSubDec():
        children = []
        if(Parser.tokens.actual.type == "SUB"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "IDENTIFIER"):
                name = Parser.tokens.actual.value.lower()
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "("):
                    Parser.tokens.selectNext()
                    while True:
                        if(Parser.tokens.actual.type == ")"):
                            Parser.tokens.selectNext()
                            break
                        else:
                            if(Parser.tokens.actual.type == "IDENTIFIER"):
                                varName = Identifier(Parser.tokens.actual.value, [])
                                Parser.tokens.selectNext()
                                if(Parser.tokens.actual.type == "AS"):
                                    Parser.tokens.selectNext()
                                    if(Parser.tokens.actual.type == "TYPE"):
                                        varType = Parser.parseType()
                                        children.append(VarDec("", [varName, varType]))
                            if(Parser.tokens.actual.type == "COMMA"):
                                Parser.tokens.selectNext()

                    if(Parser.tokens.actual.type == "EOL"):
                        Parser.tokens.selectNext()
                        stmts = []
                        while(True):
                            if(Parser.tokens.actual.type == "END"):
                                Parser.tokens.selectNext()
                                break
                            stmt = Parser.parseStatement()
                            stmts.append(stmt)
                            if(Parser.tokens.actual.type == "EOL"):
                                Parser.tokens.selectNext()
                        children.append(Statements(None, stmts))
                        if(Parser.tokens.actual.type == "SUB"):
                            Parser.tokens.selectNext()
            node = SubDec(name, children)
            return node
            
    @staticmethod
    def parseFuncDec():
        children = []
        if(Parser.tokens.actual.type == "FUNCTION"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "IDENTIFIER"):
                name = Parser.tokens.actual.value.lower()
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "("):
                    Parser.tokens.selectNext()
                    while True:
                        if(Parser.tokens.actual.type == ")"):
                            Parser.tokens.selectNext()
                            break
                        else:
                            if(Parser.tokens.actual.type == "IDENTIFIER"):
                                varName = Identifier(Parser.tokens.actual.value, [])
                                Parser.tokens.selectNext()
                                if(Parser.tokens.actual.type == "AS"):
                                    Parser.tokens.selectNext()
                                    if(Parser.tokens.actual.type == "TYPE"):
                                        varType = Parser.parseType()
                                        children.append(VarDec("", [varName, varType]))
                        if(Parser.tokens.actual.type == "COMMA"):
                            Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "AS"):
                        Parser.tokens.selectNext()
                        if(Parser.tokens.actual.type == "TYPE"):
                            funcType = Parser.parseType() 
                            children.insert(0, funcType)

                    if(Parser.tokens.actual.type == "EOL"):
                        Parser.tokens.selectNext()
                        stmts = []
                        while(True):
                            if(Parser.tokens.actual.type == "END"):
                                Parser.tokens.selectNext()
                                break
                            stmt = Parser.parseStatement()
                            stmts.append(stmt)
                            if(Parser.tokens.actual.type == "EOL"):
                                Parser.tokens.selectNext()
                        children.append(Statements(None, stmts))
                        if(Parser.tokens.actual.type == "FUNCTION"):
                            Parser.tokens.selectNext()
            node = FuncDec(name, children)
            return node
        
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        res = Parser.parseStatements()
        if(Parser.tokens.actual.type == "EOF"):
            res.children.append(SubFuncCall("main", []))
            return res
        else:
            raise ValueError("Error: Unexpected token")
class PrePro():
    @staticmethod
    def filter(text):
        code = re.sub("'.*\n", "\n", data)
        return code

class SymbolTable:
    """
    Store variables.
    Dictionary:
        key: name
        value: [value, type]
    """
    def __init__(self, parent=None):
        self.symbolTable = {}
        self.parent = parent
    
    """
    If name exists, returns (value, type)
    """
    def get(self, name):  
        if(name in self.symbolTable.keys()):
            return (self.symbolTable[name][0], self.symbolTable[name][1])
        elif(self.parent != None):
            return self.parent.get(name)
        else:
            raise ValueError(name, " does not exists") 
    
    def getPointer(self, name):
        # print(self.symbolTable.keys())
        if(name in self.symbolTable.keys()):
            if(self.symbolTable[name][1] == "SUB" or self.symbolTable[name][1] == "FUNC"):
                return (self.symbolTable[name][0], self.symbolTable[name][1])        
        return self.parent.getPointer(name)
        # else:
        #     raise ValueError(name, " does not exists") 

    """
    If name exists, creates {name: [None, type]} inside symbol Table
    Else, raise error
    """
    def create(self, name, type):
        if(name in self.symbolTable.keys()):
            raise ValueError(f"Reassign of variable: {type}, {name}")
        else:
            self.symbolTable[name] = [None, type]
            return 1
    
    """
    Sets 'name' value. name: [value, type].
    """
    def setValue(self, name, value):
        if(name in self.symbolTable.keys()):
            self.symbolTable[name][0] = value
            return 1
        else:
            raise ValueError(name, " does not exists")             

gettrace = getattr(sys, 'gettrace', None)
if gettrace():
    #It's on debugger
    file_name = "teste.vbs"
else:
    file_name = str(sys.argv[1])


with open(file_name) as file:
    data = file.read()
symbolTable = SymbolTable()
res = Parser.run(data)
res.Evaluate(symbolTable)