from .Data_analysis import judgeMode
from .Data_Encoding import DataEncoding,minimize_version,bin_ext
from .Error_Correction_Coding import PolynomialLongDivision,toBlocks,generator_polynomial
from .constants import EC_table,remainders

def get_Codes(text:str,ErrorCorrectionLevel:str,version:int,Mode:str,show=False):
    codewords=DataEncoding(text,ErrorCorrectionLevel,version,Mode)
    EC_num=int(EC_table["{}-{}".format(version,ErrorCorrectionLevel)][1])
    totalStruct=toBlocks(codewords,version,ErrorCorrectionLevel)
    DataCodewords=[[[int(i,base=2) for i in block] for block in groups] for groups in totalStruct]
    ECCodewords=[[PolynomialLongDivision(block+[0]*EC_num,generator_polynomial(EC_num)) for block in groups] for groups in DataCodewords]
    DataCodewords,ECCodewords=sum(DataCodewords,[]),sum(ECCodewords,[])
    if show:DataCodewords,ECCodewords=[[0 for i in j] for j in DataCodewords],[[255 for i in j] for j in ECCodewords]
    codes=[]
    for i in range(len(max(DataCodewords,key=len))):
        for j in DataCodewords:
            if i<len(j):
                codes.append(j[i])
    for i in range(EC_num):
        for j in ECCodewords:
            codes.append(j[i])
    codes="".join(bin_ext(i,8) for i in codes)+remainders[version]*'0'
    return codes
if __name__=="__main__":
    text,ErrorCorrectionLevel="HELLO WORLD","Q"
    Mode=judgeMode(text)
    version=minimize_version(text,ErrorCorrectionLevel,Mode)
    print(get_Codes(text,ErrorCorrectionLevel,version,Mode))