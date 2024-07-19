import os

def compile(program, program_file):

    filename = "runtime.asm"

    # Format the assembly code
    out = f"""
; declare variables
section .data
    hello db '{program}', 10, 0

; actual code
section .text
    global _start

_start:
    ; write the message to stdout
    mov eax, 4         ; syscall number for sys_write
    mov ebx, 1         ; file descriptor 1 (stdout)
    mov ecx, hello     ; pointer to the message
    mov edx, {len(program) + 2}    ; message length
    int 0x80           ; make syscall

    ; exit the program
    mov eax, 1         ; syscall number for sys_exit
    xor ebx, ebx       ; exit status 0
    int 0x80           ; make syscall
    """
    # Open the file in write mode
    with open(filename, 'w') as file:
        file.write(out)

    print(f'COMPILING {program_file}...')

    os.system('nasm -f elf32 runtime.asm -o hello.o')
    os.system('ld -m elf_i386 hello.o -o out')
    os.system('rm hello.o runtime.asm')

PROGRAM = 'Ok now what'
name = 'test.inst'
compile(PROGRAM, name)
