section .data
c dd 0
b dd 0
t5 dd 0
a dd 0
fmt_int db "%d",10,0
fmt_str db "%s",10,0
str_0 db "hola",0
str_1 db "opcion dos",0
str_2 db "opcion uno",0
section .text
global _main
extern _printf
_main:
mov dword [a], 5
mov dword [b], 10
mov dword [c], 11
push dword str_0
push fmt_str
call _printf
add esp, 8
push dword [c]
push fmt_int
call _printf
add esp, 8
mov dword [t5], 1
mov eax, [t5]
cmp eax, 1
je L1
push dword str_1
push fmt_str
call _printf
add esp, 8
jmp L2
L1:
push dword str_2
push fmt_str
call _printf
add esp, 8
L2:
mov eax, 0
ret