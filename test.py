test = " 789 +345 - 123"
test = test.split()
test = "".join(test)

clean = []
comeco = 0
for i in range(len(test)):
    # print("Current i: ", test[i])

    if((test[i] == "+" or test[i] == "-") and i != 0):
        fim = i
        numero = test[comeco:fim]
        clean.append(int(numero))
        # print("Achou numero: ", numero)
        clean.append(test[i]) #deveria ser um operador
        # print("Achou operador: ", test[i])
        comeco = i+1
        # print("Clean: ", clean)

    elif(i == len(test)-1):
        # print("Last")
        clean.append(int(test[comeco:(len(test))]))

    else:
        pass    

res = 0

test_char = clean

if(test[-1] == "+" or test[-1] == "-"):
    raise ValueError("Inválido, último carácter não pode ser sinal.")

while (len(test_char) > 0):
    num1 = int(test_char[0])
    operador = test_char[1]
    num2 = int(test_char[2])
    # print(f"conta: {num1} {operador} {num2}")
    if operador == "+":
        res = (num1 + num2)
    elif operador == "-":
        res = (num1 - num2)
    # print("Before: ", test_char)
    del test_char[0]
    del test_char[0]
    del test_char[0]
    # print("After: ", test_char)
    # print("Res: ", res)

    if(len(test_char) > 0):
        test_char = [res] + test_char

print(res)