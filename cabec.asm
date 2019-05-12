; c o n s t a n t e s
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
F al s e equ 0
segment . data
segment . b s s ; v a r i a v e i s
r e s RESB 1
s e c t i o n . t e x t
g l o b a l _ s t a r t
p r i n t : ; s u b r o ti n a p ri n t
PUSH EBP ; guarda o b a se p oi n t e r
1
MOV EBP, ESP ; e s t a b e l e c e um novo b a se p oi n t e r
MOV EAX, [EBP+8] ; 1 argumento a n t e s do RET e EBP
XOR ESI , ESI
p rin t_dec : ; empilha t od o s o s d i g i t o s
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0 '
PUSH EDX
INC ESI ; c on t ad o r de d i g i t o s
CMP EAX, 0
JZ p rin t_ne x t ; quando ac ab a r pul a
JMP p rin t_dec
p rin t_nex t :
CMP ESI , 0
JZ p ri n t _ e xi t ; quando ac ab a r de imp rimi r
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [ r e s ] , ECX
MOV ECX, r e s
MOV EDX, 1
INT 0 x80
JMP p rin t_ne x t
p ri n t _ e xi t :
POP EBP
RET
; s u b r o ti n a s i f / w hil e
binop_ je :
JE binop_true
JMP bi n o p_ f al s e
binop_ jg :
JG binop_true
JMP bi n o p_ f al s e
bi n o p_ jl :
JL binop_true
JMP bi n o p_ f al s e
bi n o p_ f al s e :
MOV EBX, F al s e
JMP bin op_e xi t
binop_true :
MOV EBX, True
bin op_e xi t :
RET
_ s t a r t :
PUSH EBP ; guarda o b a se p oi n t e r
2
MOV EBP, ESP ; e s t a b e l e c e um novo b a se p oi n t e r