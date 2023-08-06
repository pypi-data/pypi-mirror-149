from .Data_analysis import Alphanumeric,judgeMode
from .constants import capacitie_data,EC_table
def bin_ext(code,l:int):
    if type(code)==str:code=int(code)
    ret=bin(code)[2:]
    return '0'*(l-len(ret))+ret
def capacities(version:int,ErrorCorrectionLevel:str,Mode:str):
    """Returns the Capacities depending on version,ErrorCorrectionLevel and Mode.
    version:[1,40]
    ErrorCorrectionLevel:['L','M','Q','H']
    Mode:['Numeric','Alphanumeric','Byte','Kanji']
    """
    e="LMQH".index(ErrorCorrectionLevel)
    m="Numeric Alphanumeric Byte Kanji".split().index(Mode)
    return capacitie_data[(version-1)*4+e][m]
def minimize_version(text:str,ErrorCorrectionLevel:str,Mode:str):
    l=len(text)
    for v in range(1,41):
        if capacities(v,ErrorCorrectionLevel,Mode)>=l:return v
    else:raise Exception("Input 'text' is too large.")
def Mode_indicator(Mode:str):
    """Returns the mode indicator of different Modes.
    Mode:['Numeric','Alphanumeric','Byte','Kanji']"""
    return {"Numeric":"0001",
    "Alphanumeric":"0010",
    "Byte":"0100",
    "Kanji":"1000"}[Mode]
def character_count_indicator(text:str,version:int,Mode:str):
    """text: The original input text.
    version:[1,40]
    Mode:['Numeric','Alphanumeric','Byte','Kanji']"""
    if version>40 or version<1:raise Exception("Version=={} not supported.".format(version))
    l={"Numeric":10,"Alphanumeric":9}[Mode] if version<=9 else \
      {"Numeric":12,"Alphanumeric":11}[Mode] if 10<=version and version<=26 else \
      {"Numeric":14,"Alphanumeric":13}[Mode]
    return bin_ext(len(text),l)
def NumericEncoding(text:str,version:int):
    splied=[int(text[i:min(i+3,len(text))]) for i in range(0,len(text),3)]
    binary=[bin_ext(i,10 if len(str(i))==3 else 7 if len(str(i))==2 else 4) for i in splied]
    return [
        Mode_indicator("Numeric"),
        character_count_indicator(text,version,"Numeric")
    ]+binary
def AlphanumericEncoding(text:str,version:int):
    splied=[text[i:min(i+2,len(text))] for i in range(0,len(text),2)]
    binary=[bin_ext(Alphanumeric[i[0]]*45+Alphanumeric[i[1]],11) if len(i)==2 else bin_ext(Alphanumeric[i],6) for i in splied]
    return [
        Mode_indicator("Alphanumeric"),
        character_count_indicator(text,version,"Alphanumeric")
    ]+binary
def num_databits(version:int,ErrorCorrectionLevel:str):
    """Determine how many data bits are required for a particular QR code with version and ErrorCorrectionLevel."""
    return int(EC_table["{}-{}".format(version,ErrorCorrectionLevel)][0])*8
def DataEncoding(text:str,ErrorCorrectionLevel:str,version:int,Mode:str):
    databit="".join(NumericEncoding(text,version) if Mode=="Numeric" else AlphanumericEncoding(text,version))
    l=num_databits(version,ErrorCorrectionLevel)
    databit+="0"*min(4,l-len(databit))
    databit+='0'*((8-len(databit)%8)%8)
    databit+="".join([['11101100','00010001'][i%2] for i in range((l-len(databit))//8)])  
    return databit
if __name__=="__main__":
    text,ErrorCorrectionLevel="HTTPS://SPACE.BILIBILI.COM/170218655","H"
    Mode=judgeMode(text)
    version=minimize_version(text,ErrorCorrectionLevel,Mode)
    print(DataEncoding(text,ErrorCorrectionLevel,version,Mode))
    
    print(num_databits(5,'Q'))