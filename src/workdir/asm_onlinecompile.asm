section .data
hello db "Hello, world!",0xa  ; Hello, world! string followed by a newline character
len equ $ - hello            ; Length of the Hello, world! string

section .text
global _start

_start:
    ; Write Hello, world! to stdout
    mov eax, 4            ; The system call for sys_write (4)
    mov ebx, 1            ; File descriptor 1 - stdout
    mov ecx, hello        ; Pointer to the message
    mov edx, len          ; Message length
    int 0x80              ; Call kernel

    ; Exit the program
    mov eax, 1            ; The system call for sys_exit (1)
    xor ebx, ebx          ; Return a code of 0
    int 0x80              ; Call kernel