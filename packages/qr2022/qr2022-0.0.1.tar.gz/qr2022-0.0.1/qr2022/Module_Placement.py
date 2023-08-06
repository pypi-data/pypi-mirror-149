from .Data_analysis import judgeMode
from .Data_Encoding import minimize_version
from .Structure_Final_Message import get_Codes
from .constants import alignment_table,Mask_Pattern,Format_info,Version_info
import numpy as np
import cv2

def version2size(version:int):
    if version<1 or version>40:raise ValueError("version {} error".format(version))
    return 4*version+17
def _overlap(size:int,x:int,y:int):
    return (x<8 and y<8) or (x>size-9 and y<8) or (y>size-9 and x<8)
def overlap(size:int,i:int,j:int):
    return _overlap(size,i-2,j-2) or _overlap(size,i-2,j+2) or _overlap(size,i+2,j-2) or _overlap(size,i+2,j+2)
def Blank(version:int):
    size=version2size(version)
    ret=np.full((size,size),-1)
    finder=np.ones((7,7))
    finder[1,1:-1],finder[-2,1:-1],finder[1:-1,1],finder[1:-1,-2]=0,0,0,0
    ret[:7,:7]=ret[:7,-7:]=ret[-7:,:7]=finder
    ret[7,:8],ret[:8,7],ret[-8,:8],ret[-7:,7],ret[:8,-8],ret[7,-7:]=0,0,0,0,0,0
    ap=np.ones((5,5))
    ap[1:-1,1:-1]=0
    ap[2,2]=1
    for i in alignment_table[version]:
        for j in alignment_table[version]:
            if not overlap(size,i,j):ret[i-2:i+3,j-2:j+3]=ap
    for i in range(8,size-8):
        ret[6,i]=ret[i,6]=(i+1)%2
    ret[4*version+9,8]=1
    ret[8,:6],ret[:6,8],ret[7:9,8],ret[8,7],ret[8,-8:],ret[-7:,8]=2,2,2,2,2,2
    if version>=7:ret[-11:-8,:6],ret[:6,-11:-8]=2,2
    return ret
def PlaceData(codes:str,src:np.ndarray,mask:int,order=None,show=False):
    src=src.copy()
    size=src.shape[0]
    codes=list(reversed(codes))
    i,j=size-1,size-1
    state=11
    while j>6:
        if src[i,j]==-1:
            src[i,j]=codes.pop()
            if show and src[i,j]==1:src[i,j]=3
            if order!=None:order.append((i,j))
            if mask!=None and Mask_Pattern[mask](i,j):
                src[i,j]=1 if src[i,j]==0 else 0
        if state==11:j,state=j-1,12
        elif state==12:
            if i==0:j,state=j-1,21
            else:i,j,state=i-1,j+1,11
        elif state==21:j,state=j-1,22
        elif state==22:
            if i==size-1:j,state=j-1,11
            else:i,j,state=i+1,j+1,21
        else:raise ValueError("state {} not defined.".format(state))
    state=21
    i,j=0,5
    while not (i==size-1 and j==0):
        if src[i,j]==-1:
            src[i,j]=codes.pop()
            if show and src[i,j]==1:src[i,j]=3
            if order!=None:order.append((i,j))
            if mask!=None and Mask_Pattern[mask](i,j):
                src[i,j]=1 if src[i,j]==0 else 0
        if state==11:j,state=j-1,12
        elif state==12:
            if i==0:j,state=j-1,21
            else:i,j,state=i-1,j+1,11
        elif state==21:j,state=j-1,22
        elif state==22:
            if i==size-1:j,state=j-1,11
            else:i,j,state=i+1,j+1,21
        else:raise ValueError("state {} not defined.".format(state))
    if codes:raise Exception("ERROR occured in PlaceData!!!")
    return src
