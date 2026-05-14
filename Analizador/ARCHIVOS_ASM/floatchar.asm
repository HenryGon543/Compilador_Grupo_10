section .data
    _fc0 dq 2.33
    x dq 0.0
    c db 0
    fmt_int   db "%d",10,0
    fmt_float db "%f",10,0
    fmt_char  db "%c",10,0
    fmt_str   db "%s",10,0
section .text
global _main
extern _printf
_main:
    fld  qword [_fc0]
    fstp qword [x]
    fld  qword [x]
    sub  esp, 8
    fstp qword [esp]
    push fmt_float
    call _printf
    add  esp, 12
    mov  byte [c], 65
    movzx eax, byte [c]
    push eax
    push fmt_char
    call _printf
    add  esp, 8
    mov eax, 0
    ret