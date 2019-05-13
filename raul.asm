; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss ; variaveis
res RESB 1

section .text
global_start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False  
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:
PUSH EBP ; guarda o b a se p oi n t e r
MOV EBP, ESP ; e s t a b e l e c e um novo b a se p oi n t e r
; c o di g o ge r ad o p el o c ompil ad o r
PUSH DWORD 0 ; Dim i a s I n t e g e r [EBP−4]
PUSH DWORD 0 ; Dim n a s I n t e g e r [EBP−8]
PUSH DWORD 0 ; Dim f a s I n t e g e r [EBP−12]
MOV EBX, 5
MOV [EBP-8], EBX ; n = 5
MOV EBX, 2
MOV [EBP-4], EBX ; i = 2
MOV EBX, 1
MOV [EBP-12], EBX ; f = 1
LOOP_34:
MOV EBX, [EBP-4]
PUSH EBX ; empilha i
MOV EBX, [EBP-8]
PUSH EBX ; empilha n
MOV EBX, 1
POP EAX
ADD EAX, EBX ; n + 1
MOV EBX, EAX
POP EAX
CMP EAX, EBX
CALL binop_jl ; i < n + 1
CMP EBX, False
JE EXIT_34
MOV EBX, [EBP-12]
PUSH EBX ; empilha f
MOV EBX, [EBP-4]
POP EAX ; empilha i
IMUL EBX ; i ∗ f
MOV EBX, EAX
MOV [EBP-12], EBX ; f = 2
MOV EBX, [EBP-4]
PUSH EBX ; empilha i
MOV EBX, 1
POP EAX
ADD EAX, EBX ; i + 1
MOV EBX, EAX
MOV [EBP-4], EBX ; i = 3
JMP LOOP_34
EXIT_34:
MOV EBX, [EBP-12]
PUSH EBX ; empilha f
CALL print ; P ri n t f
POP EBX ; limpa a r g s
; i n t e r r u p c a o de s ai d a
POP EBP
MOV EAX, 1
INT 0x80