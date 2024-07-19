; declare variables
section .data
    hello db 'Hello World!', 10, 0

; actual code
section .text
    global _start

_start:
    ; write the message to stdout
    mov eax, 4         ; syscall number for sys_write
    mov ebx, 1         ; file descriptor 1 (stdout)
    mov ecx, hello     ; pointer to the message
    mov edx, 14        ; message length
    int 0x80           ; make syscall

    ; exit the program
    mov eax, 1         ; syscall number for sys_exit
    xor ebx, ebx       ; exit status 0
    int 0x80           ; make syscall
