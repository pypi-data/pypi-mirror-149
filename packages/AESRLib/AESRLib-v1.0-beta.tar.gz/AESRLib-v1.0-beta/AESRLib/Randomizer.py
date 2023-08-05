import base64
import random
from .FileHandler import fileHandler
from .KMI import KMI
class Randomize:
    def encrypt(self, file: str) -> tuple[str, int]:
        if fileHandler.isExistingFile(fileHandler(),file):
            alpha = KMI.createAlpha(KMI())
            rawList = fileHandler.readLines(fileHandler(),file)[0]
            rawList[len(rawList)-1]+='\n'
            mapper = KMI.AlphaMap(KMI(), alpha)
            encList = [None]*len(rawList)
            aKey = base64.b64encode(''.join(alpha).encode('utf-8')).decode('utf-8')+'\n'
            for i in range(len(rawList)):
                encList[i]=rawList[i].translate(rawList[i].maketrans(mapper))
            loc = random.randint(0, len(rawList)-1)
            encList.insert(loc, aKey)
            enc = ''.join(encList)
            return (enc, loc)

    def decrypt(self, ciphertext: str, loc: int) -> str:
        #encList=fileHandler.readLines(fileHandler(), ciphertext)[0]
        demapper = KMI.transAlphaMap(KMI(), ciphertext, loc)
        #ciphertext.remove(ciphertext[loc])
        decList = [None]*len(ciphertext)
        for i in range(len(ciphertext)):
            decList[i] = ciphertext[i].translate(ciphertext[i].maketrans(demapper))
        dec = ''.join(decList).replace(''.join(KMI().cArray),'')
        return dec