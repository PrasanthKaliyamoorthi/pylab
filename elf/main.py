import binascii as bi

ELF = []

HEX = { 
    ### program header ###
    "magic":'7f454c46',                 # set to ELF, magic no tells OS what type of file it is
    "memory_arch":"02",                 # set to 64 bit, executable meaning that addresses in memory are 64 bits long
    "endian":"01",                      # set to little endian
    "elf_version":"01",                 # set to 1, elf version still 1
    "os_abi":"00",                      # set to 0, 0 for Unix compatable 3 for Linux
    "os_abi_version":"00",              # set to 0
    "padding":"00000000000000",         # set to 0 for 7 bytes

    "object_type":"0200",               # set to 2, means executable / written in little endian
    "architecture":"3e00",              # set to AMD x86-64 / written in little endian
    "file_version":"01000000",          # set to 1 / written in little endian
    "entry_point":"7800400000000000",   # header_size + n_headers * header_table_entry_size = 64 + 1 * 56 = 120 = 0x78
    "h_table_offset":"4000000000000000",# set to 64, 0x40
    "s_table_offset":"0000000000000000",# set to 0, means there is none
    "flags":"00000000",                 # set to 0, there is no flags defined
    "header_size":"4000",               # set to 60, 0x40
    "h_entry_size":"3800",              # set to 56,
    "no_h_entrys":"0100",               # set to 1,
    "s_entry_size":"4000",              # set to 64,
    "no_s_entrys":"0000",               # set to 0,
    "s_index_in_entry":"0000",            # set to 0, section header table index to section names
    ### program header table ###
    "segment_type":"01000000",          # set to 1,
    "bit_mask":"05000000",              # set to 5,
    "segment_offset":"0000000000000000",# set to 0,
    "seg_load_vaddr":"0000400000000000",# set to virtual address
    "seg_load_paddr":"0000400000000000",# set to virtual address
    "file_size":"7f00000000000000",     # set to header_size(64) * no_headers(1) + table_entry_size(56) + code_size (???)
    "f_size_in_memo":"7f00000000000000",# set to same as file_size
    "alignment":"0010000000000000",     # set to 1000
}

LIB = {
    "exit":{
        "exit":"b8"+"3c000000",             # means move 1 byte to AL, 60 to register AL (60 is syscall exit)
        "exit_code":"bf"+"00000000",               # means move 0 to dil(b7) with prefix 40
        "syscall":"0f05",                   # means syscall
    },
    "print":{
        "print":"48b8"+"01000000",          # rax = 1 , syscall write
        "fd":"48bf"+"01000000",             # rdi = 1 , file discripter to write
        "str":"",
    },
    "str_hello":{
        "push_bp":"55",                     # push base pointer to stack
        "mv_sp_bp":"4889e5",                # mv stack pointer to base pointer
        "mv_rstr_rax":"48b8"+"6f20576f726c6400" # 
    }
}

CODE = {
    "exit": LIB["exit"],
}

def hex_2_bi(txt :str) -> bytes:
    return bi.unhexlify(txt)

def elf_build():
    for value in HEX.values():
        ELF.append(hex_2_bi(value))
    for code in CODE.values():
        for value in code.values():
            ELF.append(hex_2_bi(value))

def elf_writer():
    with open('test', 'bw') as elf:
        elf.writelines(ELF)

def main():
    elf_build()
    elf_writer()


if __name__ == "__main__":
    main()
