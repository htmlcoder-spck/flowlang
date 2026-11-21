import re

code = '''
var int:x = 5
if (x = 5) then:
   PrintLine("OK")
'''

# 1. LEXER (Tokenizer)
TOKENS = [
    ('VAR', r'var\b'), ('TYPE', r'int|bool|char|string'),
    ('IF', r'if\b'), ('THEN', r'then\b'), ('PRINT', r'PrintLine\b'),
    ('NUM', r'\d+'), ('STR', r'"[^"]*"'), ('ID', r'[a-zA-Z_]\w*'),
    ('OP', r'[=:()]'), ('SKIP', r'[ \t\n]+|//.*')
]
regex = '|'.join(f'(?P<{name}>{pat})' for name, pat in TOKENS)
tokens = [(m.lastgroup, m.group()) for m in re.finditer(regex, code) if m.lastgroup != 'SKIP']

# 2. PARSER (Builds AST)
pos = 0
def eat(kind):
    global pos
    val = tokens[pos][1]
    pos += 1
    return val

def parse():
    ast = []
    while pos < len(tokens):
        if tokens[pos][0] == 'VAR':
            eat('VAR'); eat('TYPE'); eat('OP')
            name = eat('ID'); eat('OP'); val = int(eat('NUM'))
            ast.append(('VAR', name, val))
        elif tokens[pos][0] == 'IF':
            eat('IF'); eat('OP'); left = eat('ID'); eat('OP')
            right = int(eat('NUM')); eat('OP'); eat('THEN'); eat('OP')
            eat('PRINT'); eat('OP'); msg = eat('STR').strip('"'); eat('OP')
            ast.append(('IF', left, right, msg))
    return ast

# 3. CODEGEN (Emits raw x86-64 Linux Machine Code)
def compile_x64(ast):
    mc = bytearray()
    data = bytearray()
    for node in ast:
        if node[0] == 'VAR':
            # mov eax, <val>
            mc += b'\xb8' + node[2].to_bytes(4, 'little')
        elif node[0] == 'IF':
            msg = (node[3] + '\n').encode()
            data += msg
            # cmp eax, <right>  |  jne +24 (skip print)
            mc += b'\x3d' + node[2].to_bytes(4, 'little') + b'\x75\x18'
            # sys_write(1, msg, len)
            mc += b'\xb8\x01\x00\x00\x00'          # mov eax, 1 (write)
            mc += b'\xbf\x01\x00\x00\x00'          # mov edi, 1 (stdout)
            mc += b'\x48\x8d\x35\x10\x00\x00\x00'  # lea rsi, [rip + 16]
            mc += b'\xba' + len(msg).to_bytes(4, 'little') # mov edx, len
            mc += b'\x0f\x05'                      # syscall
    # sys_exit(0)
    mc += b'\xb8\x3c\x00\x00\x00\x31\xff\x0f\x05'
    return bytes(mc + data)

machine_code = compile_x64(parse())
print("Machine Code (Hex):", machine_code.hex(' '))
