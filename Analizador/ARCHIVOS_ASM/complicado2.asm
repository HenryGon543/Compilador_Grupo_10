section .data
    _fc0 dq 5.44
    t5 dd 0
    i dd 0
    t4 dd 0
    contador dd 0
    t3 dd 0
    repetir dd 0
    b dd 0
    t6 dd 0
    t7 dd 0
    c dd 0
    debe dd 0
    a dq 0.0
    letra db 0
    fmt_int   db "%d",10,0
    fmt_float db "%f",10,0
    fmt_char  db "%c",10,0
    fmt_str   db "%s",10,0
    str_0 db "hola",0
    str_1 db "float",0
    str_2 db "falso",0
    str_3 db "verdadero",0
    str_4 db "se debe repetir 4 veces",0
    str_5 db "Hola 5 veces",0
section .text
global _main
extern _printf
_main:
    fld  qword [_fc0]
    fstp qword [a]
    mov  dword [b], 10
    mov  dword [contador], 0
    mov  dword [c], 128
    push str_0
    push fmt_str
    call _printf
    add  esp, 8
    push str_1
    push fmt_str
    call _printf
    add  esp, 8
    fld  qword [a]
    sub  esp, 8
    fstp qword [esp]
    push fmt_float
    call _printf
    add  esp, 12
    mov  dword [t3], 0
    mov eax, [t3]
    cmp eax, 1
    je  L1
    push str_2
    push fmt_str
    call _printf
    add  esp, 8
    jmp L2
L1:
    push str_3
    push fmt_str
    call _printf
    add  esp, 8
L2:
L3:
    mov  eax, [contador]
    cmp  eax, 4
    jl TRUE_t4
    mov  dword [t4], 0
    jmp  END_t4
TRUE_t4:
    mov  dword [t4], 1
END_t4:
    mov eax, [t4]
    cmp eax, 0
    je END_L3
    push str_4
    push fmt_str
    call _printf
    add  esp, 8
    mov  eax, [contador]
    add  eax, 1
    mov  [t5], eax
    mov  eax, [t5]
    mov  [contador], eax
    jmp L3
END_L3:
    mov  byte [letra], 66
    movzx eax, byte [letra]
    push eax
    push fmt_char
    call _printf
    add  esp, 8
    mov  dword [i], 0
L4:
    mov  eax, [i]
    cmp  eax, 5
    jl TRUE_t6
    mov  dword [t6], 0
    jmp  END_t6
TRUE_t6:
    mov  dword [t6], 1
END_t6:
    mov eax, [t6]
    cmp eax, 0
    je END_L4
    push str_5
    push fmt_str
    call _printf
    add  esp, 8
    mov  eax, [i]
    add  eax, 1
    mov  [t7], eax
    mov  eax, [t7]
    mov  [i], eax
    jmp L4
END_L4:
    mov eax, 0
    ret