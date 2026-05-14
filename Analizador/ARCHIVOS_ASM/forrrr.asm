section .data
t1 dd 0
t2 dd 0
i dd 0
fmt_int db "%d",10,0
fmt_str db "%s",10,0
str_0 db "Hola",0
section .text
global _main
extern _printf
_main:
mov dword [i], 0
L1:
mov eax, [i]
cmp eax, 5
jl TRUE_t1
mov dword [t1], 0
jmp END_t1
TRUE_t1:
mov dword [t1], 1
END_t1:
mov eax, [t1]
cmp eax, 0
je END_L1
push dword str_0
push fmt_str
call _printf
add esp, 8
mov eax, [i]
add eax, 1
mov [t2], eax
mov eax, [t2]
mov [i], eax
jmp L1
END_L1:
mov eax, 0
ret