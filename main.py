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

class Statements(Node):
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
                self.children[2].Evaluate(symbolTable)

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
            new_node = Parser.parseExpression()
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

        else:
            raise ValueError("Invalid Token: ", Parser.tokens.actual.type)
    
    @staticmethod
    def parseStatements():
        children = []
        while(True):
            child = Parser.parseStatement()
            children.append(child)
            if(Parser.tokens.actual.type == "EOL"):
                Parser.tokens.selectNext()

            if(Parser.tokens.actual.type == "EOF" or Parser.tokens.actual.type == "END" or Parser.tokens.actual.type == "WEND"):
                break
            

        statements = Statements(None, children)
        return statements
    
    @staticmethod
    def parseStatement():
        if(Parser.tokens.actual.type == "IDENTIFIER"):
            child1 = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "ASSIGNMENT"):
                Parser.tokens.selectNext()
                new_node = Assignment("=", [child1, Parser.parseExpression()]) 
                return new_node

        elif(Parser.tokens.actual.type == "PRINT"):
            Parser.tokens.selectNext()
            print_node = Print("Print", [Parser.parseExpression()])
            return print_node
        
        elif(Parser.tokens.actual.type == "WHILE"):
            Parser.tokens.selectNext()
            relExp = Parser.parseRelExpression()
            if(Parser.tokens.actual.type == "EOL"):
                    Parser.tokens.selectNext()
            statements = Parser.parseStatements()
            if(Parser.tokens.actual.type == "WEND"):
                Parser.tokens.selectNext()
                while_node = While("WHILE", [relExp, statements])
                return while_node
            else:
                raise ValueError("Expecting WEND, got: ", Parser.tokens.actual.type)

        elif(Parser.tokens.actual.type == "IF"):
            children = []
            Parser.tokens.selectNext()
            relExp = Parser.parseRelExpression()
            children.append(relExp)

            if(Parser.tokens.actual.type == "THEN"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "EOL"):
                    Parser.tokens.selectNext()
                    statements = Parser.parseStatements()
                    children.append(statements)

                if(Parser.tokens.actual.type == "ELSE"):
                    statements2 = Parser.parseStatements()
                    children.append(statements2)

                if(Parser.tokens.actual.type == "END"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "IF"):
                        Parser.tokens.selectNext()
                        if_node = If("IF", children)
                        return if_node

                    else:
                        raise ValueError("Expecting IF after END, got: ", Parser.tokens.actual.type)
                        
                else:
                    raise ValueError("Expecting ELSE or END, got: ", Parser.tokens.actual.type)

            else:
                raise ValueError("Expecting THEN after while declaration")

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
        res = Parser.parseStatements()
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