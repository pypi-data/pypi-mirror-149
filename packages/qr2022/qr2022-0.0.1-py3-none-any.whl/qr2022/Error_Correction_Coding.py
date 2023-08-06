from .Data_analysis import judgeMode
from .Data_Encoding import DataEncoding,minimize_version
from .constants import EC_table,Log_table,AntiLog_table

def toBlocks(codewords:str,version:int,ErrorCorrectionLevel:str):
    codewords=[codewords[i:i+8] for i in range(0,len(codewords),8)]
    row=[int(i) if i else 0 for i in EC_table["{}-{}".format(version,ErrorCorrectionLevel)]]
    Groups=[[],[]]
    for i in range(row[2]):Groups[0].append(codewords[i*row[3]:(i+1)*row[3]])
    for i in range(row[4]):Groups[1].append(codewords[row[2]*row[3]+i*row[5]:row[2]*row[3]+(i+1)*row[5]])
    return Groups
def PolynomialLongDivision(a:list,b:list,retval="remainder"):
    """retval:['remainder','Quotient']"""
    a,b=list(reversed(a)),list(reversed(b))
    ret=[0]*(len(a)-len(b)+1)
    while len(a)>=len(b):
        ret[len(a)-len(b)]=Div(a[-1],b[-1])
        b1=[0]*(len(a)-len(b))+[Mul(i,ret[len(a)-len(b)]) for i in b]
        a=[Sub(a[i],b1[i]) for i in range(len(a)-1)]
    ret.reverse(),a.reverse()
    return a if retval=="remainder" else ret
def Add(a:int,b:int):
    if a<0 or a>255 or b<0 or b>255:raise ValueError("Add input not in GF(256)!")
    return a^b
def Sub(a:int,b:int):
    if a<0 or a>255 or b<0 or b>255:raise ValueError("Sub input not in GF(256)!")
    return a^b
def Mul(a:int,b:int):
    if a<0 or a>255 or b<0 or b>255:raise ValueError("Mul input not in GF(256)!")
    if a==0 or b==0:return 0
    return AntiLog_table[(Log_table[a]+Log_table[b])%255]
def Div(a:int,b:int):
    if a<0 or a>255 or b<0 or b>255:raise ValueError("Div input not in GF(256)!")
    if a==0:return 0
    return AntiLog_table[(Log_table[a]-Log_table[b])%255]
def PolynomialMul(a:list,b:list):
    a,b=list(reversed(a)),list(reversed(b))
    ret=[0]*(len(a)+len(b)-1)
    for ii,i in enumerate(a):
        for jj,j in enumerate(b):
            ret[ii+jj]=Add(ret[ii+jj],Mul(i,j))
    ret.reverse()
    return ret
def generator_polynomial(n:int):
    ret=[1,AntiLog_table[0]]
    for i in range(1,n):
        ret=PolynomialMul(ret,[1,AntiLog_table[i]])
    return ret
if __name__=="__main__":
    text,ErrorCorrectionLevel="HELLO WORLD","M"
    Mode=judgeMode(text)
    version=minimize_version(text,ErrorCorrectionLevel,Mode)
    codewords=DataEncoding(text,ErrorCorrectionLevel,version,Mode)
    EC_num=int(EC_table["{}-{}".format(version,ErrorCorrectionLevel)][1])
    print(PolynomialLongDivision([int(i,base=2) for i in toBlocks(codewords,version,"M")[0][0]]+[0]*EC_num,generator_polynomial(EC_num)))