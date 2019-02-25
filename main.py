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
        if(self.position == len(self.origin)):
            new_token = Token("EOF", "EOF")
            self.actual = new_token
            return new_token

        while ( (self.position < len(self.origin)) and self.origin[self.position] == ' '):
            self.position += 1

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

            else:
                raise ValueError("Invalid Token", aux)
        
        else:
            # print("Last else")
            new_token = Token("INT", int(current_token))
            self.actual = new_token
            return new_token
            
class Parser:
    # tokens = []
    def parseExpression():
        res = None
        if(Parser.tokens.actual.type == "INT"):
            res = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS"):
                if(Parser.tokens.actual.type == "PLUS"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        res += Parser.tokens.actual.value
                    else:
                        raise ValueError("Next token is invalid", Parser.tokens.actual.type)
                    
                elif(Parser.tokens.actual.type == "MINUS"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        res -= Parser.tokens.actual.value
                    else:
                        raise ValueError("Next token is invalid", Parser.tokens.actual.type)

                Parser.tokens.selectNext()
        else:
            raise ValueError("First token is invalid", Parser.tokens.actual.type)
        return res
    
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()


teste = input("Digite a expressao: ")
print(Parser.run(teste))
