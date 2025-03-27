import struct
import time

class Seg74:
    def __init__(self, i2c, i2c_addr):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.seg74init()
        self.dic = {'0':0x3f, '1':0x06, '2':0x5b, '3':0x4f, '4':0x66, '5':0x6d, '6':0x7d, '7':0x27, '8':0x7f, '9':0x67,
               'A':0x77, 'b':0x7c, 'c':0x58, 'd':0x5e, 'E':0x79, 'F':0x71, '-':0x40, '.':0x80, ' ':0x00,
               'o':0x5c, 'P':0x73, 'r':0x50, 'h':0x74, '_':0x08, 'n':0x54, '=':0x48, 'U':0x3e, 'u':0x1c,
               'C':0x39, '[':0x21, ']':0x0c, 'L':0x38, 'I':0x30, 'i':0x04, 'S':0x6d, 't':0x78, 's':0x6d,
               'p':0x73, 'N':0x54, 'a':0x77, 'B':0x7c, 'D':0x5e, 'G':0x3d, 'g':0x3d, 'J':0x0e, 'j':0x0e,
               'l':0x38, 'O':0x3f, 'Q':0x67, 'q':0x67, 'R':0x50, 'y':0x66, 'Y':0x66, 'e':0x7b, 'T':0x78,
               'H':0x76, 'f':0x71, '{':0x21, '}':0x06, ':':0x48}
        self.rawdic = {'a':0x01, 'b':0x02, 'c':0x04, 'd':0x08, 'e':0x10, 'f':0x20, 'g':0x40, '.':0x80, ' ':0x00}
    def seg74init(self):
        self.i2c.writeto(self.i2c_addr, b'\x21')
        self.i2c.writeto(self.i2c_addr, b'\xea')
        self.i2c.writeto(self.i2c_addr, b'\x81')

    def max(self):
        self.i2c.writeto(self.i2c_addr, b'\xef')

    def min(self):
        self.i2c.writeto(self.i2c_addr, b'\xe1')

    def blink(self):
        self.i2c.writeto(self.i2c_addr, b'\x83')

    def off(self):
        self.i2c.writeto(self.i2c_addr, b'\x80')

    def on(self):
        self.i2c.writeto(self.i2c_addr, b'\x81')
        
    def eightall(self):
        self.seg74('8.8.8.8.')

    def dot4(self):
        self.seg74(' . . . .')
        
    def seg74(self, four_letter, blink = False):
        letters = []
        dotpos = []
        dotposnew = []
        n = len(four_letter)
        for i in range(n):
            if four_letter[i] == '.':
                dotpos.append('.')
            else:
                dotpos.append(0)
                letters.append(four_letter[i])
        n = len(dotpos)
        flag = False
        for i in range(n):
            m = n-i-1
            if dotpos[m] == '.':
                dotposnew.append(self.dic['.'])
                flag = True
            elif flag != True:
                dotposnew.append(0)
            else:
                flag = False
        dotposnew.reverse()
        if (letters[0] in self.dic) == False:
            letters[0] = '_'
        if (letters[1] in self.dic) == False:
            letters[1] = '_'
        if (letters[2] in self.dic) == False:
            letters[2] = '_'
        if (letters[3] in self.dic) == False:
            letters[3] = '_'

        self.i2c.writeto(self.i2c_addr, struct.pack('BB',0,self.dic[letters[0]] + dotposnew[0]))
        self.i2c.writeto(self.i2c_addr, struct.pack('BB',2,self.dic[letters[1]] + dotposnew[1]))
        self.i2c.writeto(self.i2c_addr, struct.pack('BB',4,self.dic[letters[2]] + dotposnew[2]))
        self.i2c.writeto(self.i2c_addr, struct.pack('BB',6,self.dic[letters[3]] + dotposnew[3]))

    def seg74ada(self, four_letter, blink = False):
        letters = []
        dotpos = []
        dotposnew = []
        n = len(four_letter)
        for i in range(n):
            if four_letter[i] == '.':
                dotpos.append('.')
            else:
                dotpos.append(0)
                letters.append(four_letter[i])
        n = len(dotpos)
        flag = False
        for i in range(n):
            m = n-i-1
            if dotpos[m] == '.':
                dotposnew.append(self.dic['.'])
                flag = True
            elif flag != True:
                dotposnew.append(0)
            else:
                flag = False
        dotposnew.reverse()
        if (letters[0] in self.dic) == False:
            letters[0] = '_'
        if (letters[1] in self.dic) == False:
            letters[1] = '_'
        if (letters[2] in self.dic) == False:
            letters[2] = '_'
        if (letters[3] in self.dic) == False:
            letters[3] = '_'

        self.i2c.writeto(self.i2c_addr, struct.pack('BB',0,self.dic[letters[0]] + dotposnew[0]))
        self.i2c.writeto(self.i2c_addr, struct.pack('BB',2,self.dic[letters[1]] + dotposnew[1]))
        self.i2c.writeto(self.i2c_addr, struct.pack('BB',6,self.dic[letters[2]] + dotposnew[2]))
        self.i2c.writeto(self.i2c_addr, struct.pack('BB',8,self.dic[letters[3]] + dotposnew[3]))

    def scroll(self, string, endhold = True, blink = False):
        tmpstr = "    " + string
        n = len(tmpstr)+1
        if endhold == True:
            n = n -4 -tmpstr.count('.')
        for i in range(n):
            self.seg74(tmpstr, blink)
            time.sleep(0.3)
            tmpstr = tmpstr[1:] + " "
            if tmpstr[0] == '.':
                tmpstr = tmpstr[1:]

    def scrollada(self, string, endhold = True, blink = False):
        tmpstr = "    " + string
        n = len(tmpstr)+1
        if endhold == True:
            n = n -4 -tmpstr.count('.')
        for i in range(n):
            self.seg74ada(tmpstr, blink)
            time.sleep(0.5)
            tmpstr = tmpstr[1:] + " "
            if tmpstr[0] == '.':
                tmpstr = tmpstr[1:]


    def seg74raw(self, four_letter ):
        letters = []
        dotpos = []
        dotposnew = []
        n = len(four_letter)
        for i in range(n):
            if four_letter[i] == '.':
                dotpos.append('.')
            else:
                dotpos.append(0)
                letters.append(four_letter[i])
        n = len(dotpos)
        flag = False
        for i in range(n):
            m = n-i-1
            if dotpos[m] == '.':
                dotposnew.append(self.dic['.'])
                flag = True
            elif flag != True:
                dotposnew.append(0)
            else:
                flag = False
        dotposnew.reverse()
        if (letters[0] in self.rawdic) == False:
            letters[0] = '_'
        if (letters[1] in self.rawdic) == False:
            letters[1] = '_'
        if (letters[2] in self.rawdic) == False:
            letters[2] = '_'
        if (letters[3] in self.rawdic) == False:
            letters[3] = '_'

        self.i2c.writeto(self.i2c_addr, struct.pack('bb',0,self.rawdic[letters[0]] + dotposnew[0]))
        self.i2c.writeto(self.i2c_addr, struct.pack('bb',2,self.rawdic[letters[1]] + dotposnew[1]))
        self.i2c.writeto(self.i2c_addr, struct.pack('bb',6,self.rawdic[letters[2]] + dotposnew[2]))
        self.i2c.writeto(self.i2c_addr, struct.pack('bb',8,self.rawdic[letters[3]] + dotposnew[3]))


