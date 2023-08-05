import os
class ErrorScan:
    def nTry(self,ismodify=None) -> int:
        if not os.path.exists('nt'):
            f=open('nt','x',encoding="utf-8")
            f.close()
        with open('nt', 'r',encoding="utf-8") as f:
            erc = f.read(1)
            f.close()
        if (erc == '' or erc is None):
            erc=0
        erc=int(erc)
        if ismodify:
            with open('nt','w',encoding="utf-8") as f:
                f.write(str(erc + 1))
                f.close()
        return erc

class FaultCheck:
    def faultTest(self):
        return False
