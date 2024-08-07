import os

def compile(program, program_file):

    with open('test.inst', 'r') as file:
        lines = file.readlines()

    memname = "str"

    filename = "runtime.asm"
    out = f"""

    section .data


    ; actual code
    section .text
        global _start

    _start:
        ; nothing to do

    """

    first = True
    integer1 = 0
    integer2 = 0

    while lines:
        token = 0
        program = lines[0].strip()

        if lines[0].startswith("std::out <<"):
            token = 1 # PRINT token
        elif lines[0].startswith("int"):
            token = 2 # INT token
            if(first):
                integer1 = int(program[4:])
                first = False
            else:
                integer2 = int(program[4:])
        elif lines[0].startswith("+"):
            token = 3 # ADD token
        elif lines[0].startswith("std::out_int >>"):
            token = 4 # PRINT INT token
        else:
            print('Invalid syntax')
            return

        if (token == 1):
            memname += "1"

            # Format the assembly code
            out += f"""
                ; write the message to stdout
                mov eax, 4         ; syscall number for sys_write
                mov ebx, 1         ; file descriptor 1 (stdout)
                mov ecx, {memname}     ; pointer to the message
                mov edx, {len(program[12:]) + 2}    ; message length
                int 0x80           ; make syscall
            """

            out = out.replace("section .data\n", f"section .data\n {memname} db '{program[12:]}', 10, 0\n")

        elif (token == 2):
            out += f""" 
                ; integer : push to stack
                mov eax, {program[4:]}
                push eax
            """

        elif (token == 3):
            out += f""" 
                ; integer : add
                pop eax
                pop ebx
                add eax, ebx

                mov ebx, eax
            """

        elif (token == 4):

            memname += "n1"

            out = out.replace("section .data\n", f"section .data\n {memname} db '{str(integer1+integer2)}', 10, 0\n")
            out = out.replace(f"section .data\n {memname} db '{str(integer1+integer2)}', 10, 0\n", f"section .data\n {memname} db '{str(integer1+integer2)}', 10, 0\n {memname + "len"} equ $-{memname}\n")

            out += f""" 
                ; integer : print
                ; write the message to stdout
                mov eax, 4         ; syscall number for sys_write
                mov ebx, 1         ; file descriptor 1 (stdout)
                mov ecx, {memname}     ; pointer to the message
                mov edx, {memname + "len"}    ; message length
                int 0x80           ; make syscall
            """

        lines = lines[1:]

    out += f"""
    ; exit the program
                mov eax, 1         ; syscall number for sys_exit
                ;xor ebx, ebx       ; exit status 0
                int 0x80           ; make syscall
    """

    # Open the file in write mode
    with open(filename, 'w') as file:
        file.write(out)

    print(f'COMPILING {program_file}...')

    os.system('nasm -f elf32 runtime.asm -o hello.o')
    os.system('ld -m elf_i386 hello.o -o out')
    os.system('rm hello.o runtime.asm')


PROGRAM = "prints Hello World, my program works"
name = 'test.inst'
compile(PROGRAM, name)
