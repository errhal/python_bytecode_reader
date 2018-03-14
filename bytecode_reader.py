import dis
import marshal
import types

ifPtr = open("input.pyc", 'rb')
header = ifPtr.read(8)
codeObject = marshal.load(ifPtr)
ifPtr.close()


def parse_code_object(code_object):
    co_argcount = code_object.co_argcount
    co_nlocals = code_object.co_nlocals
    co_stacksize = code_object.co_stacksize
    co_flags = code_object.co_flags

    insBytes = bytearray(code_object.co_code)

    i = 0
    while i < len(insBytes):
        opcode = insBytes[i]
        if opcode not in dis.opmap.values():
            print(str(i) + ":", "NOT EXISTING INSTRUCTION")
            i += 1
        elif opcode < dis.HAVE_ARGUMENT:
            print(str(i) + " : ", dis.opname[opcode], opcode, 0, 1)
            i += 1
        elif opcode >= dis.HAVE_ARGUMENT:
            if len(insBytes) > i + 2:
                arg = (insBytes[i + 2] << 8) | insBytes[i + 1]
            else:
                arg = -1
            print(str(i) + " : ", dis.opname[opcode], opcode, arg, 3)
            i += 3

    co_names = code_object.co_names

    co_varnames = code_object.co_varnames
    co_filename = code_object.co_filename
    co_name = code_object.co_name
    co_firstlineno = code_object.co_firstlineno
    co_lnotab = code_object.co_lnotab

    mod_const = []
    for const in code_object.co_consts:
        if isinstance(const, types.CodeType):
            mod_const.append(parse_code_object(const))
            pass
        else:
            mod_const.append(const)
    co_constants = tuple(mod_const)

    return types.CodeType(co_argcount, co_nlocals, co_stacksize, co_flags,
                          str(insBytes), co_constants, co_names, co_varnames,
                          co_filename, co_name, co_firstlineno, co_lnotab)


ofPtr = open('output.pyc', 'wb')
ofPtr.write(header)
marshal.dump(parse_code_object(codeObject), ofPtr)

ofPtr.close()
