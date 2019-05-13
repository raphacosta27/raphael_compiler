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

_start :
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer

; codigo gerado pelo compilador

PUSH DWORD 0 ; Dim tb as BOOLEAN [EBP−4]
PUSH DWORD 0 ; Dim ti as INTEGER [EBP−8]
MOV EBX, True
MOV [EBP - 4], EBX ; tb = True
MOV EBX, 10
MOV [EBP - 8], EBX ; ti = 10
IF_19:
MOV EBX, [EBP - 4]
CMP EBX, False
JE EXIT_19
MOV EBX, [EBP - 8]
PUSH EBX
MOV EBX, 10
POP EAX
ADD EAX, EBX
MOV EBX, EAX
PUSH EBX
CALL print
POP EBX
EXIT_19:

; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80
