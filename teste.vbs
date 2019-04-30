Sub Main()

Dim a as Integer
Dim b as Integer
Dim c as Integer
a = 10
b = 20
c = input

if a < b then
    if b < c then
        ' test comment

        while c > 0
            ' hello

            print c
            c = c-5
        wend
    end if
end if
End Sub