#!/usr/bin/python

def hexdump(src,length=16):

    print
    result = []
    digits = 4 if isinstance(src,unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7f else b'.' for x in s])
        result.append( b"%04X  %-*s  %s" % (i, length*(digits + 1), hexa, text) )
        print b'\n'.join(result)
        print


