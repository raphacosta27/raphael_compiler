test = input("Digite a equação: ")
test = test.replace(" ", "")

clean = []
comeco = 0
for i in range(len(test)):
    if((test[i] == "+" or test[i] == "-") and i != 0):
        fim = i
        numero = test[comeco:fim]
        clean.append(int(numero))
        clean.append(test[i]) 
        comeco = i+1
    elif(i == len(test)-1):
        clean.append(int(test[comeco:(len(test))]))
    else:
        pass    

print(clean)
res = 0
test_char = clean

if(test_char[-1] == "+" or test_char[-1] == "-"):
    raise ValueError("Inválido, último carácter não pode ser sinal.")

if(len(test_char) < 3):
    raise ValueError("Equação Inválida.")

while (len(test_char) > 0):
    num1 = int(test_char[0])
    operador = test_char[1]
    num2 = int(test_char[2])
    
    if operador == "+":
        res = (num1 + num2)
    elif operador == "-":
        res = (num1 - num2)

    del test_char[0]
    del test_char[0]
    del test_char[0]
    
    if(len(test_char) > 0):
        test_char = [res] + test_char

print(res)