default rel

section .data

msg db "Hola mundo", 0
fmt db "%s",10,0

section .text

global main
extern printf

main:

    sub rsp, 40

    mov rcx, fmt
    mov rdx, msg

    call printf

    add rsp, 40

    mov eax, 0
    ret