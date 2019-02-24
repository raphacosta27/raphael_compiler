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
            return new_token

        while ( (self.position < len(self.origin) ) and (self.origin[self.position]).isdigit()):
            current_token += self.origin[self.position]
            self.position += 1

        if(len(current_token) == 0):
            aux = self.origin[self.position]
            if(aux == "+"):
                new_token = Token("PLUS", "+")
                self.position += 1
                return new_token
                
            elif(aux == "-"):
                new_token = Token("MINUS", "-")
                self.position += 1
                return new_token

            elif(aux == " "):
                self.position += 1
                return self.selectNext()

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
            current_token = Parser.tokens.selectNext()
            while(current_token.type == "PLUS" or current_token.type == "MINUS"):
                if(current_token.type == "PLUS"):
                    current_token = Parser.tokens.selectNext()
                    if(current_token.type == "INT"):
                        res += current_token.value
                    else:
                        raise ValueError("Next token is invalid", current_token.type)
                    
                elif(current_token.type == "MINUS"):
                    current_token = Parser.tokens.selectNext()
                    if(current_token.type == "INT"):
                        res -= current_token.value
                    else:
                        raise ValueError("Next token is invalid", current_token.type)
                
                current_token = Parser.tokens.selectNext()
        else:
            raise ValueError("First token is invalid", current_token.type)
        print(current_token.type)
        return res
    
    def run(code):
        Parser.tokens = Tokenizer(code)
        return Parser.parseExpression()


#teste = "2 + 3 * 5"
#print(Parser.run(teste))
