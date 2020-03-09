#!/usr/bin/python

# for python 3.x

import sys
import re
#reload(sys)
#sys.setdefaultencoding('utf-8')

# usage: nt2pgcopy.py ntfile_name pgfile_name
#print ('test str.encode(\\u0259').decode('unicode-escape'))

fh = open(sys.argv[1],'r')

newfh = open(sys.argv[2],'w', encoding='utf-8')

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
            cl = str.encode(cl).decode("unicode-escape")
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
                cl = str.encode(cl).decode("unicode-escape")
                cl = cl.replace('\n','\\n')
                cr = ""
                clang = c[c.find('"@')+2:]
            else:
                clang = ""
                cl = c[1:-1]
                cl = str.encode(cl).decode("unicode-escape")
                cl = cl.replace('\n','\\n')
                cr = ""
    newfh.write ("%s\t%s\t%s\t%s\t%s\n" % (a, b, cl, cr, clang))
