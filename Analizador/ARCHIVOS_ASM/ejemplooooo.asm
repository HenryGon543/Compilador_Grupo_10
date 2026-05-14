section .data
t2 dd 0
i dd 0
t1 dd 0
hola dd 0
w dd 0
t3 dd 0
fmt_int db "%d",10,0
fmt_str db "%s",10,0
str_0 db "es mayor",0
section .text
global _main
extern _printf
_main:
mov dword [w], 900
mov dword [hola], 4000
push dword [w]
push fmt_int
call _printf
add esp, 8
push dword [hola]
push fmt_int
call _printf
add esp, 8
mov eax, [w]
cmp eax, 500
jg TRUE_t1
mov dword [t1], 0
jmp END_t1
TRUE_t1:
mov dword [t1], 1
END_t1:
mov eax, [t1]
cmp eax, 1
je L1
L1:
push dword str_0
push fmt_str
call _printf
add esp, 8
L2:
mov dword [i], 10
L3:
mov eax, [i]
cmp eax, 1
je TRUE_t2
mov dword [t2], 0
jmp END_t2
TRUE_t2:
mov dword [t2], 1
END_t2:
mov eax, [t2]
cmp eax, 0
je END_L3
push dword [i]
push fmt_int
call _printf
add esp, 8
mov eax, [i]
sub eax, 1
mov [t3], eax
mov eax, [t3]
mov [i], eax
jmp L3
END_L3:
mov eax, 0
ret