default rel

global main
extern printf

section .data
fmt_int db '%lld',10,0
fmt_float db '%lf',10,0
fmt_str db '%s',0
x dq 0
y dq 0.0
contador dq 0
t1 dq 0.0
t2 dq 0
flt_0 dq 3.44
msg_0 db "Hola mundo",0
msg_1 db "hola esto es un print",10,0
flt_1 dq 23
flt_2 dq 3.44
msg_2 db "ye es mayor",0
msg_3 db "equis es mayor",0
msg_4 db "se debe repetir 5 veces",0

section .text
main:

push rbp
mov rbp, rsp
sub rsp, 40

mov qword [rel x], 23

movsd xmm0, [rel flt_0]
movsd [rel y], xmm0

mov qword [rel contador], 0

lea rcx, [rel fmt_str]
lea rdx, [rel msg_0]
xor rax, rax
call printf

lea rcx, [rel fmt_str]
lea rdx, [rel msg_1]
xor rax, rax
call printf

movsd xmm0, [rel flt_1]
movsd [rel t1], xmm0

cmp qword [rel t1], 0
jne L1

lea rcx, [rel fmt_str]
lea rdx, [rel msg_2]
xor rax, rax
call printf

jmp L2

L1:
lea rcx, [rel fmt_str]
lea rdx, [rel msg_3]
xor rax, rax
call printf

L2:
L3:
mov qword [rel t2], 0

cmp qword [rel t2], 0
jne L4

jmp END_L3

L4:
lea rcx, [rel fmt_str]
lea rdx, [rel msg_4]
xor rax, rax
call printf

mov qword [rel contador], 1

jmp L3

END_L3:

add rsp, 40
pop rbp
mov rax, 0
ret