import re
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
        return symbolTable.get(self.value)

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
            children.Evaluate()


class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        if(self.value == "PLUS"):
            return self.children[0].Evaluate() + self.children[1].Evaluate()
            
        elif(self.value == "MINUS"):
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        
        elif(self.value == "MULT"):
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        
        elif(self.value == "DIV"):
            return self.children[0].Evaluate() // self.children[1].Evaluate()

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        if(self.value == "MINUS"):
            return -self.children[0].Evaluate()

        if(self.value == "PLUS"):
            return +self.children[0].Evaluate()

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self):
        return self.value

class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self):
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
        while(Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS"):
            if(Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                children1 = Parser.parseTerm()
                res = BinOp("PLUS", [res, children1])
            elif(Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                children1 = Parser.parseTerm()
                res = BinOp("MINUS", [res, children1])
        return res

    @staticmethod
    def parseTerm():
        res = Parser.parseFactor()
        while(Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV"):
            if(Parser.tokens.actual.type == "MULT"):
                Parser.tokens.selectNext()
                children1 = Parser.parseFactor()
                res = BinOp("MULT", [res, children1])
            elif(Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                children1 = Parser.parseFactor()
                res = BinOp("DIV", [res, children1])
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

        elif(Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "PLUS"):
            if(Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                new_node = UnOp("MINUS", [Parser.parseFactor()])
                return new_node

            elif(Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                new_node = UnOp("PLUS", [Parser.parseFactor()])
                return new_node
            else:
                raise ValueError("Invalid Token, expecting INT, received: ", Parser.tokens.actual.type)

        elif(Parser.tokens.actual.type == "IDENTIFIER"):
            Parser.tokens.selectNext()
            new_node = Identifier(Parser.tokens.actual.value, [])
            return new_node

        else:
            raise ValueError("Invalid Token: ", Parser.tokens.actual.type)
    
    @staticmethod
    def parseStatements():
        #Criar statements node e ir appendando filhos do tipo statement
        #a medida que passando por coisas que nao forem END

        #devo criar um token do tipo \n???
        #Devo criar um Node do Begin?
        #Como vou adicionando a children (Checo se não é END ou se nao
        #é \n?
        statements = Statements(None, None)
        children = []
        if(Parser.tokens.actual.type == "BEGIN"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "EOL"):
                Parser.tokens.selectNext()
                while(Parser.tokens.actual.value != "END"):
                    child = Parser.parseStatement()
                    children.append(child)
                
        # for 
    
    @staticmethod
    def parseStatement():
        res = None
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
        elif(Parser.tokens.actual.type == "BEGIN"): #nao consumo, portanto nao tem selectNext()
            return Parser.parseStatements()
        else:
            return

            



        
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        print("------------------------")
        # res = Parser.parseExpression()
        res = Parser.parseStatements()
        if(Parser.tokens.actual.type == "EOF"):
            return res
        else:
            raise ValueError("Error: Unexpected token")
class PrePro():
    @staticmethod
    def filter(text):
        code = re.sub("'.*\n", "", data)
        return code

class SymbolTable:
    def __init__(self):
        self.symbolTable = {}
    
    def get(self, name):
        if(self.symbolTable[name]):
            return self.symbolTable[name]
        else:
            raise ValueError(name, " does not exists") 
    
    def set(self, name, value):
        self.symbolTable[name] = value
        return 1
    

# teste = input("Filename: ")
teste = "teste"
with open(f"{teste}.vbs") as file:
    data = file.read() + '\n'
print(Parser.run(data).Evaluate())

# tokenizer 
# Parser
# node statments 0 ou + filhos
# node assigment 2 filhos
# node identifier 0 filhos
# isalpha