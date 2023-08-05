import sys

class BruckError(Exception):
    def __init__(self, value):
        Exception.__init__(self, value)

class BruckInterpreter:

    CHARS = ['[', ']']

    STRIP_LENGTH = 114514
    DEFAULT_STRIP = [0] * STRIP_LENGTH

    ADD = 0
    SUB = 1
    NXT = 2
    PRV = 3
    WRT = 4
    RDN = 5
    LFT = 6
    RGT = 7

    TOKENS = {
        '[]]': ADD,
        '[[]': SUB,
        ']][': NXT,
        '][[': PRV,
        '[][': WRT,
        '][]': RDN,
        '[[[': LFT,
        ']]]': RGT
    }

    def purify(self, origin):
        '''
        Remove all characters other than [ and ] in `origin'.
        '''
        pgm = ''
        for char in origin:
            if char in self.CHARS:
                pgm += char
        return pgm

    def __init__(self, origin):
        '''
        Initialize the interpreter with `origin' as the program, and purify the program.
        '''
        self.pgm = self.purify(origin)
        self.length = len(self.pgm)
        self.strip = self.DEFAULT_STRIP
        self.ptr = 0

    def tokenize(self, crt=0, depth=0):
        '''
        Tokenize the program.
        '''
        tokens = []
        self.length = len(self.pgm)
        if self.length % 3 != 0:
            err = '%d = 3 * %d + %d. How surprising.' % (self.length, self.length // 3, self.length % 3)
            raise BruckError(err)
        while crt < self.length:
            if self.TOKENS[self.pgm[crt:crt+3]] == self.LFT:
                crt, subtokens = self.tokenize(crt + 3, depth + 1)
                tokens.append(subtokens)
            elif self.TOKENS[self.pgm[crt:crt+3]] == self.RGT:
                if depth == 0:
                    err = ']' * (crt + 1)
                    raise BruckError(err)
                return crt + 3, tokens
            else:
                tokens.append((self.TOKENS[self.pgm[crt:crt+3]], crt + 1))
                crt += 3
        if depth > 0:
            err = 'Whatever we do, we must see it through to completion and not give up half way.'
            raise BruckError(err)
        return crt, tokens

    def run(self, tokens):
        '''
        Run a part (mostly between a pair of [[[ and ]]]) of the program.
        '''
        for token in tokens:
            if token[0] == self.ADD:
                self.strip[self.ptr] += 1
            elif token[0] == self.SUB:
                if self.strip[self.ptr] == 0:
                    err = 'We should always be p%ssitive.' % ('o' * token[1])
                    raise BruckError(err)
                self.strip[self.ptr] -= 1
            elif token[0] == self.NXT:
                self.ptr += 1
                if self.ptr >= self.STRIP_LENGTH:
                    err = 'Do not be so gr%sd.' % ('e' * token[1])
                    raise BruckError(err)
            elif token[0] == self.PRV:
                if self.ptr == 0:
                    err = 'N%sxt one, please!' % ('e' * token[1])
                    raise BruckError(err)
            elif token[0] == self.WRT:
                print(chr(self.strip[self.ptr]), end='')
            elif token[0] == self.RDN:
                self.strip[self.ptr] = ord(sys.stdin.read(1))
            else:
                while self.strip[self.ptr]:
                    self.run(token)

    def exec(self):
        '''
        Execute the program.
        '''
        _, tokens = self.tokenize()
        self.run(tokens)

if __name__ == '__main__':
    interpreter = BruckInterpreter(input())
    interpreter.exec()
