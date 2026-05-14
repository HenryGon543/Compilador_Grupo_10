section .data
contador dd 0
t4 dd 0
t6 dd 0
t7 dd 0
t5 dd 0
repetir dd 0
debe dd 0
b dd 0
t3 dd 0
c dd 0
a dd 0
fmt_int db "%d",10,0
fmt_str db "%s",10,0
str_0 db "hola",0
str_1 db "opcion dos",0
str_2 db "opcion uno",0
str_3 db "se debe repetir 5 veces",0
section .text
global _main
extern _printf
_main:
mov dword [a], 5
mov dword [b], 10
mov dword [contador], 0
mov dword [t3], 6
mov eax, [a]
add eax, [t3]
mov [t4], eax
mov eax, [t4]
mov [c], eax
push dword str_0
push fmt_str
call _printf
add esp, 8
mov eax, [a]
cmp eax, 5
je TRUE_t5
mov dword [t5], 0
jmp END_t5
TRUE_t5:
mov dword [t5], 1
END_t5:
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
L3:
mov eax, [contador]
cmp eax, 5
jl TRUE_t6
mov dword [t6], 0
jmp END_t6
TRUE_t6:
mov dword [t6], 1
END_t6:
mov eax, [t6]
cmp eax, 0
je END_L3
push dword str_3
push fmt_str
call _printf
add esp, 8
mov eax, [contador]
add eax, 1
mov [t7], eax
mov eax, [t7]
mov [contador], eax
jmp L3
END_L3:
mov eax, 0
ret