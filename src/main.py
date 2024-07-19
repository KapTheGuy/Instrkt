import os

def compile(program, program_file):

    token = 0
    memname = "str"

    if program.startswith("prints"):
        token = 1 # PRINT token
    else:
        print('Invalid syntax')
        return


    filename = "runtime.asm"
    out = f"""


; actual code
section .text
    global _start

_start:
    ; nothing to do

"""
    if (token == 1):
        memname += "1"
        # Format the assembly code
        out += f"""
            ; write the message to stdout
            mov eax, 4         ; syscall number for sys_write
            mov ebx, 1         ; file descriptor 1 (stdout)
            mov ecx, {memname}     ; pointer to the message
            mov edx, {len(program[7:]) + 2}    ; message length
            int 0x80           ; make syscall

            ; exit the program
            mov eax, 1         ; syscall number for sys_exit
            xor ebx, ebx       ; exit status 0
            int 0x80           ; make syscall

        {memname} db '{program[7:]}', 10, 0
        """
    # Open the file in write mode
    with open(filename, 'w') as file:
        file.write(out)

    print(f'COMPILING {program_file}...')

    os.system('nasm -f elf32 runtime.asm -o hello.o')
    os.system('ld -m elf_i386 hello.o -o out')
    os.system('rm hello.o runtime.asm')


PROGRAM = "prints Hello World!"
name = 'test.inst'
compile(PROGRAM, name)
