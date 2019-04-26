import re
import sys
class Node: #abstract
    def __init__(self):
        self.value = None
        self.children = None
    
    def Evaluate(self, symbolTable):
        pass

class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable): #receber SymbolTable
        try:
            return symbolTable.get(self.value)
        except:
            raise ValueError("Identifier: ", self.value, " does not exists")

class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable): #receber SymbolTable
        children2 = self.children[1].Evaluate(symbolTable)
        symbolTable.set(self.children[0].value, children2)
        return 

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable): #receber SymbolTable
        print(self.children[0].Evaluate(symbolTable))
        return 

class Program(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable): #receber SymbolTable
        for children in self.children:
            children.Evaluate(symbolTable)

class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        #!Trocar evaluate pq agr recebe listas dentro de listas
        #e nao mais um no do tipo Statements pra so dar Evaluate
        while self.children[0].Evaluate(symbolTable): #garantir que retorna true
            self.children[1].Evaluate(symbolTable)

class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        if(self.children[0].Evaluate(symbolTable)):
            self.children[1].Evaluate(symbolTable)
        else:
            if(len(self.children) == 3):
                self.children[2].Evaluate(symbolTable) #!Trocar evaluate pq agr recebe listas dentro de listas
                                                        #e nao mais um no do tipo Statements pra so dar Evaluate

class Input(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
        
    def Evaluate(self, symbolTable):
        return int(input())

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        if(self.value == "PLUS"):
            return self.children[0].Evaluate(symbolTable) + self.children[1].Evaluate(symbolTable)
            
        elif(self.value == "MINUS"):
            return self.children[0].Evaluate(symbolTable) - self.children[1].Evaluate(symbolTable)
        
        elif(self.value == "MULT"):
            return self.children[0].Evaluate(symbolTable) * self.children[1].Evaluate(symbolTable)
        
        elif(self.value == "DIV"):
            return self.children[0].Evaluate(symbolTable) // self.children[1].Evaluate(symbolTable)
        
        elif(self.value == "GREATERTHAN"):
            return self.children[0].Evaluate(symbolTable) > self.children[1].Evaluate(symbolTable)
        
        elif(self.value == "LESSTHAN"):
            return self.children[0].Evaluate(symbolTable) < self.children[1].Evaluate(symbolTable)

        elif(self.value == "OR"):
            return self.children[0].Evaluate(symbolTable) or self.children[1].Evaluate(symbolTable)
        
        elif(self.value == "AND"):
            return self.children[0].Evaluate(symbolTable) and self.children[1].Evaluate(symbolTable)
        
        elif(self.value == "EQUAL"):
            return self.children[0].Evaluate(symbolTable) == self.children[1].Evaluate(symbolTable)

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbolTable):
        if(self.value == "MINUS"):
            return -self.children[0].Evaluate(symbolTable)

        elif(self.value == "PLUS"):
            return +self.children[0].Evaluate(symbolTable)
        
        elif(self.value == "NOT"):
            return not self.children[0].Evaluate(symbolTable)

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        return self.value

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        pass
    
class Type(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        return self.value

class BoolVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        return self.value

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, symbolTable):
        return self.value #Nao sei o que retorna!

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

                elif(current_token.upper() == "MAIN"):
                    new_token = Token("MAIN", "MAIN")
                    self.actual = new_token
                    return new_token

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

        elif(Parser.tokens.actual.type == "IDENTIFIER"):
            new_node = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
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
    def parseProgram():
        children = []
        if(Parser.tokens.actual.type == "SUB"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "MAIN"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "("):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == ")"):
                        Parser.tokens.selectNext()
                        if(Parser.tokens.actual.type == "EOL"):
                            Parser.tokens.selectNext()
                            while(True):
                                if(Parser.tokens.actual.type == "END"):
                                    Parser.tokens.selectNext()
                                    break
                                child = Parser.parseStatement()
                                children.append(child)
                                if(Parser.tokens.actual.type == "EOL"):
                                    Parser.tokens.selectNext()

                            if(Parser.tokens.actual.type == "SUB"):
                                Parser.tokens.selectNext()

        program = Program(None, children)
        return program

    @staticmethod
    def parseType():
        if(Parser.tokens.actual.type == "INTEGER"):
            Parser.tokens.selectNext()
            new_node = Type("INTEGER", "INTEGER")
            return new_node
        elif(Parser.tokens.actual.type == "BOOLEAN"):
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
            
            while(Parser.tokens.actual.type != "WEND"):
                child = Parser.parseStatement()
                children.append(child)
                if(Parser.tokens.actual.type == "EOL"):
                    Parser.tokens.selectNext()
            
            Parser.tokens.selectNext()
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
                
                    while(Parser.tokens.actual.type != "ELSE" or Parser.tokens.actual.type != "END"):
                        if_children = []
                        child = Parser.parseStatement()
                        if_children.append(child)
                        if(Parser.tokens.actual.type == "EOL"):
                            Parser.tokens.selectNext()
                
                    if(Parser.tokens.actual.type == "ELSE"):
                        while(Parser.tokens.actual.type != "END"):
                            else_children = []
                            child = Parser.parseStatement()
                            else_children.append(child)
                            if(Parser.tokens.actual.type == "EOL"):
                                Parser.tokens.selectNext()
                                
                    Parser.tokens.selectNext() #Consumir o END que ja foi verificado nos whiles
                    if(Parser.tokens.actual.type == "IF"):
                        Parser.tokens.selectNext()
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

        else:
            new_node = NoOp(None, [])
            return

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
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        res = Parser.parseProgram()
        if(Parser.tokens.actual.type == "EOF"):
            return res
        else:
            raise ValueError("Error: Unexpected token")
class PrePro():
    @staticmethod
    def filter(text):
        code = re.sub("'.*\n", "\n", data)
        return code

class SymbolTable:
    def __init__(self):
        self.symbolTable = {}
    
    def get(self, name):
        if(name in self.symbolTable.keys()):
            return self.symbolTable[name]
        else:
            raise ValueError(name, " does not exists") 
    
    def set(self, name, value):
        self.symbolTable[name] = value
        return 1

gettrace = getattr(sys, 'gettrace', None)
if gettrace():
    #Its on debugger
    file_name = "teste.vbs"
else:
    file_name = str(sys.argv[1])


with open(file_name) as file:
    data = file.read() + '\n'
symbolTable = SymbolTable()
res = Parser.run(data)
res.Evaluate(symbolTable)