def toqr(src:np.ndarray,dsize=(400,400),order=None):
    tmp=np.zeros((*src.shape,3))
    tmp[:,:,0]=tmp[:,:,1]=tmp[:,:,2]=src
    for i in range(tmp.shape[0]):
        for j in range(tmp.shape[1]):
            if tmp[i,j,0]==1:tmp[i,j]=0
            elif tmp[i,j,0]==0:tmp[i,j]=255
            elif tmp[i,j,0]==2:tmp[i,j]=[255,128,128]
            elif tmp[i,j,0]==3:tmp[i,j]=[128,255,128]
            else :tmp[i,j]=[128,255,128]
    tmp2=np.full((tmp.shape[0]+8,tmp.shape[1]+8,tmp.shape[2]),255)
    tmp2[4:-4,4:-4,:]=tmp
    ret=cv2.resize(tmp2.astype(np.uint8),dsize,interpolation=cv2.INTER_NEAREST)
    if order:
        for i in range(len(order)-1):
            ret=cv2.line(ret,(int((order[i][1]+4.5)*400)//tmp2.shape[1],int((order[i][0]+4.5)*400)//tmp2.shape[0]),(int((order[i+1][1]+4.5)*400)//tmp2.shape[1],int((order[i+1][0]+4.5)*400)//tmp2.shape[0]),(0,0,255),1)
    return ret
def addFormat(src:np.ndarray,ErrorCorrectionLevel:str,mask:int):
    src=src.copy()
    data=[int(i) for i in Format_info["{}-{}".format(ErrorCorrectionLevel,mask)]]
    src[8,:6]=data[:6]
    src[8,7],src[8,8],src[7,8]=data[6],data[7],data[8]
    for i in range(7):
        src[src.shape[0]-1-i,8]=data[i]
    src[8,-8:]=data[7:]
    for i in range(9,15):
        src[14-i,8]=data[i]
    return src
def addVersion(src:np.ndarray,version:int):
    data=[int(i) for i in reversed(Version_info[str(version)])]
    for i in range(6):
        src[-11,i]=src[i,-11]=data[i*3]
        src[-10,i]=src[i,-10]=data[i*3+1]
        src[-9,i]=src[i,-9]=data[i*3+2]
    return src
def judgemask(src:np.ndarray):
    score=0
    for i in range(src.shape[0]):
        tmp="".join([str(i) for i in src[i,:]])
        score+=(tmp.count("10111010000")+tmp.count("00001011101"))*40
        for j in tmp.split('0'):
            if len(j)>=5:score+=len(j)-2
        for j in tmp.split('1'):
            if len(j)>=5:score+=len(j)-2
    for i in range(src.shape[1]):
        tmp="".join([str(i) for i in src[:,i]])
        score+=(tmp.count("10111010000")+tmp.count("00001011101"))*40
        for j in tmp.split('0'):
            if len(j)>=5:score+=len(j)-2
        for j in tmp.split('1'):
            if len(j)>=5:score+=len(j)-2
    for i in range(src.shape[0]-1):
        for j in range(src.shape[1]-1):
            if src[i,j]==src[i+1,j]==src[i,j+1]==src[i+1,j+1]:score+=3
    tmp=int(np.sum(src)*100/(src.shape[0]*src.shape[1]))//5
    score+=10*(min(abs(tmp*5-50)//5,abs((tmp+1)*5-50)//5))
    return score
if __name__=="__main__":
    text,ErrorCorrectionLevel="HELLO WORLD "*50,"H"
    Mode=judgeMode(text)
    version=minimize_version(text,ErrorCorrectionLevel,Mode)
    codes=get_Codes(text,ErrorCorrectionLevel,version,Mode)
    qr=Blank(version)
    qrs=[addVersion(addFormat(PlaceData(codes,qr,mask),ErrorCorrectionLevel,mask),version) if version>=7 else addFormat(PlaceData(codes,qr,mask),ErrorCorrectionLevel,mask) for mask in range(8)]
    cv2.imshow("qr",toqr(min(qrs,key=judgemask)))
    cv2.waitKey(0)