section .data
    ; No data section needed for this example

section .text
    global _start

_start:
    ; Pushing integers onto the stack
    mov eax, 10         ; first integer (change values as needed)
    push eax
    mov eax, 20         ; second integer (change values as needed)
    push eax

    ; Adding the integers
    pop eax             ; pop the second integer into eax
    pop ebx             ; pop the first integer into ebx
    add eax, ebx        ; eax = eax + ebx

    ; Store the result to be returned
    mov ebx, eax        ; move result (in eax) to ebx for syscall argument

    ; Exit the program and return the result
    mov eax, 1          ; syscall number for sys_exit
    int 0x80            ; perform syscall to return ebx (result)
