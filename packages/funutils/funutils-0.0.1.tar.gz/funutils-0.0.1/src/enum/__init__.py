import sys
from typing import *

__all__ = ['parseEnumTree']

class EnumSyntaxError(SystemError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'Enum Syntax Error: {self.msg}'

class ArgCountError(ValueError):
    def __init__(self, real, should):
        self.real = real
        self.should = should

    def __str__(self):
        return f'Inappropriate Argument Count: {self.real}, expected {self.should}'

code: List[str] = []

def parseEnumTree(lines: List[str]):
    newlst = []
    for tokens in lines:
        newlst2 = []
        for token in tokens:
            if token.strip() != '':
                newlst2.append(token)
        if newlst2 != []:
            newlst.append(newlst2)
    lines: List[List[str]] = newlst
    del newlst
    if lines[0][0] != 'enum':
        raise EnumSyntaxError('You must use the enum keyword when creating an enum')
    else:
        nam = lines[0][1]
        try:
            _ = lines.index(['end', nam])
        except ValueError:
            raise EnumSyntaxError(f'Opening of enum {nam} found but closing not found')
        else:
            if lines.index(['end', nam]) == len(lines)-1:
                # single enum tree to parse, look for cases
                code.append(f'class {nam}:')
                cases = lines[1:-1]
                # re_add the string
                newlst = []
                for case in cases:
                    newstr = ''
                    for token in case[1:]:
                        newstr = newstr + token + ' '
                    newlst.append(newstr.strip())
                cases: List[str] = newlst
                del newlst
                for case in cases:
                    # parse case
                    idx = case.find('(')
                    idy = case.find(')')
                    if idx == -1 and idy == -1:
                        # plain case with no args
                        caseName = case
                        code.append(f'    class {caseName}:')
                        code.append('        def __init__(self):')
                        code.append('            pass')
                    elif idx != -1 and idy != -1:
                        # case with args
                        if idx < idy:
                            # normal args
                            caseName = case[:idx]
                            code.append(f'    class {caseName}:')
                            args = case[idx+1:idy]
                            args = args.split(',')
                            newlst = []
                            i = 1
                            for arg in args:
                                if arg.strip() != '':
                                    parts = arg.strip().split(' ')
                                    newparts = []
                                    for part in parts:
                                        if part.strip() != '':
                                            newparts.append(part.strip())
                                    parts = newparts
                                    del newparts
                                    if len(parts) == 1:
                                        newlst.append((parts[0], i, False))
                                        i += 1
                                    elif len(parts) == 2:
                                        newlst.append((parts[0], parts[1], True))
                            args = newlst
                            del newlst
                            initdef = '        def __init__(self'
                            for arg in args:
                                if arg[2]:
                                    initdef += f', {arg[1]}: {arg[0]}'
                                else:
                                    initdef += f', {arg[0]}{arg[1]}: {arg[0]}'
                            initdef += '):'
                            code.append(initdef)
                            for arg in args:
                                if arg[2]:
                                    code.append(f'            self.{arg[1]} = {arg[1]}')
                                else:
                                    code.append(f'            self.{arg[0]}{arg[1]} = {arg[0]}{arg[1]}')
                        else:
                            raise EnumSyntaxError('Found opening and closing parenthes, but mismatched in position.')
                    else:
                        raise EnumSyntaxError('Found opening or closing parenthes, but not matched.')
            else:
                # recursively parse
                parseEnumTree(lines[0:lines.index(['end', nam])+1])
                parseEnumTree(lines[lines.index(['end', nam])+1:])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ArgCountError(len(sys.argv)-1, 2)

    with open(sys.argv[1], 'r') as f:
        lines: List[str] = f.readlines()
        cpy = lines
        lines = []
        for line in cpy:
            if line.strip().replace('\n', '') != '':
                lines.append(line.replace('\n', '').strip())
        del cpy
        lines = [line.split(' ') for line in lines]
        parseEnumTree(lines)
        with open(sys.argv[2], 'w') as f:
            for line in code:
                f.write(line + '\n')