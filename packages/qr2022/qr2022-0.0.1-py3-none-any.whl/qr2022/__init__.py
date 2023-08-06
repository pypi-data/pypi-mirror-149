from .Data_analysis import judgeMode
from .Data_Encoding import minimize_version
from .Structure_Final_Message import get_Codes
from .Module_Placement import Blank,addVersion,addFormat,PlaceData,toqr,judgemask
import cv2

def qrcode(text:str,ErrorCorrectionLevel="H"):
    """Supported characters in text:0 ~ 9, A ~ Z and the symbols $, %, *, +, -, ., /, : as well as a space.
    ErrorCorrectionLevel:['L','M','Q','H']"""
    Mode=judgeMode(text)
    version=minimize_version(text,ErrorCorrectionLevel,Mode)
    codes=get_Codes(text,ErrorCorrectionLevel,version,Mode)
    qr=Blank(version)
    qrs=[addVersion(addFormat(PlaceData(codes,qr,mask),ErrorCorrectionLevel,mask),version) if version>=7 else addFormat(PlaceData(codes,qr,mask),ErrorCorrectionLevel,mask) for mask in range(8)]
    return toqr(min(qrs,key=judgemask))
if __name__=="__main__":
    text,ErrorCorrectionLevel="HTTPS://SPACE.BILIBILI.COM/170218655","H"
    Mode=judgeMode(text)
    version=minimize_version(text,ErrorCorrectionLevel,Mode)
    codes=get_Codes(text,ErrorCorrectionLevel,version,Mode)
    qr=Blank(version)
    order=[]
    PlaceData(codes,qr,None,order)
    cv2.imwrite("Figure_1.png",toqr(qr,(400,400),order))
    qrs=[addVersion(addFormat(PlaceData(codes,qr,mask),ErrorCorrectionLevel,mask),version) if version>=7 else addFormat(PlaceData(codes,qr,mask),ErrorCorrectionLevel,mask) for mask in range(8)]
    cv2.imwrite("Figure_2.png",toqr(min(qrs,key=judgemask)))
    ################
    codes=get_Codes(text,ErrorCorrectionLevel,version,Mode,show=1)
    qr=Blank(version)
    cv2.imwrite("Figure_3.png",toqr(PlaceData(codes,qr,None,show=1)))
    ####### usage #########
    cv2.imshow("qr",qrcode("HTTPS://SPACE.BILIBILI.COM/170218655","H"))
    cv2.waitKey(0)