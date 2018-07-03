# -*- coding: utf-8 -*-

def fun(st,f):
    s2 = unicode('(注:',"utf-8")
    s3 = unicode(')',"utf-8")
    pos = 0
    pos2 = 0
    start = 0
    s1 = unicode(st,"utf-8")
    newline = unicode('\n',"utf-8")
    a=0
    while(pos >= 0):
        pos = f.find(s1,a)
        pos2 = f.find(s1,pos+1)
        a = f.find(newline,pos2+1)
        seg = f[pos2+len(s1):a]
        if(pos > -1):
            f = f[0:pos]+s2+seg+s3+f[pos+len(s1):pos2]+f[a+2:-1]
            a += len(seg)
        print(len(seg), pos, pos2, a, len(f))
    return f
    
a = open('ss.txt', 'r')
f = a.read()
a.close()
f = unicode(f,"utf-8")
print(len(f))

f = fun('【注】',f)
f = fun('【注1】',f)
f = fun('【注2】',f)
f = fun('【注3】',f)
f = fun('【注4】',f)
f = fun('【注5】',f)
f = fun('【注6】',f)
f = fun('【注7】',f)

a = open('ss2.txt', 'w')
a.write(f.encode('utf-8'))
a.close()
