from .ErrChecker import ErrorScan, FaultCheck
from .FileHandler import fileHandler
from .KMI import KMI
from .Randomizer import Randomize
class AESEncrypter:
    def __init__(self):
        self.PAD_SIZE=16
        self.sep='.'

    def pad(self,s: str) -> str:
        s+= (self.PAD_SIZE - len(s) % self.PAD_SIZE) * chr(self.PAD_SIZE - len(s) % self.PAD_SIZE)
        return s

    def unpad(self,s: str) -> str:
        s+=s[:-ord(s[len(s) - 1])]
        return s

    def AESencrypt(self,raw,conf):
        return conf.encrypt(self.pad(raw).encode('utf-8'))

    def AESdecrypt(self,ciphertext,conf):
        return self.unpad(conf.decrypt(ciphertext).decode('utf-8'))

def initializer(file):
    if ErrorScan.nTry(ErrorScan(), None)<3:
        choice = input("Do you want to create a new key or proceed with existing key: [y/n]")
        match choice.lower():
            case 'y':
                flag=True
                while(flag):
                    try:
                        if(fileHandler.isExistingFile(fileHandler(), file)):
                            print("<--- ENCRYPTION INTERFACE -->")
                            flen = str(fileHandler.reader(fileHandler(), file)[1])
                            renc,ptr=Randomize.encrypt(Randomize(), file)
                            pwd = input("Please enter a new password:")
                            print("Executing Phase 1/2 Encryption")
                            print("Executing Phase 2/2 Encryption")
                            conf = KMI.createConf(KMI(), pwd)
                            enc = KMI.BtoS(KMI(), AESEncrypter.AESencrypt(AESEncrypter(), renc, conf[0]))
                            pKey = conf[1] + KMI.BtoS(KMI(), (str(ptr) + AESEncrypter().sep).encode('utf-8')) + KMI.BtoS(KMI(), flen.encode('utf-8'))
                            print("Done. Started automated fault check [beta]...")
                            flag = FaultCheck.faultTest(FaultCheck())
                            if(flag):
                                print("Fault found in pKey, please re-create your key again!")
                            print("Completed fault check: No issues found.")
                            print("Note: This pkey below will be shown only once! Please keep it safe and remember the password that you entered before!")
                            print("Your pKey is: {}".format(pKey))
                            fileHandler.writer(fileHandler(), enc, file)
                        else:
                            print("Provided input is not a file or doesn't exist! Give filename including exts [e.g.] test.txt ")
                            break
                    except Exception as e:
                        print(e)
            case 'n':
                try:
                    if (fileHandler.isExistingFile(fileHandler(), file)):
                        print("<-- DECRYPTION INTERFACE -->")
                        print("Note: Max 3 attempts are allowed! Its case sensitive.")
                        pKey=input("Please enter your pKey:")
                        pwd = input("Please enter your password:")
                        conf = KMI.getConf(KMI(), pwd, pKey)
                        bdec = KMI.StoB(KMI(), fileHandler.reader(fileHandler(), file)[0])
                        dec = AESEncrypter.AESdecrypt(AESEncrypter(), bdec, conf)
                        lsep=pKey.rindex(KMI.BtoS(KMI(), AESEncrypter().sep.encode('utf-8')))
                        loc,sep=pKey[2*KMI().plength:lsep],pKey[lsep+2:]
                        ptr = int(KMI.StoB(KMI(), loc).decode('utf-8'))
                        rdec = Randomize.decrypt(Randomize(), dec.splitlines(True), ptr)[:int(KMI.StoB(KMI(),sep).decode('utf-8'))]
                        fileHandler.writer(fileHandler(), rdec, file)
                        print("Decrypted Successfully.")
                    else:
                        print("Provided input is not a file or doesn't exist! Give filename including exts [e.g.] test.txt ")
                except Exception:
                    ErrorScan.nTry(ErrorScan(), True)
                    print("You entered wrong password!")
            case _:
                raise ValueError("Please provide valid input!")
    else:
        print("You exceeded max attempts!")
