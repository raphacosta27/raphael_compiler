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

            else:
                raise ValueError("Invalid Token", aux)

        else:
            new_token = Token("INT", int(current_token))
            self.actual = new_token
            return new_token

class Parser:
    def parseExpression():
        res = Parser.parseTerm()
        while(Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS"):
            if(Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                res += Parser.parseTerm()
            elif(Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                res -= Parser.parseTerm()
        return res

    def parseTerm():
        res = None
        if(Parser.tokens.actual.type == "INT"):
            res = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV"):
                if(Parser.tokens.actual.type == "MULT"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        res *= Parser.tokens.actual.value
                    else:
                        raise ValueError("Next token is invalid", Parser.tokens.actual.type)

                elif(Parser.tokens.actual.type == "DIV"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        res = res // Parser.tokens.actual.value
                    else:
                        raise ValueError("Next token is invalid", Parser.tokens.actual.type)

                Parser.tokens.selectNext()
        else:
            raise ValueError("First token is invalid", Parser.tokens.actual.type)
        return res

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
print(Parser.run(teste))