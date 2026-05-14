global main
extern printf

section .data
msg0 db "wwwwwwwww",0
fmt_int db "%lld",10,0
d dq 0

section .text

main:
    mov qword [d], 5
    lea rcx, [msg0]
    sub rsp, 32
    call printf
    add rsp, 32
    mov rdx, [d]
    lea rcx, [fmt_int]
    sub rsp, 32
    call printf
    add rsp, 32

    xor eax, eax
    ret