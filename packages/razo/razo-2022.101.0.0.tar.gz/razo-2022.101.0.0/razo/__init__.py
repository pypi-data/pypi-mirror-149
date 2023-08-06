#coding=utf-8
import datetime
import sys
import time
import os
import numpy as np
import password as pw

class razo_p():
    password = pw.Password(method='sha512', hash_encoding='base64')

try:
    from langpack import pack
except ModuleNotFoundError as aheddew:
    from langpack_d import pack
vers=['2022.101.0.0','sys_2']
rooting=False
sudoroot=False
nowsudo=False
try:
    if sys.argv[1]=='-root':
        rooting=True
except IndexError as inddde:
    rooting=False
liense=pack[0]
def etting():
    print(pack[1])
    print(liense)
    a=input(pack[2])
    if a=='n':
        print(pack[3])
        time.sleep(5)
        sys.exit(0)
    print(pack[4])
    a=input('\033[0;30;40m')
    print('\033[0;37;40m')
    c=razo_p()
    c.password=a
    np.save('passw.npy', c)
    a=input(pack[5])
    with open('settings.py','a') as c:
        c.write("username='{}'\n".format(a))
    
def showinfo():
    listget=pack[13]
    timer=datetime.datetime.now()
    weekday=listget[timer.weekday()]
    print(timer.strftime(pack[14])+' {}'.format(weekday) )
    tdo=[]
    print('Razo {0}({1})'.format(vers[0],vers[1]))
    print(pack[6])


h=pack[8]



if __name__=='__main__':
    try:
        read1 = np.load('passw.npy', allow_pickle=True).item()
    except FileNotFoundError as e:
        etting()
    
def sc():
    global sudoroot
    if not sudoroot:
        a=input(pack[9]+'\033[8;37;40m')
        print('\033[8;37;40m')
        if read1.password==a:
            sudoroot=True
            return True
        else:
            print(pack[18])
            return False
    else:
        return True

def help():
    print(h)
def su():
    global rooting
    if rooting:
        return 0
    a = input(pack[9] + '\033[8;37;40m')
    print('\033[0;37;40m')
    if read1.password==a:
        rooting = True
    else:
        time.sleep(2)
        print(pack[10])
def shutdown():
    if rooting:
        yes=input(pack[11])
        if yes=='y':
            print(pack[12])
            time.sleep(5)
            sys.exit(0)

def setting():
    global rooting
    if rooting:
        etting()
        rooting = False
    else:
        print(pack[15])
def time():
    listget = pack[13]
    timer = datetime.datetime.now()
    weekday = listget[timer.weekday()]
    print(timer.strftime(pack[14]) + ' {}'.format(weekday))
def info():
    showinfo()
def wai(a):
    global nowsudo
    try:
        exec(a+'()')
    except (SyntaxError,NameError) as abcddd:
        if a.split(' ')[0]=='sudo':
            sc()
            try:
                exec(a.split(" ")[1]+'()')
            except (SyntaxError,NameError) as abcdde:
                try:
                    os.system(a)
                except SystemExit as fhuuuifr:
                    pass
        else:
            try:
                os.system(a)
            except SystemExit as fhuuuifr:
                pass
def main_p():
    while True:
        if rooting:
            a=input('[root]>>>')
        else:
            a=input('[user]>>>')
        wai(a)
if __name__=='__main__':
    showinfo()
    import settings
    print(pack[17].format(settings.username))
    main_p()

