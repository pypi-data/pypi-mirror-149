from .constants import Alphanumeric,Numeric
def judgeMode(text:str):
    s=set(text)
    if not s-set(Numeric.keys()):return "Numeric"
    if not s-set(Alphanumeric.keys()):return "Alphanumeric"
    raise NotImplementedError("code contains unsupported characters")
    