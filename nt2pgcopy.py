#!/usr/bin/python
# for python 2.7

import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


#print 'test \\u0259'.decode('unicode-escape')

fh = open(sys.argv[1],'r')


i = 0;
while(1):
    i = i + 1
    s = fh.readline().strip()
    if (s == ""):
        break;
    (a, b, c) = s.split(' ', 2)
    c = c[:-2]
    if c.find('"^^<') > 0:
        e = c.find('"^^<')
        cl = c[1:e]
        cr = c[e+3:]
        clang = ""
        if cr.find("XMLSchema#string") > 0:
            cl = cl.decode("unicode-escape")
            cl = cl.replace('\n','\\n')
    elif re.match('^<.+>$', c):
        cl = ""
        cr = c
        clang = ""
    else:
        if c.find('"') != 0:
           cl = c
           cr = ""
           clang = ""
        else:
            if c.find('"@') > 0:
                cl = c[1:c.find('"@')]
                cl = cl.decode("unicode-escape")
                cl = cl.replace('\n','\\n')
                cr = ""
                clang = c[c.find('"@')+2:]
            else:
                clang = ""
                cl = c[1:-1]
                cl = cl.decode("unicode-escape")
                cl = cl.replace('\n','\\n')
                cr = ""
    print "%s\t%s\t%s\t%s\t%s" % (a, b, cl, cr, clang)
