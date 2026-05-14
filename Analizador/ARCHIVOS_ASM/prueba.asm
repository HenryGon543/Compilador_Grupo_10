section .data
b dd 0
c dd 0
a dd 0
fmt db "%d",10,0
section .text
global main
extern printf
main:
mov dword [a], 5
mov dword [b], 10
mov dword [c], 11
ret
