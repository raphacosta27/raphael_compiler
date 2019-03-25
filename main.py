class Node: #abstract
    def __init__(self):
        self.value = None
        self.children = None
    
    def Evaluate(self):
        pass

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

        while ( (self.position < len(self.origin)) and self.origin[self.position] == ' '):
            self.position += 1

        if(self.position == len(self.origin)):
            new_token = Token("EOF", "EOF")
            self.actual = new_token
            return new_token

        while ( (self.position < len(self.origin) ) and (self.origin[self.position]).isdigit()):
            current_token += self.origin[self.position]
            self.position += 1

        if(len(current_token) == 0):
            aux = self.origin[self.position]
            if(aux == "+"):
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

            else:
                raise ValueError("Invalid Token", aux)

        else:
            new_token = Token("INT", int(current_token))
            self.actual = new_token
            return new_token

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

        else:
            raise ValueError("Invalid Token: ", Parser.tokens.actual.type)
            
        
    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        # print(len(code))
        Parser.tokens = Tokenizer(code)
        res = Parser.parseExpression()
        if(Parser.tokens.actual.type == "EOF"):
            return res
        else:
            raise ValueError("Error: Unexpected token")

class PrePro():
    @staticmethod
    def filter(text):
        code = ""
        i = 0
        while (i < len(text)):
            if(text[i] == "'"):
                # wait for \n
                while (i < len(text)):
                    if(text[i] == "\n"):
                        break
                    else:
                        i += 1
            else:
                code += text[i]
                i += 1

        return code

teste = input("Digite a expressao: ")
print(Parser.run(teste).Evaluate())